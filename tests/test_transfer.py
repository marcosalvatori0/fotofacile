import threading
from pathlib import Path

import pytest

from fotofacile.core.errors import AdbError, FotoFacileError
from fotofacile.core.history import History
from fotofacile.core.planner import PlannedFile, TransferOptions, TransferPlan
from fotofacile.core.scanner import MediaFile
from fotofacile.core.transfer import download_file_stream, transfer


def media(nome: str = "a.jpg", size: int = 8, mtime: int = 1) -> MediaFile:
    return MediaFile(remote_path=f"/sdcard/DCIM/Camera/{nome}", size=size, mtime=mtime, kind="photo")


class BackendFinto:
    """Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni."""

    def __init__(
        self,
        contenuti: dict[str, bytes],
        fallimenti: list[str] | None = None,
        cancel: threading.Event | None = None,
        annulla_dopo: int | None = None,
    ):
        self.contenuti = dict(contenuti)
        self.fallimenti = list(fallimenti or [])
        self.cancellati: list[str] = []
        self.chiusure = 0
        self.cancel = cancel
        self.annulla_dopo = annulla_dopo
        self.blocchi_inviati = 0

    def stream_file(self, serial, remote_path, chunk_size=4):
        if remote_path in self.fallimenti:
            self.fallimenti.remove(remote_path)
            raise AdbError("Connessione persa")
        contenuto = self.contenuti.get(remote_path, b"")
        try:
            for inizio in range(0, len(contenuto), chunk_size):
                if self.cancel is not None and self.annulla_dopo is not None:
                    if self.blocchi_inviati >= self.annulla_dopo:
                        self.cancel.set()
                self.blocchi_inviati += 1
                yield contenuto[inizio : inizio + chunk_size]
        finally:
            self.chiusure += 1

    def delete_file(self, serial, remote_path):
        self.cancellati.append(remote_path)
        self.contenuti.pop(remote_path, None)


def piano(destination: Path, *file: MediaFile, **extra) -> TransferPlan:
    return TransferPlan(
        files=[
            PlannedFile(
                media=f,
                rel_path=f"DCIM/Camera/{f.name}",
                dest_path=destination / f.name,
            )
            for f in file
        ],
        total_bytes=sum(f.size for f in file),
        **extra,
    )


def test_copia_un_file_e_registra_la_cronologia(tmp_path):
    percorso = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso: b"12345678"})
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media()),
        TransferOptions(destination=tmp_path),
        history=cronologia,
    )
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert (tmp_path / "a.jpg").read_bytes() == b"12345678"
    assert risultato.bytes_copied == 8
    assert risultato.failed == []
    assert risultato.cancelled is False
    assert cronologia.contains("S1", "DCIM/Camera/a.jpg", 8, 1)
    assert (tmp_path / "history.json").is_file()


def test_conta_i_file_saltati_dal_piano(tmp_path):
    backend = BackendFinto({})
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, skipped_duplicates=3, skipped_existing=2),
        TransferOptions(destination=tmp_path),
    )
    assert risultato.skipped == 5
    assert risultato.copied == []


def test_progressi_monotoni_e_finali(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 20})
    letture = []

    def osserva(progresso):
        letture.append((progresso.done_files, progresso.bytes_done))

    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=20)),
        TransferOptions(destination=tmp_path),
        on_progress=osserva,
        clock=lambda: 0.5,
    )
    assert letture[-1] == (1, 20)
    assert [lettura[1] for lettura in letture] == sorted(lettura[1] for lettura in letture)
    assert risultato.bytes_copied == 20


def test_progressi_riportano_velocita_e_tempo_rimanente(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 40})
    istanti = iter([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    letture = []

    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=40)),
        TransferOptions(destination=tmp_path),
        on_progress=letture.append,
        chunk_size=8,
        clock=lambda: next(istanti, 8.0),
    )
    assert risultato.bytes_copied == 40
    assert letture[-1].speed_bps > 0
    assert letture[-1].eta_seconds is None or letture[-1].eta_seconds >= 0


def test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream(tmp_path):
    cancel = threading.Event()
    backend = BackendFinto(
        {"/sdcard/DCIM/Camera/a.jpg": b"x" * 200}, cancel=cancel, annulla_dopo=3
    )
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=200)),
        TransferOptions(destination=tmp_path),
        cancel=cancel,
        chunk_size=16,
    )
    assert risultato.cancelled is True
    assert risultato.copied == []
    assert backend.blocchi_inviati >= 3  # la copia era davvero in corso
    assert list(tmp_path.iterdir()) == []  # nessun file, nessun .part
    assert backend.chiusure == 1  # la lettura dal telefono è stata chiusa


def test_annullamento_prima_di_iniziare_non_copia_nulla(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"abc"})
    cancel = threading.Event()
    cancel.set()
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=3)),
        TransferOptions(destination=tmp_path),
        cancel=cancel,
    )
    assert risultato.cancelled is True
    assert list(tmp_path.iterdir()) == []


def test_errore_transitorio_viene_ritentato(tmp_path):
    percorso = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso: b"abcdefgh"}, fallimenti=[percorso])
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media()),
        TransferOptions(destination=tmp_path),
        retries=2,
        chunk_size=4,
        clock=lambda: 0.0,
    )
    assert (tmp_path / "a.jpg").read_bytes() == b"abcdefgh"
    assert risultato.failed == []
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert risultato.bytes_copied == 8


def test_errore_persistente_finisce_nel_resoconto_senza_interrompere(tmp_path):
    rotto = "/sdcard/DCIM/Camera/rotto.jpg"
    buono = "/sdcard/DCIM/Camera/buono.jpg"
    backend = BackendFinto({rotto: b"aaaa", buono: b"bbbb"}, fallimenti=[rotto, rotto, rotto])
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media("rotto.jpg", 4), media("buono.jpg", 4)),
        TransferOptions(destination=tmp_path),
        retries=2,
        clock=lambda: 0.0,
    )
    assert [errore[0].name for errore in risultato.failed] == ["rotto.jpg"]
    assert (tmp_path / "buono.jpg").read_bytes() == b"bbbb"
    assert not (tmp_path / "rotto.jpg.part").exists()
    assert risultato.bytes_copied == 4


def test_dimensione_diversa_segnala_errore_e_non_scrive_il_file(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"1234"})
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=999)),
        TransferOptions(destination=tmp_path),
    )
    assert risultato.copied == []
    assert [errore[0].name for errore in risultato.failed] == ["a.jpg"]
    assert "incompleta" in risultato.failed[0][1].lower()
    assert not (tmp_path / "a.jpg").exists()
    assert not (tmp_path / "a.jpg.part").exists()


def test_dimensione_sconosciuta_non_blocca_la_copia(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"1234"})
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=0)),
        TransferOptions(destination=tmp_path),
    )
    assert (tmp_path / "a.jpg").read_bytes() == b"1234"
    assert risultato.copied == [tmp_path / "a.jpg"]


def test_cancella_dal_telefono_solo_dopo_copia_verificata(tmp_path):
    buono = "/sdcard/DCIM/Camera/buono.jpg"
    rotto = "/sdcard/DCIM/Camera/rotto.jpg"
    backend = BackendFinto({buono: b"bbbb", rotto: b"1"}, fallimenti=[rotto] * 3)
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media("buono.jpg", 4), media("rotto.jpg", 9)),
        TransferOptions(destination=tmp_path, delete_after=True),
        retries=0,
        clock=lambda: 0.0,
    )
    assert backend.cancellati == [buono]
    assert risultato.deleted_from_phone == 1


def test_cancellazione_fallita_non_compromette_la_copia(tmp_path):
    percorso = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso: b"abcd"})

    def esplode(*_args, **_kwargs):
        raise AdbError("Il telefono non risponde")

    backend.delete_file = esplode  # type: ignore[method-assign]
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=4)),
        TransferOptions(destination=tmp_path, delete_after=True),
    )
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert risultato.deleted_from_phone == 0
    assert risultato.failed == []


def test_copia_multipla_in_blocchi_da_dimensioni_diverse(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"z" * 100})
    scritti = download_file_stream(
        backend, "S1", "/sdcard/DCIM/Camera/a.jpg", tmp_path / "copia.jpg", chunk_size=7
    )
    assert scritti == 100
    assert (tmp_path / "copia.jpg").read_bytes() == b"z" * 100
    assert not (tmp_path / "copia.jpg.part").exists()


def test_copia_in_sottocartella_inesistente_la_crea(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"xy"})
    destinazione = tmp_path / "DCIM" / "Camera" / "a.jpg"
    download_file_stream(backend, "S1", "/sdcard/DCIM/Camera/a.jpg", destinazione)
    assert destinazione.read_bytes() == b"xy"


def test_disco_pieno_produce_messaggio_comprensibile(tmp_path, monkeypatch):
    import fotofacile.core.transfer as modulo

    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 100})

    def open_pieno(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(modulo, "open", open_pieno, raising=False)
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=100)),
        TransferOptions(destination=tmp_path),
        retries=0,
    )
    messaggio = risultato.failed[0][1].lower()
    assert "spazio" in messaggio
    assert list(tmp_path.iterdir()) == []


def test_permesso_negato_produce_messaggio_comprensibile(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 100})
    cartella_bloccata = tmp_path / "bloccata"
    cartella_bloccata.mkdir()
    cartella_bloccata.chmod(0o500)
    try:
        risultato = transfer(
            backend,
            "S1",
            piano(cartella_bloccata, media(size=100)),
            TransferOptions(destination=cartella_bloccata),
            retries=0,
        )
    finally:
        cartella_bloccata.chmod(0o700)
    assert risultato.failed
    assert "a.jpg" in risultato.failed[0][1]
    assert isinstance(risultato.failed[0][1], str)


def test_errore_di_rete_usa_il_messaggio_dell_errore(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 10}, fallimenti=["/sdcard/DCIM/Camera/a.jpg"] * 2)
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=10)),
        TransferOptions(destination=tmp_path),
        retries=1,
        clock=lambda: 0.0,
    )
    assert risultato.failed
    assert "Connessione persa" in risultato.failed[0][1] or "collegamento" in risultato.failed[0][1].lower()


def test_elapsed_riflette_l_orologio(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 5})
    istanti = iter([100.0, 103.0])
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=5)),
        TransferOptions(destination=tmp_path),
        clock=lambda: next(istanti, 103.0),
    )
    assert risultato.elapsed == pytest.approx(3.0, abs=0.5)


def test_senza_cronologia_la_copia_funziona_comunque(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 5})
    risultato = transfer(backend, "S1", piano(tmp_path, media(size=5)), TransferOptions(destination=tmp_path))
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert not (tmp_path / "history.json").exists()


def test_errori_di_tipo_fotofacile_non_vengono_riconfezionati(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b""}, fallimenti=[])
    backend.stream_file = lambda *_a, **_k: (_ for _ in ()).throw(
        FotoFacileError("Messaggio già pronto per l'utente")
    )
    risultato = transfer(
        backend,
        "S1",
        piano(tmp_path, media(size=3)),
        TransferOptions(destination=tmp_path),
        retries=0,
    )
    assert "Messaggio già pronto per l'utente" in risultato.failed[0][1]

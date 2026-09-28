import time
from pathlib import Path

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.core.ops import ProcessoEsterno, ScaricatoreAPassi, esegui_fino_alla_fine


def script(tmp_path: Path, nome: str, corpo: str) -> str:
    percorso = tmp_path / nome
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return str(percorso)


def test_processo_breve_riporta_output_e_codice(tmp_path):
    comando = script(tmp_path, "breve", "echo 'List of devices attached'\n")
    processo = ProcessoEsterno([comando])
    esito = esegui_fino_alla_fine(processo.aspetta())
    assert "List of devices attached" in esito.output
    assert esito.returncode == 0


def test_processo_lungo_non_blocca_chi_lo_guida(tmp_path):
    comando = script(tmp_path, "lungo", "sleep 0.3\necho fatto\n")
    processo = ProcessoEsterno([comando])
    esito = esegui_fino_alla_fine(processo.aspetta())
    assert "fatto" in esito.output


def test_processo_fallito_produce_errore_umano(tmp_path):
    comando = script(tmp_path, "fallisce", "echo 'errore tecnico' >&2\nexit 1\n")
    processo = ProcessoEsterno([comando], umano="Il telefono non risponde.", hint="Controlla il cavo.")
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(processo.aspetta())
    assert errore.value.message == "Il telefono non risponde."
    assert errore.value.hint == "Controlla il cavo."


def test_processo_che_non_risponde_scade_e_viene_interrotto(tmp_path):
    comando = script(tmp_path, "bloccato", "sleep 5\n")
    processo = ProcessoEsterno([comando], timeout=0.3)
    inizio = time.monotonic()
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(processo.aspetta())
    assert time.monotonic() - inizio < 3
    assert "risposto" in errore.value.message.lower() or "tempo" in errore.value.message.lower()
    assert processo.process is not None and processo.process.poll() is not None


def test_output_grande_va_su_file_per_non_intasare_il_collegamento(tmp_path):
    comando = script(tmp_path, "molto", "i=0\nwhile [ $i -lt 2000 ]; do echo riga-$i; i=$((i+1)); done\n")
    file_output = tmp_path / "output.txt"
    processo = ProcessoEsterno([comando], output_file=file_output)
    esito = esegui_fino_alla_fine(processo.aspetta())
    assert esito.returncode == 0
    righe = file_output.read_text().splitlines()
    assert len(righe) == 2000
    assert righe[-1] == "riga-1999"


def test_processo_interrotto_a_mano_non_lascia_processi_appesi(tmp_path):
    comando = script(tmp_path, "lungo2", "sleep 5\n")
    processo = ProcessoEsterno([comando])
    generatore = processo.aspetta()
    next(generatore)
    processo.termina()
    assert processo.process is not None
    assert processo.process.poll() is not None


def test_comando_inesistente_produce_errore_umano(tmp_path):
    processo = ProcessoEsterno([str(tmp_path / "non-esiste")])
    with pytest.raises(FotoFacileError):
        esegui_fino_alla_fine(processo.aspetta())


def test_scaricatore_scrive_i_byte_e_riporta_avanzamento(tmp_path):
    import io

    dati = b"x" * 300_000

    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    visti = []
    destinazione = tmp_path / "scaricato.bin"
    generatore = ScaricatoreAPassi(
        "https://esempio/file.zip",
        destinazione,
        on_progress=visti.append,
        opener=lambda *_a, **_k: Risposta(dati),
        blocco=64 * 1024,
    ).scarica()
    percorso = esegui_fino_alla_fine(generatore)
    assert percorso.read_bytes() == dati
    assert visti and visti[-1]["ricevuti"] == len(dati)
    assert not (tmp_path / "scaricato.bin.scarico").exists()


def test_scaricatore_annullabile(tmp_path):
    import io
    import threading

    dati = b"y" * 500_000
    annulla = threading.Event()

    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    def osserva(info):
        if info["ricevuti"] > 0:
            annulla.set()

    generatore = ScaricatoreAPassi(
        "https://esempio/file.zip",
        tmp_path / "x.bin",
        on_progress=osserva,
        annulla=annulla,
        opener=lambda *_a, **_k: Risposta(dati),
        blocco=16 * 1024,
    ).scarica()
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(generatore)
    assert "interrotto" in errore.value.message.lower()
    assert list(tmp_path.iterdir()) == []


def test_scaricatore_senza_rete_spiega_cosa_controllare(tmp_path):
    def opener(*_a, **_k):
        raise OSError("network unreachable")

    generatore = ScaricatoreAPassi(
        "https://esempio/file.zip", tmp_path / "x.bin", opener=opener
    ).scarica()
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(generatore)
    assert "internet" in errore.value.hint.lower()

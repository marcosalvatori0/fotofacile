import io
import threading
import zipfile
from pathlib import Path

import pytest

from fotofacile.core.adb_passi import AdbDemoAPassi
from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.errors import FotoFacileError
from fotofacile.core.installer import installa_a_passi
from fotofacile.core.ops import Annullato, esegui_fino_alla_fine
from fotofacile.core.scanner import parse_stat_stream


# ── installazione a passi ────────────────────────────────────────────────
def _zip(tmp_path: Path) -> Path:
    percorso = tmp_path / "pt.zip"
    with zipfile.ZipFile(percorso, "w") as archivio:
        archivio.writestr("platform-tools/adb", b"#!/bin/sh\n")
    return percorso


def _risposta(dati: bytes):
    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    return lambda *_a, **_k: Risposta(dati)


def test_installazione_a_passi_scarica_ed_estrae(tmp_path, monkeypatch):
    # Il controllo «archivio troppo piccolo» è pensato per un componente vero da ~10 MB:
    # qui si prova il meccanismo a passi, quindi la soglia viene abbassata.
    monkeypatch.setattr("fotofacile.core.installer.MIN_DIMENSIONE_ARCHIVIO", 1)
    archivio = _zip(tmp_path)
    visti = []
    generatore = installa_a_passi(
        target_dir=tmp_path / "componente",
        url="https://esempio/pt.zip",
        opener=_risposta(archivio.read_bytes()),
        on_progress=visti.append,
        system="linux",
    )
    percorso = esegui_fino_alla_fine(generatore)
    assert percorso == tmp_path / "componente" / "adb"
    assert percorso.is_file()
    assert visti and visti[-1]["ricevuti"] > 0


def test_installazione_a_passi_annullabile(tmp_path):
    archivio = _zip(tmp_path)
    annulla = threading.Event()
    annulla.set()
    generatore = installa_a_passi(
        target_dir=tmp_path / "componente",
        url="https://esempio/pt.zip",
        opener=_risposta(archivio.read_bytes()),
        annulla=annulla,
        system="linux",
    )
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(generatore)
    assert "interrotto" in errore.value.message.lower()


# ── backend demo a passi ─────────────────────────────────────────────────
def test_demo_a_passi_elenca_e_copia(tmp_path):
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=6), intervallo=0.0)
    dispositivi = esegui_fino_alla_fine(demo.dispositivi())
    assert dispositivi[0].is_ready

    file_trovati = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "stat"))
    assert len(file_trovati) == 6

    destinazione = tmp_path / "out" / file_trovati[0].name
    visti = []
    scritti = esegui_fino_alla_fine(
        demo.copia("DEMO12345", file_trovati[0].remote_path, destinazione, on_scritti=visti.append)
    )
    assert destinazione.is_file() and destinazione.stat().st_size == scritti
    assert visti and visti[-1] == scritti


def test_demo_a_passi_riporta_avanzamento_a_pezzi(tmp_path):
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0, pezzi_per_passo=1)
    file_trovati = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "stat"))
    visti = []
    esegui_fino_alla_fine(
        demo.copia("DEMO12345", file_trovati[0].remote_path, tmp_path / "x.bin", on_scritti=visti.append)
    )
    assert len(visti) >= 2


def test_demo_a_passi_annullabile_senza_residui(tmp_path):
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0, pezzi_per_passo=1)
    file_trovati = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "stat"))
    annulla = threading.Event()

    def ferma(byte):
        if byte > 0:
            annulla.set()

    destinazione = tmp_path / "uscita" / "x.bin"
    with pytest.raises(Annullato):
        esegui_fino_alla_fine(
            demo.copia("DEMO12345", file_trovati[0].remote_path, destinazione, on_scritti=ferma, annulla=annulla)
        )
    assert list(destinazione.parent.iterdir()) == []


def test_demo_a_passi_cancella_e_riavvia(tmp_path):
    backend = DemoAdbBackend(file_count=3)
    demo = AdbDemoAPassi(backend, intervallo=0.0)
    file_trovati = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    esegui_fino_alla_fine(demo.cancella("DEMO12345", file_trovati[0].remote_path))
    rimasti = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    assert file_trovati[0].remote_path not in [f.remote_path for f in rimasti]
    esegui_fino_alla_fine(demo.riavvia())

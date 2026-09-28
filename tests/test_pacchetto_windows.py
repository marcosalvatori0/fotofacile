"""Verifica che la cartella pronta per Windows sia completa e avviabile.

Il pacchetto Windows non può essere *compilato* su macOS (PyInstaller non fa
cross-compilazione): quello che si può garantire è che la cartella contenga tutto il
necessario, che i file `.bat` siano corretti per Windows e che il codice copiato funzioni.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.crea_pacchetto_windows import NOME_CARTELLA, crea_pacchetto

RADICE = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def pacchetto(tmp_path_factory):
    destinazione = tmp_path_factory.mktemp("pacchetto") / NOME_CARTELLA
    crea_pacchetto(destinazione)
    return destinazione


def test_contiene_tutto_il_codice(pacchetto):
    for relativo in (
        "fotofacile.py",
        "fotofacile/__init__.py",
        "fotofacile/cli.py",
        "fotofacile/core/adb.py",
        "fotofacile/core/ops.py",
        "fotofacile/ui/app.py",
        "fotofacile/ui/page_connect.py",
        "scripts/build_app.py",
        "scripts/make_icon.py",
        "assets/fotofacile.ico",
        "assets/fotofacile.png",
        "README.md",
    ):
        assert (pacchetto / relativo).is_file(), f"manca {relativo}"


def test_contiene_i_file_per_windows(pacchetto):
    for nome in (
        "Avvia FotoFacile.bat",
        "Crea l'eseguibile per Windows.bat",
        "LEGGIMI - Windows.txt",
    ):
        assert (pacchetto / nome).is_file(), f"manca {nome}"


def test_i_file_bat_sono_da_windows(pacchetto):
    for nome in ("Avvia FotoFacile.bat", "Crea l'eseguibile per Windows.bat"):
        dati = (pacchetto / nome).read_bytes()
        assert b"\r\n" in dati, f"{nome} deve usare fine riga Windows (CRLF)"
        assert b"\n\n" not in dati.replace(b"\r\n", b""), f"{nome} ha righe con fine riga sbagliato"
        testo = dati.decode("utf-8")
        assert "%~dp0" in testo, f"{nome} deve spostarsi nella propria cartella"
        assert "chcp 65001" in testo, f"{nome} deve usare UTF-8 per gli accenti"
        # niente caratteri “intelligenti”: cmd.exe li mostra male
        for vietato in ("’", "“", "”", "…", "→"):
            assert vietato not in testo, f"{nome} contiene {vietato!r}"


def test_avvio_sa_trovare_o_installare_python(pacchetto):
    testo = (pacchetto / "Avvia FotoFacile.bat").read_text(encoding="utf-8")
    assert "py -3" in testo and "python" in testo  # prova il launcher e poi python
    assert "winget" in testo  # se manca Python lo installa
    assert "tkinter" in testo  # controlla che la grafica ci sia
    assert "fotofacile.py doctor" in testo  # in caso di errore mostra la diagnosi
    assert 'pause' in testo  # la finestra non si chiude prima di leggere


def test_creazione_eseguibile_usa_la_build_del_progetto(pacchetto):
    testo = (pacchetto / "Crea l'eseguibile per Windows.bat").read_text(encoding="utf-8")
    assert "pip install" in testo and "pyinstaller" in testo
    assert "build_app.py" in testo
    assert "--selftest" in testo  # verifica l'eseguibile appena creato
    assert "dist\\FotoFacile" in testo


def test_leggimi_spiega_cosa_fare(pacchetto):
    testo = (pacchetto / "LEGGIMI - Windows.txt").read_text(encoding="utf-8")
    assert "Avvia FotoFacile.bat" in testo
    assert "Crea l'eseguibile per Windows.bat" in testo
    assert "Debug USB" in testo  # la parte che serve per il telefono
    assert "python.org" in testo
    assert "SmartScreen" in testo


def test_il_codice_copiato_funziona(pacchetto, tmp_path):
    """La copia deve essere completa: qui la si esegue davvero (diagnosi, senza finestra)."""
    esito = subprocess.run(
        [sys.executable, "fotofacile.py", "doctor"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=pacchetto,
        env={
            "HOME": str(tmp_path),
            "USERPROFILE": str(tmp_path),
            "PATH": "",
            "PYTHONDONTWRITEBYTECODE": "1",  # non sporcare il pacchetto con i file delle cache
        },
    )
    assert esito.returncode == 0, esito.stderr
    assert "FotoFacile" in esito.stdout
    assert "Sistema:" in esito.stdout


def test_il_pacchetto_non_contiene_file_di_sviluppo(pacchetto):
    """Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve all'utente."""
    nomi = {percorso.name for percorso in pacchetto.iterdir()}
    for indesiderato in (".venv", "graphify-out", "tests", "__pycache__", ".git"):
        assert indesiderato not in nomi
    for percorso in pacchetto.rglob("*"):
        assert "__pycache__" not in percorso.parts
        assert percorso.name != ".DS_Store"

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

from scripts import crea_pacchetto_windows as modulo_pacchetto
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
    assert "python.org" in testo
    assert "SmartScreen" in testo


def test_leggimi_non_obbliga_ad_attivare_il_debug_usb(pacchetto):
    """Il Debug USB non deve mai sembrare un passaggio obbligato: è la richiesta principale
    dell'utente e la vecchia versione delle istruzioni diceva l'opposto."""
    testo = (pacchetto / "LEGGIMI - Windows.txt").read_text(encoding="utf-8")
    assert "NON devi attivare il Debug USB" in testo
    # Il Debug USB si nomina solo come ultima possibilità, non fra i primi passi.
    posizione_primi_passi = testo.index("COLLEGARE IL TELEFONO")
    posizione_fine_passi = testo.index("SE QUALCOSA NON FUNZIONA")
    primi_passi = testo[posizione_primi_passi:posizione_fine_passi]
    righe = [riga for riga in primi_passi.splitlines() if riga.strip()]
    assert any("NON devi attivare" in riga for riga in righe[:8])
    assert primi_passi.count("Debug USB") <= 2
    # La copia piatta va spiegata: è il comportamento predefinito.
    assert "senza ricreare le cartelle" in testo


def test_il_pacchetto_porta_l_aiutante_per_windows(pacchetto):
    """Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non chiede
    il Debug USB — non può funzionare nella versione distribuita."""
    script = pacchetto / "fotofacile" / "aiutanti" / "wpd_win.ps1"
    assert script.is_file(), "manca l'aiutante wpd_win.ps1"
    dati = script.read_bytes()
    assert dati.startswith(b"\xef\xbb\xbf"), "gli script .ps1 devono avere il BOM UTF-8"
    assert (pacchetto / "fotofacile" / "aiutanti" / "wpd_win.py").is_file()
    for modulo in ("trasporto.py", "trasporto_aiutante.py", "trasporto_win.py"):
        assert (pacchetto / "fotofacile" / "core" / modulo).is_file(), f"manca {modulo}"


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


def test_rifiuta_di_cancellare_la_cartella_corrente(tmp_path, monkeypatch):
    """«python3 scripts/crea_pacchetto_windows.py .» non deve svuotare la cartella corrente."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "fotofacile").mkdir()  # sembra un pacchetto, ma la cartella corrente è intoccabile
    with pytest.raises(SystemExit) as errore:
        crea_pacchetto(Path("."))
    assert "sicurezza" in str(errore.value)
    assert (tmp_path / "fotofacile").is_dir()


def test_rifiuta_di_cancellare_la_cartella_personale(tmp_path, monkeypatch):
    # home finta: se il controllo non funzionasse, il test non toccherebbe la home vera
    finta_home = tmp_path / "home"
    (finta_home / "fotofacile").mkdir(parents=True)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: finta_home))
    with pytest.raises(SystemExit):
        crea_pacchetto(finta_home)
    assert (finta_home / "fotofacile").is_dir()


def test_rifiuta_di_cancellare_una_cartella_che_contiene_il_progetto(tmp_path, monkeypatch):
    """Una cartella padre del repository non va mai cancellata (qui il repository è finto)."""
    finto_repo = tmp_path / "repo" / "scripts"
    finto_repo.mkdir(parents=True)
    monkeypatch.setattr(modulo_pacchetto, "RADICE", finto_repo)
    with pytest.raises(SystemExit):
        crea_pacchetto(tmp_path / "repo")
    assert (tmp_path / "repo").is_dir()


def test_rifiuta_una_cartella_esistente_che_non_sembra_un_pacchetto(tmp_path):
    cartella = tmp_path / "documenti"
    cartella.mkdir()
    (cartella / "tesi.txt").write_text("da non perdere")
    with pytest.raises(SystemExit) as errore:
        crea_pacchetto(cartella)
    assert "--force" in str(errore.value)
    assert (cartella / "tesi.txt").is_file()


def test_la_riga_di_comando_senza_force_non_cancella_la_cartella(tmp_path):
    cartella = tmp_path / "documenti"
    cartella.mkdir()
    (cartella / "tesi.txt").write_text("da non perdere")
    esito = subprocess.run(
        [sys.executable, str(RADICE / "scripts" / "crea_pacchetto_windows.py"), str(cartella)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=RADICE,
    )
    assert esito.returncode == 1, esito.stdout
    assert "Errore" in esito.stderr
    assert (cartella / "tesi.txt").is_file()


def test_la_riga_di_comando_con_force_ricrea_la_cartella(tmp_path):
    cartella = tmp_path / "vecchia"
    cartella.mkdir()
    (cartella / "residuo.txt").write_text("vecchio")
    esito = subprocess.run(
        [sys.executable, str(RADICE / "scripts" / "crea_pacchetto_windows.py"), "--force", str(cartella)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=RADICE,
    )
    assert esito.returncode == 0, esito.stderr
    assert (cartella / "Avvia FotoFacile.bat").is_file()
    assert not (cartella / "residuo.txt").exists()

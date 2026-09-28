"""Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.

Include il test che avrebbe intercettato il difetto vero: uno snippet Python scritto dentro i
`.bat` conteneva `^>=` (escape di `cmd` finito dentro il codice Python) → il controllo di Python
falliva sempre e il file diceva «Python non è installato» anche quando c'era.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.crea_pacchetto_windows import NOME_CARTELLA, crea_pacchetto

RADICE = Path(__file__).resolve().parent.parent
SNIPPET = re.compile(r'-c\s+"([^"]+)"')


@pytest.fixture(scope="module")
def pacchetto(tmp_path_factory):
    destinazione = tmp_path_factory.mktemp("pacchetto") / NOME_CARTELLA
    crea_pacchetto(destinazione)
    return destinazione


def _bat(pacchetto: Path) -> list[Path]:
    return sorted(pacchetto.glob("*.bat"))


def test_gli_snippet_python_dentro_i_bat_sono_validi(pacchetto):
    """Ogni frammento Python scritto nei .bat deve essere compilabile davvero."""
    trovati = 0
    for percorso in _bat(pacchetto):
        testo = percorso.read_text(encoding="utf-8")
        for frammento in SNIPPET.findall(testo):
            trovati += 1
            try:
                compile(frammento, str(percorso.name), "exec")
            except SyntaxError as errore:  # pragma: no cover - solo se si rompe di nuovo
                raise AssertionError(
                    f"{percorso.name}: lo snippet Python non è valido ({errore}): {frammento!r}"
                ) from errore
    assert trovati >= 4, "i .bat devono controllare Python prima di usarlo"


def test_nei_bat_non_ci_sono_caret_dentro_il_codice_python(pacchetto):
    """Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire."""
    for percorso in _bat(pacchetto):
        for frammento in SNIPPET.findall(percorso.read_text(encoding="utf-8")):
            assert "^" not in frammento, f"{percorso.name}: caret dentro lo snippet: {frammento!r}"


def test_i_bat_cercano_python_in_tutti_i_modi_utili(pacchetto):
    testo = (pacchetto / "Avvia FotoFacile.bat").read_text(encoding="utf-8")
    assert "py -3" in testo, "manca il launcher ufficiale"
    assert "Programs\\Python" in testo and "ProgramFiles" in testo, "mancano i percorsi tipici"
    assert "for %%C in (python python3)" in testo, "manca la ricerca nel PATH"
    assert "py -0p" in testo, "manca l'elenco delle versioni del launcher"
    assert "EnableDelayedExpansion" in testo
    assert ":diagnostica" in testo, "se non trova Python deve dire cosa ha visto"


def test_se_python_non_c_e_lo_dice_e_propone_le_alternative(pacchetto):
    testo = (pacchetto / "Avvia FotoFacile.bat").read_text(encoding="utf-8")
    assert "winget install -e --id Python.Python.3.13" in testo
    assert "Microsoft Store" in testo and "python.org" in testo
    assert "Installa FotoFacile.bat" in testo


def test_installer_windows_installa_e_registra_la_disinstallazione(pacchetto):
    testo = (pacchetto / "Installa FotoFacile.bat").read_text(encoding="utf-8")
    assert "InstallaFotoFacile.ps1" in testo
    assert "ExecutionPolicy Bypass" in testo
    ps1 = (RADICE / "installer/windows/InstallaFotoFacile.ps1").read_text(encoding="utf-8")
    assert "$env:LOCALAPPDATA" in ps1, "installazione per utente, senza amministratore"
    assert (
        "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall" in ps1
    ), "manca la voce in «App e funzionalità»"
    assert r"Uninstall\$Nome" in ps1
    assert "UninstallString" in ps1 and "DisplayVersion" in ps1
    assert "CreateShortcut" in ps1 and "Start Menu" in ps1 and "Desktop" in ps1
    disinstalla = (RADICE / "installer/windows/DisinstallaFotoFacile.ps1").read_text(encoding="utf-8")
    assert "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall" in disinstalla
    assert "fotofacile-disinstallazione" in disinstalla, "deve potersi cancellare da sola"


def test_installer_windows_funziona_con_o_senza_eseguibile():
    ps1 = (RADICE / "installer/windows/InstallaFotoFacile.ps1").read_text(encoding="utf-8")
    assert "Trova-Eseguibile" in ps1 and "Trova-Python" in ps1
    assert "modalitaSorgente" in ps1
    assert "dist\\FotoFacile" in ps1


def test_script_inno_setup_pronto_per_la_pipeline():
    iss = (RADICE / "installer/windows/FotoFacile.iss").read_text(encoding="utf-8")
    assert "[Setup]" in iss and "[Files]" in iss and "[Icons]" in iss
    assert "PrivilegesRequired=lowest" in iss, "installazione senza amministratore"
    assert "UninstallDisplayIcon" in iss
    assert "CartellaSorgente" in iss and "dist\\FotoFacile" in iss
    assert "Italian.isl" in iss, "l'installazione deve essere in italiano"


def test_pipeline_github_costruisce_entrambi_gli_installer():
    flusso = (RADICE / ".github/workflows/build-installers.yml").read_text(encoding="utf-8")
    assert "macos-14" in flusso and "windows-2022" in flusso
    assert "crea_installer_mac.py" in flusso, "manca la creazione del .dmg"
    assert "FotoFacile.iss" in flusso and "ISCC.exe" in flusso, "manca il Setup.exe di Windows"
    assert "--selftest" in flusso, "gli installer vanno verificati nella pipeline"
    assert "softprops/action-gh-release" in flusso, "manca la pubblicazione della Release"


def test_creazione_del_dmg_solo_su_macos():
    script = (RADICE / "scripts/crea_installer_mac.py").read_text(encoding="utf-8")
    assert "hdiutil" in script
    assert "Applicazioni" in script and "/Applications" in script
    assert "LEGGIMI - macOS.txt" in script
    if sys.platform != "darwin":
        pytest.skip("il .dmg si crea solo da macOS")


@pytest.mark.skipif(sys.platform != "darwin", reason="hdiutil esiste solo su macOS")
def test_il_dmg_si_crea_e_contiene_l_app(tmp_path):
    """Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per guardarci dentro."""
    finta_app = tmp_path / "FotoFacile.app"
    (finta_app / "Contents" / "MacOS").mkdir(parents=True)
    (finta_app / "Contents" / "MacOS" / "FotoFacile").write_text("#!/bin/sh\necho ciao\n")
    (finta_app / "Contents" / "Info.plist").write_text("<plist/>")
    (finta_app / "Contents" / "MacOS" / "FotoFacile").chmod(0o755)

    from scripts.crea_installer_mac import crea_dmg

    dmg = crea_dmg(finta_app, tmp_path / "prova.dmg", "FotoFacileProva")
    assert dmg.is_file() and dmg.stat().st_size > 0

    montato = subprocess.run(
        ["hdiutil", "attach", "-nobrowse", "-readonly", str(dmg)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    punto = montato.strip().splitlines()[-1].split("\t")[-1].strip()
    try:
        contenuto = sorted(percorso.name for percorso in Path(punto).iterdir())
        assert "FotoFacile.app" in contenuto
        assert "Applicazioni" in contenuto
        assert "LEGGIMI - macOS.txt" in contenuto
        assert (Path(punto) / "Applicazioni").is_symlink()
    finally:
        subprocess.run(["hdiutil", "detach", punto], capture_output=True, check=False)

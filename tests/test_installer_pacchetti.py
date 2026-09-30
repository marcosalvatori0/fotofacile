"""Verifica degli installer: il `Setup.exe` di Windows (Inno Setup) e il `.dmg` di macOS.

Per Windows l'unico installatore è il `Setup.exe`: niente `.bat` né `.ps1` da lanciare a
mano (D3). L'aiutante `wpd_win.ps1`, che parla con il telefono, è un'altra cosa e resta:
lo controlla `tests/test_aiutante_windows.py`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parent.parent


def test_windows_ha_solo_il_setup_e_nessuno_script_da_lanciare_a_mano():
    """Nel repository non restano `.bat`/`.ps1` d'installazione né lo script del pacchetto."""
    cartella = RADICE / "installer" / "windows"
    assert not list(cartella.glob("*.bat")), "i .bat d'installazione non ci sono più"
    # gli unici .ps1 ammessi sono quelli che usa la pipeline GitHub (D4), mai l'utente
    solo_ci = {"prova-installazione.ps1", "verifica-eseguibile.ps1"}
    assert {p.name for p in cartella.glob("*.ps1")} <= solo_ci, "i .ps1 d'installazione non ci sono più"
    assert (cartella / "FotoFacile.iss").is_file()
    assert not (RADICE / "scripts" / "crea_pacchetto_windows.py").exists()


def test_script_inno_setup_pronto_per_la_pipeline():
    iss = (RADICE / "installer/windows/FotoFacile.iss").read_text(encoding="utf-8")
    assert "[Setup]" in iss and "[Files]" in iss and "[Icons]" in iss
    assert "PrivilegesRequired=lowest" in iss, "installazione senza amministratore"
    assert "UninstallDisplayIcon" in iss
    assert "CartellaSorgente" in iss and "dist\\FotoFacile" in iss
    assert "Italian.isl" in iss, "l'installazione deve essere in italiano"


def test_lo_zip_portatile_non_importa_lo_script_del_pacchetto():
    """Il passo «Versione portatile (zip)» usava `import scripts.crea_pacchetto_windows`."""
    flusso = (RADICE / ".github/workflows/build-installers.yml").read_text(encoding="utf-8")
    assert "crea_pacchetto_windows" not in flusso
    assert "shutil.make_archive('dist/FotoFacile-portable', 'zip', 'dist', 'FotoFacile')" in flusso


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

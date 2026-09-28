import subprocess
from pathlib import Path

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.core.osutil import (
    app_dir,
    default_photos_dir,
    file_manager_command,
    is_case_insensitive_fs,
    open_in_file_manager,
    python_command,
)


def test_cartella_app_multipiattaforma(tmp_path):
    assert app_dir(env={"HOME": str(tmp_path)}) == tmp_path / ".fotofacile"
    assert app_dir(env={"USERPROFILE": str(tmp_path), "HOME": "/altro"}) == tmp_path / ".fotofacile"


def test_cartella_app_senza_variabili_ambientali():
    assert app_dir(env={}).name == ".fotofacile"


def test_cartella_foto_predefinita(tmp_path):
    assert default_photos_dir(env={"HOME": str(tmp_path)}) == tmp_path / "Pictures" / "FotoFacile"


def test_comando_di_apertura_per_sistema():
    percorso = Path("/tmp/foto")
    assert file_manager_command(percorso, "darwin") == ["open", "/tmp/foto"]
    assert file_manager_command(percorso, "win32") == ["explorer", "/tmp/foto"]
    assert file_manager_command(percorso, "linux") == ["xdg-open", "/tmp/foto"]
    assert file_manager_command(percorso, "freebsd") == ["xdg-open", "/tmp/foto"]


def test_apertura_cartella_usa_il_comando_giusto():
    chiamate = []

    def runner(comando, **_kwargs):
        chiamate.append(comando)
        return subprocess.CompletedProcess(comando, 0)

    open_in_file_manager(Path("/tmp/foto"), system="linux", runner=runner)
    assert chiamate == [["xdg-open", "/tmp/foto"]]


def test_apertura_cartella_senza_file_manager_mostra_il_percorso():
    def runner(comando, **_kwargs):
        raise FileNotFoundError(comando[0])

    with pytest.raises(FotoFacileError) as exc:
        open_in_file_manager(Path("/tmp/foto"), system="linux", runner=runner)
    assert "/tmp/foto" in exc.value.message
    assert "/tmp/foto" in exc.value.hint


def test_codice_di_uscita_diverso_da_zero_e_un_errore_su_linux():
    def runner(comando, **_kwargs):
        return subprocess.CompletedProcess(comando, 1)

    with pytest.raises(FotoFacileError):
        open_in_file_manager(Path("/tmp/foto"), system="linux", runner=runner)


def test_sensibilita_maiuscole_per_sistema():
    assert is_case_insensitive_fs("win32") is True
    assert is_case_insensitive_fs("darwin") is True
    assert is_case_insensitive_fs("linux") is False


def test_comando_python_per_sistema():
    assert python_command("win32") == "py"
    assert python_command("darwin") == "python3"
    assert python_command("linux") == "python3"

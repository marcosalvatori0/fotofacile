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


def test_flag_nascosta_su_windows_e_zero_altrove():
    """Su Windows i comandi non devono far lampeggiare finestre nere."""
    from fotofacile.core.osutil import flag_nascosta

    assert flag_nascosta("win32") != 0
    assert flag_nascosta("darwin") == 0
    assert flag_nascosta("linux") == 0


def test_i_comandi_esterni_usano_il_flag_nascosta(monkeypatch, tmp_path):
    """Ops e adb devono passare creationflags=... al processo esterno."""
    from fotofacile.core import adb as modulo_adb
    from fotofacile.core import ops as modulo_ops

    raccolti = []

    class PopoFinto:
        returncode = 0
        stdout = None
        stderr = None

        def __init__(self, argomenti, **kwargs):
            raccolti.append(kwargs)
            self.args = argomenti

        def poll(self):
            return 0

        def wait(self, timeout=None):
            return 0

        def kill(self):
            pass

        def terminate(self):
            pass

        def communicate(self, *args, **kwargs):
            return (b"", b"")

    monkeypatch.setattr(modulo_ops.subprocess, "Popen", PopoFinto)
    monkeypatch.setattr(modulo_ops, "FLAG_NAPOSTA" if False else "flag_nascosta", lambda: 134217728)
    processo = modulo_ops.ProcessoEsterno(["finto-comando"], timeout=5)
    processo.avvia()
    assert raccolti and raccolti[0].get("creationflags") == 134217728


def test_dpi_non_fa_nulla_fuori_da_windows():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    assert rendi_consapevole_dpi(sistema="darwin") is False
    assert rendi_consapevole_dpi(sistema="linux") is False


def test_dpi_su_windows_chiede_la_consapevolezza_per_monitor():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    chiamate = []

    class Shcore:
        def SetProcessDpiAwareness(self, valore):
            chiamate.append(valore)
            return 0

    class Windll:
        shcore = Shcore()

    assert rendi_consapevole_dpi(sistema="win32", windll=Windll()) is True
    assert chiamate == [2]  # 2 = per-monitor


def test_dpi_ripiega_sulla_vecchia_funzione():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    chiamate = []

    class Shcore:
        def SetProcessDpiAwareness(self, _valore):
            raise OSError("non disponibile")

    class User32:
        def SetProcessDPIAware(self):
            chiamate.append("vecchia")
            return 1

    class Windll:
        shcore = Shcore()
        user32 = User32()

    assert rendi_consapevole_dpi(sistema="win32", windll=Windll()) is True
    assert chiamate == ["vecchia"]

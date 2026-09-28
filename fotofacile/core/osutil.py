"""Unico punto in cui il programma si adatta al sistema operativo."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Mapping

from .errors import FotoFacileError

COMANDI_APERTURA = {
    "darwin": "open",
    "win32": "explorer",
    "linux": "xdg-open",
}


def _system(system: str | None) -> str:
    return system or sys.platform


def app_dir(env: Mapping[str, str] | None = None) -> Path:
    """Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale."""
    ambiente = dict(env if env is not None else os.environ)
    base = ambiente.get("USERPROFILE") or ambiente.get("HOME") or str(Path.home())
    return Path(base) / ".fotofacile"


def default_photos_dir(env: Mapping[str, str] | None = None) -> Path:
    """Cartella proposta per salvare le foto (Immagini/FotoFacile)."""
    return Path(app_dir(env)).parent / "Pictures" / "FotoFacile"


def file_manager_command(path: Path, system: str) -> list[str]:
    """Comando che apre una cartella nel file manager del sistema."""
    eseguibile = COMANDI_APERTURA.get(system, "xdg-open")
    return [eseguibile, str(path)]


def open_in_file_manager(
    path: Path,
    system: str | None = None,
    runner: Callable[..., object] | None = None,
) -> None:
    """Apre la cartella nel file manager, con errore comprensibile se non è possibile."""
    comando = file_manager_command(Path(path), _system(system))
    esegui = runner or subprocess.run
    try:
        esito = esegui(comando, check=False)
    except OSError as errore:
        raise FotoFacileError(
            f"Non riesco ad aprire la cartella {path}.",
            hint=f"Apri manualmente questa cartella: {path}",
        ) from errore
    if getattr(esito, "returncode", 0) not in (0, None):
        raise FotoFacileError(
            f"Non riesco ad aprire la cartella {path}.",
            hint=f"Apri manualmente questa cartella: {path}",
        )


def is_case_insensitive_fs(system: str | None = None) -> bool:
    """True sui sistemi dove «Foto.jpg» e «foto.jpg» sono lo stesso file."""
    return _system(system) in ("win32", "darwin", "cygwin")


def python_command(system: str | None = None) -> str:
    """Come si avvia Python da terminale su questo sistema."""
    return "py" if _system(system) == "win32" else "python3"

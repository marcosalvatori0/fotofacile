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
    """Apre la cartella nel file manager, senza bloccare la finestra e senza falsi allarmi."""
    percorso = Path(path)
    sistema = _system(system)
    try:
        if runner is not None:
            esito = runner(file_manager_command(percorso, sistema), check=False)
            # Su Windows «explorer» esce con codice 1 anche quando la cartella si apre:
            # giudicare dal codice di uscita darebbe un errore inesistente.
            if sistema != "win32" and getattr(esito, "returncode", 0) not in (0, None):
                raise OSError(f"codice di uscita {getattr(esito, 'returncode', None)}")
        elif sistema == "win32":
            os.startfile(str(percorso))  # type: ignore[attr-defined]
        else:
            # Avvio e via: su alcuni sistemi il comando resta attivo finché il file
            # manager è aperto, e attenderlo bloccherebbe la finestra.
            subprocess.Popen(
                file_manager_command(percorso, sistema),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except OSError as errore:
        raise FotoFacileError(
            f"Non riesco ad aprire la cartella {path}.",
            hint=f"Apri manualmente questa cartella: {path}",
        ) from errore


def is_case_insensitive_fs(system: str | None = None) -> bool:
    """True sui sistemi dove «Foto.jpg» e «foto.jpg» sono lo stesso file."""
    return _system(system) in ("win32", "darwin", "cygwin")


def flag_nascosta(system: str | None = None) -> int:
    """Su Windows nasconde la finestra nera dei comandi esterni (0 = nessun flag altrove)."""
    if _system(system) != "win32":
        return 0
    return getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def python_command(system: str | None = None) -> str:
    """Come si avvia Python da terminale su questo sistema."""
    return "py" if _system(system) == "win32" else "python3"

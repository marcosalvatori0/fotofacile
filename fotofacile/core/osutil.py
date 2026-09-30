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


def is_windows(system: str | None = None) -> bool:
    """True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)."""
    return _system(system).lower().startswith(("win", "cygwin"))


def chiave_sistema(system: str | None = None) -> str:
    """Nome del sistema normalizzato a «win32» / «darwin» / «linux»."""
    grezzo = _system(system).lower()
    if grezzo.startswith(("win", "cygwin")):
        return "win32"
    if grezzo.startswith("darwin") or grezzo.startswith("mac"):
        return "darwin"
    return grezzo


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


def comando_se_stesso(*argomenti: str) -> list[str]:
    """Come rilanciare **questo stesso programma** con un'opzione interna.

    Serve alle operazioni che devono girare in un processo separato (per esempio
    l'aiutante che parla con il telefono, o la prova che la finestra si apra).

    Funziona in due situazioni molto diverse:

    - **programma impacchettato** (PyInstaller): non esiste un interprete Python separato,
      quindi si richiama l'eseguibile stesso;
    - **dal sorgente**: si richiama il file di avvio del progetto.

    Il percorso si calcola dalla posizione di questo pacchetto, **non** dalla cartella
    corrente: così funziona anche se il programma è stato avviato da un'altra cartella.
    """
    if getattr(sys, "frozen", False):  # PyInstaller
        return [sys.executable, *argomenti]
    avvio = Path(__file__).resolve().parent.parent.parent / "fotofacile.py"
    if avvio.is_file():
        return [sys.executable, str(avvio), *argomenti]
    # Ultima possibilità: il pacchetto è installato e raggiungibile come modulo.
    return [sys.executable, "-m", "fotofacile", *argomenti]


def cartella_progetto() -> Path:
    """Cartella che contiene il pacchetto: serve a far ritrovare i moduli al processo figlio."""
    return Path(__file__).resolve().parent.parent.parent

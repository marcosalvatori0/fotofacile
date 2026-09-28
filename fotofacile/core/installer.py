"""Scaricamento e installazione del componente di collegamento (Android platform-tools).

Gli URL sono quelli ufficiali Google per Windows, macOS e Linux. Su Windows vengono
estratti anche ``AdbWinApi.dll`` e ``AdbWinUsbApi.dll``, indispensabili per ``adb.exe``.
"""

from __future__ import annotations

import platform
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Callable, Generator, Mapping

from .errors import FotoFacileError
from .osutil import app_dir

BASE_URL = "https://dl.google.com/android/repository/"
PLATFORM_TOOLS_URLS = {
    "darwin": BASE_URL + "platform-tools-latest-darwin.zip",
    "linux": BASE_URL + "platform-tools-latest-linux.zip",
    "win32": BASE_URL + "platform-tools-latest-windows.zip",
}
ALIAS = {"windows": "win32", "macos": "darwin", "mac": "darwin"}


def _chiave_sistema(system: str | None) -> str:
    grezzo = (system or platform.system().lower()).lower()
    return ALIAS.get(grezzo, grezzo)


def _nome_eseguibile(system: str | None) -> str:
    return "adb.exe" if _chiave_sistema(system) == "win32" else "adb"


def platform_tools_url(system: str | None = None) -> str:
    """Indirizzo ufficiale del pacchetto per questo sistema operativo."""
    url = PLATFORM_TOOLS_URLS.get(_chiave_sistema(system))
    if url is None:
        raise FotoFacileError(
            "Il download automatico non è disponibile su questo sistema.",
            hint="Scarica «platform-tools» dal sito di Android, scompattalo e riprova.",
        )
    return url


def component_dir(env: Mapping[str, str] | None = None) -> Path:
    """Dove viene installato il componente: <cartella utente>/.fotofacile/platform-tools."""
    return app_dir(env) / "platform-tools"


def is_installed(target_dir: Path | None = None, system: str | None = None) -> bool:
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    return (cartella / _nome_eseguibile(system or sys.platform)).is_file()


def extract_component(zip_path: Path, target_dir: Path, system: str | None = None) -> Path:
    """Estrae il componente (eseguibile e librerie) nella cartella indicata."""
    cartella = Path(target_dir)
    cartella.mkdir(parents=True, exist_ok=True)
    nome_eseguibile = _nome_eseguibile(system or sys.platform)
    try:
        with zipfile.ZipFile(zip_path) as archivio:
            for membro in archivio.namelist():
                if membro.endswith("/"):
                    continue
                nome = Path(membro).name
                if not nome:
                    continue
                with archivio.open(membro) as sorgente, open(cartella / nome, "wb") as uscita:
                    shutil.copyfileobj(sorgente, uscita)
    except zipfile.BadZipFile as errore:
        raise FotoFacileError(
            "Il file scaricato è danneggiato.",
            hint="Controlla la connessione a internet e riprova il download.",
        ) from errore
    eseguibile = cartella / nome_eseguibile
    if not eseguibile.is_file():
        raise FotoFacileError(
            f"Non ho trovato il componente dentro il file scaricato per {cartella}.",
            hint="Riprova il download; se continua a fallire, scarica platform-tools dal sito di Android.",
        )
    if _chiave_sistema(system or sys.platform) != "win32":
        eseguibile.chmod(eseguibile.stat().st_mode | 0o755)
    return eseguibile


def download_file(
    url: str,
    dest: Path,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
    opener: Callable | None = None,
) -> Path:
    """Scarica un file riportando l'avanzamento."""
    import urllib.request

    apri = opener or urllib.request.urlopen
    destinazione = Path(dest)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".scarico")
    try:
        with apri(url, timeout=60) as risposta, open(temporaneo, "wb") as uscita:
            intestazioni = getattr(risposta, "headers", None)
            totale = int((intestazioni or {}).get("Content-Length") or 0)
            ricevuti = 0
            while True:
                if cancel is not None and cancel.is_set():
                    raise FotoFacileError(
                        "Download interrotto.",
                        hint="Puoi riprovare quando vuoi.",
                    )
                blocco = risposta.read(64 * 1024)
                if not blocco:
                    break
                uscita.write(blocco)
                ricevuti += len(blocco)
                if on_progress is not None:
                    on_progress({"ricevuti": ricevuti, "totale": totale})
        destinazione.unlink(missing_ok=True)
        temporaneo.replace(destinazione)
    except FotoFacileError:
        temporaneo.unlink(missing_ok=True)
        raise
    except OSError as errore:
        temporaneo.unlink(missing_ok=True)
        raise FotoFacileError(
            "Non sono riuscito a scaricare il componente di collegamento.",
            hint="Controlla la connessione a internet e riprova.",
        ) from errore
    return destinazione


def install_component(
    target_dir: Path | None = None,
    url: str | None = None,
    downloader: Callable[..., Path] | None = None,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
    system: str | None = None,
) -> Path:
    """Scarica ed estrae il componente, restituendo il percorso dell'eseguibile adb."""
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    indirizzo = url or platform_tools_url(system)
    scarica = downloader or download_file
    archivio = cartella.parent / "platform-tools.zip"
    archivio.parent.mkdir(parents=True, exist_ok=True)
    scarica(indirizzo, archivio, on_progress=on_progress, cancel=cancel)
    return extract_component(archivio, cartella, system=system)


def installa_a_passi(
    target_dir: Path | None = None,
    url: str | None = None,
    on_progress: Callable[[dict], None] | None = None,
    annulla=None,
    opener: Callable | None = None,
    system: str | None = None,
) -> "Generator[float, None, Path]":
    """Scarica ed estrae il componente **a piccoli passi**, senza bloccare la finestra."""
    from .ops import ScaricatoreAPassi

    cartella = Path(target_dir) if target_dir is not None else component_dir()
    indirizzo = url or platform_tools_url(system)
    archivio = cartella.parent / "platform-tools.zip"
    yield from ScaricatoreAPassi(
        indirizzo, archivio, on_progress=on_progress, annulla=annulla, opener=opener
    ).scarica()
    return extract_component(archivio, cartella, system=system)

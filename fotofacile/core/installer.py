"""Scaricamento e installazione del componente di collegamento (Android platform-tools).

Gli URL sono quelli ufficiali Google per Windows, macOS e Linux. Su Windows vengono
estratti anche ``AdbWinApi.dll`` e ``AdbWinUsbApi.dll``, indispensabili per ``adb.exe``.

L'installazione è **atomica**: si estrae in una cartella di appoggio, si controlla che il
programma funzioni davvero e solo allora si sostituisce l'installazione precedente. Se
qualcosa va storto a metà, sul computer non resta un componente rotto a metà.
"""

from __future__ import annotations

import hashlib
import http.client
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Generator, Mapping

from .errors import FotoFacileError
from .osutil import app_dir, flag_nascosta

BASE_URL = "https://dl.google.com/android/repository/"
PLATFORM_TOOLS_URLS = {
    "darwin": BASE_URL + "platform-tools-latest-darwin.zip",
    "linux": BASE_URL + "platform-tools-latest-linux.zip",
    "win32": BASE_URL + "platform-tools-latest-windows.zip",
}
#: Catalogo ufficiale: contiene l'indirizzo preciso e l'impronta di ogni versione.
CATALOGO_URL = BASE_URL + "repository2-3.xml"
ALIAS = {"windows": "win32", "macos": "darwin", "mac": "darwin"}
#: Nome con cui Google indica il nostro sistema dentro il catalogo.
CATALOGO_HOST_OS = {"darwin": "macosx", "linux": "linux", "win32": "windows"}
#: Lunghezza dell'impronta nel catalogo → algoritmo con cui è stata calcolata.
ALGORITMI_PER_LUNGHEZZA = {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}
#: Un platform-tools valido non è mai più piccolo di così: scarta le pagine di errore.
MIN_DIMENSIONE_ARCHIVIO = 1_000_000
#: Quanto si aspetta il catalogo ufficiale prima di ripiegare sull'indirizzo «latest».
#: Volutamente breve: la lettura blocca la finestra, e senza catalogo si scarica comunque
#: (solo senza impronta da verificare).
TIMEOUT_CATALOGO = 6.0


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


def catalogo_platform_tools(system: str | None = None, opener: Callable | None = None) -> tuple[str, str]:
    """Indirizzo *preciso* (con versione) e impronta SHA-1 letti dal catalogo Google.

    Il catalogo ufficiale (``repository2-3.xml``) è l'unico posto in cui Google pubblica
    l'impronta del file da scaricare: usarlo è il modo corretto di verificare che il
    componente non sia stato manomesso lungo la strada.
    """
    import urllib.request

    apri = opener or urllib.request.urlopen
    host = CATALOGO_HOST_OS.get(_chiave_sistema(system))
    if host is None:
        raise FotoFacileError(
            "Il download automatico non è disponibile su questo sistema.",
            hint="Scarica platform-tools dal sito di Android e scompattalo a mano.",
        )
    try:
        with apri(CATALOGO_URL, timeout=TIMEOUT_CATALOGO) as risposta:
            contenuto = risposta.read()
    except (OSError, http.client.HTTPException) as errore:  # D22: non tutte sono OSError
        raise FotoFacileError(
            "Non riesco a leggere il catalogo ufficiale di Android.",
            hint="Controlla la connessione a internet e riprova.",
        ) from errore
    try:
        radice = ET.fromstring(contenuto)
    except ET.ParseError as errore:
        raise FotoFacileError(
            "Il catalogo ufficiale di Android non è leggibile.",
            hint="Riprova più tardi oppure scarica platform-tools dal sito di Android.",
        ) from errore
    for pacchetto in radice.iter("remotePackage"):
        if pacchetto.get("path") != "platform-tools":
            continue
        for archivio in pacchetto.iter("archive"):
            if archivio.findtext("host-os") != host:
                continue
            url = archivio.findtext("complete/url") or ""
            impronta = archivio.findtext("complete/checksum") or ""
            if url and impronta:
                return BASE_URL + url, impronta
    raise FotoFacileError(
        "Il catalogo di Android non contiene il componente per questo sistema.",
        hint="Scarica platform-tools dal sito di Android e scompattalo a mano.",
    )


def impronta_file(percorso: Path, algoritmo: str = "sha1") -> str:
    """Impronta (hash) di un file, calcolata a blocchi: non lo carica mai in memoria."""
    calcolo = hashlib.new(algoritmo)
    with open(percorso, "rb") as sorgente:
        for blocco in iter(lambda: sorgente.read(1024 * 1024), b""):
            calcolo.update(blocco)
    return calcolo.hexdigest()


def component_dir(env: Mapping[str, str] | None = None) -> Path:
    """Dove viene installato il componente: <cartella utente>/.fotofacile/platform-tools."""
    return app_dir(env) / "platform-tools"


def is_installed(target_dir: Path | None = None, system: str | None = None) -> bool:
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    return (cartella / _nome_eseguibile(system or sys.platform)).is_file()


def extract_component(zip_path: Path, target_dir: Path, system: str | None = None) -> Path:
    """Estrae il componente (eseguibile e librerie) e lo installa **in modo atomico**.

    Se una vecchia installazione esiste viene conservata fino all'ultimo istante: si estrae
    in una cartella di appoggio, si controlla che ``adb`` parta davvero e solo allora si
    sostituisce quella vecchia. Un'interruzione a metà lascia il computer esattamente come
    era prima.
    """
    cartella = Path(target_dir)
    cartella.parent.mkdir(parents=True, exist_ok=True)
    nome_eseguibile = _nome_eseguibile(system or sys.platform)
    with tempfile.TemporaryDirectory(prefix="fotofacile-estrai-", dir=str(cartella.parent)) as appoggio:
        provvisoria = Path(appoggio) / "contenuto"
        provvisoria.mkdir()
        _scompatta(zip_path, provvisoria)
        eseguibile_provvisorio = provvisoria / nome_eseguibile
        if not eseguibile_provvisorio.is_file():
            raise FotoFacileError(
                "Il file scaricato non contiene il componente atteso.",
                hint="Riprova il download; se continua a fallire, scarica platform-tools dal sito di Android.",
            )
        if _chiave_sistema(system or sys.platform) != "win32":
            eseguibile_provvisorio.chmod(eseguibile_provvisorio.stat().st_mode | 0o755)
        if _chiave_sistema(system or sys.platform) == _chiave_sistema(sys.platform):
            # Su un sistema diverso il controllo non avrebbe senso (un programma Windows non
            # può partire su macOS): succede solo nei test multipiattaforma.
            _verifica_eseguibile(eseguibile_provvisorio)
        vecchia = cartella.with_name(cartella.name + ".precedente")
        if not cartella.exists() and vecchia.exists():
            # Una sostituzione precedente si era interrotta a metà: la copia buona è rimasta
            # nel ripiego. Rimetterla a posto **prima** di cancellarla è l'unico modo di non
            # lasciare il computer senza componente.
            vecchia.replace(cartella)
        _rimuovi(vecchia)
        if cartella.exists():
            cartella.replace(vecchia)
        try:
            provvisoria.replace(cartella)
        except OSError:
            # La sostituzione non è riuscita: rimettiamo a posto quella di prima.
            if vecchia.exists() and not cartella.exists():
                vecchia.replace(cartella)
            raise
        _rimuovi(vecchia)
    return cartella / nome_eseguibile


def _scompatta(archivio_path: Path, destinazione: Path) -> None:
    """Scompatta il pacchetto appiattendo i percorsi (dentro c'è una sola cartella)."""
    try:
        with zipfile.ZipFile(archivio_path) as archivio:
            for membro in archivio.namelist():
                if membro.endswith("/"):
                    continue
                nome = Path(membro).name
                if not nome or nome.startswith("."):
                    continue
                with archivio.open(membro) as sorgente, open(destinazione / nome, "wb") as uscita:
                    shutil.copyfileobj(sorgente, uscita)
    except zipfile.BadZipFile as errore:
        raise FotoFacileError(
            "Il file scaricato è danneggiato.",
            hint="Controlla la connessione a internet e riprova il download.",
        ) from errore


def _verifica_eseguibile(percorso: Path) -> None:
    """Prova davvero il componente appena estratto: un file presente non è un file funzionante."""
    try:
        esito = subprocess.run(
            [str(percorso), "version"],
            capture_output=True,
            timeout=30,
            creationflags=flag_nascosta(),
        )
    except (OSError, subprocess.TimeoutExpired) as errore:
        raise FotoFacileError(
            "Il componente scaricato non funziona su questo computer.",
            hint="Riprova il download; se il problema resta, segnalalo con «doctor».",
        ) from errore
    if esito.returncode != 0:
        raise FotoFacileError(
            "Il componente scaricato non funziona su questo computer.",
            hint="Riprova il download; se il problema resta, segnalalo con «doctor».",
        )


def _rimuovi(percorso: Path) -> None:
    try:
        if percorso.is_dir():
            shutil.rmtree(percorso, ignore_errors=True)
        else:
            percorso.unlink(missing_ok=True)
    except OSError:  # pragma: no cover - pulizia difensiva
        pass


def download_file(
    url: str,
    dest: Path,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
    opener: Callable | None = None,
    validatore: Callable[[Path], None] | None = None,
) -> Path:
    """Scarica un file riportando l'avanzamento.

    ``validatore`` (facoltativo) riceve il file **prima** che prenda il suo nome definitivo:
    se solleva un errore, il file scaricato non viene mai messo al posto di quello buono.
    """
    import urllib.request

    apri = opener or urllib.request.urlopen
    destinazione = Path(dest)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".scarico")
    completato = False
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
        if validatore is not None:
            validatore(temporaneo)
        temporaneo.replace(destinazione)
        completato = True
    except FotoFacileError:
        raise
    except (OSError, http.client.HTTPException) as errore:  # D22: non tutte sono OSError
        raise FotoFacileError(
            "Non sono riuscito a scaricare il componente di collegamento.",
            hint="Controlla la connessione a internet e riprova.",
        ) from errore
    finally:
        if not completato:
            temporaneo.unlink(missing_ok=True)
    return destinazione


def controlla_archivio(percorso: Path, checksum: str = "") -> None:
    """Controlla che il file scaricato sia davvero il pacchetto ufficiale.

    Due verifiche indipendenti: l'impronta dichiarata da Google (quando disponibile) e la
    struttura del file. Una pagina di errore del server, o un file manomesso, non superano
    nessuna delle due.
    """
    try:
        dimensione = percorso.stat().st_size
    except OSError as errore:
        raise FotoFacileError(
            "Il file scaricato non è leggibile.",
            hint="Riprova il download.",
        ) from errore
    if dimensione < MIN_DIMENSIONE_ARCHIVIO:
        raise FotoFacileError(
            "Il file scaricato è troppo piccolo: probabilmente c'è stato un errore di rete.",
            hint="Controlla la connessione a internet e riprova.",
        )
    if checksum:
        atteso = checksum.strip().lower()
        algoritmo = ALGORITMI_PER_LUNGHEZZA.get(len(atteso))
        if algoritmo is None:
            # Impronta di forma sconosciuta: non si può verificare, ma non si rifiuta il file
            # per questo (il resto dei controlli resta valido).
            algoritmo = ""
        trovato = impronta_file(percorso, algoritmo) if algoritmo else ""
        if algoritmo and trovato != atteso:
            raise FotoFacileError(
                "Il componente scaricato non corrisponde a quello ufficiale di Android.",
                hint="Riprova il download da una rete affidabile; se il problema resta, segnalalo.",
            )
    if not zipfile.is_zipfile(percorso):
        raise FotoFacileError(
            "Il file scaricato non è un pacchetto valido.",
            hint="Controlla la connessione a internet e riprova.",
        )


def install_component(
    target_dir: Path | None = None,
    url: str | None = None,
    downloader: Callable[..., Path] | None = None,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
    system: str | None = None,
    opener: Callable | None = None,
) -> Path:
    """Scarica, verifica ed estrae il componente, restituendo il percorso dell'eseguibile adb."""
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    indirizzo, checksum = risolvi_sorgente(url, opener=opener, system=system)
    scarica = downloader or download_file
    archivio = cartella.parent / "platform-tools.zip"
    archivio.parent.mkdir(parents=True, exist_ok=True)
    try:
        scarica(
            indirizzo,
            archivio,
            on_progress=on_progress,
            cancel=cancel,
            validatore=lambda percorso: controlla_archivio(percorso, checksum),
        )
        return extract_component(archivio, cartella, system=system)
    finally:
        # Il pacchetto (~10 MB) serve solo all'estrazione: non va lasciato sul computer.
        _rimuovi(archivio)


def risolvi_sorgente(
    url: str | None = None, opener: Callable | None = None, system: str | None = None
) -> tuple[str, str]:
    """Indirizzo e impronta del pacchetto: dal catalogo ufficiale, con ripiego su «latest»."""
    if url is not None:
        return url, ""
    try:
        return catalogo_platform_tools(system=system, opener=opener)
    except FotoFacileError:
        # Il catalogo è un di più: senza di esso si scarica comunque, solo senza impronta.
        return platform_tools_url(system), ""


def installa_a_passi(
    target_dir: Path | None = None,
    url: str | None = None,
    on_progress: Callable[[dict], None] | None = None,
    annulla=None,
    opener: Callable | None = None,
    system: str | None = None,
) -> "Generator[float, None, Path]":
    """Scarica, verifica ed estrae il componente **a piccoli passi**, senza bloccare la finestra."""
    from .ops import ScaricatoreAPassi

    cartella = Path(target_dir) if target_dir is not None else component_dir()
    indirizzo, checksum = risolvi_sorgente(url, opener=opener, system=system)
    archivio = cartella.parent / "platform-tools.zip"
    try:
        yield from ScaricatoreAPassi(
            indirizzo,
            archivio,
            on_progress=on_progress,
            annulla=annulla,
            opener=opener,
            validatore=lambda percorso: controlla_archivio(percorso, checksum),
        ).scarica()
        return extract_component(archivio, cartella, system=system)
    finally:
        # Vale anche quando il download viene abbandonato a metà (finestra chiusa):
        # il pacchetto non deve restare sul computer.
        _rimuovi(archivio)

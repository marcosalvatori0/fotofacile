"""Come FotoFacile parla con il telefono.

Il programma non usa **un solo** metodo di collegamento, ma ne prova diversi e sceglie da sé
il migliore disponibile. Questo è il punto centrale: la persona che usa il programma non deve
attivare niente di speciale sul telefono.

I modi di collegamento possibili sono:

``Collegamento diretto`` (nessun Debug USB, nessuna impostazione da cambiare)
    Il telefono si presenta come una «fotocamera» o come un «lettore multimediale», che è
    il comportamento normale di ogni telefono Android appena lo si collega. Cambia il modo
    di parlarci a seconda del sistema:

    - **macOS**: PTP/MTP tramite il componente di sistema ``ImageCaptureCore``;
    - **Windows**: WPD tramite ``Shell.Application`` (lo stesso meccanismo di Esplora file);
    - **Linux**: MTP tramite ``gio``/gvfs (lo stesso meccanismo di File).

``Debug USB`` (collegamento rapido, se è già attivo)
    Se per qualche motivo il Debug USB è attivo, si usa ``adb``: è più veloce e permette di
    cancellare i file dal telefono. Non è mai obbligatorio.

``Demo``
    Telefono finto, per provare il programma senza nessun dispositivo.

Tutti i metodi sono **a passi**: le operazioni sono generatori che cedono il controllo alla
finestra fra un pezzo e l'altro (vedi :mod:`fotofacile.core.ops`). Nessun thread.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Generator, Protocol, Sequence, runtime_checkable

from .adb_passi import AdbAPassi
from .devices import DeviceInfo
from .errors import FotoFacileError
from .scanner import DEFAULT_ROOTS, MediaFile, build_scan_command

# ── come si presenta un trasporto ────────────────────────────────────────


@runtime_checkable
class Trasporto(Protocol):
    """Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a passi.

    ``remote_path`` è un identificativo opaco: per adb è il percorso del file sul telefono,
    per gli altri collegamenti può essere qualcos'altro. Va sempre usato così come è stato
    ricevuto da :meth:`cerca_media`, senza interpretarlo.
    """

    #: Nome breve mostrato all'utente («Collegamento diretto»).
    nome: str
    #: Una riga che spiega perché è stato scelto questo modo di collegamento.
    spiegazione: str

    def disponibile(self) -> bool:
        """True se su questo computer il collegamento può funzionare (non serve un telefono)."""

    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        """Elenca i telefoni collegati e il loro stato."""

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        """Elenca foto e video presenti sul telefono."""

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        """Copia un file dal telefono, restituendo i byte scritti."""

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        """Cancella un file dal telefono (solo dopo una copia verificata)."""

    def riavvia(self) -> Generator[float, None, None]:
        """Prova a far ripartire il collegamento (usato dal pulsante «Riavvia collegamento»)."""

    def pulisci(self) -> None:
        """Rimuove i file temporanei di lavoro."""


# ── adb (Debug USB): collegamento rapido, mai obbligatorio ───────────────


class TrasportoAdb:
    """Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce."""

    def __init__(self, adb_path: str, intervallo: float = 0.02, cartella_lavoro: Path | None = None) -> None:
        self.nome = "Collegamento rapido"
        self.spiegazione = "Uso il Debug USB, che hai già attivo: è il collegamento più veloce."
        self._adb = AdbAPassi(adb_path, intervallo=intervallo, cartella_lavoro=cartella_lavoro)
        self.adb_path = adb_path

    def disponibile(self) -> bool:
        return bool(self.adb_path) and Path(self.adb_path).is_file()

    @property
    def intervallo(self) -> float:
        """Pausa fra un controllo e l'altro (nei test si azzera per non aspettare)."""
        return self._adb.intervallo

    @intervallo.setter
    def intervallo(self, valore: float) -> None:
        self._adb.intervallo = valore

    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        return (yield from self._adb.dispositivi())

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        comando = build_scan_command(DEFAULT_ROOTS, include_videos=include_videos)
        return (
            yield from self._adb.cerca_media(
                serial, comando, annulla=annulla, include_videos=include_videos
            )
        )

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        return (
            yield from self._adb.copia(
                serial,
                remoto,
                destinazione,
                on_scritti=on_scritti,
                annulla=annulla,
                remoto_dimensione=remoto_dimensione,
            )
        )

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        return (yield from self._adb.cancella(serial, remoto))

    def riavvia(self) -> Generator[float, None, None]:
        return (yield from self._adb.riavvia())

    def pulisci(self) -> None:
        self._adb.pulisci()


# ── telefono finto (demo e test) ─────────────────────────────────────────


class TrasportoDemo:
    """Telefono finto, senza dispositivo: serve alla modalità demo e ai test."""

    def __init__(self, backend=None, intervallo: float = 0.02, pezzi_per_passo: int = 4) -> None:
        from .adb_passi import AdbDemoAPassi
        from .demo import DemoAdbBackend

        self.nome = "Telefono demo"
        self.spiegazione = "Stai usando un telefono finto: serve solo a vedere come funziona."
        self._demo = AdbDemoAPassi(
            backend if backend is not None else DemoAdbBackend(), intervallo, pezzi_per_passo
        )
        self.backend = self._demo.backend

    def disponibile(self) -> bool:
        return True

    @property
    def intervallo(self) -> float:
        return self._demo.intervallo

    @intervallo.setter
    def intervallo(self, valore: float) -> None:
        self._demo.intervallo = valore

    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        return (yield from self._demo.dispositivi())

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        return (
            yield from self._demo.cerca_media(
                serial, "demo", include_videos=include_videos, annulla=annulla
            )
        )

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        return (
            yield from self._demo.copia(
                serial,
                remoto,
                destinazione,
                on_scritti=on_scritti,
                annulla=annulla,
                remoto_dimensione=remoto_dimensione,
            )
        )

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        return (yield from self._demo.cancella(serial, remoto))

    def riavvia(self) -> Generator[float, None, None]:
        return (yield from self._demo.riavvia())

    def pulisci(self) -> None:
        self._demo.pulisci()


# ── più trasporti insieme: si usa quello che vede davvero il telefono ────


class TrasportoComposto:
    """Prova i collegamenti disponibili in ordine e usa il primo che trova un telefono.

    Serve a non obbligare nessuno a scegliere: chi ha già il Debug USB attivo usa il
    collegamento veloce, chi non ce l'ha usa il collegamento diretto, e in nessun caso
    l'utente deve sapere quale dei due è scattato.
    """

    def __init__(self, trasporti: Sequence[Trasporto]) -> None:
        self.trasporti = [trasporto for trasporto in trasporti if trasporto.disponibile()]
        if not self.trasporti:
            raise FotoFacileError(
                "Non riesco a collegarmi al telefono su questo computer.",
                hint="Apri la diagnosi con «doctor» e segnala il risultato.",
            )
        self._scelto: Trasporto | None = None
        self.nome = self.trasporti[0].nome
        self.spiegazione = self.trasporti[0].spiegazione

    @property
    def attivo(self) -> Trasporto:
        """Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora risposto)."""
        return self._scelto or self.trasporti[0]

    @property
    def intervallo(self) -> float:
        return getattr(self.attivo, "intervallo", 0.02)

    @intervallo.setter
    def intervallo(self, valore: float) -> None:
        for trasporto in self.trasporti:
            if hasattr(trasporto, "intervallo"):
                trasporto.intervallo = valore

    def disponibile(self) -> bool:
        return True

    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        for indice, trasporto in enumerate(self.trasporti):
            if indice:
                yield 0.0  # lascia respirare la finestra fra un tentativo e l'altro
            try:
                trovati = yield from trasporto.dispositivi()
            except FotoFacileError:
                continue  # questo collegamento non è utilizzabile: si prova il prossimo
            if trovati:
                self._scegli(trasporto)
                return trovati
        return []

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        return (
            yield from self.attivo.cerca_media(serial, include_videos=include_videos, annulla=annulla)
        )

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        return (
            yield from self.attivo.copia(
                serial,
                remoto,
                destinazione,
                on_scritti=on_scritti,
                annulla=annulla,
                remoto_dimensione=remoto_dimensione,
            )
        )

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        return (yield from self.attivo.cancella(serial, remoto))

    def riavvia(self) -> Generator[float, None, None]:
        """Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante."""
        for trasporto in self.trasporti:
            try:
                yield from trasporto.riavvia()
            except FotoFacileError:
                continue
        self._scelto = None
        return None

    def pulisci(self) -> None:
        for trasporto in self.trasporti:
            try:
                trasporto.pulisci()
            except Exception:  # pulizia difensiva: non deve mai bloccare la chiusura
                continue

    def _scegli(self, trasporto: Trasporto) -> None:
        self._scelto = trasporto
        self.nome = trasporto.nome
        self.spiegazione = trasporto.spiegazione


# ── scelta automatica ────────────────────────────────────────────────────


def trasporti_disponibili(
    env=None,
    sistema: str | None = None,
    adb_path: str | None = None,
) -> list[Trasporto]:
    """Elenco dei collegamenti utilizzabili su questo computer, dal più comodo al ripiego."""
    import sys

    from .adb import find_adb
    from .osutil import is_windows, chiave_sistema

    piattaforma = chiave_sistema(sistema or sys.platform)
    ambiente = env
    elenco: list[Trasporto] = []

    # 1. Collegamento diretto: non chiede niente all'utente.
    diretto = _trasporto_diretto(piattaforma, ambiente)
    if diretto is not None:
        elenco.append(diretto)

    # 2. Debug USB, solo se è già attivo: è un di più, mai un obbligo.
    percorso = adb_path or find_adb(env=ambiente, is_windows=is_windows(sistema))
    if percorso:
        elenco.append(TrasportoAdb(percorso))

    return elenco


def _trasporto_diretto(piattaforma: str, env) -> "Trasporto | None":
    """Costruisce il collegamento diretto adatto al sistema, se esiste."""
    from .trasporto_mac import TrasportoPtpMac
    from .trasporto_linux import TrasportoMtpLinux
    from .trasporto_win import TrasportoWpdWindows

    if piattaforma == "darwin":
        trasporto = TrasportoPtpMac(env=env)
        return trasporto if trasporto.disponibile() else None
    if piattaforma == "win32":
        trasporto = TrasportoWpdWindows(env=env)
        return trasporto if trasporto.disponibile() else None
    if piattaforma == "linux":
        trasporto = TrasportoMtpLinux(env=env)
        return trasporto if trasporto.disponibile() else None
    return None


def scegli_trasporto(env=None, sistema: str | None = None, adb_path: str | None = None) -> Trasporto | None:
    """Il modo migliore disponibile, oppure ``None`` se non ce n'è nessuno."""
    elenco = trasporti_disponibili(env=env, sistema=sistema, adb_path=adb_path)
    if not elenco:
        return None
    if len(elenco) == 1:
        return elenco[0]
    return TrasportoComposto(elenco)

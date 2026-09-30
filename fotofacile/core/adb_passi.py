"""Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia grafica.

Sono le stesse operazioni di :mod:`fotofacile.core.adb`, ma invece di bloccare il programma
finché il comando non è finito, cedono il controllo alla finestra fra un controllo e l'altro.
In questo modo l'app resta reattiva senza usare thread.

L'output lungo (per esempio l'elenco di migliaia di foto) viene scritto su un file temporaneo:
così il processo non resta mai bloccato a scrivere nel tubo di comunicazione.
"""

from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path
from typing import Callable, Generator, Sequence

from .adb import CHUNK_SIZE, shell_quote
from .devices import DeviceInfo, parse_devices
from .errors import FotoFacileError, traduci_errore_file
from .format import format_size
from .ops import Annullato, ProcessoEsterno
from .scanner import (
    FALLBACK_MAX_DEPTH,
    FALLBACK_ROOT,
    MediaFile,
    build_scan_command,
    parse_stat_stream,
)

TIMEOUT_SCANSIONE = 180.0
TIMEOUT_COPIA = 900.0
#: Sotto questa soglia si avvisa prima di iniziare: meglio dirlo subito che a metà video.
SPAZIO_MINIMO = 16 * 1024 * 1024


def percorso_temporaneo(destinazione: Path) -> Path:
    """Nome del file «a metà», unico per processo.

    Il numero del processo evita che due copie avviate insieme (due finestre aperte sulla
    stessa cartella) scrivano nello stesso file e si rovinino a vicenda.
    """
    return destinazione.with_name(f"{destinazione.name}.{os.getpid()}.part")


def _dimensione_prevista(dimensione: int | None) -> int | None:
    """Quanti byte serviranno, se si sa: serve a non chiedere spazio a caso."""
    return dimensione if dimensione and dimensione > 0 else None


def _controlla_spazio(destinazione: Path, dimensione: int | None = None) -> None:
    """Avvisa in modo comprensibile se il disco è pieno, **prima** di iniziare a copiare.

    Senza questo controllo il disco pieno arrivava come un generico «adb non è riuscito»,
    che non dice all'utente cosa fare.

    Con ``dimensione`` si controlla che il file ci stia davvero; senza, si pretende solo un
    margine minimo, perché chiedere 16 MB liberi per una foto da 200 KB sarebbe assurdo.
    """
    import shutil

    cartella = destinazione.parent
    while not cartella.exists() and cartella != cartella.parent:
        cartella = cartella.parent
    try:
        liberi = shutil.disk_usage(cartella).free
    except OSError:  # pragma: no cover - disco di rete o permessi
        return
    if dimensione is not None and dimensione > 0:
        if dimensione <= liberi:
            return
        richiesto = format_size(dimensione)
    else:
        if liberi >= SPAZIO_MINIMO:
            return
        richiesto = "il file da copiare"
    raise FotoFacileError(
        f"Non c'è più spazio per salvare {destinazione.name}.",
        hint=(
            f"In {cartella} restano solo {format_size(liberi)} e servono {richiesto}. "
            "Libera spazio oppure scegli un'altra cartella: le foto già copiate sono al sicuro."
        ),
    )


def _esito_di_copia(processo: ProcessoEsterno, destinazione: Path) -> None:
    """Controlla che il comando di copia sia finito bene, spiegando il motivo se no."""
    try:
        processo.esito()
    except FotoFacileError as errore:
        # Il disco pieno non arriva mai come eccezione Python (a scrivere è il comando
        # esterno): lo si riconosce dal testo dell'errore riportato dal sistema.
        testo = f"{errore.hint} {errore.message}".lower()
        if "no space" in testo or "spazio" in testo or "enospc" in testo:
            raise FotoFacileError(
                f"Non c'è più spazio mentre copiavo {destinazione.name}.",
                hint="Libera spazio e riprova: le foto già copiate sono al sicuro.",
            ) from errore
        raise


class AdbAPassi:
    """Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione."""

    def __init__(
        self,
        adb_path: str,
        intervallo: float = 0.02,
        cartella_lavoro: Path | None = None,
        orologio: Callable[[], float] = time.monotonic,
    ) -> None:
        self.adb_path = adb_path
        self.intervallo = intervallo
        self.orologio = orologio
        self.cartella_lavoro = Path(cartella_lavoro) if cartella_lavoro is not None else Path(
            tempfile.mkdtemp(prefix="fotofacile-lavoro-")
        )
        self.cartella_lavoro.mkdir(parents=True, exist_ok=True)

    # ── aiuti interni ─────────────────────────────────────────────────────
    def _file_temporaneo(self, prefisso: str) -> Path:
        descrittore, nome = tempfile.mkstemp(prefix=prefisso, dir=self.cartella_lavoro)
        os.close(descrittore)
        return Path(nome)

    def _processo(
        self,
        args: Sequence[str],
        timeout: float,
        umano: str = "",
        hint: str = "",
        output_file: Path | None = None,
        leggi_output: bool = True,
    ) -> ProcessoEsterno:
        return ProcessoEsterno(
            [self.adb_path, *args],
            timeout=timeout,
            umano=umano,
            hint=hint,
            output_file=output_file,
            orologio=self.orologio,
            leggi_output=leggi_output,
        )

    def pulisci(self) -> None:
        """Rimuove la cartella di appoggio usata per gli elenchi temporanei."""
        import shutil

        try:
            shutil.rmtree(self.cartella_lavoro, ignore_errors=True)
        except OSError:  # pragma: no cover - pulizia difensiva
            pass

    def _ripulisci(self, percorso: Path) -> None:
        try:
            percorso.unlink(missing_ok=True)
        except OSError:  # pragma: no cover - difensivo
            pass

    # ── operazioni ────────────────────────────────────────────────────────
    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        """Elenca i telefoni collegati e il loro stato."""
        processo = self._processo(
            ["devices", "-l"],
            timeout=30.0,
            umano="Non riesco a sentire il telefono.",
            hint="Controlla il cavo e riprova; se serve, premi «Riprova il collegamento».",
        )
        try:
            esito = yield from processo.aspetta()
        finally:
            # Vale anche se il controllo viene abbandonato (cambio schermata, finestra chiusa).
            processo.termina()
        return parse_devices(esito.output)

    def cerca_media(
        self,
        serial: str,
        comando: str,
        timeout: float = TIMEOUT_SCANSIONE,
        annulla=None,
        ripiega: bool = True,
        include_videos: bool = True,
    ) -> Generator[float, None, list[MediaFile]]:
        """Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria.

        Il ripiego serve perché molti telefoni tengono le foto in cartelle non prevedibili
        (per esempio Telegram, WeChat, «Edited»): senza di esso l'utente non vedrebbe nulla
        e non saprebbe perché. Il ripiego però deve rispettare la scelta «includi i video»:
        altrimenti chi ha tolto la spunta se li ritroverebbe comunque in elenco.
        """
        trovati = yield from self._esegui_ricerca(serial, comando, timeout, annulla)
        if trovati or not ripiega or (annulla is not None and annulla.is_set()):
            return trovati
        comando_ampio = build_scan_command(
            [FALLBACK_ROOT], include_videos=include_videos, max_depth=FALLBACK_MAX_DEPTH
        )
        return (yield from self._esegui_ricerca(serial, comando_ampio, timeout, annulla))

    def _esegui_ricerca(
        self, serial: str, comando: str, timeout: float, annulla
    ) -> Generator[float, None, list[MediaFile]]:
        file_output = self._file_temporaneo("ricerca-")
        processo = self._processo(
            ["-s", serial, "shell", comando],
            timeout=timeout,
            umano="La ricerca delle foto sul telefono non è andata a buon fine.",
            hint="Sblocca il telefono e riprova: la ricerca si interrompe se lo schermo si blocca.",
            output_file=file_output,
        )
        try:
            processo.avvia()
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    processo.termina()
                    raise Annullato()
                if processo.scaduto():
                    processo.termina()
                    raise FotoFacileError(
                        "La ricerca delle foto è durata troppo tempo.",
                        hint="Riprova: se succede sempre, prova con un altro cavo USB.",
                    )
                yield self.intervallo
            esito = processo.esito()
            return parse_stat_stream(esito.output)
        finally:
            processo.termina()
            self._ripulisci(file_output)

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        timeout: float = TIMEOUT_COPIA,
        chunk_size: int = CHUNK_SIZE,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        """Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla fine.

        L'output del comando **è** il file appena scritto: non viene mai riletto in memoria
        (un video da 4 GB diventerebbe altrimenti una stringa da 4 GB), e il tempo necessario
        è controllato guardando la dimensione del file a metà.
        """
        destinazione = Path(destinazione)
        _controlla_spazio(destinazione, _dimensione_prevista(remoto_dimensione))
        temporaneo = percorso_temporaneo(destinazione)
        processo = self._processo(
            ["-s", serial, "exec-out", "cat", shell_quote(remoto)],
            timeout=timeout,
            umano=f"Non sono riuscito a copiare {destinazione.name}.",
            hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
            output_file=temporaneo,
            leggi_output=False,
        )
        scritti = 0
        completato = False
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
            processo.avvia()
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    raise Annullato()
                if processo.scaduto():
                    raise FotoFacileError(
                        f"La copia di {destinazione.name} è durata troppo tempo.",
                        hint="Riprova: se succede sempre con i video, prova un altro cavo USB.",
                    )
                scritti = self._dimensione(temporaneo, scritti, on_scritti)
                yield self.intervallo
            scritti = self._dimensione(temporaneo, scritti, on_scritti)
            _esito_di_copia(processo, destinazione)
            self._rallenta_scrittura(temporaneo)
            os.replace(temporaneo, destinazione)
            completato = True
        except Annullato:
            raise
        except FotoFacileError:
            raise
        except OSError as errore:
            raise traduci_errore_file(errore, destinazione) from errore
        finally:
            # Vale anche se il lavoro viene abbandonato (chiusura della finestra o cambio idea):
            # il processo viene interrotto e il file parziale rimosso.
            processo.termina()
            if not completato:
                self._ripulisci(temporaneo)
        return scritti

    def _dimensione(
        self, temporaneo: Path, precedente: int, on_scritti: Callable[[int], None] | None
    ) -> int:
        try:
            attuale = temporaneo.stat().st_size
        except OSError:
            return precedente
        if attuale != precedente and on_scritti is not None:
            on_scritti(attuale)
        return attuale

    def _rallenta_scrittura(self, temporaneo: Path) -> None:
        """Assicura che i byte siano davvero sul disco prima di rinominare il file."""
        try:
            descrittore = os.open(temporaneo, os.O_RDWR)
        except OSError:  # pragma: no cover - difensivo
            return
        try:
            os.fsync(descrittore)
        except OSError:  # pragma: no cover - alcuni file system non lo permettono
            pass
        finally:
            os.close(descrittore)

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        """Cancella un file dal telefono (solo dopo che la copia è stata verificata)."""
        processo = self._processo(
            ["-s", serial, "shell", "rm", "-f", shell_quote(remoto)],
            timeout=60.0,
            umano="Non sono riuscito a cancellare un file dal telefono.",
            hint="Il file resta sul telefono: puoi cancellarlo a mano in un secondo momento.",
        )
        try:
            yield from processo.aspetta()
        finally:
            processo.termina()
        return None

    def riavvia(self) -> Generator[float, None, None]:
        """Riavvia il collegamento: risolve molti casi di «telefono non risponde»."""
        chiusura = self._processo(
            ["kill-server"],
            timeout=30.0,
            umano="Non riesco a chiudere il collegamento.",
            hint="Riprova fra qualche secondo.",
        )
        avvio = self._processo(
            ["start-server"],
            timeout=60.0,
            umano="Non riesco ad avviare il collegamento.",
            hint="Scollega e ricollega il cavo, poi riprova.",
        )
        try:
            try:
                yield from chiusura.aspetta()
            except FotoFacileError:
                pass
            yield from avvio.aspetta()
        finally:
            # Anche interrompendo, nessuno dei due comandi deve restare vivo.
            chiusura.termina()
            avvio.termina()
        return None


class AdbDemoAPassi:
    """Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo vero.

    Serve alla modalità demo: permette di provare tutta la procedura (compresa la barra di
    avanzamento) su un computer dove non è collegato nessun telefono.
    """

    def __init__(
        self,
        backend=None,
        intervallo: float = 0.02,
        pezzi_per_passo: int = 4,
        cartella_lavoro: Path | None = None,
    ) -> None:
        from .demo import DemoAdbBackend

        self.backend = backend if backend is not None else DemoAdbBackend()
        self.intervallo = intervallo
        self.pezzi_per_passo = max(1, pezzi_per_passo)
        # Serve a `pulisci()`, che l'app chiama alla chiusura: senza questo attributo la
        # pulizia falliva con AttributeError (errore non coperto da `except OSError`).
        self.cartella_lavoro = Path(cartella_lavoro) if cartella_lavoro is not None else Path(
            tempfile.mkdtemp(prefix="fotofacile-demo-")
        )

    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        yield self.intervallo
        return parse_devices(self.backend.devices_raw())

    def cerca_media(
        self, serial: str, comando: str, include_videos: bool = True, **_kwargs
    ) -> Generator[float, None, list[MediaFile]]:
        yield self.intervallo
        trovati = parse_stat_stream(self.backend.list_media_raw(serial, comando))
        if include_videos:
            return trovati
        return [file for file in trovati if file.kind != "video"]

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        chunk_size: int = CHUNK_SIZE,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        destinazione = Path(destinazione)
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
        except OSError as errore:
            # Come per il telefono vero: un OSError grezzo fermerebbe l'intera copia.
            raise traduci_errore_file(errore, destinazione) from errore
        _controlla_spazio(destinazione, _dimensione_prevista(remoto_dimensione))
        temporaneo = percorso_temporaneo(destinazione)
        scritti = 0
        completato = False
        try:
            with open(temporaneo, "wb") as uscita:
                for indice, blocco in enumerate(
                    self.backend.stream_file(serial, remoto, chunk_size=chunk_size), start=1
                ):
                    if annulla is not None and annulla.is_set():
                        raise Annullato()
                    uscita.write(blocco)
                    scritti += len(blocco)
                    if on_scritti is not None:
                        on_scritti(scritti)
                    if indice % self.pezzi_per_passo == 0:
                        yield self.intervallo
                uscita.flush()
                os.fsync(uscita.fileno())
            os.replace(temporaneo, destinazione)
            completato = True
        except Annullato:
            raise
        except FotoFacileError:
            raise
        except OSError as errore:
            raise traduci_errore_file(errore, destinazione) from errore
        finally:
            # Vale anche se la copia viene abbandonata a metà (chiusura della finestra):
            # il file parziale non deve restare nella cartella delle foto.
            if not completato:
                self._ripulisci(temporaneo)
        return scritti

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        yield self.intervallo
        self.backend.delete_file(serial, remoto)
        return None

    def riavvia(self) -> Generator[float, None, None]:
        yield self.intervallo
        self.backend.restart_server()
        return None

    def pulisci(self) -> None:
        """Rimuove la cartella di appoggio del telefono finto."""
        import shutil

        try:
            shutil.rmtree(self.cartella_lavoro, ignore_errors=True)
        except OSError:  # pragma: no cover - pulizia difensiva
            pass

    def _ripulisci(self, percorso: Path) -> None:
        try:
            percorso.unlink(missing_ok=True)
        except OSError:  # pragma: no cover - difensivo
            pass

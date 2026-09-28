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
from .errors import FotoFacileError
from .ops import Annullato, ProcessoEsterno
from .scanner import MediaFile, parse_stat_stream

TIMEOUT_SCANSIONE = 180.0
TIMEOUT_COPIA = 900.0


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
    ) -> ProcessoEsterno:
        return ProcessoEsterno(
            [self.adb_path, *args],
            timeout=timeout,
            umano=umano,
            hint=hint,
            output_file=output_file,
            orologio=self.orologio,
        )

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
            hint="Controlla il cavo e riprova; se serve, premi «Riavvia collegamento».",
        )
        esito = yield from processo.aspetta()
        return parse_devices(esito.output)

    def cerca_media(
        self, serial: str, comando: str, timeout: float = TIMEOUT_SCANSIONE
    ) -> Generator[float, None, list[MediaFile]]:
        """Esegue la ricerca delle foto sul telefono e restituisce i file trovati."""
        file_output = self._file_temporaneo("ricerca-")
        processo = self._processo(
            ["-s", serial, "shell", comando],
            timeout=timeout,
            umano="La ricerca delle foto sul telefono non è andata a buon fine.",
            hint="Sblocca il telefono e riprova: la ricerca si interrompe se lo schermo si blocca.",
            output_file=file_output,
        )
        try:
            esito = yield from processo.aspetta()
            return parse_stat_stream(esito.output)
        finally:
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
    ) -> Generator[float, None, int]:
        """Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla fine."""
        destinazione = Path(destinazione)
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        temporaneo = destinazione.with_name(destinazione.name + ".part")
        processo = self._processo(
            ["-s", serial, "exec-out", "cat", shell_quote(remoto)],
            timeout=timeout,
            umano=f"Non sono riuscito a copiare {destinazione.name}.",
            hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
            output_file=temporaneo,
        )
        scritti = 0
        try:
            processo.avvia()
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    processo.termina()
                    raise Annullato()
                if processo.scaduto():
                    processo.termina()
                    raise FotoFacileError(
                        f"La copia di {destinazione.name} è durata troppo tempo.",
                        hint="Riprova: se succede sempre con i video, prova un altro cavo USB.",
                    )
                scritti = self._dimensione(temporaneo, scritti, on_scritti)
                yield self.intervallo
            scritti = self._dimensione(temporaneo, scritti, on_scritti)
            processo.esito()
            self._rallenta_scrittura(temporaneo)
            os.replace(temporaneo, destinazione)
        except Annullato:
            processo.termina()
            self._ripulisci(temporaneo)
            raise
        except FotoFacileError:
            processo.termina()
            self._ripulisci(temporaneo)
            raise
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
        yield from processo.aspetta()
        return None

    def riavvia(self) -> Generator[float, None, None]:
        """Riavvia il collegamento: risolve molti casi di «telefono non risponde»."""
        chiusura = self._processo(
            ["kill-server"],
            timeout=30.0,
            umano="Non riesco a chiudere il collegamento.",
            hint="Riprova fra qualche secondo.",
        )
        try:
            yield from chiusura.aspetta()
        except FotoFacileError:
            pass
        avvio = self._processo(
            ["start-server"],
            timeout=60.0,
            umano="Non riesco ad avviare il collegamento.",
            hint="Scollega e ricollega il cavo, poi riprova.",
        )
        yield from avvio.aspetta()
        return None

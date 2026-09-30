"""Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.

L'orchestrazione (:func:`transfer_steps`) è un **generatore**: cede il controllo alla
finestra fra un pezzo e l'altro, così la grafica resta reattiva senza usare thread
(vedi :mod:`fotofacile.core.ops`). Chi non ha bisogno dei passi (test, riga di comando)
usa :func:`transfer`, che la porta a termine di seguito.

Regole di sicurezza dei dati:
- si scrive sempre su un file temporaneo ``.part`` e si rinomina solo a copia verificata;
- se la copia viene annullata o fallisce, il temporaneo viene rimosso (mai file troncati);
- la dimensione finale viene confrontata con quella dichiarata dal telefono;
- la cancellazione dal telefono avviene solo per i file copiati e verificati.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Generator

from .adb import AdbBackend
from .errors import FotoFacileError, traduci_errore_file
from .history import History
from .adb_passi import percorso_temporaneo
from .ops import Annullato, esegui_fino_alla_fine
from .planner import TransferOptions, TransferPlan
from .scanner import MediaFile

CHUNK_SIZE = 64 * 1024
INTERVALLO_AGGIORNAMENTO = 0.08
PAUSA_PREDEFINITA = 0.0


@dataclass
class Progress:
    total_files: int = 0
    done_files: int = 0
    current_name: str = ""
    bytes_done: int = 0
    bytes_total: int = 0
    speed_bps: float = 0.0
    eta_seconds: float | None = None
    #: Avanzamento del file in corso, per la seconda barra: senza questi due campi la barra
    #: del singolo file ripeteva semplicemente quella generale.
    file_bytes_done: int = 0
    file_bytes_total: int = 0


@dataclass
class TransferResults:
    copied: list[Path] = field(default_factory=list)
    skipped: int = 0
    failed: list[tuple[MediaFile, str]] = field(default_factory=list)
    bytes_copied: int = 0
    elapsed: float = 0.0
    cancelled: bool = False
    deleted_from_phone: int = 0
    warnings: list[str] = field(default_factory=list)


def _rimuovi(percorso: Path) -> None:
    try:
        percorso.unlink(missing_ok=True)
    except OSError:  # pragma: no cover - pulizia difensiva
        pass


def _chiudi(generatore) -> None:
    chiusura = getattr(generatore, "close", None)
    if chiusura is not None:
        try:
            chiusura()
        except Exception:  # pragma: no cover - la chiusura non deve mai bloccare
            pass


_trasforma = traduci_errore_file  # un unico posto dove si traducono gli errori di file


def download_file_stream(
    adb: AdbBackend,
    serial: str,
    remote_path: str,
    dest_path: Path,
    on_bytes: Callable[[int, bytes], None] | None = None,
    cancel=None,
    chunk_size: int = CHUNK_SIZE,
) -> int:
    """Scrive un file dal telefono su disco passando da un temporaneo ``.part`` (modo diretto)."""
    destinazione = Path(dest_path)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = percorso_temporaneo(destinazione)
    flusso = adb.stream_file(serial, remote_path, chunk_size=chunk_size)
    scritti = 0
    try:
        with open(temporaneo, "wb") as uscita:
            for blocco in flusso:
                if cancel is not None and cancel.is_set():
                    raise Annullato()
                uscita.write(blocco)
                scritti += len(blocco)
                if on_bytes is not None:
                    on_bytes(len(blocco), blocco)
            uscita.flush()
            os.fsync(uscita.fileno())
        os.replace(temporaneo, destinazione)
    except Annullato:
        _rimuovi(temporaneo)
        raise
    except FotoFacileError:
        _rimuovi(temporaneo)
        raise
    except OSError as errore:
        _rimuovi(temporaneo)
        raise _trasforma(errore, destinazione) from errore
    finally:
        _chiudi(flusso)
    return scritti


class CopiatoreInterno:
    """Copia usando un backend in memoria (modalità demo e test) o il telefono demo.

    Per un telefono vero l'interfaccia grafica usa
    :class:`fotofacile.core.adb_passi.AdbAPassi`, che copia a piccoli passi senza bloccare
    niente; questo copiatore esiste per i test e per la modalità demo.
    """

    def __init__(self, backend: AdbBackend, chunk_size: int = CHUNK_SIZE) -> None:
        self.backend = backend
        self.chunk_size = chunk_size

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        totale = 0

        def conta(byte: int, _blocco: bytes) -> None:
            nonlocal totale
            totale += byte
            if on_scritti is not None:
                on_scritti(totale)

        scritti = download_file_stream(
            self.backend,
            serial,
            remoto,
            Path(destinazione),
            on_bytes=conta,
            cancel=annulla,
            chunk_size=self.chunk_size,
        )
        yield 0.0
        return scritti

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        """Cancella un file dal telefono (usato solo dopo una copia verificata)."""
        self.backend.delete_file(serial, remoto)
        yield 0.0
        return None


def transfer_steps(
    plan: TransferPlan,
    options: TransferOptions,
    copiatore,
    serial: str,
    history: History | None = None,
    on_progress: Callable[[Progress], None] | None = None,
    annulla=None,
    retries: int = 2,
    orologio: Callable[[], float] = time.monotonic,
) -> Generator[float, None, TransferResults]:
    """Copia il piano sul disco a piccoli passi, verificando ogni file.

    ``copiatore`` deve esporre ``copia(serial, remoto, destinazione, on_scritti, annulla)``
    come generatore (lo fanno sia :class:`CopiatoreInterno` sia ``AdbAPassi``).
    """
    esiti = TransferResults(skipped=plan.skipped_duplicates + plan.skipped_existing)
    avanzamento = Progress(total_files=plan.file_count, bytes_total=plan.total_bytes)
    inizio = orologio()
    ultimo = _pubblica(on_progress, avanzamento, orologio, 0.0, forza=True)

    for pianificato in plan.files:
        if annulla is not None and annulla.is_set():
            esiti.cancelled = True
            break
        avanzamento.current_name = pianificato.media.name
        avanzamento.file_bytes_total = pianificato.media.size
        avanzamento.file_bytes_done = 0
        bytes_prima = avanzamento.bytes_done
        ultimo = _pubblica(on_progress, avanzamento, orologio, ultimo, forza=True)

        def conta(byte_totali: int) -> None:
            nonlocal ultimo
            avanzamento.bytes_done = bytes_prima + byte_totali
            avanzamento.file_bytes_done = byte_totali
            trascorso = max(orologio() - inizio, 0.001)
            avanzamento.speed_bps = avanzamento.bytes_done / trascorso
            restanti = max(avanzamento.bytes_total - avanzamento.bytes_done, 0)
            avanzamento.eta_seconds = (
                restanti / avanzamento.speed_bps if avanzamento.speed_bps > 0 else None
            )
            ultimo = _pubblica(on_progress, avanzamento, orologio, ultimo)

        riuscito = False
        messaggio = ""
        for _tentativo in range(retries + 1):
            try:
                scritti = yield from copiatore.copia(
                    serial,
                    pianificato.media.remote_path,
                    pianificato.dest_path,
                    on_scritti=conta,
                    annulla=annulla,
                    # La dimensione serve solo a controllare lo spazio libero: chiedere
                    # 16 MB per una foto da 200 KB non avrebbe senso.
                    remoto_dimensione=pianificato.media.size,
                )
            except Annullato:
                avanzamento.bytes_done = bytes_prima
                avanzamento.file_bytes_done = 0
                esiti.cancelled = True
                break
            except FotoFacileError as errore:
                avanzamento.bytes_done = bytes_prima
                avanzamento.file_bytes_done = 0
                messaggio = errore.message
                if not errore.ritentabile:
                    break  # inutile ritentare: il motivo non è temporaneo
                continue
            if pianificato.media.size and scritti != pianificato.media.size:
                _rimuovi(pianificato.dest_path)
                avanzamento.bytes_done = bytes_prima
                avanzamento.file_bytes_done = 0
                messaggio = (
                    f"La copia di {pianificato.media.name} è incompleta "
                    f"(attesi {pianificato.media.size} byte, ricevuti {scritti})."
                )
                break
            riuscito = True
            break

        if esiti.cancelled:
            break
        avanzamento.done_files += 1
        avanzamento.file_bytes_done = avanzamento.file_bytes_total
        if not riuscito:
            esiti.failed.append((pianificato.media, messaggio))
            continue

        esiti.copied.append(pianificato.dest_path)
        if history is not None:
            history.record(
                serial,
                pianificato.rel_path,
                pianificato.media.size,
                pianificato.media.mtime,
                str(pianificato.dest_path),
            )
        if options.delete_after:
            try:
                yield from copiatore.cancella(serial, pianificato.media.remote_path)
                esiti.deleted_from_phone += 1
            except FotoFacileError:
                pass

    esiti.bytes_copied = avanzamento.bytes_done
    esiti.elapsed = max(orologio() - inizio, 0.0)
    _pubblica(on_progress, avanzamento, orologio, ultimo, forza=True)
    if history is not None:
        try:
            history.save()
        except OSError:
            # Le foto sono già al sicuro: non riuscire a ricordare cosa è stato copiato
            # non deve rovinare il risultato (al massimo la prossima volta si ricontrolla).
            esiti.warnings.append(
                "Non sono riuscito a salvare l'elenco dei file copiati: "
                "alla prossima copia il programma ricontrollerà tutto."
            )
    return esiti


def transfer(
    adb: AdbBackend,
    serial: str,
    plan: TransferPlan,
    options: TransferOptions,
    history: History | None = None,
    on_progress: Callable[[Progress], None] | None = None,
    cancel=None,
    chunk_size: int = CHUNK_SIZE,
    retries: int = 2,
    clock: Callable[[], float] = time.monotonic,
) -> TransferResults:
    """Copia il piano e restituisce il resoconto (modo diretto, senza passi)."""
    copiatore = CopiatoreInterno(adb, chunk_size=chunk_size)
    generatore = transfer_steps(
        plan,
        options,
        copiatore,
        serial,
        history=history,
        on_progress=on_progress,
        annulla=cancel,
        retries=retries,
        orologio=clock,
    )
    return esegui_fino_alla_fine(generatore)


def _pubblica(
    callback: Callable[[Progress], None] | None,
    avanzamento: Progress,
    clock: Callable[[], float],
    ultimo: float,
    forza: bool = False,
) -> float:
    """Chiama la funzione di avanzamento, ma non più di 12 volte al secondo."""
    if callback is None:
        return ultimo
    adesso = clock()
    if forza or (adesso - ultimo) >= INTERVALLO_AGGIORNAMENTO:
        callback(avanzamento)
        return adesso
    return ultimo

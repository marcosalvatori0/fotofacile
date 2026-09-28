"""Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.

Regole di sicurezza dei dati:
- si scrive sempre su un file temporaneo ``.part`` e si rinomina solo a copia verificata;
- se la copia viene annullata o fallisce, il temporaneo viene rimosso (mai file troncati);
- la dimensione finale viene confrontata con quella dichiarata dal telefono;
- la cancellazione dal telefono avviene solo per i file copiati e verificati.
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .adb import AdbBackend
from .errors import FotoFacileError
from .history import History
from .planner import TransferOptions, TransferPlan
from .scanner import MediaFile

CHUNK_SIZE = 64 * 1024
INTERVALLO_AGGIORNAMENTO = 0.08


class _Annullato(Exception):
    """Segnale interno: l'utente ha interrotto la copia."""


@dataclass
class Progress:
    total_files: int = 0
    done_files: int = 0
    current_name: str = ""
    bytes_done: int = 0
    bytes_total: int = 0
    speed_bps: float = 0.0
    eta_seconds: float | None = None


@dataclass
class TransferResults:
    copied: list[Path] = field(default_factory=list)
    skipped: int = 0
    failed: list[tuple[MediaFile, str]] = field(default_factory=list)
    bytes_copied: int = 0
    elapsed: float = 0.0
    cancelled: bool = False
    deleted_from_phone: int = 0


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


def _trasforma(errore: Exception, destinazione: Path) -> FotoFacileError:
    """Traduce un errore di sistema in una frase comprensibile per l'utente."""
    testo = str(errore).lower()
    if "no space" in testo or "disk full" in testo or getattr(errore, "errno", None) == 28:
        return FotoFacileError(
            f"Non c'è più spazio sul disco mentre copiavo {destinazione.name}.",
            hint="Libera spazio e riprova: le foto già copiate sono al sicuro.",
        )
    if "permission" in testo or getattr(errore, "errno", None) == 13:
        return FotoFacileError(
            f"Non ho il permesso di scrivere {destinazione.name} nella cartella scelta.",
            hint="Scegli un'altra cartella (per esempio Immagini) e riprova.",
        )
    return FotoFacileError(
        f"Non sono riuscito a copiare {destinazione.name}.",
        hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
    )


def download_file_stream(
    adb: AdbBackend,
    serial: str,
    remote_path: str,
    dest_path: Path,
    on_bytes: Callable[[int, bytes], None] | None = None,
    cancel: threading.Event | None = None,
    chunk_size: int = CHUNK_SIZE,
) -> int:
    """Scrive un file dal telefono su disco passando da un temporaneo ``.part``."""
    destinazione = Path(dest_path)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".part")
    flusso = adb.stream_file(serial, remote_path, chunk_size=chunk_size)
    scritti = 0
    try:
        with open(temporaneo, "wb") as uscita:
            for blocco in flusso:
                if cancel is not None and cancel.is_set():
                    raise _Annullato()
                uscita.write(blocco)
                scritti += len(blocco)
                if on_bytes is not None:
                    on_bytes(len(blocco), blocco)
            uscita.flush()
            os.fsync(uscita.fileno())
        os.replace(temporaneo, destinazione)
    except _Annullato:
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


def transfer(
    adb: AdbBackend,
    serial: str,
    plan: TransferPlan,
    options: TransferOptions,
    history: History | None = None,
    on_progress: Callable[[Progress], None] | None = None,
    cancel: threading.Event | None = None,
    chunk_size: int = CHUNK_SIZE,
    retries: int = 2,
    clock: Callable[[], float] = time.monotonic,
) -> TransferResults:
    """Copia il piano sul disco, verificando ogni file e riportando ogni esito."""
    esiti = TransferResults(skipped=plan.skipped_duplicates + plan.skipped_existing)
    avanzamento = Progress(total_files=plan.file_count, bytes_total=plan.total_bytes)
    inizio = clock()
    ultimo = _pubblica(on_progress, avanzamento, clock, 0.0, forza=True)

    for pianificato in plan.files:
        if cancel is not None and cancel.is_set():
            esiti.cancelled = True
            break
        avanzamento.current_name = pianificato.media.name
        bytes_prima = avanzamento.bytes_done
        ultimo = _pubblica(on_progress, avanzamento, clock, ultimo, forza=True)

        def conta(byte: int, _blocco: bytes) -> None:
            nonlocal ultimo
            avanzamento.bytes_done += byte
            trascorso = max(clock() - inizio, 0.001)
            avanzamento.speed_bps = avanzamento.bytes_done / trascorso
            restanti = max(avanzamento.bytes_total - avanzamento.bytes_done, 0)
            avanzamento.eta_seconds = (
                restanti / avanzamento.speed_bps if avanzamento.speed_bps > 0 else None
            )
            ultimo = _pubblica(on_progress, avanzamento, clock, ultimo)

        riuscito = False
        messaggio = ""
        for _tentativo in range(retries + 1):
            try:
                scritti = download_file_stream(
                    adb,
                    serial,
                    pianificato.media.remote_path,
                    pianificato.dest_path,
                    on_bytes=conta,
                    cancel=cancel,
                    chunk_size=chunk_size,
                )
            except _Annullato:
                avanzamento.bytes_done = bytes_prima
                esiti.cancelled = True
                break
            except FotoFacileError as errore:
                avanzamento.bytes_done = bytes_prima
                messaggio = errore.message
                continue
            if pianificato.media.size and scritti != pianificato.media.size:
                _rimuovi(pianificato.dest_path)
                avanzamento.bytes_done = bytes_prima
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
                adb.delete_file(serial, pianificato.media.remote_path)
                esiti.deleted_from_phone += 1
            except FotoFacileError:
                pass

    esiti.bytes_copied = avanzamento.bytes_done
    esiti.elapsed = max(clock() - inizio, 0.0)
    _pubblica(on_progress, avanzamento, clock, ultimo, forza=True)
    if history is not None:
        history.save()
    return esiti


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

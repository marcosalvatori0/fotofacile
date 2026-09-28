"""Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from .devices import DeviceInfo
from .errors import FotoFacileError
from .format import format_duration, format_size
from .planner import TransferPlan
from .transfer import TransferResults

RIGA = "─" * 46


def build_report(
    results: TransferResults,
    plan: TransferPlan,
    device: DeviceInfo,
    started_at: float,
    destination: Path,
) -> str:
    """Testo del resoconto, leggibile da chiunque."""
    righe = [
        "FotoFacile — resoconto del trasferimento",
        RIGA,
        f"Data: {datetime.fromtimestamp(started_at).strftime('%d/%m/%Y alle %H:%M')}",
        f"Telefono: {device.display_name}",
        f"Cartella: {destination}",
        "",
        f"Copiate: {len(results.copied)} file ({format_size(results.bytes_copied)})",
        f"Saltate (già presenti o già copiate): {results.skipped}",
        f"Errori: {len(results.failed)}",
        f"Durata: {format_duration(results.elapsed)}",
    ]
    if results.deleted_from_phone:
        righe.append(f"Cancellate dal telefono: {results.deleted_from_phone}")
    if results.cancelled:
        righe.extend(
            [
                "",
                "Trasferimento interrotto da te: le foto già copiate sono al sicuro.",
            ]
        )
    elif not results.copied and not results.failed:
        righe.extend(["", "Nota: non c'era nulla di nuovo da copiare."])
    if results.failed:
        righe.extend(["", "File non copiati:"])
        for media, motivo in results.failed:
            righe.append(f"  • {media.name} — {motivo}")
    return "\n".join(righe) + "\n"


def _cartelle_di_riserva() -> list[Path]:
    """Dove salvare il resoconto se la cartella delle foto non è scrivibile."""
    base = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or str(Path.home()))
    return [base / "Desktop", base / ".fotofacile"]


def save_report(text: str, destination: Path) -> Path:
    """Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop, altrimenti nella cartella dati."""
    nome = f"resoconto-fotofacile-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    errori: list[OSError] = []
    for cartella in [Path(destination), *_cartelle_di_riserva()]:
        try:
            cartella.mkdir(parents=True, exist_ok=True)
            percorso = cartella / nome
            percorso.write_text(text, encoding="utf-8")
            return percorso
        except OSError as errore:
            errori.append(errore)
    raise FotoFacileError(
        "Non sono riuscito a salvare il resoconto.",
        hint="Copia il testo dall'area «Dettagli» e incollalo in un documento.",
    ) from errori[-1]

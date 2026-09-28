"""Formattazione in italiano di dimensioni, velocità, tempi e date."""

from __future__ import annotations

from datetime import datetime

UNITA = ("B", "KB", "MB", "GB", "TB")


def format_size(num_bytes: int) -> str:
    """Dimensione leggibile all'italiana: «3,4 GB»."""
    valore = float(max(num_bytes, 0))
    for unita in UNITA:
        if valore < 1024 or unita == UNITA[-1]:
            if unita == "B":
                return f"{int(valore)} B"
            return f"{valore:.1f}".replace(".", ",") + f" {unita}"
        valore /= 1024
    return f"{valore:.1f} {UNITA[-1]}"  # pragma: no cover - irraggiungibile


def format_speed(bytes_per_second: float) -> str:
    if bytes_per_second <= 0:
        return "—"
    return f"{format_size(int(bytes_per_second))}/s"


def format_duration(seconds: float) -> str:
    secondi = int(round(max(seconds, 0)))
    if secondi < 60:
        return f"{secondi} secondi" if secondi != 1 else "1 secondo"
    minuti, sec = divmod(secondi, 60)
    if minuti < 60:
        testo = f"{minuti} minuti" if minuti != 1 else "1 minuto"
        return f"{testo} e {sec} secondi" if sec else testo
    ore, minuti = divmod(minuti, 60)
    testo = f"{ore} ore" if ore != 1 else "1 ora"
    return f"{testo} e {minuti} minuti" if minuti else testo


def format_eta(seconds: float | None) -> str:
    if seconds is None:
        return "calcolo in corso…"
    if seconds < 1:
        return "meno di un secondo"
    return f"circa {format_duration(seconds)}"


def format_date(epoch: int) -> str:
    return datetime.fromtimestamp(epoch).strftime("%d/%m/%Y")


def parse_date(text: str) -> int | None:
    """Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile."""
    testo = (text or "").strip()
    if not testo:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return int(datetime.strptime(testo, formato).timestamp())
        except ValueError:
            continue
    return None

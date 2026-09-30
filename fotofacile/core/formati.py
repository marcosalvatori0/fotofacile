"""Formato **vero** di un file immagine o video, riconosciuto dai primi byte.

L'estensione si può sbagliare o essere cambiata; i primi byte no. Serve a due cose:
capire perché una cartella piena di foto contiene file WebP e decidere se convertirli.
"""

from __future__ import annotations

from pathlib import Path

_MARCHI_HEIF = {b"heic": "heic", b"heix": "heic", b"mif1": "heic", b"msf1": "heic", b"heim": "heic",
                b"heis": "heic", b"hevc": "heic", b"avif": "avif", b"avis": "avif"}


def formato_reale(inizio: bytes) -> str:
    """Riconosce il formato dai primi 12 byte (bastano per tutti quelli elencati)."""
    if inizio[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if inizio[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if inizio[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if inizio[:4] == b"RIFF" and inizio[8:12] == b"WEBP":
        return "webp"
    if inizio[:2] == b"BM":
        return "bmp"
    if inizio[:4] in (b"II*\0", b"MM\0*"):
        return "tiff"
    if inizio[4:8] == b"ftyp":
        return _MARCHI_HEIF.get(inizio[8:12], "mp4")
    return "sconosciuto"


def formato_del_file(percorso: Path) -> str:
    """Formato vero di un file; ``"sconosciuto"`` se non si può leggere."""
    try:
        with open(percorso, "rb") as file:
            return formato_reale(file.read(12))
    except OSError:
        return "sconosciuto"


def analizza_cartella(cartella: Path) -> dict[str, dict[str, int]]:
    """Conta i file per estensione e per formato vero: ``{"jpg": {"webp": 1, "jpeg": 2}}``."""
    conteggi: dict[str, dict[str, int]] = {}
    for percorso in Path(cartella).rglob("*"):
        if not percorso.is_file():
            continue
        estensione = percorso.suffix.lstrip(".").lower() or "(nessuna)"
        formato = formato_del_file(percorso)
        per_estensione = conteggi.setdefault(estensione, {})
        per_estensione[formato] = per_estensione.get(formato, 0) + 1
    return conteggi

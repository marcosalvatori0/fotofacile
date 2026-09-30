"""Conversione delle immagini WebP in JPG (o PNG se hanno trasparenza).

Il WebP non si apre con molti programmi (Foto di Windows 10 senza estensione, vecchi
visualizzatori, stampanti, siti). JPG e PNG sì. Pillow è **opzionale**: senza, il programma
copia i WebP così come sono.
"""

from __future__ import annotations

import os
from pathlib import Path

from .formati import formato_del_file


def pillow_disponibile() -> bool:
    """True se Pillow c'è e sa leggere il WebP."""
    try:
        from PIL import features
    except ImportError:
        return False
    return bool(features.check("webp"))


def e_webp(percorso: Path) -> bool:
    """True se il **contenuto** del file è WebP, qualunque sia il nome."""
    return formato_del_file(Path(percorso)) == "webp"


def _libero(percorso: Path, occupato_da: Path | None) -> Path:
    """Un nome non ancora usato (aggiunge « (1)», « (2)»…); ``occupato_da`` è il file stesso."""
    if not percorso.exists() or (occupato_da is not None and percorso == occupato_da):
        return percorso
    for contatore in range(1, 1000):
        candidato = percorso.with_name(f"{percorso.stem} ({contatore}){percorso.suffix}")
        if not candidato.exists():
            return candidato
    return percorso


def converti_webp(percorso: Path, qualita: int = 95) -> Path:
    """Converte **sul posto** un file WebP e restituisce il percorso finale.

    - opaco → ``.jpg`` (qualità alta, EXIF e profilo colore conservati);
    - con trasparenza → ``.png``;
    - animato → resta WebP, ma con l'estensione giusta.

    Si scrive su un file temporaneo e lo si rimpiazza solo a lavoro finito: se qualcosa va
    storto l'originale è intatto. La data del file viene conservata.
    """
    from PIL import Image

    sorgente = Path(percorso)
    stato = sorgente.stat()
    temporaneo = sorgente.with_name(sorgente.name + ".conv")
    try:
        with Image.open(sorgente) as immagine:
            if getattr(immagine, "is_animated", False):
                finale = _libero(sorgente.with_suffix(".webp"), sorgente)
                temporaneo = None  # niente da scrivere: basta rinominare
            else:
                trasparente = immagine.mode in ("RGBA", "LA", "PA") or "transparency" in immagine.info
                opzioni: dict = {}
                if immagine.info.get("exif"):
                    opzioni["exif"] = immagine.info["exif"]
                if immagine.info.get("icc_profile"):
                    opzioni["icc_profile"] = immagine.info["icc_profile"]
                if trasparente:
                    formato, estensione, pronta = "PNG", ".png", immagine.convert("RGBA")
                else:
                    formato, estensione, pronta = "JPEG", ".jpg", immagine.convert("RGB")
                    opzioni.update(quality=qualita, subsampling=0)
                finale = _libero(sorgente.with_suffix(estensione), sorgente)
                with open(temporaneo, "wb") as uscita:
                    pronta.save(uscita, formato, **opzioni)
                    uscita.flush()
                    os.fsync(uscita.fileno())
        # l'immagine è chiusa: ora si può rimpiazzare anche su Windows
        if temporaneo is not None:
            os.replace(temporaneo, finale)
            if finale != sorgente:
                sorgente.unlink()
        elif finale != sorgente:
            os.replace(sorgente, finale)
        os.utime(finale, (stato.st_atime, stato.st_mtime))
        return finale
    except BaseException:
        if temporaneo is not None:
            temporaneo.unlink(missing_ok=True)
        raise

"""Nomi comprensibili per le cartelle del telefono e riconoscimento di sticker e miniature."""

from __future__ import annotations

# (frammento del percorso in minuscolo, nome da mostrare): vince il **primo** che combacia.
_NOMI = (
    ("whatsapp stickers", "Sticker di WhatsApp"),
    ("whatsapp images", "Foto ricevute su WhatsApp"),
    ("whatsapp video", "Video ricevuti su WhatsApp"),
    ("whatsapp animated gifs", "Animazioni ricevute su WhatsApp"),
    ("dcim/camera", "Foto e video scattati con il telefono"),
    ("screenshots", "Schermate salvate"),
    ("/download", "Scaricati da internet"),
    ("/movies", "Video"),
)

_SEGMENTI_RUMORE = frozenset(
    {".thumbnails", "thumbnails", ".cache", "cache", "whatsapp stickers", "telegram stickers", "stickers"}
)

_PREFISSI = ("/storage/emulated/0/", "/storage/self/primary/", "/sdcard/")


def _minuscolo(percorso: str) -> str:
    return percorso.lower().rstrip("/")


def nome_amichevole(percorso_remoto: str) -> str:
    """Il nome da mostrare a una persona: «Foto ricevute su WhatsApp», non un percorso."""
    minuscolo = _minuscolo(percorso_remoto)
    for frammento, nome in _NOMI:
        if minuscolo.endswith(frammento) or (frammento + "/") in (minuscolo + "/"):
            if frammento.startswith("/") and not minuscolo.endswith(frammento):
                continue
            return nome
    pulito = percorso_remoto.rstrip("/")
    for prefisso in _PREFISSI:
        if pulito.startswith(prefisso):
            pulito = pulito[len(prefisso):]
            break
    return pulito.rsplit("/", 1)[-1] or "Memoria del telefono"


def e_rumore(percorso_remoto: str) -> bool:
    """True per cartelle che quasi nessuno vuole: miniature, cache, sticker."""
    return any(parte in _SEGMENTI_RUMORE for parte in _minuscolo(percorso_remoto).split("/"))

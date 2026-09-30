"""Nomi comprensibili per le cartelle del telefono e riconoscimento di sticker e miniature."""

from __future__ import annotations

# Nome dell'**ultima** cartella (in minuscolo) -> nome da mostrare. Le sotto-cartelle non ereditano
# il nome della cartella madre: «Camera/2024» si chiama «2024», non come «Camera».
_NOMI = {
    "whatsapp stickers": "Sticker di WhatsApp",
    "whatsapp images": "Foto ricevute su WhatsApp",
    "whatsapp video": "Video ricevuti su WhatsApp",
    "whatsapp animated gifs": "Animazioni ricevute su WhatsApp",
    "screenshots": "Schermate salvate",
    "download": "Scaricati da internet",
    "movies": "Video",
}

# (penultima cartella, ultima cartella) -> nome da mostrare.
_NOMI_DUE_LIVELLI = {
    ("dcim", "camera"): "Foto e video scattati con il telefono",
    ("whatsapp images", "sent"): "Foto inviate su WhatsApp",
    ("whatsapp video", "sent"): "Video inviati su WhatsApp",
}

_SEGMENTI_RUMORE = frozenset(
    {".thumbnails", "thumbnails", ".cache", "cache", "whatsapp stickers", "telegram stickers", "stickers"}
)

_BASI = ("/storage/emulated/0", "/storage/self/primary", "/sdcard")
_MEMORIA = "Memoria del telefono"


def _minuscolo(percorso: str) -> str:
    return percorso.lower().rstrip("/")


def _segmenti_dopo_la_memoria(percorso: str) -> list[str]:
    """I segmenti del percorso senza la radice della memoria (``/sdcard``, ``/storage/emulated/0``)."""
    pulito = percorso.rstrip("/")
    for base in _BASI:
        if pulito == base:
            return []
        if pulito.startswith(base + "/"):
            pulito = pulito[len(base):]
            break
    return [parte for parte in pulito.split("/") if parte]


def nome_amichevole(percorso_remoto: str) -> str:
    """Il nome da mostrare a una persona: «Foto ricevute su WhatsApp», non un percorso."""
    segmenti = _segmenti_dopo_la_memoria(percorso_remoto)
    if not segmenti:
        return _MEMORIA
    ultimo = segmenti[-1].lower()
    if len(segmenti) >= 2:
        nome = _NOMI_DUE_LIVELLI.get((segmenti[-2].lower(), ultimo))
        if nome:
            return nome
    return _NOMI.get(ultimo, segmenti[-1])


def nomi_distinti(percorsi: list[str]) -> dict[str, str]:
    """Nome da mostrare per ogni percorso; se due cartelle avrebbero lo stesso nome, si aggiunge la madre."""
    nomi = {percorso: nome_amichevole(percorso) for percorso in percorsi}
    conteggio: dict[str, int] = {}
    for nome in nomi.values():
        conteggio[nome] = conteggio.get(nome, 0) + 1
    for percorso, nome in list(nomi.items()):
        if conteggio[nome] > 1:
            segmenti = _segmenti_dopo_la_memoria(percorso)
            if len(segmenti) >= 2:
                nomi[percorso] = f"{nome} (in {segmenti[-2]})"
    return nomi


def e_rumore(percorso_remoto: str) -> bool:
    """True per cartelle che quasi nessuno vuole: miniature, cache, sticker."""
    return any(parte in _SEGMENTI_RUMORE for parte in _minuscolo(percorso_remoto).split("/"))

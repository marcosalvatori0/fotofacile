"""Telefono finto: serve per i test automatici e per la modalità demo senza dispositivo.

Il contenuto dei file è generato in modo deterministico dal nome, così i test sono
ripetibili, e i nomi includono di proposito accenti, emoji, apostrofi e caratteri strani.
"""

from __future__ import annotations

import hashlib
import time
from typing import Iterator

from .errors import AdbError

SERIALE_DEMO = "DEMO12345"
MODELLO_DEMO = "Pixel_7_demo"

CARTELLE_DEMO = (
    ("/sdcard/DCIM/Camera", "IMG_%04d.jpg", "photo"),
    ("/sdcard/DCIM/Screenshots", "Screenshot_%04d.png", "photo"),
    ("/sdcard/Pictures/WhatsApp Images", "IMG-WhatsApp-%04d.jpg", "photo"),
    ("/sdcard/Movies", "VID_%04d.mp4", "video"),
)
NOMI_DIFFICILI = (
    "Foto è così 😀.jpg",
    "Vacanze d'estate (1).jpg",
    "IMG con # e & strani.jpg",
)
DIMENSIONE_MINIMA = 200_000
DIMENSIONE_MASSIMA = 2_000_000


def demo_files(file_count: int = 54) -> list[dict]:
    """Albero di esempio deterministico con foto e video realistici."""
    file: list[dict] = []
    for indice in range(max(file_count, 0)):
        cartella, schema, genere = CARTELLE_DEMO[indice % len(CARTELLE_DEMO)]
        if indice < len(NOMI_DIFFICILI):
            nome = NOMI_DIFFICILI[indice]
            cartella, genere = CARTELLE_DEMO[0][0], "photo"
        else:
            nome = schema % indice
        if indice >= len(CARTELLE_DEMO) and indice < len(CARTELLE_DEMO) + 3:
            genere, schema = "video", "VID_%04d.mp4"
            nome = schema % indice
            cartella = CARTELLE_DEMO[-1][0]
        dimensione = DIMENSIONE_MINIMA + (indice * 37_111) % DIMENSIONE_MASSIMA
        file.append(
            {
                "path": f"{cartella}/{nome}",
                "size": dimensione,
                "mtime": int(time.time()) - indice * 3600,
                "kind": genere,
            }
        )
    return file


class DemoAdbBackend:
    """Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno."""

    def __init__(self, state: str = "device", file_count: int = 54, delay: float = 0.005) -> None:
        self.state = state
        self.delay = delay
        self._files = {voce["path"]: voce for voce in demo_files(file_count)}

    def check(self) -> str:
        return "FotoFacile — componente demo"

    def devices_raw(self) -> str:
        if self.state == "nessuno":
            return "List of devices attached\n\n"
        return (
            "List of devices attached\n"
            f"{SERIALE_DEMO}          {self.state} product:demo model:{MODELLO_DEMO} "
            "device:demo transport_id:1\n"
        )

    def list_media_raw(self, serial: str, command: str) -> str:
        righe = [f"{voce['size']}|{voce['mtime']}|{voce['path']}" for voce in self._files.values()]
        return "\n".join(righe) + ("\n" if righe else "")

    def stream_file(self, serial: str, remote_path: str, chunk_size: int = 65536) -> Iterator[bytes]:
        voce = self._files.get(remote_path)
        if voce is None:
            raise AdbError(
                "File non trovato sul telefono (demo).",
                hint="Riprova la ricerca delle foto.",
            )
        seme = hashlib.sha256(remote_path.encode("utf-8")).digest()
        generati = 0
        while generati < voce["size"]:
            lunghezza = min(chunk_size, voce["size"] - generati)
            blocco = (seme * ((lunghezza // len(seme)) + 1))[:lunghezza]
            generati += lunghezza
            if self.delay:
                time.sleep(min(self.delay, 0.02))
            yield blocco

    def delete_file(self, serial: str, remote_path: str) -> None:
        if remote_path not in self._files:
            raise AdbError(
                "File non trovato sul telefono (demo).",
                hint="Riprova la ricerca delle foto.",
            )
        del self._files[remote_path]

    def start_server(self) -> None:
        return None

    def restart_server(self) -> None:
        return None


DemoBackend = DemoAdbBackend

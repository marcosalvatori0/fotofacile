#!/usr/bin/env python3
"""Genera l'icona di FotoFacile senza dipendenze esterne (PNG, .ico, .icns).

Disegna una tessera blu con il simbolo di una foto: serve a far riconoscere il programma
a colpo d'occhio. Sul Mac produce anche il file .icns usato dal pacchetto .app.

    python3 scripts/make_icon.py [cartella_destinazione]
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

SFONDO_ALTO = (21, 101, 192)
SFONDO_BASSO = (13, 71, 161)
SUPER_CAMPIONAMENTO = 2
LATO = 1024


def _arrotondato(x: float, y: float, x0: float, y0: float, x1: float, y1: float, raggio: float) -> bool:
    """True se il punto sta dentro un rettangolo con gli angoli arrotondati."""
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    for cx in (x0 + raggio, x1 - raggio):
        for cy in (y0 + raggio, y1 - raggio):
            dentro_x = (x < x0 + raggio) if cx == x0 + raggio else (x > x1 - raggio)
            dentro_y = (y < y0 + raggio) if cy == y0 + raggio else (y > y1 - raggio)
            if dentro_x and dentro_y:
                return (x - cx) ** 2 + (y - cy) ** 2 <= raggio**2
    return True


def _cerchio(x: float, y: float, cx: float, cy: float, raggio: float) -> bool:
    return (x - cx) ** 2 + (y - cy) ** 2 <= raggio**2


def _colore_pixel(x: float, y: float) -> tuple[int, int, int, int]:
    """Colore del pixel alle coordinate indicate (lato 1024, già campionato)."""
    if not _arrotondato(x, y, 0, 0, LATO, LATO, 200):
        return (0, 0, 0, 0)

    # sfumatura verticale dello sfondo
    quanto = y / LATO
    r = round(SFONDO_ALTO[0] + (SFONDO_BASSO[0] - SFONDO_ALTO[0]) * quanto)
    g = round(SFONDO_ALTO[1] + (SFONDO_BASSO[1] - SFONDO_ALTO[1]) * quanto)
    b = round(SFONDO_ALTO[2] + (SFONDO_BASSO[2] - SFONDO_ALTO[2]) * quanto)

    # corpo della "foto": rettangolo bianco arrotondato
    if _arrotondato(x, y, 232, 296, 792, 752, 56):
        bianco = (255, 255, 255, 255)
        # mirino della macchina fotografica (rilievo sopra il corpo)
        if _arrotondato(x, y, 424, 232, 600, 320, 28):
            return bianco
        # obiettivo: cerchio azzurro con anello chiaro
        if _cerchio(x, y, 512, 540, 132):
            if _cerchio(x, y, 512, 540, 96):
                return (21, 101, 192, 255)
            return bianco
        # "montagne" in basso a destra
        if y > 560 and 300 < x < 760:
            cima = 560 + abs(x - 560) * 0.42
            if y > cima:
                return (222, 235, 250, 255)
        return bianco
    return (r, g, b, 255)


def disegna(riduzione: int = SUPER_CAMPIONAMENTO) -> list[list[tuple[int, int, int, int]]]:
    """Costruisce l'immagine riducendo il rumore dei bordi (campionamento multiplo)."""
    lato_finale = LATO // riduzione
    righe: list[list[tuple[int, int, int, int]]] = []
    for riga in range(lato_finale):
        riga_pixel: list[tuple[int, int, int, int]] = []
        for colonna in range(lato_finale):
            somma_r = somma_g = somma_b = somma_a = 0
            for sotto_y in range(riduzione):
                for sotto_x in range(riduzione):
                    x = (colonna + (sotto_x + 0.5) / riduzione) * riduzione
                    y = (riga + (sotto_y + 0.5) / riduzione) * riduzione
                    r, g, b, a = _colore_pixel(x, y)
                    somma_r += r * a
                    somma_g += g * a
                    somma_b += b * a
                    somma_a += a
            if somma_a == 0:
                riga_pixel.append((0, 0, 0, 0))
            else:
                riga_pixel.append(
                    (somma_r // somma_a, somma_g // somma_a, somma_b // somma_a, somma_a // (riduzione**2))
                )
        righe.append(riga_pixel)
    return righe


def scrivi_png(percorso: Path, righe: list[list[tuple[int, int, int, int]]]) -> Path:
    altezza = len(righe)
    larghezza = len(righe[0])
    dati = bytearray()
    for riga in righe:
        dati.append(0)  # nessun filtro
        for r, g, b, a in riga:
            dati.extend((r, g, b, a))

    def blocco(tipo: bytes, contenuto: bytes) -> bytes:
        return (
            struct.pack(">I", len(contenuto))
            + tipo
            + contenuto
            + struct.pack(">I", zlib.crc32(tipo + contenuto) & 0xFFFFFFFF)
        )

    intestazione = struct.pack(">IIBBBBB", larghezza, altezza, 8, 6, 0, 0, 0)
    percorso.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + blocco(b"IHDR", intestazione)
        + blocco(b"IDAT", zlib.compress(bytes(dati), 9))
        + blocco(b"IEND", b"")
    )
    return percorso


def scrivi_ico(percorso: Path, png_256: Path) -> Path:
    """Crea un .ico contenente il PNG 256×256 (formato accettato da Windows)."""
    dati = png_256.read_bytes()
    intestazione = struct.pack("<HHH", 0, 1, 1)
    voce = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(dati), 22)
    percorso.write_bytes(intestazione + voce + dati)
    return percorso


def crea_iconset(cartella: Path, righe: list[list[tuple[int, int, int, int]]]) -> Path:
    """Crea le dimensioni richieste da macOS a partire dall'immagine grande."""
    iconset = cartella / "FotoFacile.iconset"
    iconset.mkdir(parents=True, exist_ok=True)
    for lato in (16, 32, 64, 128, 256, 512):
        base = righe[:: len(righe) // lato]
        ridimensionata = [riga[:: len(riga) // lato] for riga in base][:lato]
        scrivi_png(iconset / f"icon_{lato}x{lato}.png", ridimensionata)
        scrivi_png(iconset / f"icon_{lato}x{lato}@2x.png", ridimensionata)
    return iconset


def main(destinazione: str | None = None) -> int:
    import subprocess

    cartella = Path(destinazione) if destinazione else Path(__file__).resolve().parent.parent / "assets"
    cartella.mkdir(parents=True, exist_ok=True)
    righe = disegna()
    png = scrivi_png(cartella / "fotofacile.png", righe)
    print(f"Icona PNG: {png} ({png.stat().st_size // 1024} KB)")

    piccola = [riga[::4] for riga in righe[::4]]
    ico = scrivi_ico(cartella / "fotofacile.ico", scrivi_png(cartella / "fotofacile-256.png", piccola))
    print(f"Icona ICO: {ico}")

    if sys.platform == "darwin":
        iconset = crea_iconset(cartella, righe)
        try:
            subprocess.run(
                ["iconutil", "-c", "icns", str(iconset), "-o", str(cartella / "fotofacile.icns")],
                check=True,
                capture_output=True,
            )
            print(f"Icona ICNS: {cartella / 'fotofacile.icns'}")
        except (subprocess.CalledProcessError, FileNotFoundError) as errore:  # pragma: no cover
            print(f"Non ho potuto creare il file .icns ({errore}); il pacchetto userà l'icona generica.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))

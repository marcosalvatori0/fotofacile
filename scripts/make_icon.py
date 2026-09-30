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
# Slot dell'iconset macOS: (lato nominale, fattore di scala). 64×64 non è uno slot valido
# e ogni @2x va disegnato alla sua dimensione vera (per esempio 16@2x = 32×32 pixel).
SLOT_ICONSET = ((16, 1), (16, 2), (32, 1), (32, 2), (128, 1), (128, 2), (256, 1), (256, 2), (512, 1), (512, 2))
# Misure incluse nel .ico: Windows sceglie la più adatta da solo.
LATI_ICO = (16, 32, 64, 128, 256)


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


def disegna(lato: int = LATO, campioni: int = SUPER_CAMPIONAMENTO) -> list[list[tuple[int, int, int, int]]]:
    """Costruisce l'immagine alla dimensione richiesta, con più campioni per pixel.

    Il disegno è definito su una griglia di LATO punti: chiedendo un `lato` diverso si
    ottiene la stessa icona alla dimensione vera voluta, non un ingrandimento.
    """
    passo = LATO / lato
    righe: list[list[tuple[int, int, int, int]]] = []
    for riga in range(lato):
        riga_pixel: list[tuple[int, int, int, int]] = []
        for colonna in range(lato):
            somma_r = somma_g = somma_b = somma_a = 0
            for sotto_y in range(campioni):
                for sotto_x in range(campioni):
                    x = (colonna + (sotto_x + 0.5) / campioni) * passo
                    y = (riga + (sotto_y + 0.5) / campioni) * passo
                    r, g, b, a = _colore_pixel(x, y)
                    somma_r += r * a
                    somma_g += g * a
                    somma_b += b * a
                    somma_a += a
            if somma_a == 0:
                riga_pixel.append((0, 0, 0, 0))
            else:
                riga_pixel.append(
                    (somma_r // somma_a, somma_g // somma_a, somma_b // somma_a, somma_a // (campioni**2))
                )
        righe.append(riga_pixel)
    return righe


def ridimensiona(righe: list[list[tuple[int, int, int, int]]], lato: int) -> list[list[tuple[int, int, int, int]]]:
    """Riduce l'immagine con una media a blocchi (i lati richiesti dividono il master).

    La media pesa i colori con l'alfa: senza questo peso i pixel trasparenti dei bordi
    tirerebbero il colore verso il nero e comparirebbe un alone scuro attorno all'icona.
    """
    if len(righe) % lato:
        raise ValueError(f"il lato {lato} non divide l'immagine {len(righe)}")
    fattore = len(righe) // lato
    if fattore <= 1:
        return righe
    quanti = fattore * fattore
    nuove: list[list[tuple[int, int, int, int]]] = []
    for riga in range(lato):
        nuova_riga: list[tuple[int, int, int, int]] = []
        for colonna in range(lato):
            somma_r = somma_g = somma_b = somma_a = 0
            for y in range(riga * fattore, (riga + 1) * fattore):
                for x in range(colonna * fattore, (colonna + 1) * fattore):
                    r, g, b, a = righe[y][x]
                    somma_r += r * a
                    somma_g += g * a
                    somma_b += b * a
                    somma_a += a
            if somma_a == 0:
                nuova_riga.append((0, 0, 0, 0))
            else:
                nuova_riga.append(
                    (somma_r // somma_a, somma_g // somma_a, somma_b // somma_a, somma_a // quanti)
                )
        nuove.append(nuova_riga)
    return nuove


def livelli(master: list[list[tuple[int, int, int, int]]]) -> dict[int, list[list[tuple[int, int, int, int]]]]:
    """Prepara tutte le dimensioni riducendo il master a metà per volta (catena 1024…16)."""
    disponibili = {len(master): master}
    corrente = master
    while len(corrente) > 16:
        corrente = ridimensiona(corrente, len(corrente) // 2)
        disponibili[len(corrente)] = corrente
    return disponibili


def immagine_png(righe: list[list[tuple[int, int, int, int]]]) -> bytes:
    """Serializza l'immagine in un PNG RGBA, senza librerie esterne."""
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
    return (
        b"\x89PNG\r\n\x1a\n"
        + blocco(b"IHDR", intestazione)
        + blocco(b"IDAT", zlib.compress(bytes(dati), 9))
        + blocco(b"IEND", b"")
    )


def scrivi_png(percorso: Path, righe: list[list[tuple[int, int, int, int]]]) -> Path:
    percorso.write_bytes(immagine_png(righe))
    return percorso


def scrivi_ico(percorso: Path, immagini: list[tuple[int, bytes]]) -> Path:
    """Crea il .ico con una voce per dimensione, ognuna dichiarata per la sua misura vera.

    Nel formato ICO il valore 0 in larghezza/altezza significa 256: qui si scrivono le
    dimensioni reali, così Windows non ripiega sull'icona generica.
    """
    intestazione = struct.pack("<HHH", 0, 1, len(immagini))
    voci = []
    dati = b""
    for lato, png in immagini:
        byte_lato = 0 if lato >= 256 else lato
        offset = 6 + 16 * len(immagini) + len(dati)
        voci.append(struct.pack("<BBBBHHII", byte_lato, byte_lato, 0, 0, 1, 32, len(png), offset))
        dati += png
    percorso.write_bytes(intestazione + b"".join(voci) + dati)
    return percorso


def crea_iconset(cartella: Path, livelli_icona: dict[int, list[list[tuple[int, int, int, int]]]]) -> Path:
    """Crea le dimensioni richieste da macOS, ognuna con i pixel della sua misura vera."""
    iconset = cartella / "FotoFacile.iconset"
    iconset.mkdir(parents=True, exist_ok=True)
    for vecchio in iconset.glob("icon_*.png"):
        vecchio.unlink()  # via le misure non più previste (per esempio la 64×64 di prima)
    for lato, scala in SLOT_ICONSET:
        suffisso = "" if scala == 1 else "@2x"
        scrivi_png(iconset / f"icon_{lato}x{lato}{suffisso}.png", livelli_icona[lato * scala])
    return iconset


def main(destinazione: str | None = None) -> int:
    import subprocess

    cartella = Path(destinazione) if destinazione else Path(__file__).resolve().parent.parent / "assets"
    cartella.mkdir(parents=True, exist_ok=True)
    master = disegna()  # 1024×1024 con bordi morbidi: da qui derivano tutte le misure
    livelli_icona = livelli(master)
    png = scrivi_png(cartella / "fotofacile.png", master)
    print(f"Icona PNG: {png} ({png.stat().st_size // 1024} KB)")

    scrivi_png(cartella / "fotofacile-256.png", livelli_icona[256])
    ico = scrivi_ico(
        cartella / "fotofacile.ico",
        [(lato, immagine_png(livelli_icona[lato])) for lato in LATI_ICO],
    )
    print(f"Icona ICO: {ico}")

    if sys.platform == "darwin":
        iconset = crea_iconset(cartella, livelli_icona)
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

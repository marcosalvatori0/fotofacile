"""Verifica che le icone generate abbiano le dimensioni che dichiarano.

Il difetto originale: le copie @2x contenevano gli stessi identici pixel della 1x,
l'iconset includeva una misura 64×64 non prevista da macOS e il .ico dichiarava
256×256 mentre il PNG al suo interno era 128×128. Un'icona così viene scartata da
Windows, che mostra quella generica.

I controlli leggono i byte dei file (blocco IHDR dei PNG, ICONDIR dell'ICO): non
serve nessuna libreria di immagini.
"""

from __future__ import annotations

import struct
from pathlib import Path

ASSET = Path(__file__).resolve().parent.parent / "assets"

# Dimensioni vere attese per ogni slot dell'iconset macOS.
SLOT_ICONSET = {
    "icon_16x16.png": 16,
    "icon_16x16@2x.png": 32,
    "icon_32x32.png": 32,
    "icon_32x32@2x.png": 64,
    "icon_128x128.png": 128,
    "icon_128x128@2x.png": 256,
    "icon_256x256.png": 256,
    "icon_256x256@2x.png": 512,
    "icon_512x512.png": 512,
    "icon_512x512@2x.png": 1024,
}


def _dimensioni_png(percorso: Path) -> tuple[int, int]:
    """Legge larghezza e altezza direttamente dal blocco IHDR del PNG."""
    dati = percorso.read_bytes()
    assert dati[:8] == b"\x89PNG\r\n\x1a\n", f"{percorso.name} non è un PNG"
    return struct.unpack(">II", dati[16:24])


def test_ogni_icona_dell_iconset_ha_la_dimensione_del_suo_nome():
    iconset = ASSET / "FotoFacile.iconset"
    for nome, lato in SLOT_ICONSET.items():
        percorso = iconset / nome
        assert percorso.is_file(), f"manca {nome}"
        assert _dimensioni_png(percorso) == (lato, lato), f"{nome} dovrebbe contenere {lato}×{lato}"


def test_l_iconset_contiene_solo_gli_slot_previsti_da_macos():
    nomi = {percorso.name for percorso in (ASSET / "FotoFacile.iconset").glob("*.png")}
    assert nomi == set(SLOT_ICONSET), "64×64 non è uno slot valido: iconutil potrebbe rifiutare l'iconset"


def test_le_copie_2x_non_ripetono_i_pixel_della_1x():
    iconset = ASSET / "FotoFacile.iconset"
    for nome in SLOT_ICONSET:
        if not nome.endswith("@2x.png"):
            continue
        uno = (iconset / nome.replace("@2x", "")).read_bytes()
        due = (iconset / nome).read_bytes()
        assert uno != due, f"{nome} è identica alla versione 1x: su Retina apparirebbe sfocata"


def test_fotofacile_256_e_davvero_256():
    assert _dimensioni_png(ASSET / "fotofacile-256.png") == (256, 256)


def test_le_voci_del_ico_dichiarano_la_dimensione_del_png_incorporato():
    dati = (ASSET / "fotofacile.ico").read_bytes()
    riservato, tipo, quante = struct.unpack("<HHH", dati[:6])
    assert (riservato, tipo) == (0, 1)
    assert quante >= 1
    dichiarate = []
    for indice in range(quante):
        inizio = 6 + 16 * indice
        larghezza, altezza, _colori, _riservato, _piani, _bit, dimensione, offset = struct.unpack(
            "<BBBBHHII", dati[inizio : inizio + 16]
        )
        dichiarata = (larghezza or 256, altezza or 256)
        assert dati[offset : offset + 8] == b"\x89PNG\r\n\x1a\n", f"voce {indice}: il PNG incorporato non c'è"
        assert offset + dimensione <= len(dati), f"voce {indice}: dimensione fuori dal file"
        reale = struct.unpack(">II", dati[offset + 16 : offset + 24])
        assert dichiarata == reale, f"voce {indice}: dichiara {dichiarata} ma contiene {reale}"
        dichiarate.append(dichiarata[0])
    assert dichiarate == [16, 32, 64, 128, 256], "il .ico deve contenere tutte le misure principali"

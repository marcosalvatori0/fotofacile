import pytest

from fotofacile.core.nomi_cartelle import e_rumore, nome_amichevole


@pytest.mark.parametrize(
    "percorso, atteso",
    [
        ("/sdcard/DCIM/Camera", "Foto e video scattati con il telefono"),
        ("/storage/emulated/0/DCIM/Camera", "Foto e video scattati con il telefono"),
        ("/sdcard/DCIM/Screenshots", "Schermate salvate"),
        ("/sdcard/Pictures/Screenshots", "Schermate salvate"),
        ("/sdcard/Pictures/WhatsApp Images", "Foto ricevute su WhatsApp"),
        ("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images", "Foto ricevute su WhatsApp"),
        ("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video", "Video ricevuti su WhatsApp"),
        ("/sdcard/Download", "Scaricati da internet"),
        ("/sdcard/Movies", "Video"),
        ("/sdcard/Pictures/Vacanze 2024", "Vacanze 2024"),
    ],
)
def test_nomi_amichevoli(percorso, atteso):
    assert nome_amichevole(percorso) == atteso


def test_percorso_sconosciuto_usa_l_ultima_cartella():
    assert nome_amichevole("/sdcard/Boh/Cose Mie") == "Cose Mie"
    assert nome_amichevole("/") == "Memoria del telefono"


@pytest.mark.parametrize(
    "percorso",
    [
        "/sdcard/DCIM/.thumbnails",
        "/sdcard/Pictures/.cache",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Stickers",
        "/sdcard/Telegram/Telegram Stickers",
        "/sdcard/Android/data/com.app/cache/images",
    ],
)
def test_rumore_riconosciuto(percorso):
    assert e_rumore(percorso) is True


@pytest.mark.parametrize(
    "percorso",
    ["/sdcard/DCIM/Camera", "/sdcard/Pictures/WhatsApp Images", "/sdcard/Download", "/sdcard/Pictures/Cache di famiglia"],
)
def test_le_cartelle_normali_non_sono_rumore(percorso):
    assert e_rumore(percorso) is False

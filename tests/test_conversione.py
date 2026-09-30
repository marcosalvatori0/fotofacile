import os
from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image, features  # noqa: E402

from fotofacile.core.conversione import converti_webp, e_webp, pillow_disponibile  # noqa: E402

pytestmark = pytest.mark.skipif(not features.check("webp"), reason="questo Pillow non sa il WebP")


def _webp(percorso: Path, modo="RGB", colore=(200, 20, 20), dimensione=(16, 16)) -> Path:
    Image.new(modo, dimensione, colore).save(percorso, "WEBP")
    return percorso


def test_pillow_e_riconoscimento():
    assert pillow_disponibile() is True


def test_e_webp_guarda_il_contenuto_non_il_nome(tmp_path):
    finto = _webp(tmp_path / "foto.jpg")  # contenuto WebP, nome .jpg
    assert e_webp(finto) is True
    (tmp_path / "vero.jpg").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 16)
    assert e_webp(tmp_path / "vero.jpg") is False
    assert e_webp(tmp_path / "non-esiste.jpg") is False


def test_immagine_opaca_diventa_jpg_e_conserva_la_data(tmp_path):
    sorgente = _webp(tmp_path / "a.webp")
    os.utime(sorgente, (1_500_000_000, 1_500_000_000))
    finale = converti_webp(sorgente)
    assert finale == tmp_path / "a.jpg"
    assert not sorgente.exists()
    assert not list(tmp_path.glob("*.conv"))
    with Image.open(finale) as immagine:
        assert immagine.format == "JPEG"
    assert int(finale.stat().st_mtime) == 1_500_000_000


def test_nome_gia_jpg_viene_rimpiazzato_sul_posto(tmp_path):
    sorgente = _webp(tmp_path / "a.jpg")  # WebP travestito da JPG
    finale = converti_webp(sorgente)
    assert finale == sorgente
    with Image.open(finale) as immagine:
        assert immagine.format == "JPEG"


def test_trasparenza_diventa_png(tmp_path):
    sorgente = _webp(tmp_path / "sticker.webp", modo="RGBA", colore=(10, 200, 10, 90))
    finale = converti_webp(sorgente)
    assert finale.suffix == ".png"
    with Image.open(finale) as immagine:
        assert immagine.format == "PNG"


def test_animazione_resta_webp_con_estensione_giusta(tmp_path):
    fotogrammi = [Image.new("RGB", (8, 8), (i * 40, 0, 0)) for i in range(4)]
    animata = tmp_path / "gif-animata.jpg"
    fotogrammi[0].save(animata, "WEBP", save_all=True, append_images=fotogrammi[1:], duration=80, loop=0)
    finale = converti_webp(animata)
    assert finale == tmp_path / "gif-animata.webp"
    assert finale.exists() and not animata.exists()


def test_file_rovinato_solleva_e_non_tocca_l_originale(tmp_path):
    rotto = tmp_path / "rotto.webp"
    rotto.write_bytes(b"RIFF\x04\0\0\0WEBPzzzz")
    with pytest.raises(Exception):
        converti_webp(rotto)
    assert rotto.exists()
    assert not list(tmp_path.glob("*.conv"))

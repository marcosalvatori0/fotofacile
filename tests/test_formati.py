from pathlib import Path

from fotofacile.core.formati import analizza_cartella, formato_del_file, formato_reale


def test_riconosce_i_formati_dai_primi_byte():
    assert formato_reale(b"\xff\xd8\xff\xe0" + b"\0" * 8) == "jpeg"
    assert formato_reale(b"\x89PNG\r\n\x1a\n" + b"\0" * 4) == "png"
    assert formato_reale(b"RIFF\x10\0\0\0WEBPVP8 ") == "webp"
    assert formato_reale(b"\0\0\0\x18ftypheic" + b"\0" * 4) == "heic"
    assert formato_reale(b"\0\0\0\x1cftypavif" + b"\0" * 4) == "avif"
    assert formato_reale(b"\0\0\0\x18ftypisom" + b"\0" * 4) == "mp4"
    assert formato_reale(b"qualcosa di strano") == "sconosciuto"
    assert formato_reale(b"") == "sconosciuto"


def test_un_wav_non_e_webp():
    # anche i WAV iniziano con «RIFF»: conta la parola «WEBP» in posizione 8
    assert formato_reale(b"RIFF\x10\0\0\0WAVEfmt ") == "sconosciuto"


def test_analizza_cartella_trova_estensioni_bugiarde(tmp_path: Path):
    (tmp_path / "finta.jpg").write_bytes(b"RIFF\x10\0\0\0WEBPVP8 ")
    (tmp_path / "vera.jpg").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 8)
    (tmp_path / "sticker.webp").write_bytes(b"RIFF\x10\0\0\0WEBPVP8 ")
    (tmp_path / "sotto").mkdir()
    (tmp_path / "sotto" / "a.JPG").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 8)
    risultato = analizza_cartella(tmp_path)
    assert risultato["jpg"] == {"webp": 1, "jpeg": 2}
    assert risultato["webp"] == {"webp": 1}
    assert formato_del_file(tmp_path / "vera.jpg") == "jpeg"
    assert formato_del_file(tmp_path / "non-esiste.jpg") == "sconosciuto"

from pathlib import Path

import pytest

from fotofacile.core.errors import TransferError
from fotofacile.core.history import History
from fotofacile.core.planner import (
    MAX_NOME,
    MAX_PERCORSO,
    TransferOptions,
    build_plan,
    destination_for,
    ensure_space,
    relative_path,
    suggested_destination,
)
from fotofacile.core.scanner import MediaFile


def foto(percorso: str, size: int = 100, mtime: int = 1000) -> MediaFile:
    kind = "video" if percorso.lower().endswith(".mp4") else "photo"
    return MediaFile(remote_path=percorso, size=size, mtime=mtime, kind=kind)


def test_relative_path_toglie_la_memoria_del_telefono():
    assert relative_path("/sdcard/DCIM/Camera/a.jpg") == "DCIM/Camera/a.jpg"
    assert relative_path("/storage/emulated/0/DCIM/a.jpg") == "DCIM/a.jpg"
    assert relative_path("/storage/self/primary/DCIM/a.jpg") == "DCIM/a.jpg"
    assert relative_path("/sdcard/a.jpg") == "a.jpg"


def test_destinazione_con_e_senza_struttura(tmp_path):
    assert destination_for("/sdcard/DCIM/Camera/a.jpg", tmp_path, True) == tmp_path / "DCIM/Camera/a.jpg"
    assert destination_for("/sdcard/DCIM/Camera/a.jpg", tmp_path, False) == tmp_path / "a.jpg"


def test_piano_somma_dimensioni_e_filtra_i_video(tmp_path):
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100), foto("/sdcard/DCIM/Camera/b.mp4", 900)]
    opzioni = TransferOptions(destination=tmp_path, include_videos=False)
    piano = build_plan(file, opzioni)
    assert piano.file_count == 1
    assert piano.total_bytes == 100


def test_piano_filtra_per_data(tmp_path):
    file = [
        foto("/sdcard/DCIM/Camera/vecchia.jpg", mtime=1000),
        foto("/sdcard/DCIM/Camera/nuova.jpg", mtime=5000),
    ]
    opzioni = TransferOptions(destination=tmp_path, date_from=2000)
    piano = build_plan(file, opzioni)
    assert [f.media.name for f in piano.files] == ["nuova.jpg"]


def test_piano_salta_i_file_gia_copiati(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("S1", "DCIM/Camera/a.jpg", 100, 1000, str(tmp_path / "a.jpg"))
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100, 1000), foto("/sdcard/DCIM/Camera/b.jpg", 100, 1000)]
    piano = build_plan(
        file, TransferOptions(destination=tmp_path), serial="S1", history=cronologia
    )
    assert [f.media.name for f in piano.files] == ["b.jpg"]
    assert piano.skipped_duplicates == 1


def test_dedup_non_attiva_quando_disattivata(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("S1", "DCIM/Camera/a.jpg", 100, 1000, "x")
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100, 1000)]
    piano = build_plan(
        file,
        TransferOptions(destination=tmp_path, skip_existing=False),
        serial="S1",
        history=cronologia,
    )
    assert piano.file_count == 1
    assert piano.skipped_duplicates == 0


def test_collisione_stessa_dimensione_viene_saltata(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "a.jpg").write_bytes(b"x" * 100)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 100)],
        TransferOptions(destination=tmp_path, preserve_structure=True),
    )
    assert piano.files == []
    assert piano.skipped_existing == 1


def test_collisione_dimensione_diversa_rinomina(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "a.jpg").write_bytes(b"x" * 50)
    (cartella / "a (1).jpg").write_bytes(b"x" * 60)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 100)],
        TransferOptions(destination=tmp_path, preserve_structure=True),
    )
    (previsto,) = piano.files
    assert previsto.dest_path.name == "a (2).jpg"


def test_piano_ignora_i_file_senza_dimensione_nel_totale(tmp_path):
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 0), foto("/sdcard/DCIM/Camera/b.jpg", 200)],
        TransferOptions(destination=tmp_path),
    )
    assert piano.total_bytes == 200


def test_nomi_non_validi_su_windows_vengono_resi_sicuri(tmp_path):
    percorso = destination_for("/sdcard/DCIM/Camera/IMG:01?-sera*.jpg", tmp_path, False)
    assert percorso.name == "IMG_01_-sera_.jpg"


def test_nomi_riservati_vengono_prefissati(tmp_path):
    assert destination_for("/sdcard/DCIM/CON.jpg", tmp_path, False).name == "_CON.jpg"
    assert destination_for("/sdcard/DCIM/Camera/LPT1.png", tmp_path, False).name == "_LPT1.png"
    assert destination_for("/sdcard/DCIM/Camera/nul.jpeg", tmp_path, False).name == "_nul.jpeg"


def test_punti_e_spazi_finali_rimossi(tmp_path):
    assert destination_for("/sdcard/DCIM/Camera/foto.jpg ", tmp_path, False).name == "foto.jpg"
    assert destination_for("/sdcard/DCIM/Camera/foto...", tmp_path, False).name == "foto"


def test_nome_vuoto_o_solo_caratteri_strani(tmp_path):
    assert destination_for("/sdcard/DCIM/Camera/???.jpg", tmp_path, False).name == "___.jpg"


def test_nome_lunghissimo_accorciato_mantenendo_estensione(tmp_path):
    lungo = "A" * 300 + ".jpg"
    percorso = destination_for(f"/sdcard/DCIM/Camera/{lungo}", Path("/tmp/ff"), False)
    assert percorso.suffix == ".jpg"
    assert len(percorso.stem) == MAX_NOME


def test_percorso_profondo_troppo_lungo_accorciato(tmp_path):
    profondo = "/sdcard/DCIM/" + "/".join(f"cartella_lunga_{i:02d}" for i in range(12))
    percorso = destination_for(f"{profondo}/foto.jpg", tmp_path, True)
    assert len(str(percorso)) <= MAX_PERCORSO
    assert percorso.name.endswith(".jpg")


def test_nome_con_maiuscole_diverse_e_un_file_diverso(tmp_path):
    """FOTO.JPG e foto.jpg sono due foto diverse: non vanno confuse, né sovrascritte."""
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "FOTO.JPG").write_bytes(b"x" * 100)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/foto.jpg", 100)],
        TransferOptions(destination=tmp_path, preserve_structure=True),
        case_insensitive=True,
    )
    (previsto,) = piano.files
    assert previsto.dest_path.name == "foto (1).jpg"
    assert (cartella / "FOTO.JPG").read_bytes() == b"x" * 100  # intatto


def test_su_linux_le_maiuscole_contano(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "FOTO.JPG").write_bytes(b"x" * 100)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/foto.jpg", 100)],
        TransferOptions(destination=tmp_path, preserve_structure=True),
        case_insensitive=False,
    )
    assert piano.file_count == 1


def test_rinomina_evita_anche_i_nomi_con_maiuscole_diverse(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "a.jpg").write_bytes(b"x" * 50)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 100)],
        TransferOptions(destination=tmp_path, preserve_structure=True),
        case_insensitive=True,
    )
    (previsto,) = piano.files
    assert previsto.dest_path.name == "a (1).jpg"


def test_ensure_space_avvisa_se_manca_spazio(tmp_path):
    piano = build_plan([foto("/sdcard/DCIM/Camera/a.jpg", 1000)], TransferOptions(destination=tmp_path))
    with pytest.raises(TransferError) as errore:
        ensure_space(piano, tmp_path, free_bytes=500)
    assert "spazio" in errore.value.message.lower()
    assert "1000 B" in errore.value.hint
    ensure_space(piano, tmp_path, free_bytes=1_000_000)


def test_destinazione_suggerita_usa_modello_e_data(tmp_path):
    proposta = suggested_destination("SM A525F", base=tmp_path, today="2026-09-28")
    assert proposta == tmp_path / "SM A525F" / "2026-09-28"
    assert suggested_destination("", base=tmp_path, today="2026-09-28").parent.name == "Telefono"


def test_destinazione_suggerita_ripulisce_il_modello(tmp_path):
    proposta = suggested_destination("Pixel/7:Pro", base=tmp_path, today="2026-09-28")
    assert proposta.parent.name == "Pixel_7_Pro"


def test_piano_non_modifica_i_file_di_input(tmp_path):
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100)]
    copia = list(file)
    build_plan(file, TransferOptions(destination=tmp_path))
    assert file == copia
    assert isinstance(file[0].remote_path, str)
    assert Path(file[0].remote_path).name == "a.jpg"


def test_webp_pianificato_con_estensione_jpg(tmp_path):
    assert destination_for("/sdcard/Pictures/a.webp", tmp_path, False, converti_webp=True) == tmp_path / "a.jpg"
    assert destination_for("/sdcard/Pictures/a.WEBP", tmp_path, False, converti_webp=True) == tmp_path / "a.jpg"
    assert destination_for("/sdcard/Pictures/a.webp", tmp_path, False) == tmp_path / "a.webp"
    assert destination_for("/sdcard/Pictures/a.png", tmp_path, False, converti_webp=True) == tmp_path / "a.png"


def test_webp_convertito_non_si_scambia_per_gia_presente(tmp_path):
    (tmp_path / "a.jpg").write_bytes(b"x" * 100)  # una foto diversa, stesso nome e stessa dimensione
    file = [foto("/sdcard/Pictures/a.webp", size=100)]
    piano = build_plan(file, TransferOptions(destination=tmp_path, converti_webp=True))
    assert [f.dest_path.name for f in piano.files] == ["a (1).jpg"]
    assert piano.skipped_existing == 0


def test_webp_da_convertire_riserva_anche_png_e_webp(tmp_path):
    # Il WebP trasparente può diventare a.png (o restare a.webp se animato): un file
    # successivo con quel nome non deve finirci sopra.
    file = [foto("/sdcard/Pictures/a.webp"), foto("/sdcard/Download/a.png"), foto("/sdcard/Music/a.webp")]
    opzioni = TransferOptions(destination=tmp_path, preserve_structure=False, converti_webp=True)
    piano = build_plan(file, opzioni)
    # Il terzo file salta «a (1).jpg»: «a (1).png» è del PNG e le tre varianti devono restare libere.
    assert [f.dest_path.name for f in piano.files] == ["a.jpg", "a (1).png", "a (2).jpg"]


def test_webp_riserva_png_e_webp_senza_distinzione_di_maiuscole(tmp_path):
    file = [foto("/sdcard/Pictures/a.webp"), foto("/sdcard/Download/A.PNG")]
    opzioni = TransferOptions(destination=tmp_path, preserve_structure=False, converti_webp=True)
    piano = build_plan(file, opzioni, case_insensitive=True)
    assert [f.dest_path.name for f in piano.files] == ["a.jpg", "A (1).PNG"]


def test_senza_conversione_il_piano_dei_webp_non_cambia(tmp_path):
    file = [foto("/sdcard/Pictures/a.webp"), foto("/sdcard/Download/a.png"), foto("/sdcard/Music/a.webp")]
    opzioni = TransferOptions(destination=tmp_path, preserve_structure=False)
    piano = build_plan(file, opzioni)
    assert [f.dest_path.name for f in piano.files] == ["a.webp", "a.png", "a (1).webp"]


def test_webp_da_convertire_ha_le_tre_varianti_libere_e_distinte_dagli_altri(tmp_path):
    # PNG, WebP, PNG: a runtime il WebP può diventare a.jpg, a.png o restare a.webp e il nome
    # lo sceglie il disco, non il piano; per questo le tre varianti sono riservate al WebP.
    file = [foto("/sdcard/Download/a.png"), foto("/sdcard/Pictures/a.webp"), foto("/sdcard/Music/a.png")]
    opzioni = TransferOptions(destination=tmp_path, preserve_structure=False, converti_webp=True)
    piano = build_plan(file, opzioni)
    destinazioni = [f.dest_path for f in piano.files]
    assert len(set(destinazioni)) == 3
    webp = destinazioni[1]
    assert webp.suffix == ".jpg"
    varianti = {webp.with_suffix(e) for e in (".jpg", ".png", ".webp")}
    assert not varianti & {destinazioni[0], destinazioni[2]}


def test_webp_sceglie_il_primo_nome_con_tutte_le_varianti_libere(tmp_path):
    (tmp_path / "a.webp").write_bytes(b"x")  # già su disco: a.jpg sarebbe libero, ma a.webp no
    file = [foto("/sdcard/Pictures/a.webp"), foto("/sdcard/Music/a (1).png")]
    opzioni = TransferOptions(destination=tmp_path, preserve_structure=False, converti_webp=True)
    piano = build_plan(file, opzioni)
    assert [f.dest_path.name for f in piano.files] == ["a (1).jpg", "a (1) (1).png"]

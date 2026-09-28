import threading

from fotofacile.core.scanner import (
    DEFAULT_ROOTS,
    FALLBACK_MAX_DEPTH,
    MediaFile,
    build_scan_command,
    group_folders,
    list_media,
    parse_stat_stream,
)

FLUSSO = (
    "2456789|1700000000|/sdcard/DCIM/Camera/IMG_20231114_101010.jpg\n"
    "1048576|1700000123|/sdcard/DCIM/Camera/Video bello (1).mp4\n"
    "555|1700000200|/sdcard/DCIM/Camera/foto con | nel nome.jpg\n"
)


def test_parsing_flusso_stat():
    foto = parse_stat_stream(FLUSSO)
    assert [f.remote_path for f in foto] == [
        "/sdcard/DCIM/Camera/IMG_20231114_101010.jpg",
        "/sdcard/DCIM/Camera/Video bello (1).mp4",
        "/sdcard/DCIM/Camera/foto con | nel nome.jpg",
    ]
    assert foto[0].size == 2456789
    assert foto[0].mtime == 1700000000
    assert foto[0].kind == "photo"
    assert foto[1].kind == "video"
    assert foto[2].name == "foto con | nel nome.jpg"
    assert foto[2].parent == "/sdcard/DCIM/Camera"


def test_parsing_ignora_righe_corrotte_e_estensioni_non_media():
    flusso = (
        "non-una-riga-buona\n"
        "12345|1700000000|/sdcard/DCIM/Camera/note.txt\n"
        "12345|abc|/sdcard/DCIM/Camera/x.jpg\n"
        "abc|1700000000|/sdcard/DCIM/Camera/y.jpg\n"
        "12345|1700000000|\n"
        "\n"
    )
    assert parse_stat_stream(flusso) == []


def test_parsing_gestisce_nomi_con_emoji_accenti_e_maiuscole():
    flusso = (
        "100|1700000000|/sdcard/DCIM/Camera/Foto è così 😀.jpg\n"
        "200|1700000001|/sdcard/DCIM/Camera/IMG_0001.JPEG\n"
        "300|1700000002|/sdcard/DCIM/Camera/panorama.HEIC\n"
    )
    foto = parse_stat_stream(flusso)
    assert foto[0].name == "Foto è così 😀.jpg"
    assert foto[1].kind == "photo"
    assert foto[2].kind == "photo"


def test_comando_scansione_quota_percorsi_e_filtra_estensioni():
    comando = build_scan_command(["/sdcard/DCIM", "/sdcard/Le mie foto"], include_videos=False)
    assert "'/sdcard/DCIM'" in comando
    assert "'/sdcard/Le mie foto'" in comando
    assert "*.jpg" in comando and "*.heic" in comando
    assert "*.mp4" not in comando
    assert "stat -c" in comando
    assert "-maxdepth" not in comando


def test_comando_scansione_con_video_e_profondita():
    comando = build_scan_command(["/sdcard"], include_videos=True, max_depth=3)
    assert "*.mp4" in comando
    assert "-maxdepth 3" in comando


def test_group_folders_raggruppa_e_ordina_per_dimensione():
    flusso = (
        "1000|1700000000|/sdcard/DCIM/Camera/a.jpg\n"
        "2000|1700000001|/sdcard/DCIM/Camera/b.jpg\n"
        "500|1700000002|/sdcard/DCIM/Screenshots/c.png\n"
    )
    cartelle = group_folders(parse_stat_stream(flusso))
    assert [c.label for c in cartelle] == ["DCIM/Camera", "DCIM/Screenshots"]
    assert cartelle[0].file_count == 2
    assert cartelle[0].total_size == 3000
    assert cartelle[1].file_count == 1


def test_etichetta_della_cartella_toglie_la_memoria_del_telefono():
    flusso = "10|1700000000|/storage/emulated/0/Pictures/WhatsApp Images/a.jpg\n"
    (cartella,) = group_folders(parse_stat_stream(flusso))
    assert cartella.label == "Pictures/WhatsApp Images"


class BackendFinto:
    def __init__(self, risposte):
        self.risposte = list(risposte)
        self.comandi: list[tuple[str, str]] = []

    def list_media_raw(self, serial: str, command: str) -> str:
        self.comandi.append((serial, command))
        return self.risposte.pop(0) if self.risposte else ""


def test_list_media_usa_il_seriale_richiesto():
    backend = BackendFinto(["100|1700000000|/sdcard/DCIM/Camera/a.jpg\n"])
    risultato = list_media(backend, "SERIAL42")
    assert [f.name for f in risultato] == ["a.jpg"]
    seriale, comando = backend.comandi[0]
    assert seriale == "SERIAL42"
    assert "/sdcard/DCIM" in comando


def test_list_media_ripiega_su_tutta_la_memoria_se_non_trova_nulla():
    backend = BackendFinto(["", "100|1700000000|/sdcard/Strane/cartella/a.jpg\n"])
    risultato = list_media(backend, "S1")
    assert [f.name for f in risultato] == ["a.jpg"]
    assert len(backend.comandi) == 2
    assert f"-maxdepth {FALLBACK_MAX_DEPTH}" in backend.comandi[1][1]


def test_list_media_annullata_ritorna_vuoto():
    cancel = threading.Event()
    cancel.set()
    backend = BackendFinto(["100|1700000000|/sdcard/DCIM/Camera/a.jpg\n"])
    assert list_media(backend, "S1", cancel=cancel) == []
    assert backend.comandi == []


def test_mediafile_ha_nome_e_cartella():
    foto = MediaFile(remote_path="/sdcard/DCIM/Camera/a.jpg", size=1, mtime=2, kind="photo")
    assert foto.name == "a.jpg"
    assert foto.parent == "/sdcard/DCIM/Camera"
    assert DEFAULT_ROOTS[0] == "/sdcard/DCIM"

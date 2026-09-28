import pytest

from fotofacile.core.demo import DemoAdbBackend, demo_files
from fotofacile.core.devices import parse_devices
from fotofacile.core.errors import AdbError
from fotofacile.core.scanner import group_folders, parse_stat_stream


def test_backend_demo_si_presenta_come_dispositivo_pronto():
    backend = DemoAdbBackend()
    (dispositivo,) = parse_devices(backend.devices_raw())
    assert dispositivo.state == "device"
    assert dispositivo.serial == "DEMO12345"
    assert "demo" in dispositivo.display_name.lower()


def test_stato_modificabile_per_provare_gli_altri_casi():
    backend = DemoAdbBackend(state="unauthorized")
    (dispositivo,) = parse_devices(backend.devices_raw())
    assert dispositivo.state == "unauthorized"


def test_stato_nessuno_telefono():
    backend = DemoAdbBackend(state="nessuno")
    assert parse_devices(backend.devices_raw()) == []


def test_elenco_file_produce_righe_stat_compatibili():
    backend = DemoAdbBackend(file_count=8)
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat -c"))
    assert len(file) == 8
    assert all(f.size > 0 for f in file)
    assert all(f.mtime > 0 for f in file)
    assert len(group_folders(file)) >= 2


def test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili():
    file = demo_files(60)
    cartelle = {f["path"].rsplit("/", 1)[0] for f in file}
    assert len(cartelle) >= 3
    nomi = " ".join(f["path"] for f in file)
    assert "è" in nomi or "😀" in nomi
    assert "'" in nomi


def test_stream_restituisce_il_contenuto_della_dimensione_attesa():
    backend = DemoAdbBackend(file_count=3)
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    primo = file[0]
    dati = b"".join(backend.stream_file("DEMO12345", primo.remote_path, chunk_size=1024))
    assert len(dati) == primo.size


def test_stream_e_deterministico():
    backend = DemoAdbBackend(file_count=2)
    percorso = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))[0].remote_path
    primo = b"".join(backend.stream_file("DEMO12345", percorso, chunk_size=512))
    secondo = b"".join(backend.stream_file("DEMO12345", percorso, chunk_size=512))
    assert primo == secondo


def test_stream_di_percorso_inesistente_da_errore():
    backend = DemoAdbBackend()
    with pytest.raises(AdbError):
        list(backend.stream_file("DEMO12345", "/sdcard/DCIM/NonEsiste.jpg"))


def test_cancellazione_rimuove_il_file():
    backend = DemoAdbBackend(file_count=3)
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    bersaglio = file[0].remote_path
    backend.delete_file("DEMO12345", bersaglio)
    rimasti = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    assert bersaglio not in [f.remote_path for f in rimasti]


def test_cancellazione_di_percorso_inesistente_da_errore():
    backend = DemoAdbBackend()
    with pytest.raises(AdbError):
        backend.delete_file("DEMO12345", "/sdcard/DCIM/NonEsiste.jpg")


def test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla():
    backend = DemoAdbBackend()
    assert "demo" in backend.check().lower()
    backend.start_server()
    backend.restart_server()


def test_demo_ha_sia_foto_sia_video():
    file = parse_stat_stream(
        DemoAdbBackend(file_count=40).list_media_raw("DEMO12345", "stat")
    )
    generi = {f.kind for f in file}
    assert generi == {"photo", "video"}

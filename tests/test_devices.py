from fotofacile.core.devices import (
    STATE_MESSAGE,
    DeviceInfo,
    get_devices,
    parse_devices,
    pick_device,
)

LISTA_VUOTA = "List of devices attached\n\n"
LISTA_UNO = (
    "List of devices attached\n"
    "R5CT30ABCDE            device product:a52q model:SM_A525F device:a52 transport_id:2\n"
)
LISTA_NON_AUTORIZZATO = (
    "List of devices attached\n"
    "0123456789ABCDEF       unauthorized transport_id:3\n"
)
LISTA_DUE = (
    "List of devices attached\n"
    "* daemon started successfully\n"
    "R5CT30ABCDE            device product:a52q model:SM_A525F device:a52 transport_id:2\n"
    "emulator-5554          offline\n"
)


def test_lista_vuota():
    assert parse_devices(LISTA_VUOTA) == []


def test_un_dispositivo_pronto():
    (dispositivo,) = parse_devices(LISTA_UNO)
    assert dispositivo.serial == "R5CT30ABCDE"
    assert dispositivo.state == "device"
    assert dispositivo.model == "SM_A525F"
    assert dispositivo.product == "a52q"
    assert dispositivo.is_ready is True
    assert dispositivo.display_name == "SM A525F"


def test_dispositivo_non_autorizzato_non_pronto():
    (dispositivo,) = parse_devices(LISTA_NON_AUTORIZZATO)
    assert dispositivo.state == "unauthorized"
    assert dispositivo.is_ready is False
    assert "Consenti" in STATE_MESSAGE["unauthorized"][0]
    assert dispositivo.display_name == "0123456789ABCDEF"


def test_lista_con_righe_spurie_e_due_dispositivi():
    dispositivi = parse_devices(LISTA_DUE)
    assert [d.serial for d in dispositivi] == ["R5CT30ABCDE", "emulator-5554"]
    assert dispositivi[1].state == "offline"
    assert dispositivi[1].model == ""


def test_modello_vuoto_ricade_sul_seriale():
    dispositivo = DeviceInfo(serial="ABC", state="device", model="", product="")
    assert dispositivo.display_name == "ABC"


def test_modello_con_underscore_diventa_leggibile():
    dispositivo = DeviceInfo(serial="ABC", state="device", model="Pixel_7_Pro", product="")
    assert dispositivo.display_name == "Pixel 7 Pro"


def test_pick_device_sceglie_il_primo_pronto():
    non_pronto = DeviceInfo(serial="OFF", state="offline", model="", product="")
    pronto = DeviceInfo(serial="X", state="device", model="Pixel", product="p")
    assert pick_device([non_pronto, pronto]) is pronto


def test_pick_device_none_se_nessuno_e_pronto():
    dispositivo = DeviceInfo(serial="0123", state="unauthorized", model="", product="")
    assert pick_device([dispositivo]) is None


def test_pick_device_rispetta_il_seriale_richiesto():
    dispositivi = parse_devices(LISTA_DUE)
    scelto = pick_device(dispositivi, serial="emulator-5554")
    assert scelto is not None and scelto.state == "offline"


def test_pick_device_none_senza_dispositivi():
    assert pick_device([]) is None


def test_pick_device_none_se_il_seriale_richiesto_non_esiste():
    assert pick_device(parse_devices(LISTA_UNO), serial="ALTRO") is None


def test_get_devices_usa_il_backend():
    class BackendFinto:
        def devices_raw(self) -> str:
            return LISTA_UNO

    (dispositivo,) = get_devices(BackendFinto())
    assert dispositivo.serial == "R5CT30ABCDE"


def test_ogni_stato_notevole_ha_un_messaggio_umano():
    for stato in ("device", "unauthorized", "offline", "no permissions"):
        messaggio, _suggerimento = STATE_MESSAGE[stato]
        assert messaggio

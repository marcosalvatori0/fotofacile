import subprocess
from pathlib import Path

import pytest

from fotofacile.core.adb import AdbBackend, RealAdbBackend, find_adb, shell_quote
from fotofacile.core.errors import AdbError, FotoFacileError


def _script_adb(tmp_path: Path, corpo: str) -> Path:
    percorso = tmp_path / "adb"
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return percorso


def test_shell_quote_lascia_intatti_i_percorsi_normali():
    assert shell_quote("/sdcard/DCIM/Camera") == "'/sdcard/DCIM/Camera'"


def test_shell_quote_gestisce_apostrofi_e_spazi():
    # La quotatura POSIX chiude la stringa, inserisce l'apostrofo protetto e la riapre.
    assert shell_quote("/sdcard/Le mie foto/Vacanze d'estate.jpg") == (
        "'/sdcard/Le mie foto/Vacanze d'\\''estate.jpg'"
    )


def test_shell_quote_gestisce_dollaro_backtick_e_virgolette():
    assert shell_quote("/sdcard/a$b`c`") == "'/sdcard/a$b`c`'"
    assert shell_quote('/sdcard/x"y') == "'/sdcard/x\"y'"
    assert shell_quote("") == "''"


def test_find_adb_preferisce_la_variabile_di_ambiente(tmp_path):
    finto = tmp_path / "adb"
    finto.write_text("#!/bin/sh\n")
    assert find_adb(env={"FOTOFACILE_ADB": str(finto)}, extra_dirs=(), is_windows=False) == str(finto)


def test_find_adb_usa_il_componente_scaricato_dalla_app(tmp_path):
    home = tmp_path / "home"
    adb = home / ".fotofacile" / "platform-tools" / "adb"
    adb.parent.mkdir(parents=True)
    adb.write_text("#!/bin/sh\n")
    assert find_adb(env={"HOME": str(home), "PATH": ""}, extra_dirs=(), is_windows=False) == str(adb)


def test_find_adb_ignora_variabile_inesistente_e_cerca_nel_percorso(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    adb = bin_dir / "adb"
    adb.write_text("#!/bin/sh\n")
    adb.chmod(0o755)
    risultato = find_adb(
        env={
            "FOTOFACILE_ADB": str(tmp_path / "nope"),
            "PATH": str(bin_dir),
            "HOME": str(tmp_path),  # non guardare la cartella utente reale
        },
        is_windows=False,
    )
    assert risultato == str(adb)


def test_find_adb_ritorna_none_se_assente(tmp_path):
    vuoto = find_adb(
        env={"PATH": str(tmp_path / "vuoto"), "HOME": str(tmp_path / "casa")},
        extra_dirs=(),
        is_windows=False,
    )
    assert vuoto is None


def test_find_adb_su_windows_cerca_adb_exe_nel_profilo(tmp_path):
    utente = tmp_path / "utente"
    adb = utente / ".fotofacile" / "platform-tools" / "adb.exe"
    adb.parent.mkdir(parents=True)
    adb.write_text("")
    trovato = find_adb(env={"USERPROFILE": str(utente), "PATH": ""}, extra_dirs=(), is_windows=True)
    assert trovato == str(adb)


def test_find_adb_su_windows_cerca_nell_sdk_android(tmp_path):
    locale = tmp_path / "AppData" / "Local"
    adb = locale / "Android" / "Sdk" / "platform-tools" / "adb.exe"
    adb.parent.mkdir(parents=True)
    adb.write_text("")
    trovato = find_adb(env={"LOCALAPPDATA": str(locale), "PATH": ""}, extra_dirs=(), is_windows=True)
    assert trovato == str(adb)


def test_find_adb_su_windows_non_usa_la_variabile_home_posix(tmp_path):
    utente = tmp_path / "utente"
    utente.mkdir()
    adb = utente / ".fotofacile" / "platform-tools" / "adb.exe"
    adb.parent.mkdir(parents=True)
    adb.write_text("")
    trovato = find_adb(env={"USERPROFILE": str(utente), "PATH": ""}, extra_dirs=(), is_windows=True)
    assert trovato == str(adb)


def test_errore_espone_messaggio_e_suggerimento():
    errore = AdbError("Il telefono non risponde", hint="Ricollega il cavo")
    assert isinstance(errore, FotoFacileError)
    assert errore.message == "Il telefono non risponde"
    assert errore.hint == "Ricollega il cavo"
    assert str(errore) == "Il telefono non risponde Ricollega il cavo"


def test_eseguibile_assente_produce_errore_umano(tmp_path):
    backend = RealAdbBackend(str(tmp_path / "non-esiste"))
    with pytest.raises(AdbError) as exc:
        backend.devices_raw()
    assert "componente" in exc.value.message.lower()
    assert exc.value.hint


def test_comando_fallito_produce_errore_umano(tmp_path):
    backend = RealAdbBackend(str(_script_adb(tmp_path, "exit 1\n")))
    with pytest.raises(AdbError) as exc:
        backend.devices_raw()
    assert exc.value.hint


def test_check_riporta_la_prima_riga_della_versione(tmp_path):
    backend = RealAdbBackend(str(_script_adb(tmp_path, "echo 'Android Debug Bridge version 1.0.41'\necho altra\n")))
    assert backend.check() == "Android Debug Bridge version 1.0.41"


def test_devices_raw_riporta_l_output_di_adb(tmp_path):
    backend = RealAdbBackend(str(_script_adb(tmp_path, "echo 'List of devices attached'\n")))
    assert "List of devices attached" in backend.devices_raw()


def test_scansione_lenta_supera_il_tempo_massimo(tmp_path):
    backend = RealAdbBackend(str(_script_adb(tmp_path, "sleep 3\n")), scan_timeout=1)
    with pytest.raises(AdbError) as exc:
        backend.list_media_raw("SERIAL", "find")
    assert exc.value.hint


def test_stream_usa_il_seriale_e_la_lettura_senza_scrittura(tmp_path, monkeypatch):
    registro = tmp_path / "argomenti.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    backend = RealAdbBackend(
        str(_script_adb(tmp_path, 'printf "%s\\n" "$@" >> "$REGISTRO"\nprintf "contenuto"\n'))
    )
    dati = b"".join(backend.stream_file("SERIAL123", "/sdcard/DCIM/Le mie foto (1).jpg", chunk_size=4))
    assert dati == b"contenuto"
    argomenti = registro.read_text().splitlines()
    assert argomenti[0] == "-s"
    assert argomenti[1] == "SERIAL123"
    assert argomenti[2] == "exec-out"
    assert argomenti[3] == "cat"
    assert argomenti[4] == "'/sdcard/DCIM/Le mie foto (1).jpg'"


def test_stream_interrotto_produce_errore_umano(tmp_path):
    backend = RealAdbBackend(str(_script_adb(tmp_path, "exit 1\n")))
    with pytest.raises(AdbError) as exc:
        list(backend.stream_file("SERIAL", "/sdcard/a.jpg"))
    assert "leggere" in exc.value.message.lower()


def test_cancellazione_usa_rm_con_seriale_e_percorso_quotato(tmp_path, monkeypatch):
    registro = tmp_path / "argomenti.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    backend = RealAdbBackend(str(_script_adb(tmp_path, 'printf "%s\\n" "$@" >> "$REGISTRO"\n')))
    backend.delete_file("SERIAL123", "/sdcard/DCIM/a'b.jpg")
    argomenti = registro.read_text().splitlines()
    assert argomenti[:3] == ["-s", "SERIAL123", "shell"]
    assert argomenti[3] == "rm"
    assert argomenti[4] == "-f"
    assert argomenti[5] == "'/sdcard/DCIM/a'\\''b.jpg'"


def test_riavvio_collegamento_ignora_errori_di_chiusura(tmp_path, monkeypatch):
    registro = tmp_path / "chiamate.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    backend = RealAdbBackend(
        str(_script_adb(tmp_path, 'printf "%s\\n" "$1" >> "$REGISTRO"\n[ "$1" = "kill-server" ] && exit 1\nexit 0\n'))
    )
    backend.restart_server()
    assert registro.read_text().split() == ["kill-server", "start-server"]


def test_protocollo_backend_richiesto():
    assert hasattr(AdbBackend, "stream_file")

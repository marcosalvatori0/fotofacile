from pathlib import Path

import pytest

from fotofacile.core.adb import shell_quote
from fotofacile.core.adb_passi import AdbAPassi
from fotofacile.core.devices import parse_devices
from fotofacile.core.errors import FotoFacileError
from fotofacile.core.ops import Annullato, esegui_fino_alla_fine
from fotofacile.core.scanner import parse_stat_stream, group_folders

LISTA = (
    "List of devices attached\n"
    "R5CT30ABCDE            device product:a52q model:SM_A525F device:a52 transport_id:2\n"
)


def script(tmp_path: Path, nome: str, corpo: str) -> str:
    percorso = tmp_path / nome
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return str(percorso)


def test_legge_i_dispositivi_collegati(tmp_path):
    adb = AdbAPassi(script(tmp_path, "adb", f"echo '{LISTA.rstrip()}'\n"))
    dispositivi = esegui_fino_alla_fine(adb.dispositivi())
    (dispositivo,) = dispositivi
    assert dispositivo.serial == "R5CT30ABCDE"
    assert dispositivo.is_ready is True


def test_errore_sui_dispositivi_produce_messaggio_umano(tmp_path):
    adb = AdbAPassi(script(tmp_path, "adb", "exit 1\n"))
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(adb.dispositivi())
    assert errore.value.hint


def test_cerca_media_legge_l_output_anche_se_e_lungo(tmp_path, tmp_path_factory):
    righe = "\n".join(f"{1000 + i}|1700000000|/sdcard/DCIM/Camera/foto_{i:05d}.jpg" for i in range(5000))
    adb = AdbAPassi(script(tmp_path, "adb", f"cat <<'FINE'\n{righe}\nFINE\n"))
    file_trovati = esegui_fino_alla_fine(adb.cerca_media("SERIAL1", "find ..."))
    assert len(file_trovati) == 5000
    cartelle = group_folders(file_trovati)
    assert cartelle[0].label == "DCIM/Camera"


def test_cerca_media_passa_il_seriale_giusto(tmp_path, monkeypatch):
    registro = tmp_path / "argomenti.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    adb = AdbAPassi(script(tmp_path, "adb", 'printf "%s\\n" "$@" >> "$REGISTRO"\n'))
    esegui_fino_alla_fine(adb.cerca_media("SERIAL42", "find ..."))
    argomenti = registro.read_text().splitlines()
    assert argomenti[:3] == ["-s", "SERIAL42", "shell"]


def test_copia_un_file_e_rinomina_solo_alla_fine(tmp_path):
    comando = script(tmp_path, "adb", "printf 'contenuto-buono'\n")
    adb = AdbAPassi(comando)
    destinazione = tmp_path / "uscita" / "foto.jpg"
    visti = []
    scritti = esegui_fino_alla_fine(
        adb.copia("SERIAL1", "/sdcard/Camera/foto.jpg", destinazione, on_scritti=visti.append)
    )
    assert scritti == len(b"contenuto-buono")
    assert destinazione.read_bytes() == b"contenuto-buono"
    assert not (destinazione.with_name("foto.jpg.part")).exists()
    assert visti and visti[-1] == scritti


def test_copia_di_un_file_grande_riporta_avanzamento_intermedio(tmp_path):
    comando = script(tmp_path, "adb", "dd if=/dev/zero bs=1024 count=600 2>/dev/null\n")
    adb = AdbAPassi(comando, intervallo=0.0)
    visti = []
    destinazione = tmp_path / "grande.bin"
    scritti = esegui_fino_alla_fine(
        adb.copia("SERIAL1", "/sdcard/grande.bin", destinazione, on_scritti=visti.append)
    )
    assert scritti == 600 * 1024
    assert destinazione.stat().st_size == 600 * 1024
    assert len(visti) >= 2  # l'avanzamento è stato riportato più di una volta


def test_copia_annullata_non_lascia_file(tmp_path):
    import threading

    comando = script(tmp_path, "adb", "dd if=/dev/zero bs=1024 count=2000 2>/dev/null\n")
    adb = AdbAPassi(comando, intervallo=0.0)
    annulla = threading.Event()

    def ferma(byte):
        if byte > 0:
            annulla.set()

    destinazione = tmp_path / "uscita" / "video.mp4"
    with pytest.raises(Annullato):
        esegui_fino_alla_fine(
            adb.copia("SERIAL1", "/sdcard/video.mp4", destinazione, on_scritti=ferma, annulla=annulla)
        )
    assert destinazione.parent.exists()
    assert list(destinazione.parent.iterdir()) == []


def test_copia_fallita_rimuove_il_file_parziale(tmp_path):
    comando = script(tmp_path, "adb", "echo 'errore di lettura' >&2\nexit 1\n")
    adb = AdbAPassi(comando)
    destinazione = tmp_path / "foto.jpg"
    with pytest.raises(FotoFacileError):
        esegui_fino_alla_fine(adb.copia("SERIAL1", "/sdcard/foto.jpg", destinazione))
    assert not destinazione.exists()
    assert not destinazione.with_name("foto.jpg.part").exists()


def test_cancellazione_usa_il_percorso_quotato(tmp_path, monkeypatch):
    registro = tmp_path / "argomenti.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    adb = AdbAPassi(script(tmp_path, "adb", 'printf "%s\\n" "$@" >> "$REGISTRO"\n'))
    esegui_fino_alla_fine(adb.cancella("SERIAL1", "/sdcard/Le mie foto/a'b.jpg"))
    argomenti = registro.read_text().splitlines()
    assert argomenti[:2] == ["-s", "SERIAL1"]
    assert argomenti[2] == "shell" and argomenti[3] == "rm"
    assert argomenti[5] == shell_quote("/sdcard/Le mie foto/a'b.jpg")


def test_riavvio_ignora_gli_errori_di_chiusura(tmp_path, monkeypatch):
    registro = tmp_path / "chiamate.txt"
    monkeypatch.setenv("REGISTRO", str(registro))
    adb = AdbAPassi(
        script(
            tmp_path,
            "adb",
            'printf "%s\\n" "$1" >> "$REGISTRO"\n[ "$1" = "kill-server" ] && exit 1\nexit 0\n',
        )
    )
    esegui_fino_alla_fine(adb.riavvia())
    assert registro.read_text().split() == ["kill-server", "start-server"]


def test_file_temporanei_non_si_accumulano(tmp_path):
    adb = AdbAPassi(script(tmp_path, "adb", "echo '100|1700000000|/sdcard/DCIM/a.jpg'\n"))
    for _ in range(3):
        esegui_fino_alla_fine(adb.dispositivi())
        esegui_fino_alla_fine(adb.cerca_media("SERIAL1", "find ..."))
    residui = [percorso for percorso in adb.cartella_lavoro.iterdir()]
    assert residui == []

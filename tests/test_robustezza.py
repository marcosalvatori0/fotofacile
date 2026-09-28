"""Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà, dati mancanti.

Sono i casi che rovinano l'esperienza a una persona non tecnica, quindi devono restare coperti.
"""

import threading
from pathlib import Path

import pytest

from fotofacile.core.adb_passi import AdbAPassi, AdbDemoAPassi
from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.devices import parse_devices
from fotofacile.core.errors import FotoFacileError
from fotofacile.core.history import History
from fotofacile.core.ops import Annullato, esegui_fino_alla_fine, ProcessoEsterno
from fotofacile.core.osutil import open_in_file_manager
from fotofacile.core.planner import TransferOptions, build_plan
from fotofacile.core.scanner import MediaFile
from fotofacile.core.transfer import transfer


def script(tmp_path: Path, nome: str, corpo: str) -> str:
    percorso = tmp_path / nome
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return str(percorso)


# ── copiatore reale: errori di sistema ───────────────────────────────────
def test_copia_reale_con_errore_di_disco_non_lascia_part(tmp_path, monkeypatch):
    adb = AdbAPassi(script(tmp_path, "adb", "printf 'dati'\n"))
    destinazione = tmp_path / "uscita" / "foto.jpg"

    def replace_rotto(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr("fotofacile.core.adb_passi.os.replace", replace_rotto)
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(adb.copia("SERIAL1", "/sdcard/foto.jpg", destinazione))
    assert "spazio" in errore.value.message.lower()
    assert list(destinazione.parent.iterdir()) == []


def test_copia_reale_con_permesso_negato_spiega_come_rimediare(tmp_path, monkeypatch):
    adb = AdbAPassi(script(tmp_path, "adb", "printf 'dati'\n"))
    destinazione = tmp_path / "uscita" / "foto.jpg"

    def open_negato(*_args, **_kwargs):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr("builtins.open", open_negato)
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(adb.copia("SERIAL1", "/sdcard/foto.jpg", destinazione))
    assert errore.value.hint
    assert not destinazione.exists()


def test_copia_reale_abbandonata_non_lascia_nulla(tmp_path):
    """Se l'utente chiude la finestra a metà copia, il file parziale deve sparire."""
    import time

    adb = AdbAPassi(script(tmp_path, "adb", "dd if=/dev/zero bs=1024 count=3000 2>/dev/null\n"))
    destinazione = tmp_path / "uscita" / "video.mp4"
    generatore = adb.copia("SERIAL1", "/sdcard/video.mp4", destinazione)
    next(generatore)
    time.sleep(0.05)
    generatore.close()  # equivale ad abbandonare il lavoro
    assert not destinazione.exists()
    assert not destinazione.with_name("video.mp4.part").exists()


def test_processo_non_avviabile_non_lascia_file_temporanei(tmp_path):
    processo = ProcessoEsterno([str(tmp_path / "non-esiste")])
    with pytest.raises(FotoFacileError):
        esegui_fino_alla_fine(processo.aspetta())
    processo.termina()
    residui = [percorso for percorso in Path("/tmp").glob("fotofacile-errori-*.txt")]
    assert residui == []


# ── scansione: ripiego e annullamento ────────────────────────────────────
def test_scansione_ripiega_su_tutta_la_memoria_se_non_trova_nulla(tmp_path):
    comando = 'echo "$@" >> ' + str(tmp_path / "chiamate.txt") + "\n"
    adb = AdbAPassi(script(tmp_path, "adb", comando))
    tro_vati = esegui_fino_alla_fine(adb.cerca_media("SERIAL1", "find ..."))
    assert tro_vati == []
    chiamate = (tmp_path / "chiamate.txt").read_text().splitlines()
    assert any("-maxdepth" in riga for riga in chiamate)  # ha provato a fondo


def test_scansione_annullabile(tmp_path):
    adb = AdbAPassi(script(tmp_path, "adb", "sleep 5\n"))
    annulla = threading.Event()
    annulla.set()
    with pytest.raises(Annullato):
        esegui_fino_alla_fine(adb.cerca_media("SERIAL1", "find ...", annulla=annulla))


# ── cronologia malandata ─────────────────────────────────────────────────
def test_cronologia_non_leggibile_non_impedisce_l_avvio(tmp_path):
    percorso = tmp_path / "history.json"
    percorso.write_text("{}")
    percorso.chmod(0o000)
    cronologia = History(percorso)
    cronologia.load()  # non deve sollevare eccezioni
    assert cronologia.count("S") == 0
    percorso.chmod(0o600)


def test_cronologia_non_scrivibile_non_perde_le_foto_copiate(tmp_path, monkeypatch):
    backend = DemoAdbBackend(file_count=2, delay=0.0)
    adb = AdbDemoAPassi(backend, intervallo=0.0)
    file_trovati = esegui_fino_alla_fine(adb.cerca_media("DEMO12345", "stat"))
    piano = build_plan(file_trovati, TransferOptions(destination=tmp_path))
    cronologia = History(tmp_path / "history.json")
    cronologia.load()

    def salva_rotto() -> None:
        raise OSError(13, "Permission denied")

    cronologia.save = salva_rotto  # type: ignore[method-assign]
    risultati = transfer(
        backend, "DEMO12345", piano, TransferOptions(destination=tmp_path), history=cronologia
    )
    assert len(risultati.copied) == 2
    assert risultati.warnings and "elenco dei file copiati" in risultati.warnings[0].lower()


# ── errori non transitori: niente tentativi inutili ──────────────────────
def test_errore_di_permesso_non_viene_ritentato(tmp_path):
    tentativi = {"n": 0}

    class CopiatoreRotto:
        def copia(self, *_args, **_kwargs):
            tentativi["n"] += 1
            raise FotoFacileError(
                "Non ho il permesso di scrivere la cartella.",
                hint="Scegli un'altra cartella.",
            )
            yield 0.0  # pragma: no cover

        def cancella(self, *_args, **_kwargs):  # pragma: no cover - non usato
            yield 0.0

    from fotofacile.core.planner import PlannedFile, TransferPlan
    from fotofacile.core.transfer import transfer_steps
    from fotofacile.core.ops import esegui_fino_alla_fine

    media = MediaFile("/sdcard/a.jpg", 10, 1, "photo")
    piano = TransferPlan(files=[PlannedFile(media=media, rel_path="a.jpg", dest_path=tmp_path / "a.jpg")])
    risultati = esegui_fino_alla_fine(
        transfer_steps(piano, TransferOptions(destination=tmp_path), CopiatoreRotto(), "S1", retries=3)
    )
    assert tentativi["n"] == 1
    assert risultati.failed


# ── collisioni con maiuscole diverse ─────────────────────────────────────
def test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "FOTO.JPG").write_bytes(b"x" * 100)
    media = MediaFile("/sdcard/DCIM/Camera/foto.jpg", 100, 1, "photo")
    piano = build_plan(
        [media], TransferOptions(destination=tmp_path), case_insensitive=True
    )
    (previsto,) = piano.files
    assert previsto.dest_path.name == "foto (1).jpg"


# ── stato "no permissions" di adb ────────────────────────────────────────
def test_stato_no_permissions_viene_riconosciuto():
    uscita = (
        "List of devices attached\n"
        "0123456789ABCDEF       no permissions (user in plugdev group; are your udev rules wrong?); "
        "see [http://developer.android.com/tools/device.html] transport_id:3\n"
    )
    (dispositivo,) = parse_devices(uscita)
    assert dispositivo.state == "no permissions"
    assert dispositivo.is_ready is False


# ── apertura cartella sui vari sistemi ───────────────────────────────────
def test_apertura_cartella_su_windows_non_boccia_explorer():
    import subprocess

    chiamate = []

    def runner(comando, **_kwargs):
        chiamate.append(comando)
        return subprocess.CompletedProcess(comando, 1)  # explorer esce spesso con 1

    open_in_file_manager(Path("C:/foto"), system="win32", runner=runner)
    assert chiamate


def test_apertura_cartella_su_linux_usa_processo_leggero():
    """Su Linux il comando non deve bloccare la finestra."""
    from fotofacile.core import osutil

    avviati = []

    class Proc:
        returncode = 0
        pid = 123

    def popen(comando, **_kwargs):
        avviati.append(comando)
        return Proc()

    originale = osutil.subprocess.Popen
    osutil.subprocess.Popen = popen  # type: ignore[assignment]
    try:
        open_in_file_manager(Path("/tmp/foto"), system="linux")
    finally:
        osutil.subprocess.Popen = originale  # type: ignore[assignment]
    assert avviati == [["xdg-open", "/tmp/foto"]]

from pathlib import Path

from fotofacile.core.devices import DeviceInfo
from fotofacile.core.planner import TransferPlan
from fotofacile.core.report import build_report, save_report
from fotofacile.core.scanner import MediaFile
from fotofacile.core.transfer import TransferResults


def test_resoconto_completo_contiene_numeri_e_destinazione(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="SM_A525F", product="a52")
    piano = TransferPlan(total_bytes=300, skipped_duplicates=2, skipped_existing=1)
    esiti = TransferResults(
        copied=[tmp_path / "a.jpg", tmp_path / "b.jpg"],
        skipped=3,
        failed=[(MediaFile("/sdcard/DCIM/brotta.jpg", 10, 1, "photo"), "Telefono scollegato")],
        bytes_copied=300,
        elapsed=95.0,
        deleted_from_phone=2,
    )
    testo = build_report(esiti, piano, dispositivo, started_at=1_700_000_000, destination=tmp_path)
    assert "SM A525F" in testo
    assert "Copiate: 2 file (300 B)" in testo
    assert "Saltate" in testo
    assert "Errori: 1" in testo
    assert "brotta.jpg" in testo
    assert "Telefono scollegato" in testo
    assert str(tmp_path) in testo
    assert "1 minuto e 35 secondi" in testo
    assert "Cancellate dal telefono: 2" in testo


def test_resoconto_annullato_lo_dice_chiaramente(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="", product="")
    esiti = TransferResults(cancelled=True, bytes_copied=0, elapsed=3.0)
    testo = build_report(esiti, TransferPlan(), dispositivo, started_at=0, destination=tmp_path)
    assert "interrotto" in testo.lower()
    assert "S1" in testo
    assert "al sicuro" in testo


def test_resoconto_senza_novita_lo_esplicita(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="Pixel", product="p")
    piano = TransferPlan(total_bytes=500, skipped_duplicates=5)
    esiti = TransferResults(skipped=5, bytes_copied=0, elapsed=2.0)
    testo = build_report(esiti, piano, dispositivo, started_at=0, destination=tmp_path)
    assert "nulla di nuovo" in testo.lower()


def test_resoconto_senza_errori_non_elenca_file(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="Pixel", product="p")
    esiti = TransferResults(copied=[tmp_path / "a.jpg"], bytes_copied=10, elapsed=1.0)
    testo = build_report(esiti, TransferPlan(total_bytes=10), dispositivo, started_at=0, destination=tmp_path)
    assert "File non copiati" not in testo


def test_salvataggio_resoconto_su_file(tmp_path):
    percorso = save_report("ciao", tmp_path)
    assert percorso.is_file()
    assert percorso.read_text() == "ciao"
    assert percorso.suffix == ".txt"
    assert percorso.name.startswith("resoconto-fotofacile-")
    assert percorso.parent == tmp_path


def test_salvataggio_resoconto_crea_la_cartella(tmp_path):
    percorso = save_report("ciao", tmp_path / "nuova" / "cartella")
    assert percorso.is_file()


def test_salvataggio_resoconto_su_cartella_non_scrivilibile_usa_il_desktop(tmp_path, monkeypatch):
    bloccata = tmp_path / "bloccata"
    bloccata.mkdir()
    bloccata.chmod(0o500)
    desktop = tmp_path / "Desktop"
    monkeypatch.setenv("HOME", str(tmp_path))
    try:
        percorso = save_report("ciao", bloccata)
    finally:
        bloccata.chmod(0o700)
    assert percorso.parent == desktop
    assert percorso.read_text() == "ciao"

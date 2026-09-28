import json

from fotofacile.core.history import History, default_path


def test_file_assente_viene_trattato_come_vuoto(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    assert cronologia.count("SERIAL1") == 0
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 20)


def test_round_trip_salva_e_rilegge(tmp_path):
    percorso = tmp_path / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/out/a.jpg")
    cronologia.save()

    altra = History(percorso)
    altra.load()
    assert altra.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 20)
    assert altra.count("SERIAL1") == 1


def test_contenuto_diverso_non_risulta_gia_copiato(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/a.jpg")
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 11, 20)
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 21)


def test_cronologie_separate_per_dispositivo(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/a.jpg")
    assert cronologia.count("SERIAL2") == 0
    assert not cronologia.contains("SERIAL2", "DCIM/Camera/a.jpg", 10, 20)


def test_file_corrotto_viene_messo_da_parte_senza_crash(tmp_path):
    percorso = tmp_path / "history.json"
    percorso.write_text("{ questo non è json")
    cronologia = History(percorso)
    cronologia.load()
    assert cronologia.count("SERIAL1") == 0
    salvataggi = list(tmp_path.glob("history.json.corrupt-*"))
    assert len(salvataggi) == 1
    assert "questo non è json" in salvataggi[0].read_text()


def test_file_con_struttura_inattesa_non_fa_esplodere_nulla(tmp_path):
    percorso = tmp_path / "history.json"
    percorso.write_text(json.dumps({"version": 1, "devices": ["non", "un", "dizionario"]}))
    cronologia = History(percorso)
    cronologia.load()
    assert cronologia.count("SERIAL1") == 0


def test_salvataggio_non_lascia_file_temporanei(tmp_path):
    percorso = tmp_path / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "a.jpg", 1, 2, "/tmp/a.jpg")
    cronologia.save()
    assert percorso.is_file()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["history.json"]


def test_salvataggio_crea_la_cartella_e_scrive_la_versione(tmp_path):
    percorso = tmp_path / "sottocartella" / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "a.jpg", 1, 2, "/tmp/a.jpg")
    cronologia.save()
    contenuto = json.loads(percorso.read_text())
    assert contenuto["version"] == 1
    assert "SERIAL1" in contenuto["devices"]


def test_percorso_predefinito_sotto_la_cartella_utente(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("USERPROFILE", raising=False)
    assert default_path() == tmp_path / ".fotofacile" / "history.json"

import pytest

from fotofacile import __version__
from fotofacile.cli import build_doctor_report, main


def test_versione(capsys):
    with pytest.raises(SystemExit) as uscita:
        main(["--version"], env={})
    assert uscita.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_aiuto_elenca_le_modalita(capsys):
    with pytest.raises(SystemExit) as uscita:
        main(["--help"], env={})
    assert uscita.value.code == 0
    uscita_testo = capsys.readouterr().out
    assert "--demo" in uscita_testo
    assert "doctor" in uscita_testo


def test_diagnostica_riporta_tutte_le_voci(capsys):
    esito = main(["doctor"], env={"HOME": "/tmp/prova", "PATH": ""})
    assert esito == 0
    testo = capsys.readouterr().out
    assert "Sistema:" in testo
    assert "Python:" in testo
    assert "Tkinter:" in testo
    assert "Componente:" in testo
    assert "Telefoni collegati: nessuno" in testo
    assert "Cartella dati: /tmp/prova/.fotofacile" in testo
    assert "Scrittura:" in testo


def test_costruzione_diagnostica_senza_componente():
    testo = build_doctor_report(
        adb_path=None,
        adb_version="",
        system="darwin",
        python_version="3.14.7",
        tk_version="9.0",
        devices=[],
        app_folder="/tmp/.fotofacile",
        writing_ok=True,
    )
    assert "Sistema: darwin" in testo
    assert "Python: 3.14.7" in testo
    assert "Tkinter: 9.0" in testo
    assert "Componente: non trovato" in testo
    assert "Telefoni collegati: nessuno" in testo
    assert "Scrittura: ok" in testo
    assert "Installa componente" in testo


def test_costruzione_diagnostica_con_telefono_e_problemi():
    testo = build_doctor_report(
        adb_path="/usr/bin/adb",
        adb_version="Android Debug Bridge version 1.0.41",
        system="win32",
        python_version="3.12.0",
        tk_version="8.6",
        devices=[("R5CT30", "device"), ("0123", "unauthorized")],
        app_folder="C:/Users/tizio/.fotofacile",
        writing_ok=False,
    )
    assert "/usr/bin/adb" in testo
    assert "Android Debug Bridge version 1.0.41" in testo
    assert "R5CT30 (device)" in testo
    assert "0123 (unauthorized)" in testo
    assert "Scrittura: problema" in testo


def test_modalita_demo_avvia_la_grafica(monkeypatch):
    from fotofacile import cli

    chiamate = {}
    monkeypatch.setattr(cli, "start_gui", lambda **kwargs: chiamate.update(kwargs) or 0)
    assert main(["--demo"], env={}) == 0
    assert chiamate == {"demo": True}


def test_avvio_normale_senza_demo(monkeypatch):
    from fotofacile import cli

    chiamate = {}
    monkeypatch.setattr(cli, "start_gui", lambda **kwargs: chiamate.update(kwargs) or 0)
    assert main([], env={}) == 0
    assert chiamate == {"demo": False}

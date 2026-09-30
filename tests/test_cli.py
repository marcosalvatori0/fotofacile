import pytest

from fotofacile import __version__
from fotofacile.cli import build_doctor_report, main


@pytest.fixture(autouse=True)
def _casa_isolata(monkeypatch, tmp_path):
    """Qui si avvia la grafica (finta): il registro di avvio deve finire in una cartella di prova.

    Prima alcuni test scrivevano nel vero ``~/.fotofacile/avvio.log`` di chi li eseguiva,
    cinque righe a ogni esecuzione della suite.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))


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
    assert "Componente aggiuntivo (adb):" in testo
    assert "Telefoni collegati: nessuno" in testo
    assert "Cartella dati: /tmp/prova/.fotofacile" in testo
    assert "Scrittura:" in testo


def test_diagnostica_dice_quali_collegamenti_sono_disponibili(capsys):
    """La diagnosi deve dire subito se il collegamento **senza Debug USB** è disponibile."""
    main(["doctor"], env={"HOME": "/tmp/prova", "PATH": ""})
    testo = capsys.readouterr().out
    assert "Modi di collegamento:" in testo
    assert "Collegamento diretto" in testo
    assert "Debug USB" in testo


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
    assert "Componente aggiuntivo (adb): non trovato" in testo
    assert "Telefoni collegati: nessuno" in testo
    assert "Scrittura: ok" in testo
    assert "Installa componente" in testo


def test_costruzione_diagnostica_elenca_i_modi():
    testo = build_doctor_report(
        adb_path=None,
        adb_version="",
        system="darwin",
        python_version="3.14.7",
        tk_version="9.0",
        devices=[],
        app_folder="/tmp/.fotofacile",
        writing_ok=True,
        modi=[("Collegamento diretto", True), ("Collegamento rapido", False)],
    )
    assert "Collegamento diretto — disponibile" in testo
    assert "Collegamento rapido — non disponibile" in testo
    assert "Non serve attivare il Debug USB" in testo


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


def test_senza_finestra_grafica_spiega_come_risolvere(monkeypatch, capsys):
    import tkinter as tk

    from fotofacile import cli

    class AppRotta:
        def __init__(self, **_kwargs):
            raise tk.TclError("no display name and no $DISPLAY environment variable")

    monkeypatch.setattr("fotofacile.ui.app.App", AppRotta, raising=False)
    esito = cli.main([], env={})
    messaggio = capsys.readouterr().out.lower()
    assert esito == 1
    assert "finestra" in messaggio or "grafica" in messaggio
    assert "doctor" in messaggio


def test_autocollaudo_riporta_esito_positivo(capsys, monkeypatch):
    """L'autocollaudo serve a verificare una build impacchettata: deve dire chiaramente ok."""
    from fotofacile import cli

    class AppFinta:
        def __init__(self, **_kwargs):
            self.pages = {"connect": 1, "select": 2, "options": 3, "transfer": 4}
            self.current_page = "connect"

        def withdraw(self):
            pass

        def update(self):
            pass

        def destroy(self):
            pass

        def stop_all_polling(self):
            pass

    monkeypatch.setattr("fotofacile.ui.app.App", AppFinta, raising=False)
    esito = cli.main(["--selftest"], env={})
    assert esito == 0
    uscita = capsys.readouterr().out
    assert '"ok": true' in uscita
    assert "connect" in uscita


def test_autocollaudo_riporta_esito_negativo(capsys, monkeypatch):
    import tkinter as tk

    from fotofacile import cli

    class AppRotta:
        def __init__(self, **_kwargs):
            raise tk.TclError("no display")

    monkeypatch.setattr("fotofacile.ui.app.App", AppRotta, raising=False)
    assert cli.main(["--selftest"], env={}) == 1
    uscita = capsys.readouterr().out
    assert '"ok": false' in uscita
    assert "no display" in uscita


def test_aiuto_menziona_autocollaudo(capsys):
    with pytest.raises(SystemExit):
        main(["--help"], env={})
    assert "--selftest" in capsys.readouterr().out


def test_log_di_avvio_viene_scritto(tmp_path):
    from fotofacile.cli import scrivi_log_avvio

    percorso = scrivi_log_avvio("prova di avvio", env={"HOME": str(tmp_path)})
    assert percorso.is_file()
    assert "prova di avvio" in percorso.read_text()
    scrivi_log_avvio("seconda riga", env={"HOME": str(tmp_path)})
    assert percorso.read_text().count("prova di avvio") == 1
    assert "seconda riga" in percorso.read_text()


def test_contesto_grafico_dubbio_quando_mancano_i_segnali(monkeypatch):
    from fotofacile import cli

    assert cli.contesto_grafico_dubbio(env={}, system="darwin") is True
    assert cli.contesto_grafico_dubbio(env={"TERM_PROGRAM": "Apple_Terminal"}, system="darwin") is False
    assert cli.contesto_grafico_dubbio(env={"__CFBundleIdentifier": "com.apple.finder"}, system="darwin") is False
    assert cli.contesto_grafico_dubbio(env={}, system="linux") is False


def test_avviso_visibile_usa_osascript_su_macos(tmp_path):
    from fotofacile.cli import avviso_visibile

    chiamate = []

    def runner(comando, **_kwargs):
        import subprocess

        chiamate.append(comando)
        return subprocess.CompletedProcess(comando, 0)

    avviso_visibile("Non riesco ad aprire la finestra", env={"HOME": str(tmp_path)}, system="darwin", runner=runner)
    assert chiamate and chiamate[0][0] == "osascript"
    assert "Non riesco ad aprire la finestra" in " ".join(chiamate[0])


def test_avvio_avvisa_in_chiaro_se_la_grafica_non_parte(monkeypatch, capsys):
    """Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare nel silenzio."""
    import tkinter as tk

    from fotofacile import cli

    avvisi = []
    monkeypatch.setattr(cli, "avviso_visibile", lambda testo, **kwargs: avvisi.append(testo))

    class AppRotta:
        def __init__(self, **_kwargs):
            raise tk.TclError("no display name and no $DISPLAY environment variable")

    monkeypatch.setattr("fotofacile.ui.app.App", AppRotta, raising=False)
    esito = cli.main([], env={"HOME": "/tmp"})
    assert esito == 1
    assert avvisi, "l'utente deve ricevere un avviso visibile"
    assert "finestra" in avvisi[0].lower()
    assert "doctor" in avvisi[0]
    capsys.readouterr()


def test_avvio_salta_la_prova_quando_il_contesto_e_grafico(monkeypatch, tmp_path):
    from fotofacile import cli

    chiamate = {"prova": 0, "avvio": 0}

    def finta_prova(*_args, **_kwargs):
        chiamate["prova"] += 1
        return True

    class AppFinta:
        def __init__(self, **_kwargs):
            chiamate["avvio"] += 1

        def mainloop(self):
            pass

    monkeypatch.setattr(cli, "prova_finestra", finta_prova)
    monkeypatch.setattr("fotofacile.ui.app.App", AppFinta, raising=False)
    monkeypatch.setenv("TERM_PROGRAM", "Apple_Terminal")
    assert cli.start_gui() == 0
    assert chiamate == {"prova": 0, "avvio": 1}


def test_formati_cartella_inesistente_da_errore(tmp_path, capsys):
    assert main(["formati", str(tmp_path / "non-esiste")], env={}) == 2
    assert "Indica una cartella esistente" in capsys.readouterr().out
    assert main(["formati"], env={}) == 2


def test_formati_mostra_il_formato_vero(tmp_path, capsys):
    cartella = tmp_path / "foto"
    cartella.mkdir()
    (cartella / "sticker.webp").write_bytes(b"RIFF\x10\0\0\0WEBPVP8 ")
    assert main(["formati", str(cartella)], env={}) == 0
    assert ".webp: 1 webp" in capsys.readouterr().out


def test_formati_cartella_vuota(tmp_path, capsys):
    assert main(["formati", str(tmp_path)], env={}) == 0
    assert "non contiene file" in capsys.readouterr().out


def test_la_diagnosi_riferisce_la_conversione_webp():
    from fotofacile.cli import build_doctor_report

    base = dict(adb_path=None, adb_version="", system="linux", python_version="3.12", tk_version="8.6",
                devices=[], app_folder="/x", writing_ok=True)
    assert "Conversione WebP: disponibile" in build_doctor_report(**base, conversione_webp=True)
    assert "Conversione WebP: non disponibile" in build_doctor_report(**base, conversione_webp=False)


def test_emetti_stampa_quando_c_e_un_terminale(capsys, tmp_path):
    from fotofacile.cli import emetti

    assert emetti("ciao", env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}) is None
    assert "ciao" in capsys.readouterr().out


def test_emetti_scrive_un_file_senza_terminale(monkeypatch, tmp_path):
    import sys

    from fotofacile.cli import emetti

    monkeypatch.setattr(sys, "stdout", None)
    aperti = []
    percorso = emetti(
        "rapporto",
        env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)},
        apri=lambda p: aperti.append(p),
    )
    assert percorso is not None and percorso.read_text(encoding="utf-8") == "rapporto"
    assert percorso == tmp_path / ".fotofacile" / "diagnosi.txt"
    assert aperti == [percorso]


def test_emetti_senza_terminale_usa_il_nome_file_richiesto(monkeypatch, tmp_path):
    import sys

    from fotofacile.cli import emetti

    monkeypatch.setattr(sys, "stdout", None)
    percorso = emetti(
        "x", "selftest.txt", env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)},
        apri=lambda _p: None,
    )
    assert percorso == tmp_path / ".fotofacile" / "selftest.txt"


def test_doctor_dal_programma_senza_finestra_nera_scrive_e_apre_il_rapporto(monkeypatch, tmp_path):
    """«FotoFacile.exe doctor» (collegamento del menu Start) deve arrivare a doctor(), non alla GUI."""
    import sys

    from fotofacile import cli

    monkeypatch.setattr(sys, "stdout", None)
    aperti = []
    monkeypatch.setattr(cli.os, "startfile", lambda p: aperti.append(p), raising=False)
    monkeypatch.setattr(cli.sys, "platform", "win32")
    monkeypatch.setattr(cli, "start_gui", lambda **_k: pytest.fail("non deve aprire la finestra"))
    ambiente = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path), "PATH": ""}
    assert cli.main(["doctor"], env=ambiente) == 0
    rapporto = tmp_path / ".fotofacile" / "diagnosi.txt"
    assert "FotoFacile" in rapporto.read_text(encoding="utf-8")
    assert aperti == [rapporto]


def test_autocollaudo_senza_terminale_scrive_selftest_txt_anche_se_ok(monkeypatch, tmp_path):
    """La CI legge selftest.txt: l'esito va scritto anche quando l'autocollaudo riesce."""
    import sys

    from fotofacile import cli

    class AppFinta:
        def __init__(self, **_kwargs):
            self.pages = {"connect": 1}
            self.current_page = "connect"

        def withdraw(self):
            pass

        def update(self):
            pass

        def destroy(self):
            pass

        def stop_all_polling(self):
            pass

    monkeypatch.setattr("fotofacile.ui.app.App", AppFinta, raising=False)
    monkeypatch.setattr(sys, "stdout", None)
    monkeypatch.setattr(cli.sys, "platform", "win32")
    aperti = []
    monkeypatch.setattr(cli.os, "startfile", lambda p: aperti.append(p), raising=False)
    assert cli.main(["--selftest"], env={}) == 0
    assert '"ok": true' in (tmp_path / ".fotofacile" / "selftest.txt").read_text(encoding="utf-8")
    assert aperti == []


def test_emetti_non_apre_il_file_se_l_ambiente_lo_vieta(monkeypatch, tmp_path):
    """Sulla pipeline (FOTOFACILE_NO_OPEN) il Blocco note non deve aprirsi e bloccare l'attesa."""
    import sys

    from fotofacile.cli import emetti

    monkeypatch.setattr(sys, "stdout", None)
    aperti = []
    env = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path), "FOTOFACILE_NO_OPEN": "1"}
    percorso = emetti("rapporto", env=env, apri=lambda p: aperti.append(p))
    assert percorso is not None and percorso.read_text(encoding="utf-8") == "rapporto"
    assert aperti == []  # il file c'è, ma nessuno lo apre

import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.errors import FotoFacileError
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app(tmp_path, monkeypatch):
    from fotofacile.ui.app import App

    monkeypatch.setenv("HOME", str(tmp_path))
    applicazione = App(backend=DemoAdbBackend(file_count=6), demo_mode=True)
    applicazione.withdraw()
    applicazione.stop_all_polling()
    yield applicazione
    applicazione.destroy()


def test_pagine_registrate(app):
    assert set(app.pages) == {"connect", "select", "options", "transfer"}
    for pagina in app.pages.values():
        assert pagina.winfo_exists()


def test_navigazione_avanti_indietro(app):
    app.go_to("select")
    assert app.current_page == "select"
    app.go_to("prev")
    assert app.current_page == "connect"
    app.go_to("next")
    assert app.current_page == "select"
    app.go_to("next")
    assert app.current_page == "options"
    app.go_to("next")
    assert app.current_page == "transfer"


def test_navigazione_non_esce_dai_limiti(app):
    app.go_to("connect")
    app.go_to("prev")
    assert app.current_page == "connect"
    app.go_to("transfer")
    app.go_to("next")
    assert app.current_page == "transfer"


def test_indicatore_passi_segue_la_pagina(app):
    app.go_to("options")
    assert app.step_indicator.current == 2


def test_registro_e_stato(app):
    app.log("ciao")
    assert "ciao" in app.log_pane.get_text()
    app.set_status("Telefono collegato", hint="Tutto pronto", kind="successo")
    assert app.banner.visible is True
    assert "Telefono collegato" in app.banner.message_text
    assert "Tutto pronto" in app.banner.hint_text
    app.go_to("select")
    assert app.banner.visible is False


def test_lavoro_in_background_aggiorna_la_ui(app):
    esiti = []
    app.run_async(lambda: 21 * 2, on_done=lambda valore: esiti.append(valore))
    for _ in range(100):
        app.update()
        app.pump_events()
        if esiti:
            break
    assert esiti == [42]


def test_errore_in_background_mostra_messaggio_umano(app):
    def fallisci():
        raise FotoFacileError("Il telefono non risponde", hint="Controlla il cavo")

    app.run_async(fallisci)
    for _ in range(100):
        app.update()
        app.pump_events()
        if app.banner.visible:
            break
    assert "Il telefono non risponde" in app.banner.message_text
    assert "Controlla il cavo" in app.banner.hint_text
    assert "Il telefono non risponde" in app.log_pane.get_text()


def test_errore_imprevisto_non_chiude_il_programma(app):
    def esplodi():
        raise RuntimeError("errore inatteso")

    app.run_async(esplodi)
    for _ in range(100):
        app.update()
        app.pump_events()
        if app.banner.visible:
            break
    assert app.banner.visible is True
    assert "funzionato" in app.banner.message_text.lower()


def test_callback_di_errore_personalizzato(app):
    visti = []

    def fallisci():
        raise FotoFacileError("Manca il componente")

    app.run_async(fallisci, on_error=visti.append)
    for _ in range(100):
        app.update()
        app.pump_events()
        if visti:
            break
    assert visti and visti[0].message == "Manca il componente"


def test_cronologia_caricata_una_volta(app):
    prima = app.history()
    assert prima is app.history()
    assert prima.count("DEMO12345") == 0


def test_chiusura_ferma_i_sondaggi(app):
    app.pages["connect"].start_polling()
    app.stop_all_polling()
    assert app.pages["connect"]._polling is False

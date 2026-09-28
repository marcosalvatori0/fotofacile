import threading

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app(finestra_condivisa, tmp_path):
    from tests.conftest import azzera

    azzera(finestra_condivisa, tmp_path)
    finestra_condivisa.INTERVALLO_PASSI = 0.0
    yield finestra_condivisa
    finestra_condivisa.INTERVALLO_PASSI = 0.02
    azzera(finestra_condivisa, tmp_path)


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


def test_task_eseguito_a_passi_senza_thread(app):
    esiti = []
    pronto = threading.Event()

    def lavoro():
        yield 0.0
        yield 0.0
        yield 0.0
        return "finito"

    app.run_task(lavoro(), on_done=esiti.append)
    assert attendi(app, lambda: bool(esiti), passi=200)
    assert esiti == ["finito"]
    assert threading.active_count() == 1  # nel programma non girano thread


def test_task_con_errore_mostra_il_messaggio_umano(app):
    def lavoro():
        yield 0.0
        raise FotoFacileError("Il telefono non risponde", hint="Controlla il cavo")

    app.run_task(lavoro())
    assert attendi(app, lambda: app.banner.visible, passi=200)
    assert "Il telefono non risponde" in app.banner.message_text
    assert "Controlla il cavo" in app.banner.hint_text
    assert "Il telefono non risponde" in app.log_pane.get_text()


def test_task_con_errore_imprevisto_non_chiude_il_programma(app):
    def lavoro():
        yield 0.0
        raise RuntimeError("errore inatteso")

    app.run_task(lavoro())
    assert attendi(app, lambda: app.banner.visible, passi=200)
    assert "funzionato" in app.banner.message_text.lower()
    assert "errore inatteso" in app.log_pane.get_text()


def test_task_con_callback_di_errore_personalizzato(app):
    visti = []

    def lavoro():
        yield 0.0
        raise FotoFacileError("Manca il componente")

    app.run_task(lavoro(), on_error=visti.append)
    assert attendi(app, lambda: bool(visti), passi=200)
    assert visti and visti[0].message == "Manca il componente"
    assert app.banner.visible is False


def test_la_finestra_resta_reattiva_durante_un_task_lungo(app):
    passi = []

    def lavoro():
        for indice in range(5):
            passi.append(indice)
            yield 0.0
        return "ok"

    app.run_task(lavoro())
    for _ in range(200):
        app.update()
        app.go_to("options")  # la finestra continua a rispondere
        app.go_to("connect")
        if passi and passi[-1] == 4:
            break
    assert passi[-1] == 4
    assert app.current_page == "connect"


def test_modalita_demo_attivabile_e_disattivabile(app):
    app.attiva_demo()
    assert app.demo_mode is True
    assert app.remote is not None
    dispositivi = []
    app.run_task(app.remote.dispositivi(), on_done=dispositivi.extend)
    assert attendi(app, lambda: bool(dispositivi), passi=200)
    assert dispositivi[0].serial == "DEMO12345"


def test_cronologia_caricata_una_volta(app):
    prima = app.history()
    assert prima is app.history()
    assert prima.count("DEMO12345") == 0


def test_chiusura_ferma_i_sondaggi(app):
    app.pages["connect"].start_polling()
    app.stop_all_polling()
    assert app.pages["connect"]._polling is False

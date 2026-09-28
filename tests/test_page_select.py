import pytest

from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")


def _scansiona(app) -> bool:
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.go_to("select")
    pagina = app.pages["select"]
    return attendi(app, lambda: pagina._scansione_fatta, passi=400)


def test_scansione_riempie_l_elenco_delle_cartelle(app):
    assert _scansiona(app)
    pagina = app.pages["select"]
    assert pagina._files
    assert pagina.folder_vars
    assert all(variabile.get() for variabile in pagina.folder_vars.values())


def test_totali_con_e_senza_video(app):
    assert _scansiona(app)
    pagina = app.pages["select"]
    tutti = pagina.total_for(pagina._files)
    solo_foto = pagina.total_for([file for file in pagina._files if file.kind == "photo"])
    assert tutti[0] >= solo_foto[0] > 0
    assert tutti[1] >= solo_foto[1]


def test_avanti_senza_selezione_spiega_e_non_avanza(app):
    assert _scansiona(app)
    pagina = app.pages["select"]
    for variabile in pagina.folder_vars.values():
        variabile.set(False)
    pagina.go_next()
    assert app.current_page == "select"
    assert "spunta" in app.banner.hint_text.lower() or "nessuna foto" in app.banner.message_text.lower()


def test_avanti_con_selezione_passa_alle_opzioni(app):
    assert _scansiona(app)
    pagina = app.pages["select"]
    pagina.go_next()
    assert app.current_page == "options"
    assert app.media_files
    assert app.selected_folders


def test_filtro_per_data_riduce_la_selezione(app):
    assert _scansiona(app)
    pagina = app.pages["select"]
    tutti = len(pagina.selected_files())
    pagina.data_minima.set("2099-01-01")
    assert len(pagina.selected_files()) == 0
    pagina.data_minima.set("")
    assert len(pagina.selected_files()) == tutti

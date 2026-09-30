import pytest

from fotofacile.core.devices import DeviceInfo
from fotofacile.ui.page_connect import HELP_BRANDS, BRAND_SCONOSCIUTO, build_help_text
from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


def test_aiuto_contiene_le_marche_e_i_passi():
    for marca in ("Samsung", "Xiaomi", "Google", "Huawei", "Oppo"):
        assert marca in HELP_BRANDS
        assert len(HELP_BRANDS[marca]) >= 4
    testo = build_help_text("Samsung")
    assert "Debug USB" in testo
    assert "Consenti" in testo
    assert "cavo" in testo.lower()
    # Il Debug USB è l'ultima spiaggia, non il primo consiglio.
    assert "ultima" in testo.lower() or "solo se" in testo.lower()


def test_l_aiuto_generico_non_parla_di_debug():
    """I primi consigli non devono nominare il Debug USB: non è obbligatorio."""
    from fotofacile.ui.page_connect import build_help_text_generico

    testo = build_help_text_generico()
    assert "cavo" in testo.lower()
    righe = [riga for riga in testo.splitlines() if riga.strip()]
    # Il Debug USB può comparire solo alla fine, come ultima possibilità.
    prime = "\n".join(righe[: max(1, len(righe) - 2)])
    assert "Debug USB" not in prime
    assert "Debug USB" in testo


def test_aiuto_per_marca_sconosciuta_non_lascia_vuoti():
    testo = build_help_text(BRAND_SCONOSCIUTO)
    assert "Debug USB" in testo
    assert len(testo) > 200


def test_riconosce_il_telefono_pronto(app):
    pagina = app.pages["connect"]
    pagina.check_now()
    assert attendi(app, lambda: app.device is not None)
    assert app.device.serial == "DEMO12345"
    assert "collegato" in pagina.message.lower()
    assert pagina.bottone_avanti.instate(["!disabled"])


def test_telefono_non_autorizzato_mostra_istruzioni(app):
    app.backend.state = "unauthorized"
    pagina = app.pages["connect"]
    pagina.check_now()
    assert attendi(app, lambda: "Consenti" in pagina.message)
    assert app.device is None
    assert pagina.bottone_avanti.instate(["disabled"])
    assert "cavo" in pagina.dettaglio.cget("text").lower()


def test_nessun_telefono_invita_a_collegarlo(app):
    app.backend.state = "nessuno"
    pagina = app.pages["connect"]
    pagina.check_now()
    assert attendi(app, lambda: "collegalo" in pagina.message.lower())
    assert app.device is None
    assert pagina.bottone_avanti.instate(["disabled"])


def test_senza_componente_lo_dice_e_propone_installazione(app):
    """Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice."""
    app.remote = None
    app.demo_mode = False
    app.adb_path = None
    pagina = app.pages["connect"]
    pagina.check_now()
    assert attendi(app, lambda: "collegarmi" in pagina.message.lower())
    assert pagina.bottone_installa.instate(["!disabled"])


def test_con_componente_presente_il_pulsante_installazione_e_spento(app, tmp_path):
    pagina = app.pages["connect"]
    pagina._aggiorna_bottone_installa()
    assert pagina.bottone_installa.instate(["disabled"])


def test_riavvio_collegamento_richiama_il_backend(app):
    chiamate = []
    app.backend.restart_server = lambda: chiamate.append("riavviato")
    pagina = app.pages["connect"]
    pagina.restart_connection()
    assert attendi(app, lambda: bool(chiamate))
    assert chiamate == ["riavviato"]


def test_riavvio_ricontrolla_i_collegamenti_disponibili(app, monkeypatch):
    """«Riprova il collegamento» non presuppone nessuna impostazione sul telefono."""
    import fotofacile.ui.app as modulo_app
    from fotofacile.core.trasporto import TrasportoDemo

    def finti_disponibili(**_kwargs):
        return [TrasportoDemo(app.backend, intervallo=0.0)]

    monkeypatch.setattr(modulo_app, "trasporti_disponibili", finti_disponibili)
    app.remote = None
    app.demo_mode = False
    pagina = app.pages["connect"]
    pagina.restart_connection()
    assert app.remote is not None
    assert attendi(app, lambda: app.banner.visible)
    testo = f"{app.banner.message_text} {app.banner.hint_text}".lower()
    assert "collegamento" in testo


def test_modalita_demo_attivabile_dal_passo_1(app):
    app.remote = None
    app.demo_mode = False
    app.adb_path = None
    pagina = app.pages["connect"]
    pagina.enable_demo()
    assert app.demo_mode is True
    assert attendi(app, lambda: app.device is not None)
    assert app.device.serial == "DEMO12345"


def test_avanti_funziona_solo_con_telefono_pronto(app):
    pagina = app.pages["connect"]
    pagina._avanti()
    assert app.current_page == "connect"
    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel", product="d")
    pagina._avanti()
    assert app.current_page == "select"
    assert pagina._polling is False


def test_sondaggio_attivo_al_primo_ingresso(app):
    pagina = app.pages["connect"]
    pagina.stop_polling()
    pagina.on_show()
    assert pagina._polling is True
    pagina.stop_polling()

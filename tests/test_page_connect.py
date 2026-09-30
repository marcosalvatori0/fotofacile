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


def test_l_aiuto_cita_trasferimento_file():
    from fotofacile.ui.page_connect import build_help_text_generico

    testo = build_help_text_generico()
    assert "Trasferimento file" in testo
    # deve venire PRIMA di qualunque accenno al Debug USB
    assert testo.index("Trasferimento file") < testo.index("Debug USB")


def test_senza_telefono_il_dettaglio_ricorda_trasferimento_file(app):
    pagina = app.pages["connect"]
    pagina._dispositivi_ricevuti([])
    assert "Trasferimento file" in pagina.dettaglio.cget("text")


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
    assert attendi(app, lambda: "non vedo ancora nessun telefono" in pagina.message.lower())
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
    pagina.bottone_avanti.state(["!disabled"])
    pagina._avanti()
    assert app.current_page == "select"
    assert pagina._polling is False


def test_sondaggio_attivo_al_primo_ingresso(app):
    pagina = app.pages["connect"]
    pagina.stop_polling()
    pagina.on_show()
    assert pagina._polling is True
    pagina.stop_polling()


# ── Passo 1 semplificato (C6) ─────────────────────────────────────────────
def _testi_della_pagina(pagina) -> str:
    testi = []
    for widget in pagina.winfo_children():
        if hasattr(widget, "cget") and "text" in widget.keys():
            testi.append(str(widget.cget("text")))
        for figlio in widget.winfo_children():
            if "text" in figlio.keys():
                testi.append(str(figlio.cget("text")))
    return " ".join(testi)


def test_le_tre_istruzioni_sono_sempre_visibili(app):
    testo = _testi_della_pagina(app.pages["connect"])
    assert "cavo USB" in testo and "sblocca" in testo.lower() and "Trasferimento file" in testo


def test_l_aiuto_grande_compare_solo_dopo_qualche_tentativo(app):
    pagina = app.pages["connect"]
    assert pagina._senza_telefono == 0
    for _ in range(pagina.SOGLIA_AIUTO - 1):
        pagina._dispositivi_ricevuti([])
    assert not pagina.aiuto_evidente.winfo_ismapped() and not pagina.aiuto_evidente.grid_info()
    pagina._dispositivi_ricevuti([])
    assert pagina.aiuto_evidente.grid_info()  # ora è visibile


def test_telefono_non_pronto_conta_come_senza_telefono(app):
    pagina = app.pages["connect"]
    non_pronto = DeviceInfo(serial="S1", state="unauthorized", model="Pixel", product="")
    for _ in range(pagina.SOGLIA_AIUTO):
        pagina._dispositivi_ricevuti([non_pronto])
    assert pagina.aiuto_evidente.grid_info()


def test_un_controllo_fallito_conta_come_senza_telefono(app, monkeypatch):
    from fotofacile.core.errors import FotoFacileError

    pagina = app.pages["connect"]
    monkeypatch.setattr(app, "cambia_collegamento", lambda: False)
    for _ in range(pagina.SOGLIA_AIUTO):
        pagina._controllo_fallito(FotoFacileError("Errore", hint="Prova il cavo."))
    assert pagina.aiuto_evidente.grid_info()


def test_trovato_il_telefono_l_aiuto_sparisce(app):
    pagina = app.pages["connect"]
    for _ in range(pagina.SOGLIA_AIUTO):
        pagina._dispositivi_ricevuti([])
    pagina._dispositivi_ricevuti([DeviceInfo(serial="S1", state="device", model="Pixel", product="")])
    assert pagina._senza_telefono == 0
    assert not pagina.aiuto_evidente.grid_info()


def test_i_pulsanti_del_testo_cambiano_la_scala(app, monkeypatch):
    chiamate = []
    monkeypatch.setattr(app, "cambia_scala", lambda d: chiamate.append(d) or True)
    pagina = app.pages["connect"]
    pagina.bottone_testo_piu.invoke()
    pagina.bottone_testo_meno.invoke()
    assert chiamate == [1, -1]


def test_invio_su_questo_passo_va_avanti_solo_col_telefono_pronto(app):
    pagina = app.pages["connect"]
    app.device = None
    pagina.azione_principale()
    assert app.current_page == "connect"


def test_invio_con_avanti_disabilitato_non_avanza(app):
    """Il tasto Invio non deve scavalcare il pulsante «Avanti» spento."""
    pagina = app.pages["connect"]
    app.device = DeviceInfo(serial="S1", state="device", model="Pixel", product="")
    pagina.bottone_avanti.state(["disabled"])
    pagina.azione_principale()
    assert app.current_page == "connect"
    pagina.bottone_avanti.state(["!disabled"])
    pagina.azione_principale()
    assert app.current_page == "select"


def test_i_messaggi_di_ricerca_non_restano_al_ritorno(app):
    """Tornando al passo 1 non deve restare l'avviso di prima."""
    pagina = app.pages["connect"]
    for _ in range(pagina.SOGLIA_AIUTO):
        pagina._dispositivi_ricevuti([])
    assert pagina.aiuto_evidente.grid_info() and "Non vedo" in pagina.message
    app.go_to("select")
    app.go_to("connect")
    app.stop_all_polling()
    assert pagina._senza_telefono == 0
    assert not pagina.aiuto_evidente.grid_info()
    assert "Non vedo" not in pagina.message
    assert pagina.dettaglio.cget("text") == ""


def test_il_messaggio_ha_un_simbolo_oltre_al_colore(app):
    pagina = app.pages["connect"]
    pagina.set_message("Tutto bene", tono="successo")
    assert pagina.indicatore.cget("text").startswith("✔")
    pagina.set_message("Attenzione", tono="avviso")
    assert pagina.indicatore.cget("text").startswith("⚠")
    pagina.set_message("Solo info")
    assert pagina.indicatore.cget("text") == "Solo info"
    assert pagina.message == "Solo info"


@pytest.mark.parametrize("scala", [1.0, 1.5])
def test_la_pagina_si_costruisce_a_ogni_scala(app, scala):
    from fotofacile.ui import theme

    theme.imposta_scala(scala)
    app.ricostruisci_pagine()
    app.stop_all_polling()
    pagina = app.pages["connect"]
    pagina.update_idletasks()
    assert pagina.bottone_testo_piu.winfo_exists()

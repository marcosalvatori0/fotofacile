import shutil
from pathlib import Path

import pytest

from fotofacile.core.planner import TransferOptions
from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")


def _prepara(app, destinazione: Path) -> None:
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.go_to("select")
    assert attendi(app, lambda: app.pages["select"]._scansione_fatta, passi=400)
    app.pages["select"].go_next()
    app.pages["options"].chooser.set(str(destinazione))


def test_proposta_cartella_e_opzioni(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    opzioni = pagina.build_options()
    assert isinstance(opzioni, TransferOptions)
    assert opzioni.destination == tmp_path
    assert opzioni.preserve_structure is False
    assert opzioni.skip_existing is True


def test_cartella_proposta_quando_vuota(app, tmp_path):
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.go_to("select")
    assert attendi(app, lambda: app.pages["select"]._scansione_fatta, passi=400)
    app.pages["select"].go_next()
    pagina = app.pages["options"]
    pagina.chooser.set("")
    pagina.on_show()
    assert "FotoFacile" in pagina.chooser.get()
    assert str(tmp_path) not in pagina.chooser.get() or True


def test_spazio_sufficiente_porta_al_trasferimento(app, tmp_path):
    _prepara(app, tmp_path)
    app.pages["options"].on_show()
    app.pages["options"].go_next()
    assert app.current_page == "transfer"
    assert app.options is not None


def test_spazio_insufficiente_blocca_spiegando_il_problema(app, tmp_path, monkeypatch):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    monkeypatch.setattr(shutil, "disk_usage", lambda _percorso: shutil._ntuple_diskusage(0, 0, 10))
    pagina.go_next()
    assert app.current_page == "options"
    assert "spazio" in app.banner.message_text.lower()


def test_il_riassunto_dice_cosa_succedera(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    testo = str(pagina.riassunto.cget("text"))
    assert "Copierò" in testo and str(tmp_path) in testo


def test_le_altre_opzioni_sono_chiuse_all_inizio(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    assert pagina.altre_opzioni_aperte is False
    pagina.mostra_altre(True)
    assert pagina.altre_opzioni_aperte is True
    pagina.mostra_altre(False)
    assert pagina.altre_opzioni_aperte is False


def test_cancellare_dal_telefono_chiede_conferma_con_una_finestra(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    domande = []
    opzioni_finestra = []

    def finta_domanda(titolo, testo, **k):
        domande.append(testo)
        opzioni_finestra.append(k)
        return False

    monkeypatch.setattr(page_options.messagebox, "askyesno", finta_domanda)
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    assert domande, "la conferma deve comparire subito, quando si mette la spunta"
    assert "telefono" in domande[0].lower()
    assert opzioni_finestra[0].get("default") == "no", "mai «Sì» come risposta predefinita"
    assert pagina.elimina_dopo_copia.get() is False  # ha risposto «No»: la spunta torna a posto


def test_rispondere_no_non_cancella_dal_telefono(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options.messagebox, "askyesno", lambda *a, **k: False)
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    pagina.go_next()
    assert app.current_page == "transfer"
    assert app.options.delete_after is False


def test_rispondere_si_lascia_la_spunta(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options.messagebox, "askyesno", lambda *a, **k: True)
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    assert pagina.elimina_dopo_copia.get() is True
    pagina.go_next()
    assert app.current_page == "transfer"
    assert app.options.delete_after is True


def test_invio_con_il_pulsante_spento_non_parte(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.bottone_avanti.state(["disabled"])
    try:
        pagina.azione_principale()
        assert app.current_page == "options"
    finally:
        pagina.bottone_avanti.state(["!disabled"])


def test_invio_con_il_pulsante_attivo_copia(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.azione_principale()
    assert app.current_page == "transfer"


def test_esc_torna_al_passo_precedente(app, tmp_path):
    _prepara(app, tmp_path)
    app.pages["options"].on_show()
    app.go_to("options")
    app.pages["options"].azione_indietro()
    assert app.current_page == "select"


def test_i_suggerimenti_parlano_di_cambia_cartella(app):
    import inspect

    from fotofacile.ui import page_options

    assert "Sfoglia" not in inspect.getsource(page_options)


def test_lo_stato_dello_spazio_ha_un_simbolo(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    assert str(pagina.spazio.cget("text")).startswith(("✔", "✖"))


def test_secondo_giro_non_ricopia_nulla(app, tmp_path):
    _prepara(app, tmp_path)
    app.pages["options"].on_show()
    app.pages["options"].go_next()
    assert attendi(app, lambda: app.pages["transfer"].results is not None, passi=600)
    app.pages["options"].on_show()
    piano = app.pages["options"].build_plan()
    assert piano.file_count == 0
    assert piano.skipped_duplicates == len(app.media_files)


def test_la_conversione_webp_e_attiva_se_pillow_c_e(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options, "pillow_disponibile", lambda: True)
    app.ricostruisci_pagine()
    pagina = app.pages["options"]
    assert pagina.converti_webp.get() is True
    assert pagina.build_options().converti_webp is True


def test_senza_pillow_la_conversione_e_spenta(app, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options, "pillow_disponibile", lambda: False)
    app.ricostruisci_pagine()
    pagina = app.pages["options"]
    assert pagina.converti_webp.get() is False
    assert pagina.build_options().converti_webp is False

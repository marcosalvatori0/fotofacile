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


def _con_file(app, file):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.core.scanner import group_folders

    app.device = DeviceInfo(serial="S1", state="device", model="Prova", product="")
    pagina = app.pages["select"]
    pagina._scansione_fatta = True  # niente ricerca automatica entrando nel passo
    pagina._files = list(file)
    pagina._folders = group_folders(pagina._files)
    pagina.rebuild_list(pagina._folders)
    return pagina


def _f(percorso, size=1000, mtime=1_700_000_000):
    from fotofacile.core.scanner import MediaFile

    return MediaFile(percorso, size=size, mtime=mtime, kind="photo")


def test_le_cartelle_mostrano_il_nome_comprensibile(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg"), _f("/sdcard/Pictures/WhatsApp Images/b.jpg")])
    testi = [str(w.cget("text")) for w in pagina.lista.winfo_children()]
    assert any("Foto e video scattati con il telefono" in t for t in testi)
    assert any("Foto ricevute su WhatsApp" in t for t in testi)
    assert not any("/sdcard" in t for t in testi)  # niente percorsi tecnici


def test_cartelle_con_lo_stesso_nome_si_distinguono(app):
    pagina = _con_file(app, [_f("/sdcard/Pictures/Vacanze/a.jpg"), _f("/sdcard/Download/Vacanze/b.jpg")])
    testi = sorted(str(w.cget("text")) for w in pagina.lista.winfo_children())
    assert len(set(t.split("  —  ")[0] for t in testi)) == 2


def test_sticker_e_miniature_sono_nascosti_di_default(app):
    pagina = _con_file(
        app,
        [
            _f("/sdcard/DCIM/Camera/a.jpg"),
            _f("/sdcard/DCIM/.thumbnails/t.jpg"),
            _f("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Stickers/s.webp"),
        ],
    )
    assert [f.name for f in pagina.selected_files()] == ["a.jpg"]
    pagina.mostra_rumore.set(True)
    pagina._ridisegna()
    assert sorted(f.name for f in pagina.selected_files()) == ["a.jpg", "s.webp", "t.jpg"]


def test_seleziona_tutto_e_nessuna(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg"), _f("/sdcard/Download/b.jpg")])
    pagina.seleziona_tutto(False)
    assert pagina.selected_files() == []
    assert "disabled" in str(pagina.bottone_avanti.state())
    pagina.seleziona_tutto(True)
    assert len(pagina.selected_files()) == 2


def test_il_periodo_sostituisce_la_data_scritta_a_mano(app, monkeypatch):
    from fotofacile.ui import page_select

    adesso = 1_700_000_000
    monkeypatch.setattr(page_select.time, "time", lambda: adesso)
    vecchia = _f("/sdcard/DCIM/Camera/vecchia.jpg", mtime=adesso - 200 * 86400)
    recente = _f("/sdcard/DCIM/Camera/recente.jpg", mtime=adesso - 5 * 86400)
    pagina = _con_file(app, [vecchia, recente])
    assert len(pagina.selected_files()) == 2
    pagina.periodo.set("Dell'ultimo mese")
    pagina._periodo_cambiato()
    assert [f.name for f in pagina.selected_files()] == ["recente.jpg"]
    pagina.periodo.set("Tutte le foto")
    pagina._periodo_cambiato()
    assert len(pagina.selected_files()) == 2


def test_esc_su_questo_passo_torna_indietro(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg")])
    app.go_to("select")
    pagina.azione_indietro()
    assert app.current_page == "connect"


def test_invio_con_avanti_spento_non_avanza(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg")])
    app.go_to("select")
    pagina.seleziona_tutto(False)
    assert pagina.bottone_avanti.instate(["disabled"])
    pagina.azione_principale()
    assert app.current_page == "select"


def test_invio_con_una_selezione_avanza(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg")])
    app.go_to("select")
    pagina.azione_principale()
    assert app.current_page == "options"


def test_il_menu_del_periodo_ha_le_voci_previste():
    from fotofacile.ui.page_select import PERIODI

    assert [nome for nome, _ in PERIODI] == [
        "Tutte le foto",
        "Dell'ultimo mese",
        "Degli ultimi 3 mesi",
        "Dell'ultimo anno",
    ]


def test_mostrare_i_nascosti_non_cancella_le_spunte_tolte(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg"), _f("/sdcard/Download/b.jpg")])
    pagina.folder_vars["/sdcard/Download"].set(False)
    pagina.mostra_rumore.set(True)
    pagina._ridisegna()
    assert [f.name for f in pagina.selected_files()] == ["a.jpg"]


def test_la_ricerca_riparte_anche_se_l_interruzione_era_rimasta_accesa(app):
    """Un «Interrompi» precedente lasciava `cancel_event` acceso e la ricerca nasceva già annullata."""
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.cancel_event.set()
    pagina = app.pages["select"]
    avviate = []
    app.run_task = lambda gen, **k: avviate.append(gen)
    try:
        pagina.start_scan()
    finally:
        del app.run_task
    assert avviate, "la ricerca doveva partire"
    assert not app.cancel_event.is_set()

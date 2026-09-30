import pytest

from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")


def _fino_al_trasferimento(app, destinazione, intervallo: float = 0.0) -> None:
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.go_to("select")
    assert attendi(app, lambda: app.pages["select"]._scansione_fatta, passi=400)
    app.pages["select"].go_next()
    pagina = app.pages["options"]
    pagina.chooser.set(str(destinazione))
    pagina.on_show()
    app.remote.intervallo = intervallo  # telefono finto più lento, per poter annullare a metà
    pagina.go_next()
    assert app.current_page == "transfer"


def test_copia_completa_e_resoconto(app, tmp_path):
    _fino_al_trasferimento(app, tmp_path)
    pagina = app.pages["transfer"]
    assert attendi(app, lambda: pagina.results is not None, passi=800)
    risultati = pagina.results
    assert risultati is not None
    assert risultati.cancelled is False
    assert risultati.copied
    assert risultati.failed == []
    for percorso in risultati.copied:
        assert percorso.is_file() and percorso.stat().st_size > 0
    assert not list(tmp_path.rglob("*.part"))
    assert "Ho copiato" in pagina.riepilogo_testo()
    assert "Copiate" in pagina.report_text
    assert pagina.bottone_apri.instate(["!disabled"])


def test_annullamento_lascia_il_disco_pulito(app, tmp_path):
    _fino_al_trasferimento(app, tmp_path, intervallo=0.02)
    pagina = app.pages["transfer"]
    assert attendi(app, lambda: pagina.barra_totale["value"] > 0, passi=600), "la copia non è mai partita"
    pagina.cancel()
    assert attendi(app, lambda: pagina.results is not None, passi=1500)
    assert pagina.results.cancelled is True
    assert pagina.results.copied, "qualcosa era già stato copiato: l'annullamento è a metà lavoro"
    assert not list(tmp_path.rglob("*.part"))
    assert "interrotto" in pagina.riepilogo_testo().lower()


def test_resoconto_salvabile(app, tmp_path):
    _fino_al_trasferimento(app, tmp_path)
    pagina = app.pages["transfer"]
    assert attendi(app, lambda: pagina.results is not None, passi=800)
    pagina.save_report()
    resoconti = list(tmp_path.glob("resoconto-fotofacile-*.txt"))
    assert resoconti and "Copiate" in resoconti[0].read_text()


def test_seconda_copia_non_ricopia_nulla(app, tmp_path):
    _fino_al_trasferimento(app, tmp_path)
    pagina = app.pages["transfer"]
    assert attendi(app, lambda: pagina.results is not None, passi=800)
    primo = len(pagina.results.copied)
    assert primo > 0
    pagina.started_at = 0.0
    pagina.results = None
    pagina.start_transfer()
    assert attendi(app, lambda: pagina.results is not None, passi=400)
    assert pagina.results.copied == []
    assert pagina.results.skipped == primo


# ── C9: percentuale grande, tempo a parole, «Fatto!» chiaro ───────────────────────────────
def test_la_percentuale_grande_segue_l_avanzamento(app):
    from fotofacile.core.transfer import Progress

    pagina = app.pages["transfer"]
    pagina.update_progress(Progress(total_files=4, done_files=1, bytes_done=37, bytes_total=100))
    assert pagina.percentuale.cget("text") == "37 %"


def test_il_tempo_residuo_e_scritto_a_parole(app):
    from fotofacile.core.transfer import Progress

    pagina = app.pages["transfer"]
    pagina.update_progress(
        Progress(total_files=4, done_files=1, bytes_done=10, bytes_total=100, speed_bps=1.0, eta_seconds=125)
    )
    assert "circa 2 minuti" in pagina.dettagli.cget("text")


def test_a_fine_copia_c_e_un_fatto_chiaro_e_gli_avvisi_si_vedono(app):
    from pathlib import Path

    from fotofacile.core.transfer import TransferResults

    pagina = app.pages["transfer"]
    esiti = TransferResults(
        copied=[Path("/x/a.jpg"), Path("/x/b.jpg")],
        bytes_copied=2048,
        elapsed=3.0,
        warnings=["Non sono riuscito a togliere a.jpg dal telefono: bloccato."],
    )
    pagina.show_summary(esiti)
    assert pagina.riepilogo.cget("text").startswith("✔")
    assert "2" in pagina.riepilogo.cget("text")
    assert "a.jpg" in pagina.riepilogo_errori.cget("text")  # l'avviso non va perso
    assert pagina.percentuale.cget("text") == "100 %"


def test_il_riepilogo_usa_il_singolare_per_un_secondo(app):
    from fotofacile.core.transfer import TransferResults

    pagina = app.pages["transfer"]
    pagina.show_summary(TransferResults(elapsed=1.0))
    testo = pagina.riepilogo.cget("text")
    assert "in 1 secondo." in testo
    assert "1 secondi" not in testo
    pagina.show_summary(TransferResults(elapsed=75.0))
    assert "in 1 minuto e 15 secondi." in pagina.riepilogo.cget("text")


def test_copia_interrotta_o_con_errori_comincia_con_l_avviso(app):
    from pathlib import Path

    from fotofacile.core.transfer import TransferResults

    pagina = app.pages["transfer"]
    pagina.show_summary(TransferResults(cancelled=True))
    assert pagina.riepilogo.cget("text").startswith("⚠")
    assert pagina.percentuale.cget("text") != "100 %"
    pagina.show_summary(TransferResults(failed=[(_media("x.jpg"), "errore")]))
    assert pagina.riepilogo.cget("text").startswith("⚠")
    assert "x.jpg" in pagina.riepilogo_errori.cget("text")


def _media(nome):
    from fotofacile.core.scanner import MediaFile

    return MediaFile(remote_path=f"/sdcard/DCIM/{nome}", size=1, mtime=0, kind="photo")


def test_l_apertura_della_cartella_e_il_pulsante_principale_a_fine_copia(app, monkeypatch, tmp_path):
    from fotofacile.core.planner import TransferOptions
    from fotofacile.core.transfer import TransferResults
    from fotofacile.ui import page_transfer

    aperte = []
    monkeypatch.setattr(page_transfer, "open_in_file_manager", lambda p: aperte.append(p))
    app.options = TransferOptions(destination=tmp_path)
    pagina = app.pages["transfer"]
    pagina.azione_principale()  # durante la copia non fa niente
    assert aperte == []
    pagina.show_summary(TransferResults())
    pagina.azione_principale()
    assert aperte == [tmp_path]


def test_i_testi_della_copia_non_sono_sotto_i_14_punti(app):
    from tkinter import font as tkfont

    pagina = app.pages["transfer"]
    for widget in (pagina.etichetta_file, pagina.dettagli, pagina.riepilogo_errori):
        assert tkfont.Font(font=widget.cget("font")).actual("size") >= 14


# ── C9: niente vicolo cieco dopo un errore, niente doppia copia ───────────────────────────
def _pronta_a_copiare(app, tmp_path, monkeypatch):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.core.planner import TransferOptions

    app.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    app.options = TransferOptions(destination=tmp_path)
    app.media_files = []
    avviate = []
    monkeypatch.setattr(app, "run_task", lambda gen, **k: (avviate.append(gen), setattr(app, "_task", gen)))
    return avviate


def test_dopo_un_errore_si_puo_tornare_alle_opzioni(app, tmp_path, monkeypatch):
    from fotofacile.core.errors import FotoFacileError

    _pronta_a_copiare(app, tmp_path, monkeypatch)
    app.go_to("transfer")
    pagina = app.pages["transfer"]
    assert app.current_page == "transfer"
    pagina.azione_indietro()  # durante la copia non si torna indietro
    assert app.current_page == "transfer"
    pagina.show_error(FotoFacileError("Il telefono si è scollegato.", "Ricollegalo."))
    assert pagina.riepilogo.cget("text").startswith("✖")
    assert pagina.bottone_indietro.winfo_ismapped() or pagina.bottone_indietro.winfo_manager()
    pagina.azione_indietro()
    assert app.current_page == "options"


def test_errore_di_lettura_della_destinazione_non_e_un_vicolo_cieco(app, tmp_path, monkeypatch):
    avviate = _pronta_a_copiare(app, tmp_path, monkeypatch)
    pagina = app.pages["transfer"]
    monkeypatch.setattr(pagina, "_pianifica", lambda seriale: (_ for _ in ()).throw(OSError("no")))
    app.go_to("transfer")
    assert avviate == []
    pagina.azione_indietro()
    assert app.current_page == "options"


def test_dopo_un_errore_si_puo_ripartire_da_zero(app, tmp_path, monkeypatch):
    from fotofacile.core.errors import FotoFacileError

    avviate = _pronta_a_copiare(app, tmp_path, monkeypatch)
    app.go_to("transfer")
    pagina = app.pages["transfer"]
    pagina.show_error(FotoFacileError("Errore.", "Riprova."))
    pagina.azione_indietro()
    app._task = None
    app.go_to("transfer")
    assert len(avviate) == 2
    assert pagina.riepilogo.cget("text") == ""
    assert pagina.percentuale.cget("text") == "0 %"
    pagina.azione_indietro()  # di nuovo in copia: niente
    assert app.current_page == "transfer"


def test_non_parte_una_seconda_copia_mentre_la_prima_e_in_corso(app, tmp_path, monkeypatch):
    avviate = _pronta_a_copiare(app, tmp_path, monkeypatch)
    app.go_to("transfer")
    pagina = app.pages["transfer"]
    assert len(avviate) == 1
    pagina.start_transfer()
    pagina.on_show()
    assert len(avviate) == 1


def test_dopo_la_fine_della_copia_se_ne_puo_far_partire_un_altra(app, tmp_path, monkeypatch):
    from fotofacile.core.transfer import TransferResults

    avviate = _pronta_a_copiare(app, tmp_path, monkeypatch)
    app.go_to("transfer")
    pagina = app.pages["transfer"]
    app._task = None
    pagina.show_summary(TransferResults())
    pagina.start_transfer()
    assert len(avviate) == 2


def test_se_il_lavoro_si_ferma_a_meta_una_nuova_copia_puo_partire(app, tmp_path, monkeypatch):
    avviate = _pronta_a_copiare(app, tmp_path, monkeypatch)
    app.go_to("transfer")
    app._task = None  # per esempio un errore imprevisto: il flag non deve restare bloccato
    app.pages["transfer"].start_transfer()
    assert len(avviate) == 2


def test_dopo_una_copia_interrotta_si_puo_tornare_indietro(app):
    """Con «Interrompi» non si resta più con il solo «Chiudi»."""
    from fotofacile.core.transfer import TransferResults

    pagina = app.pages["transfer"]
    pagina.show_summary(TransferResults(cancelled=True))
    assert pagina.bottone_indietro.winfo_manager() == "grid"
    app.go_to("transfer") if False else None
    app.current_page = "transfer"
    pagina.azione_indietro()
    assert app.current_page == "options"
    # una copia finita bene non ha il pulsante «Indietro»
    pagina._riparti_da_capo()
    pagina.show_summary(TransferResults())
    assert pagina.bottone_indietro.winfo_manager() == ""

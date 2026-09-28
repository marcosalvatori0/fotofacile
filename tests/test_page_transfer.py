import pytest

from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")


def _fino_al_trasferimento(app, destinazione) -> None:
    app.go_to("select")
    assert attendi(app, lambda: app.pages["select"]._scansione_fatta, passi=400)
    app.pages["select"].go_next()
    pagina = app.pages["options"]
    pagina.chooser.set(str(destinazione))
    pagina.on_show()
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
    assert "Copiate" in pagina.riepilogo_testo()
    assert pagina.bottone_apri.instate(["!disabled"])


def test_annullamento_lascia_il_disco_pulito(app, tmp_path):
    _fino_al_trasferimento(app, tmp_path)
    pagina = app.pages["transfer"]
    for _ in range(400):
        app.update()
        if pagina.barra_totale["value"] > 0:
            pagina.cancel()
            break
    assert attendi(app, lambda: pagina.results is not None, passi=800)
    assert pagina.results.cancelled is True
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

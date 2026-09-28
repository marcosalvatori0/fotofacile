import shutil
from pathlib import Path

import pytest

from fotofacile.core.planner import TransferOptions
from fotofacile.ui.widgets import tk_available
from tests.aiuto import attendi

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")


def _prepara(app, destinazione: Path) -> None:
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
    assert opzioni.preserve_structure is True
    assert opzioni.skip_existing is True


def test_cartella_proposta_quando_vuota(app, tmp_path):
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


def test_cancellazione_dal_telefono_richiede_conferma(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    pagina.go_next()
    assert app.current_page == "options"
    assert "conferma" in app.banner.message_text.lower()
    pagina.go_next()
    assert app.current_page == "transfer"
    assert app.options.delete_after is True


def test_secondo_giro_non_ricopia_nulla(app, tmp_path):
    _prepara(app, tmp_path)
    app.pages["options"].on_show()
    app.pages["options"].go_next()
    assert attendi(app, lambda: app.pages["transfer"].results is not None, passi=600)
    app.pages["options"].on_show()
    piano = app.pages["options"].build_plan()
    assert piano.file_count == 0
    assert piano.skipped_duplicates == len(app.media_files)

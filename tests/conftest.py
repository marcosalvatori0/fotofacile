"""Impostazioni comuni dei test.

Su macOS creare e distruggere più finestre Tk nello stesso processo fa crashare Tk:
per questo la suite usa **una sola** finestra, creata all'inizio e chiusa alla fine,
con lo stato azzerato fra un test e l'altro.
"""

from __future__ import annotations

import os
import tempfile
import threading

import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.history import History
from fotofacile.ui.widgets import tk_available


@pytest.fixture(scope="session")
def casa_temporanea():
    """Cartella utente finta: i test non devono mai toccare i file reali dell'utente."""
    with tempfile.TemporaryDirectory() as cartella:
        precedenti = {chiave: os.environ.get(chiave) for chiave in ("HOME", "USERPROFILE")}
        os.environ["HOME"] = cartella
        os.environ["USERPROFILE"] = cartella
        yield cartella
        for chiave, valore in precedenti.items():
            if valore is None:
                os.environ.pop(chiave, None)
            else:
                os.environ[chiave] = valore


@pytest.fixture(scope="session")
def finestra_condivisa(casa_temporanea):
    if not tk_available():
        pytest.skip("serve un ambiente grafico", allow_module_level=False)
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=54), demo_mode=True)
    applicazione.withdraw()
    applicazione.stop_all_polling()
    yield applicazione
    applicazione.destroy()


def azzera(applicazione, tmp_path) -> None:
    """Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)."""
    applicazione.stop_all_polling()
    applicazione.backend = DemoAdbBackend(file_count=54)
    applicazione.demo_mode = True
    applicazione.device = None
    applicazione.media_files = []
    applicazione.selected_folders = []
    applicazione.options = None
    applicazione.results = None
    applicazione.cancel_event = threading.Event()
    applicazione._history = History(tmp_path / "history.json")
    applicazione._history.load()
    pagina = applicazione.pages["connect"]
    pagina._polling = False
    pagina._in_corso = False
    pagina.bottone_avanti.state(["disabled"])
    pagina.set_message("Collega il telefono con il cavo e sbloccalo.")
    pagina.tkraise()
    applicazione.current_page = "connect"
    applicazione.step_indicator.set_step(0)
    applicazione.banner.hide()
    applicazione.log_pane.clear()


@pytest.fixture
def app(finestra_condivisa, tmp_path):
    """La finestra condivisa, azzerata prima e dopo ogni test."""
    azzera(finestra_condivisa, tmp_path)
    yield finestra_condivisa
    azzera(finestra_condivisa, tmp_path)


@pytest.fixture
def root(finestra_condivisa):
    """Contenitore usa e getta per i test dei singoli componenti grafici.

    È una finestra figlia: così non viene creata una seconda finestra principale
    (su macOS è la causa di crash) e non viene toccata la finestra dell'app.
    """
    import tkinter as tk

    contenitore = tk.Toplevel(finestra_condivisa)
    contenitore.withdraw()
    yield contenitore
    contenitore.destroy()

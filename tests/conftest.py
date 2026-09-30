"""Impostazioni comuni dei test.

Su macOS creare e distruggere più finestre Tk nello stesso processo fa crashare Tk:
per questo la suite usa **una sola** finestra, creata all'inizio e chiusa alla fine,
con lo stato azzerato fra un test e l'altro.
"""

from __future__ import annotations

import os
import sys
import tempfile
import threading

import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.history import History
from fotofacile.core.planner import TransferPlan
from fotofacile.ui.widgets import tk_available


@pytest.fixture(autouse=True)
def scala_testo_normale():
    """La scala del testo è globale: ogni test riparte dalla dimensione normale (1.0)."""
    from fotofacile.ui import theme

    theme.imposta_scala(1.0)
    yield
    theme.imposta_scala(1.0)


@pytest.fixture(scope="session")
def casa_temporanea():
    """Cartella utente finta: i test non devono mai toccare i file reali dell'utente."""
    with tempfile.TemporaryDirectory() as cartella:
        chiavi = ("HOME", "USERPROFILE")
        precedenti = {chiave: os.environ.get(chiave) for chiave in chiavi}
        os.environ["HOME"] = cartella
        if sys.platform == "win32":  # su Windows la cartella utente è USERPROFILE
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

    applicazione = App(backend=DemoAdbBackend(file_count=54), demo_mode=True, scala=1.0)
    applicazione.withdraw()
    applicazione.stop_all_polling()
    yield applicazione
    applicazione.destroy()


def azzera(applicazione, tmp_path) -> None:
    """Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)."""
    applicazione.stop_all_polling()
    applicazione._usa_backend(DemoAdbBackend(file_count=12, delay=0.0))
    applicazione.demo_mode = True
    applicazione.device = None
    applicazione.media_files = []
    applicazione.selected_folders = []
    applicazione.options = None
    applicazione.results = None
    applicazione.cancel_event = threading.Event()
    applicazione._history = History(tmp_path / "history.json")
    applicazione._history.load()
    applicazione.annulla_task()
    applicazione.cancel_event.clear()
    applicazione.ricostruisci_pagine()
    # `ricostruisci_pagine` apre il passo 1, che avvia subito un controllo del telefono:
    # lo si ferma qui, così ogni test parte da uno stato identico e prevedibile.
    applicazione.stop_all_polling()
    applicazione.annulla_task()

    seleziona = applicazione.pages["select"]
    seleziona._files = []
    seleziona._folders = []
    seleziona.folder_vars.clear()
    seleziona._scansione_fatta = False
    seleziona._scansione_in_corso = False
    seleziona.data_minima.set("")
    seleziona.periodo.set("Tutte le foto")
    seleziona.mostra_rumore.set(False)
    seleziona.sto_scegliendo_video.set(True)
    seleziona.riepilogo.configure(text="")
    seleziona.bottone_avanti.state(["disabled"])
    seleziona2 = applicazione.pages["select"].lista
    for figlio in seleziona2.winfo_children():
        figlio.destroy()

    opzioni = applicazione.pages["options"]
    opzioni.chooser.set("")
    opzioni.mantieni_cartelle.set(False)
    opzioni.salta_gia_copiate.set(True)
    opzioni.elimina_dopo_copia.set(False)
    opzioni.converti_webp.set(opzioni._conversione_possibile)
    opzioni._conferma_eliminazione = False
    opzioni.avviso_eliminazione.grid_remove()

    trasferimento = applicazione.pages["transfer"]
    trasferimento.results = None
    trasferimento.report_text = ""
    trasferimento.last_plan = TransferPlan()
    trasferimento.barra_totale.configure(value=0)
    trasferimento.barra_file.configure(value=0)
    trasferimento.riepilogo.configure(text="")
    trasferimento.riepilogo_errori.configure(text="")
    for bottone in (trasferimento.bottone_apri, trasferimento.bottone_salva, trasferimento.bottone_chiudi):
        bottone.state(["disabled"])

    pagina = applicazione.pages["connect"]
    pagina._polling = False
    pagina.bottone_avanti.state(["disabled"])
    pagina.set_message("Collega il telefono con il cavo e sbloccalo.")
    pagina.tkraise()
    applicazione.current_page = "connect"
    applicazione.step_indicator.set_step(0)
    applicazione.banner.hide()
    applicazione.log_pane.clear()
    applicazione.mostra_dettagli(False)


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

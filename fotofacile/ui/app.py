"""Finestra principale: navigazione fra i passi, lavoro in background e registro.

Regola importante: **nessuna** operazione lunga gira sul thread dell'interfaccia.
I thread di lavoro mettono i risultati in una coda che viene svuotata da
:meth:`App.pump_events`, l'unico punto in cui la grafica viene aggiornata.
"""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from ..core.adb import AdbBackend, RealAdbBackend, find_adb
from ..core.demo import DemoAdbBackend
from ..core.errors import FotoFacileError
from ..core.history import History
from .theme import apply_theme
from .widgets import Banner, LogPane, StepIndicator

PASSI = ("Collega il telefono", "Scegli le foto", "Destinazione", "Copia")
ORDINE = ("connect", "select", "options", "transfer")


class App(tk.Tk):
    """Contenitore della procedura guidata: crea le pagine e coordina il lavoro."""

    def __init__(
        self,
        backend: AdbBackend | None = None,
        demo_mode: bool = False,
        adb_path: str | None = None,
    ) -> None:
        super().__init__()
        self.title("FotoFacile — copia le foto dal telefono al computer")
        self.geometry("1000x760")
        self.minsize(900, 680)
        apply_theme(self)

        self.demo_mode = demo_mode
        self.adb_path = adb_path or find_adb()
        self.backend: AdbBackend | None = backend or (
            DemoAdbBackend() if demo_mode else self._crea_backend()
        )
        self.device = None
        self.media_files: list = []
        self.selected_folders: list[str] = []
        self.options = None
        self.results = None
        self.cancel_event = threading.Event()
        self.events: queue.Queue = queue.Queue()
        self.current_page = ""
        self._threads: list[threading.Thread] = []
        self._history = History()
        self._history.load()

        self.step_indicator = StepIndicator(self, PASSI)
        self.step_indicator.grid(row=0, column=0, sticky="w", padx=18, pady=(14, 4))
        self.banner = Banner(self)
        self.banner.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 8))
        self.banner.hide()

        self.container = ttk.Frame(self)
        self.container.grid(row=2, column=0, sticky="nsew", padx=18, pady=6)
        self.log_pane = LogPane(self, height=7)
        self.log_pane.grid(row=3, column=0, sticky="nsew", padx=18, pady=(6, 14))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1, minsize=120)

        self.pages: dict[str, ttk.Frame] = {}
        self._costruisci_pagine()

        self.protocol("WM_DELETE_WINDOW", self._chiusura)
        self.go_to("connect")
        self.after(50, self.pump_events)

    # ── costruzione ───────────────────────────────────────────────────────
    def _crea_backend(self) -> AdbBackend | None:
        if not self.adb_path:
            return None
        return RealAdbBackend(self.adb_path)

    def _costruisci_pagine(self) -> None:
        from .page_connect import ConnectPage
        from .page_options import OptionsPage
        from .page_select import SelectPage
        from .page_transfer import TransferPage

        self.register_page("connect", ConnectPage(self))
        self.register_page("select", SelectPage(self))
        self.register_page("options", OptionsPage(self))
        self.register_page("transfer", TransferPage(self))

    def register_page(self, key: str, page: ttk.Frame) -> None:
        self.pages[key] = page
        page.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    # ── navigazione ───────────────────────────────────────────────────────
    def go_to(self, key: str) -> None:
        if key == "prev":
            key = ORDINE[max(0, ORDINE.index(self.current_page) - 1)]
        elif key == "next":
            key = ORDINE[min(len(ORDINE) - 1, ORDINE.index(self.current_page) + 1)]
        pagina = self.pages[key]
        pagina.tkraise()
        pagina.on_show()
        self.current_page = key
        self.step_indicator.set_step(ORDINE.index(key))
        self.banner.hide()

    def stop_all_polling(self) -> None:
        """Ferma i controlli periodici (usato alla chiusura e nei test)."""
        for pagina in self.pages.values():
            ferma = getattr(pagina, "stop_polling", None)
            if callable(ferma):
                ferma()

    # ── messaggi e registro ───────────────────────────────────────────────
    def log(self, testo: str) -> None:
        self.log_pane.append(testo)

    def set_status(self, text: str, hint: str = "", kind: str = "info") -> None:
        self.banner.show(text, hint=hint, kind=kind)

    def history(self) -> History:
        """Cronologia dei file già copiati, caricata una volta sola."""
        return self._history

    # ── lavoro in background ──────────────────────────────────────────────
    def run_async(
        self,
        funzione: Callable[[], Any],
        on_done: Callable[[Any], None] | None = None,
        on_error: Callable[[FotoFacileError], None] | None = None,
    ) -> None:
        """Esegue ``funzione`` in un thread e consegna l'esito al thread della grafica."""

        def lavora() -> None:
            try:
                risultato = funzione()
            except FotoFacileError as errore:
                self.events.put(("errore", errore, on_error))
            except Exception as errore:  # rete di sicurezza: l'app non deve mai chiudersi
                self.events.put(("imprevisto", errore, on_error))
            else:
                self.events.put(("fatto", risultato, on_done))

        filo = threading.Thread(target=lavora, daemon=True)
        self._threads.append(filo)
        filo.start()

    def pump_events(self) -> None:
        """Svuota la coda dei risultati; è l'unico punto in cui la grafica cambia."""
        while True:
            try:
                tipo, dato, callback = self.events.get_nowait()
            except queue.Empty:
                break
            if tipo == "fatto":
                if callback is not None:
                    callback(dato)
            elif tipo == "errore":
                if callback is not None:
                    callback(dato)
                else:
                    self.set_status(dato.message, hint=dato.hint, kind="errore")
                    self.log(f"Errore: {dato.message} {dato.hint}".strip())
            else:
                self.set_status(
                    "Qualcosa non ha funzionato come previsto.",
                    hint="Riprova; se il problema resta, salva il registro e contatta il supporto.",
                    kind="errore",
                )
                self.log(f"Errore imprevisto: {dato!r}")
        self.after(50, self.pump_events)

    # ── chiusura ──────────────────────────────────────────────────────────
    def _chiusura(self) -> None:
        self.stop_all_polling()
        self.cancel_event.set()
        self.destroy()

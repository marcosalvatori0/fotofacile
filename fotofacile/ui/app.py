"""Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.

Regola importante: **niente thread**. Le operazioni lunghe (ricerca, copia, download) sono
generatori che cedono il controllo alla finestra fra un passo e l'altro: la grafica resta
reattiva e il programma non dipende dalla sicurezza dei thread di Tk, che su alcune
combinazioni (macOS con Tk 9) blocca l'intera applicazione.
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Generator

from ..core.adb import RealAdbBackend, find_adb
from ..core.adb_passi import AdbAPassi, AdbDemoAPassi
from ..core.demo import DemoAdbBackend
from ..core.errors import FotoFacileError
from ..core.history import History
from .theme import apply_theme
from .widgets import Banner, LogPane, StepIndicator

PASSI = ("Collega il telefono", "Scegli le foto", "Destinazione", "Copia")
ORDINE = ("connect", "select", "options", "transfer")


class App(tk.Tk):
    """Contenitore della procedura guidata: crea le pagine e coordina il lavoro."""

    INTERVALLO_PASSI = 0.02  # secondi fra due passi (abbassato nei test)

    def __init__(
        self,
        backend: Any | None = None,
        demo_mode: bool = False,
        adb_path: str | None = None,
    ) -> None:
        super().__init__()
        self.title("FotoFacile — copia le foto dal telefono al computer")
        self.geometry("1020x780")
        self.minsize(920, 700)
        apply_theme(self)

        self.adb_path = adb_path or find_adb()
        self.backend: Any = None
        self.remote: Any = None
        self.demo_mode = False

        self.device = None
        self.media_files: list = []
        self.selected_folders: list[str] = []
        self.options = None
        self.results = None
        self.cancel_event = threading.Event()
        self.current_page = ""
        self._task: Generator | None = None
        self._epoca_task = 0
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
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=1, minsize=110)

        if backend is not None:
            self._usa_backend(backend)
        elif demo_mode:
            self.attiva_demo()
        elif self.adb_path:
            self._usa_adb(self.adb_path)

        self.pages: dict[str, ttk.Frame] = {}
        self._costruisci_pagine()

        self.protocol("WM_DELETE_WINDOW", self._chiusura)
        self.go_to("connect")

    # ── backend ───────────────────────────────────────────────────────────
    def _usa_backend(self, backend) -> None:
        """Usa un backend in memoria (test) o il telefono demo."""
        self.backend = backend
        self.remote = AdbDemoAPassi(backend, intervallo=self.INTERVALLO_PASSI)
        self.demo_mode = True

    def _usa_adb(self, percorso: str) -> None:
        self.adb_path = percorso
        self.backend = RealAdbBackend(percorso)
        self.remote = AdbAPassi(percorso, intervallo=self.INTERVALLO_PASSI)
        self.demo_mode = False

    def attiva_demo(self) -> None:
        """Passa al telefono finto: permette di provare tutto senza dispositivo collegato."""
        self._usa_backend(DemoAdbBackend(file_count=54))
        self.log("Modalità demo attiva: verrà usato un telefono finto.")

    def usa_telefono_vero(self, percorso: str | None = None) -> bool:
        """Torna al telefono vero, se il componente di collegamento è disponibile."""
        percorso = percorso or self.adb_path or find_adb()
        if not percorso:
            return False
        self._usa_adb(percorso)
        self.log(f"Collegamento pronto: {percorso}")
        return True

    @property
    def component_mancante(self) -> bool:
        return self.remote is None and not self.demo_mode

    # ── costruzione e navigazione ─────────────────────────────────────────
    def _costruisci_pagine(self) -> None:
        from .page_connect import ConnectPage
        from .page_options import OptionsPage
        from .page_select import SelectPage
        from .page_transfer import TransferPage

        self.register_page("connect", ConnectPage(self))
        self.register_page("select", SelectPage(self))
        self.register_page("options", OptionsPage(self))
        self.register_page("transfer", TransferPage(self))

    def ricostruisci_pagine(self) -> None:
        """Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma."""
        self.stop_all_polling()
        self.annulla_task()
        for pagina in self.pages.values():
            pagina.destroy()
        self.pages.clear()
        self.current_page = ""
        self._costruisci_pagine()

    def register_page(self, key: str, page: ttk.Frame) -> None:
        self.pages[key] = page
        page.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

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

    # ── lavoro a passi (nessun thread) ────────────────────────────────────
    def run_task(
        self,
        generatore: Generator[float, None, Any],
        on_done: Callable[[Any], None] | None = None,
        on_error: Callable[[FotoFacileError], None] | None = None,
        intervallo: float | None = None,
    ) -> None:
        """Porta avanti un generatore a passi dentro il ciclo della grafica."""
        attesa = self.INTERVALLO_PASSI if intervallo is None else intervallo
        self._epoca_task += 1
        epoca = self._epoca_task
        self._task = generatore

        def tick() -> None:
            if epoca != self._epoca_task:
                return  # questo lavoro è stato abbandonato: non deve più toccare niente
            try:
                pausa = next(generatore)
            except StopIteration as fine:
                self._task = None
                if on_done is not None:
                    self._esegui_callback(on_done, fine.value)
                return
            except FotoFacileError as errore:
                self._task = None
                if on_error is not None:
                    self._esegui_callback(on_error, errore)
                else:
                    self.set_status(errore.message, hint=errore.hint, kind="errore")
                    self.log(f"Errore: {errore.message} {errore.hint}".strip())
                return
            except Exception as errore:  # rete di sicurezza: l'app non deve mai chiudersi
                self._task = None
                self.set_status(
                    "Qualcosa non ha funzionato come previsto.",
                    hint="Riprova; se il problema resta, salva il registro delle operazioni.",
                    kind="errore",
                )
                self.log(f"Errore imprevisto: {errore!r}")
                return
            ritardo = pausa if isinstance(pausa, (int, float)) else attesa
            self.after(max(0, int(ritardo * 1000)), tick)

        self.after(1, tick)

    def annulla_task(self) -> None:
        """Ferma il lavoro in corso (l'utente ha cambiato idea o è tornato indietro).

        Il generatore viene chiuso, così la sua pulizia (per esempio la rimozione dei file
        ``.part``) viene eseguita subito.
        """
        self._epoca_task += 1
        generatore, self._task = self._task, None
        if generatore is not None:
            chiusura = getattr(generatore, "close", None)
            if chiusura is not None:
                try:
                    chiusura()
                except Exception as errore:  # pragma: no cover - pulizia difensiva
                    self.log(f"Problema durante l'interruzione: {errore!r}")

    def _esegui_callback(self, callback: Callable[[Any], None], valore: Any) -> None:
        """Esegue il seguito di un task senza che un errore di grafica fermi il programma."""
        try:
            callback(valore)
        except Exception as errore:  # pragma: no cover - rete di sicurezza
            self.set_status(
                "Ho finito, ma qualcosa non si è aggiornato come doveva.",
                hint="Riprova; se il problema resta, salva il registro delle operazioni.",
                kind="errore",
            )
            self.log(f"Errore di grafica: {errore!r}")

    @property
    def task_in_corso(self) -> bool:
        return self._task is not None

    def pump_events(self) -> None:
        """Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare."""
        self.update_idletasks()

    # ── chiusura ──────────────────────────────────────────────────────────
    def _chiusura(self) -> None:
        self.stop_all_polling()
        self.cancel_event.set()
        self.destroy()

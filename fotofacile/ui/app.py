"""Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.

Regola importante: **niente thread**. Le operazioni lunghe (ricerca, copia, download) sono
generatori che cedono il controllo alla finestra fra un passo e l'altro: la grafica resta
reattiva e il programma non dipende dalla sicurezza dei thread di Tk, che su alcune
combinazioni (macOS con Tk 9) blocca l'intera applicazione.
"""

from __future__ import annotations

import threading
import tkinter as tk
import traceback
from tkinter import messagebox, ttk
from typing import Any, Callable, Generator

from ..core.adb import RealAdbBackend, find_adb
from ..core.errors import FotoFacileError
from ..core.history import History
from ..core.trasporto import Trasporto, TrasportoAdb, TrasportoDemo, trasporti_disponibili
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
        self.trasporto: Trasporto | None = None
        self.demo_mode = False
        #: Nomi dei modi di collegamento già provati senza successo (evita di riprovare
        #: sempre lo stesso e di restare in un ciclo infinito).
        self._gia_provati: set[str] = set()

        self.device = None
        self.media_files: list = []
        self.selected_folders: list[str] = []
        self.options = None
        self.results = None
        self.cancel_event = threading.Event()
        self.current_page = ""
        self._task: Generator | None = None
        self._epoca_task = 0
        self._id_primo_piano: str | None = None
        self._history = History()
        self._history.load()

        self.intestazione = ttk.Frame(self)
        self.intestazione.grid(row=0, column=0, sticky="ew", padx=18, pady=(12, 0))
        self.step_indicator = StepIndicator(self.intestazione, PASSI)
        self.step_indicator.grid(row=0, column=0, sticky="w")
        self.intestazione.columnconfigure(0, weight=1)

        self.banner = Banner(self)
        self.banner.grid(row=1, column=0, sticky="ew", padx=18, pady=(6, 6))
        self.banner.hide()

        self.container = ttk.Frame(self)
        self.container.grid(row=2, column=0, sticky="nsew", padx=18, pady=6)

        # I «Dettagli» restano nascosti finché non c'è davvero qualcosa da raccontare:
        # una grande area vuota confonde chi usa il programma.
        self.area_dettagli = ttk.Frame(self)
        self.area_dettagli.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 14))
        ttk.Label(self.area_dettagli, text="Dettagli delle operazioni", style="Tenue.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 2)
        )
        self.log_pane = LogPane(self.area_dettagli, height=6)
        self.log_pane.grid(row=1, column=0, sticky="ew")
        self.area_dettagli.columnconfigure(0, weight=1)
        self.area_dettagli.grid_remove()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # solo il contenuto si allarga

        if backend is not None:
            self._usa_backend(backend)
        elif demo_mode:
            self.attiva_demo()
        else:
            self.usa_collegamento_migliore()

        self.pages: dict[str, ttk.Frame] = {}
        self._costruisci_pagine()

        self.protocol("WM_DELETE_WINDOW", self._chiusura)
        self.go_to("connect")
        self._porta_in_primo_piano()

    def _porta_in_primo_piano(self) -> None:
        """Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro."""
        self.lift()
        self.attributes("-topmost", True)
        self._id_primo_piano = self.after(700, self._togli_primo_piano)
        self.focus_force()

    def _togli_primo_piano(self) -> None:
        """Rimette la finestra a livello normale, ma solo se esiste ancora.

        Se l'utente chiude il programma entro 700 ms il comando programmato arriverebbe su
        una finestra già distrutta e solleverebbe un `TclError`.
        """
        self._id_primo_piano = None
        try:
            if self.winfo_exists():
                self.attributes("-topmost", False)
        except tk.TclError:  # pragma: no cover - finestra chiusa nel frattempo
            pass

    # ── backend ───────────────────────────────────────────────────────────
    @property
    def remote(self) -> Trasporto | None:
        """Il modo di parlare con il telefono attualmente in uso."""
        return self.trasporto

    @remote.setter
    def remote(self, valore: Trasporto | None) -> None:
        self.trasporto = valore

    def _usa_backend(self, backend) -> None:
        """Usa un backend in memoria (test) o il telefono demo."""
        self.backend = backend
        self.trasporto = TrasportoDemo(backend, intervallo=self.INTERVALLO_PASSI)
        self.demo_mode = True

    def _usa_adb(self, percorso: str) -> None:
        """Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)."""
        self.adb_path = percorso
        self.backend = RealAdbBackend(percorso)
        self.trasporto = TrasportoAdb(percorso, intervallo=self.INTERVALLO_PASSI)
        self.demo_mode = False

    def usa_collegamento_migliore(self) -> bool:
        """Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.

        Si preferisce sempre il **collegamento diretto** (quello che non richiede il Debug
        USB); il Debug USB viene usato solo come scorciatoia se è già attivo.
        """
        self._gia_provati = set()
        return self.cambia_collegamento()

    def cambia_collegamento(self) -> bool:
        """Passa a un modo di collegamento **non ancora provato**.

        Tener traccia di quelli già falliti è indispensabile: senza, un errore faceva
        ripartire subito lo stesso tentativo, all'infinito, e l'utente non vedeva mai il
        messaggio di errore.
        """
        elenco = trasporti_disponibili(adb_path=self.adb_path or None)
        for trasporto in elenco:
            if trasporto.nome in self._gia_provati:
                continue
            self._gia_provati.add(trasporto.nome)
            self.demo_mode = False
            self.trasporto = trasporto
            self.adb_path = getattr(trasporto, "adb_path", None) or self.adb_path
            self.log(f"Collegamento scelto: {trasporto.nome} — {trasporto.spiegazione}")
            return True
        return False

    def attiva_demo(self) -> None:
        """Passa al telefono finto: permette di provare tutto senza dispositivo collegato."""
        from ..core.demo import DemoAdbBackend

        self._usa_backend(DemoAdbBackend(file_count=54))
        self.log("Modalità demo attiva: verrà usato un telefono finto.")

    def usa_telefono_vero(self, percorso: str | None = None) -> bool:
        """Torna al telefono vero, se su questo computer è possibile."""
        if percorso:
            self._usa_adb(percorso)
            return True
        return self.usa_collegamento_migliore()

    @property
    def component_mancante(self) -> bool:
        """True quando **nessun** modo di collegarsi è disponibile.

        Con il collegamento diretto il componente aggiuntivo (platform-tools) non serve più:
        il pulsante di installazione compare solo se davvero non c'è alternativa.
        """
        return self.transport is None

    @property
    def transport(self) -> Trasporto | None:
        return self.trasporto
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
        self._costruisci_pagine()
        # Senza questo la finestra resterebbe con `current_page = ""`: il primo «Indietro»
        # cercherebbe la posizione di una stringa vuota e solleverebbe ValueError.
        self.go_to("connect")

    def register_page(self, key: str, page: ttk.Frame) -> None:
        """Registra una pagina dentro il contenitore centrale (non sulla finestra)."""
        self.pages[key] = page
        page.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def go_to(self, key: str) -> None:
        if key in ("prev", "next"):
            # Con `current_page` vuoto (finestra appena costruita) «Indietro» e «Avanti»
            # devono portare al primo passo, non far saltare il programma.
            corrente = ORDINE.index(self.current_page) if self.current_page in ORDINE else 0
            if key == "prev":
                key = ORDINE[max(0, corrente - 1)]
            else:
                key = ORDINE[min(len(ORDINE) - 1, corrente + 1)]
        if key not in self.pages:
            key = ORDINE[0]
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
        # grid_info() è vuoto quando l'area è nascosta: funziona anche a finestra non ancora mostrata
        if not self.area_dettagli.grid_info():
            self.area_dettagli.grid()
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
                self.log(traceback.format_exc())
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
        """Chiude il programma; se sta copiando chiede conferma e non lascia file a metà."""
        if self.task_in_corso:
            prosegui = messagebox.askyesno(
                "Copia in corso",
                "Sto ancora copiando le foto.\n\nVuoi interrompere e chiudere?\n"
                "Le foto già copiate restano al sicuro; il file in corso viene ripreso "
                "la prossima volta.",
                parent=self,
            )
            if not prosegui:
                return
        self.stop_all_polling()
        self.cancel_event.set()
        self.annulla_task()
        if self._id_primo_piano is not None:
            try:
                self.after_cancel(self._id_primo_piano)
            except (tk.TclError, ValueError):  # pragma: no cover - difensivo
                pass
            self._id_primo_piano = None
        self._pulisci_ambiente()
        self.destroy()

    def _pulisci_ambiente(self) -> None:
        """Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio)."""
        pulisci = getattr(self.remote, "pulisci", None)
        if callable(pulisci):
            try:
                pulisci()
            except Exception:  # pragma: no cover - pulizia difensiva
                pass

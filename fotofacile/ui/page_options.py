"""Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono."""

from __future__ import annotations

import shutil
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from ..core.conversione import pillow_disponibile
from ..core.errors import FotoFacileError
from ..core.format import format_size
from ..core.planner import TransferOptions, build_plan, ensure_space, suggested_destination
from .theme import COLORI, font
from .widgets import PathChooser, TestoAdattivo


class OptionsPage(ttk.Frame):
    """Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono."""

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        # Predefinito: le foto e i video finiscono **direttamente** nella cartella scelta.
        # Ricreare le cartelle del telefono è un'opzione, non il comportamento normale.
        self.mantieni_cartelle = tk.BooleanVar(value=False)
        self.salta_gia_copiate = tk.BooleanVar(value=True)
        self.elimina_dopo_copia = tk.BooleanVar(value=False)
        # Attiva di default solo se possibile: senza Pillow non si può convertire.
        self._conversione_possibile = pillow_disponibile()
        self.converti_webp = tk.BooleanVar(value=self._conversione_possibile)

        ttk.Label(self, text="Dove salvo le foto?", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        self.riassunto = TestoAdattivo(self, text="", font=font(17))
        self.riassunto.grid(row=1, column=0, sticky="ew", pady=(4, 10))
        self.chooser = PathChooser(self, on_change=lambda _percorso: self._aggiorna_spazio())
        self.chooser.grid(row=2, column=0, sticky="ew")
        self.spazio = TestoAdattivo(self, text="", font=font(15, bold=True))
        self.spazio.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.dettaglio_salti = TestoAdattivo(self, text="", style="Tenue.TLabel", font=font(14))
        self.dettaglio_salti.grid(row=4, column=0, sticky="ew")

        # Le scelte rare stanno chiuse: chi non le cerca non le vede.
        self.altre_opzioni_aperte = False
        self.bottone_altre = ttk.Button(
            self,
            text="Altre opzioni ▸",
            style="Link.TButton",
            command=lambda: self.mostra_altre(not self.altre_opzioni_aperte),
        )
        self.bottone_altre.grid(row=5, column=0, sticky="w", pady=(12, 0))
        self.scelte = ttk.Frame(self)
        self.scelte.grid(row=6, column=0, sticky="ew")
        self.scelte.columnconfigure(0, weight=1)
        self.scelte.grid_remove()
        scelte = self.scelte
        ttk.Checkbutton(
            scelte,
            text="Ricrea anche le cartelle del telefono (di solito non serve)",
            variable=self.mantieni_cartelle,
            command=self._aggiorna_spazio,
        ).grid(row=0, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte,
            text="Salta le foto che ho già copiato",
            variable=self.salta_gia_copiate,
            command=self._aggiorna_spazio,
        ).grid(row=1, column=0, sticky="w", pady=3)
        if self._conversione_possibile:
            ttk.Checkbutton(
                scelte,
                text="Trasforma le immagini WebP in JPG (si aprono con qualsiasi programma)",
                variable=self.converti_webp,
                command=self._aggiorna_spazio,
            ).grid(row=2, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte,
            text="Cancella le foto dal telefono dopo averle copiate",
            variable=self.elimina_dopo_copia,
            command=self._eliminazione_cambiata,
        ).grid(row=3, column=0, sticky="w", pady=3)
        # promemoria rosso finché la spunta è attiva (la conferma vera è la finestra di domanda)
        self.avviso_eliminazione = TestoAdattivo(
            scelte,
            text="Attenzione: le foto verranno rimosse dal telefono. Controlla sempre la copia prima di chiudere il programma.",
            style="Errore.TLabel",
            font=font(14),
        )

        navigazione = ttk.Frame(self)
        navigazione.grid(row=7, column=0, sticky="ew", pady=(18, 0))
        ttk.Button(
            navigazione, text="←  Indietro", style="Secondary.TButton", command=self.azione_indietro
        ).grid(row=0, column=0)
        self.bottone_avanti = ttk.Button(
            navigazione, text="Copia le foto  →", style="Big.TButton", command=self.go_next
        )
        self.bottone_avanti.grid(row=0, column=1, padx=(12, 0))
        navigazione.columnconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        if not self.chooser.get():
            modello = self.app.device.display_name if self.app.device is not None else "Telefono"
            self.chooser.set(str(suggested_destination(modello)))
        self.app.set_status(
            "Ultimo passo prima della copia: controlla la cartella e premi «Copia le foto».",
            kind="info",
        )
        self._aggiorna_spazio()

    def mostra_altre(self, mostra: bool) -> None:
        self.altre_opzioni_aperte = bool(mostra)
        if mostra:
            self.scelte.grid()
            self.bottone_altre.configure(text="Altre opzioni ▾")
        else:
            self.scelte.grid_remove()
            self.bottone_altre.configure(text="Altre opzioni ▸")

    def azione_principale(self) -> None:
        """Tasto Invio: come «Copia le foto»."""
        # Invio è collegato a tutta la finestra e non guarda lo stato dei pulsanti.
        if not self.bottone_avanti.instate(["!disabled"]):
            return
        self.go_next()

    def azione_indietro(self) -> None:
        """Tasto Esc: torna al passo precedente."""
        self.app.go_to("prev")

    def _eliminazione_cambiata(self) -> None:
        if self.elimina_dopo_copia.get():
            # Togliere le foto dal telefono non si può annullare: si chiede subito e la
            # risposta predefinita è «No».
            conferma = messagebox.askyesno(
                "Togliere le foto dal telefono?",
                "Dopo la copia le foto verranno TOLTE dal telefono.\n\n"
                "Prima di chiudere il programma controlla che siano nella cartella scelta.\n\n"
                "Vuoi davvero toglierle dal telefono?",
                icon="warning",
                default="no",
                parent=self,
            )
            if not conferma:
                self.elimina_dopo_copia.set(False)
        if self.elimina_dopo_copia.get():
            self.avviso_eliminazione.grid(row=4, column=0, sticky="ew")
        else:
            self.avviso_eliminazione.grid_remove()
        self._aggiorna_spazio()

    # ── opzioni, spazio, piano ────────────────────────────────────────────
    def build_options(self) -> TransferOptions:
        return TransferOptions(
            destination=Path(self.chooser.get() or "."),
            preserve_structure=self.mantieni_cartelle.get(),
            skip_existing=self.salta_gia_copiate.get(),
            delete_after=self.elimina_dopo_copia.get(),
            include_videos=True,
            converti_webp=self.converti_webp.get() and self._conversione_possibile,
        )

    def free_space(self) -> int | None:
        """Spazio libero in byte nella cartella scelta; ``None`` se non è possibile saperlo."""
        destinazione = Path(self.chooser.get() or ".")
        while not destinazione.exists() and destinazione != destinazione.parent:
            destinazione = destinazione.parent
        try:
            return shutil.disk_usage(destinazione).free
        except OSError:  # disco di rete, permessi, unità rimossa
            return None

    def build_plan(self):
        return build_plan(
            self.app.media_files,
            self.build_options(),
            serial=self.app.device.serial if self.app.device is not None else "",
            history=self.app.history(),
        )

    def _aggiorna_spazio(self) -> None:
        try:
            piano = self.build_plan()
        except FotoFacileError as errore:
            self.riassunto.configure(text="")
            self.spazio.configure(text=f"✖ {errore.message}", foreground=COLORI["errore"])
            self.dettaglio_salti.configure(text=errore.hint)
            return
        except OSError as errore:
            self.riassunto.configure(text="")
            self.spazio.configure(
                text=f"✖ Non riesco a leggere la cartella scelta: {errore.strerror or errore}",
                foreground=COLORI["errore"],
            )
            self.dettaglio_salti.configure(text="")
            return
        quanti = piano.file_count
        if quanti == 0:
            self.riassunto.configure(text="Non c'è niente di nuovo da copiare: le foto erano già state salvate.")
        else:
            self.riassunto.configure(
                text=f"Copierò {quanti} {'foto o video' if quanti != 1 else 'foto'} "
                f"({format_size(piano.total_bytes)}) in questa cartella:  {self.chooser.get()}"
            )
        libero = self.free_space()
        if libero is None:
            simbolo, colore = "", COLORI["testo"]
            testo_spazio = f"Da copiare: {format_size(piano.total_bytes)} — spazio libero non leggibile"
        elif piano.total_bytes <= libero:
            simbolo, colore = "✔ ", COLORI["successo"]
            testo_spazio = f"Da copiare: {format_size(piano.total_bytes)} — Spazio libero: {format_size(libero)}"
        else:
            simbolo, colore = "✖ ", COLORI["errore"]
            testo_spazio = f"Da copiare: {format_size(piano.total_bytes)} — Spazio libero: {format_size(libero)}"
        self.spazio.configure(text=simbolo + testo_spazio, foreground=colore)
        saltati = piano.skipped_duplicates + piano.skipped_existing
        self.dettaglio_salti.configure(
            text=f"Verranno saltati {saltati} file già presenti." if saltati else ""
        )

    def go_next(self) -> None:
        opzioni = self.build_options()
        if not str(opzioni.destination).strip() or str(opzioni.destination) == ".":
            self.app.set_status(
                "Scegli una cartella dove salvare le foto.",
                hint="Premi «Cambia cartella…» e indica una cartella, per esempio Immagini.",
                kind="avviso",
            )
            return
        if not opzioni.destination.is_absolute():
            self.app.set_status(
                "La cartella indicata non è completa.",
                hint="Premi «Cambia cartella…» e scegli la cartella dal riquadro che si apre.",
                kind="avviso",
            )
            return
        try:
            piano = self.build_plan()
        except (FotoFacileError, OSError) as errore:
            self.app.set_status(
                getattr(errore, "message", "Non riesco a leggere la cartella scelta."),
                hint=getattr(errore, "hint", f"Controlla di avere accesso a {opzioni.destination}."),
                kind="errore",
            )
            return
        try:
            ensure_space(piano, opzioni.destination, self.free_space())
        except FotoFacileError as errore:
            self.app.set_status(errore.message, hint=errore.hint, kind="errore")
            return
        self.app.options = opzioni
        self.app.log(f"Destinazione scelta: {opzioni.destination}")
        if piano.file_count == 0:
            self.app.log("Non c'è nulla di nuovo da copiare: le foto erano già state trasferite.")
        self.app.go_to("transfer")

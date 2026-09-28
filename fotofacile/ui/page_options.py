"""Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono."""

from __future__ import annotations

import shutil
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from ..core.format import format_size
from ..core.planner import TransferOptions, build_plan, ensure_space, suggested_destination
from .theme import COLORI, font
from .widgets import PathChooser


class OptionsPage(ttk.Frame):
    """Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono."""

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        self.mantieni_cartelle = tk.BooleanVar(value=True)
        self.salta_gia_copiate = tk.BooleanVar(value=True)
        self.elimina_dopo_copia = tk.BooleanVar(value=False)
        self._conferma_eliminazione = False

        ttk.Label(self, text="Dove vuoi salvare le foto?", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self,
            text="Va bene la cartella proposta: potrai sempre spostare le foto dopo.",
            style="Sottotitolo.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.chooser = PathChooser(self, on_change=lambda _percorso: self._aggiorna_spazio())
        self.chooser.grid(row=2, column=0, sticky="ew")

        scelte = ttk.Frame(self)
        scelte.grid(row=3, column=0, sticky="w", pady=12)
        ttk.Checkbutton(
            scelte,
            text="Mantieni le cartelle come sul telefono (consigliato)",
            variable=self.mantieni_cartelle,
            command=self._aggiorna_spazio,
        ).grid(row=0, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte,
            text="Salta le foto che ho già copiato",
            variable=self.salta_gia_copiate,
            command=self._aggiorna_spazio,
        ).grid(row=1, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte,
            text="Cancella le foto dal telefono dopo averle copiate",
            variable=self.elimina_dopo_copia,
            command=self._eliminazione_cambiata,
        ).grid(row=2, column=0, sticky="w", pady=3)
        self.avviso_eliminazione = ttk.Label(
            scelte,
            text="Attenzione: le foto verranno rimosse dal telefono. Controlla sempre la copia prima di chiudere il programma.",
            style="Errore.TLabel",
            wraplength=780,
            justify="left",
            font=font(11),
        )

        self.spazio = ttk.Label(self, text="", font=font(13, bold=True))
        self.spazio.grid(row=4, column=0, sticky="w", pady=(6, 0))
        self.dettaglio_salti = ttk.Label(self, text="", style="Tenue.TLabel", font=font(11))
        self.dettaglio_salti.grid(row=5, column=0, sticky="w")

        navigazione = ttk.Frame(self)
        navigazione.grid(row=6, column=0, sticky="ew", pady=(18, 0))
        ttk.Button(
            navigazione, text="←  Indietro", style="Secondary.TButton", command=lambda: self.app.go_to("prev")
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

    def _eliminazione_cambiata(self) -> None:
        if self.elimina_dopo_copia.get():
            self.avviso_eliminazione.grid(row=3, column=0, sticky="w")
        else:
            self.avviso_eliminazione.grid_remove()
        self._conferma_eliminazione = False
        self._aggiorna_spazio()

    # ── opzioni, spazio, piano ────────────────────────────────────────────
    def build_options(self) -> TransferOptions:
        return TransferOptions(
            destination=Path(self.chooser.get() or "."),
            preserve_structure=self.mantieni_cartelle.get(),
            skip_existing=self.salta_gia_copiate.get(),
            delete_after=self.elimina_dopo_copia.get(),
            include_videos=True,
        )

    def free_space(self) -> int:
        destinazione = Path(self.chooser.get() or ".")
        while not destinazione.exists() and destinazione != destinazione.parent:
            destinazione = destinazione.parent
        try:
            return shutil.disk_usage(destinazione).free
        except OSError:  # pragma: no cover - difensivo
            return 0

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
        except OSError as errore:
            self.spazio.configure(
                text=f"Non riesco a leggere la cartella scelta: {errore.strerror or errore}",
                foreground=COLORI["errore"],
            )
            return
        libero = self.free_space()
        colore = COLORI["successo"] if piano.total_bytes <= libero else COLORI["errore"]
        self.spazio.configure(
            text=f"Da copiare: {format_size(piano.total_bytes)} — Spazio libero: {format_size(libero)}",
            foreground=colore,
        )
        saltati = piano.skipped_duplicates + piano.skipped_existing
        self.dettaglio_salti.configure(
            text=f"Verranno saltati {saltati} file già presenti." if saltati else ""
        )

    def go_next(self) -> None:
        opzioni = self.build_options()
        if not str(opzioni.destination).strip() or str(opzioni.destination) == ".":
            self.app.set_status(
                "Scegli una cartella dove salvare le foto.",
                hint="Premi «Sfoglia…» e indica una cartella, per esempio Immagini.",
                kind="avviso",
            )
            return
        if not opzioni.destination.is_absolute():
            self.app.set_status(
                "La cartella indicata non è completa.",
                hint="Premi «Sfoglia…» e scegli la cartella dal riquadro che si apre.",
                kind="avviso",
            )
            return
        try:
            piano = self.build_plan()
        except OSError as errore:
            self.app.set_status(
                "Non riesco a leggere la cartella scelta.",
                hint=f"Controlla di avere accesso a {opzioni.destination}: {errore}",
                kind="errore",
            )
            return
        try:
            ensure_space(piano, opzioni.destination, self.free_space())
        except Exception as errore:
            self.app.set_status(
                getattr(errore, "message", str(errore)),
                hint=getattr(errore, "hint", ""),
                kind="errore",
            )
            return
        if opzioni.delete_after and not self._conferma_eliminazione:
            self._conferma_eliminazione = True
            self.app.set_status(
                "Conferma la cancellazione dal telefono.",
                hint="Premi di nuovo «Copia le foto» per confermare, oppure togli la spunta alla cancellazione.",
                kind="avviso",
            )
            return
        self.app.options = opzioni
        self.app.log(f"Destinazione scelta: {opzioni.destination}")
        if piano.file_count == 0:
            self.app.log("Non c'è nulla di nuovo da copiare: le foto erano già state trasferite.")
        self.app.go_to("transfer")

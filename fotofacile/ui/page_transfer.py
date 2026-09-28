"""Passo 4: copia con avanzamento, interruzione e resoconto finale."""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from ..core.format import format_eta, format_size, format_speed
from ..core.osutil import open_in_file_manager
from ..core.planner import TransferPlan, build_plan
from ..core.report import build_report, save_report
from ..core.transfer import Progress, TransferResults, transfer_steps
from .theme import COLORI, font


class TransferPage(ttk.Frame):
    """Barra di avanzamento, velocità, tempo rimanente e resoconto finale."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.results: TransferResults | None = None
        self.report_text = ""
        self.started_at = 0.0
        self.last_plan = TransferPlan()

        ttk.Label(self, text="Copia in corso", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        self.stato = ttk.Label(self, text="Preparazione…", style="Sottotitolo.TLabel")
        self.stato.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.barra_totale = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", maximum=100)
        self.barra_totale.grid(row=2, column=0, sticky="ew")
        self.etichetta_file = ttk.Label(self, text="", style="Tenue.TLabel", font=font(11), wraplength=880)
        self.etichetta_file.grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.barra_file = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", maximum=100)
        self.barra_file.grid(row=4, column=0, sticky="ew", pady=(4, 8))

        self.dettagli = ttk.Label(self, text="", font=font(12))
        self.dettagli.grid(row=5, column=0, sticky="w")

        self.riepilogo_frame = ttk.Frame(self)
        self.riepilogo_frame.grid(row=6, column=0, sticky="ew", pady=12)
        self.riepilogo = ttk.Label(
            self.riepilogo_frame, text="", font=font(15, bold=True), wraplength=880, justify="left"
        )
        self.riepilogo.grid(row=0, column=0, sticky="w")
        self.riepilogo_errori = ttk.Label(
            self.riepilogo_frame,
            text="",
            style="Avviso.TLabel",
            wraplength=880,
            justify="left",
            font=font(11),
        )
        self.riepilogo_errori.grid(row=1, column=0, sticky="w")

        pulsanti = ttk.Frame(self)
        pulsanti.grid(row=7, column=0, sticky="ew")
        self.bottone_annulla = ttk.Button(pulsanti, text="Interrompi", style="Secondary.TButton", command=self.cancel)
        self.bottone_annulla.grid(row=0, column=0)
        self.bottone_apri = ttk.Button(
            pulsanti, text="Apri la cartella delle foto", style="Secondary.TButton", command=self.open_folder
        )
        self.bottone_apri.grid(row=0, column=1, padx=8)
        self.bottone_salva = ttk.Button(
            pulsanti, text="Salva resoconto", style="Secondary.TButton", command=self.save_report
        )
        self.bottone_salva.grid(row=0, column=2, padx=8)
        self.bottone_chiudi = ttk.Button(pulsanti, text="Chiudi", style="Big.TButton", command=self.app._chiusura)
        self.bottone_chiudi.grid(row=0, column=3, padx=(8, 0))
        pulsanti.columnconfigure(3, weight=1)

        for bottone in (self.bottone_apri, self.bottone_salva, self.bottone_chiudi):
            bottone.state(["disabled"])

        self.columnconfigure(0, weight=1)

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        self.app.set_status("Sto copiando le foto: non scollegare il telefono.", kind="info")
        self.bottone_annulla.state(["!disabled"])
        self.start_transfer()

    def start_transfer(self) -> None:
        self.app.cancel_event.clear()
        self.started_at = time.time()
        seriale = self.app.device.serial if self.app.device is not None else ""
        self.last_plan = build_plan(
            self.app.media_files,
            self.app.options,
            serial=seriale,
            history=self.app.history(),
        )
        self.app.log(
            f"Da copiare: {self.last_plan.file_count} file ({format_size(self.last_plan.total_bytes)}); "
            f"saltati: {self.last_plan.skipped_duplicates + self.last_plan.skipped_existing}."
        )
        generatore = transfer_steps(
            self.last_plan,
            self.app.options,
            self.app.remote,
            seriale,
            history=self.app.history(),
            on_progress=self.update_progress,
            annulla=self.app.cancel_event,
        )
        self.app.run_task(generatore, on_done=self.show_summary)

    # ── avanzamento ───────────────────────────────────────────────────────
    def update_progress(self, progresso: Progress) -> None:
        percentuale = (progresso.bytes_done * 100 / progresso.bytes_total) if progresso.bytes_total else 0.0
        self.barra_totale.configure(value=percentuale)
        self.barra_file.configure(value=100.0 if percentuale >= 100 else percentuale)
        self.etichetta_file.configure(text=f"File in corso: {progresso.current_name or '—'}")
        self.dettagli.configure(
            text=(
                f"{progresso.done_files} di {progresso.total_files} file — "
                f"{format_size(progresso.bytes_done)} di {format_size(progresso.bytes_total)} — "
                f"{format_speed(progresso.speed_bps)} — resta {format_eta(progresso.eta_seconds)}"
            )
        )
        self.stato.configure(text="Sto copiando le foto… non scollegare il telefono.")

    # ── fine copia ────────────────────────────────────────────────────────
    def show_summary(self, risultati: TransferResults) -> None:
        self.results = risultati
        if not risultati.cancelled:
            self.barra_totale.configure(value=100)
        testo = (
            f"Fatto! Ho copiato {len(risultati.copied)} file ({format_size(risultati.bytes_copied)}) "
            f"in {int(risultati.elapsed)} secondi."
        )
        if risultati.skipped:
            testo += f" Ne ho saltati {risultati.skipped} perché erano già presenti."
        if risultati.cancelled:
            testo = (
                f"Trasferimento interrotto: ho copiato {len(risultati.copied)} file. "
                "Quelli già copiati sono al sicuro."
            )
        self.riepilogo.configure(text=testo)
        if risultati.failed:
            primi = ", ".join(media.name for media, _motivo in risultati.failed[:5])
            self.riepilogo_errori.configure(text=f"Non copiati ({len(risultati.failed)}): {primi}")
        self.stato.configure(text="Copia conclusa." if not risultati.cancelled else "Copia interrotta.")
        self.report_text = build_report(
            risultati,
            self.last_plan,
            self.app.device,
            self.started_at,
            self.app.options.destination,
        )
        for bottone in (self.bottone_apri, self.bottone_salva, self.bottone_chiudi):
            bottone.state(["!disabled"])
        self.bottone_annulla.state(["disabled"])
        self.app.log(self.report_text)

    def riepilogo_testo(self) -> str:
        return str(self.riepilogo.cget("text"))

    def cancel(self) -> None:
        self.app.cancel_event.set()
        self.stato.configure(text="Interruzione in corso…")
        self.bottone_annulla.state(["disabled"])
        self.app.log("Interruzione richiesta: finisco il file in corso e mi fermo.")

    def open_folder(self) -> None:
        destinazione = self.app.options.destination
        try:
            open_in_file_manager(destinazione)
        except Exception as errore:
            self.app.set_status(
                getattr(errore, "message", str(errore)),
                hint=getattr(errore, "hint", f"Apri manualmente: {destinazione}"),
                kind="avviso",
            )

    def save_report(self) -> None:
        if not self.report_text:
            return
        percorso = save_report(self.report_text, self.app.options.destination)
        self.app.set_status("Resoconto salvato.", hint=f"Lo trovi qui: {percorso}", kind="successo")

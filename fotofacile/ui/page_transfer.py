"""Passo 4: copia con avanzamento, interruzione e resoconto finale."""

from __future__ import annotations

import time
from pathlib import Path

from tkinter import ttk

from ..core.devices import DeviceInfo
from ..core.errors import FotoFacileError
from ..core.format import format_duration, format_size, parole_tempo_residuo
from ..core.osutil import open_in_file_manager
from ..core.planner import TransferPlan, build_plan
from ..core.report import build_report, save_report
from ..core.transfer import Progress, TransferResults, transfer_steps
from .theme import font
from .widgets import TestoAdattivo


class TransferPage(ttk.Frame):
    """Barra di avanzamento, velocità, tempo rimanente e resoconto finale."""

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        self.results: TransferResults | None = None
        self.report_text = ""
        self.started_at = 0.0
        self.last_plan = TransferPlan()

        ttk.Label(self, text="Copia in corso", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        self.stato = ttk.Label(self, text="Preparazione…", style="Sottotitolo.TLabel")
        self.stato.grid(row=1, column=0, sticky="w", pady=(0, 6))

        self.percentuale = ttk.Label(self, text="0 %", font=font(40, bold=True))
        self.percentuale.grid(row=2, column=0, sticky="w")
        self.barra_totale = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", maximum=100)
        self.barra_totale.grid(row=3, column=0, sticky="ew", pady=(2, 4))
        self.etichetta_file = TestoAdattivo(self, text="", style="Tenue.TLabel", font=font(14))
        self.etichetta_file.grid(row=4, column=0, sticky="ew")
        self.barra_file = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", maximum=100)
        self.barra_file.grid(row=5, column=0, sticky="ew", pady=(2, 4))

        self.dettagli = TestoAdattivo(self, text="", font=font(14))
        self.dettagli.grid(row=6, column=0, sticky="ew")

        self.riepilogo_frame = ttk.Frame(self)
        self.riepilogo_frame.grid(row=7, column=0, sticky="ew", pady=(6, 8))
        self.riepilogo = TestoAdattivo(self.riepilogo_frame, text="", font=font(17, bold=True))
        self.riepilogo.grid(row=0, column=0, sticky="ew")
        self.riepilogo_errori = TestoAdattivo(
            self.riepilogo_frame, text="", style="Avviso.TLabel", font=font(14)
        )
        self.riepilogo_errori.grid(row=1, column=0, sticky="ew")
        self.riepilogo_frame.columnconfigure(0, weight=1)

        pulsanti = ttk.Frame(self)
        pulsanti.grid(row=8, column=0, sticky="ew")
        self.bottone_annulla = ttk.Button(pulsanti, text="Interrompi", style="Secondary.TButton", command=self.cancel)
        self.bottone_annulla.grid(row=0, column=0)
        self.bottone_indietro = ttk.Button(
            pulsanti, text="←  Indietro", style="Big.TButton", command=self.azione_indietro
        )
        self.bottone_indietro.grid(row=0, column=1, padx=8)
        self.bottone_indietro.grid_remove()  # compare solo se la copia si ferma per un errore
        self.bottone_apri = ttk.Button(
            pulsanti, text="Apri la cartella delle foto", style="Big.TButton", command=self.open_folder
        )
        self.bottone_apri.grid(row=0, column=2, padx=8)
        self.bottone_salva = ttk.Button(
            pulsanti, text="Salva resoconto", style="Secondary.TButton", command=self.save_report
        )
        self.bottone_salva.grid(row=0, column=3, padx=8)
        self.bottone_chiudi = ttk.Button(
            pulsanti, text="Chiudi", style="Secondary.TButton", command=self.app._chiusura
        )
        self.bottone_chiudi.grid(row=0, column=4, padx=(8, 0))
        pulsanti.columnconfigure(4, weight=1)

        self._in_corso = False  # una copia è già partita e non è ancora finita
        self._fermata_da_errore = False  # dopo un errore o un «Interrompi» si può tornare indietro
        self.mostra_altri_pulsanti(False)

        self.columnconfigure(0, weight=1)

    def mostra_altri_pulsanti(self, mostra: bool) -> None:
        """Durante la copia c'è solo «Interrompi»; a fine copia compaiono gli altri pulsanti."""
        for bottone in (self.bottone_apri, self.bottone_salva, self.bottone_chiudi):
            if mostra:
                bottone.grid()
            else:
                bottone.grid_remove()
            bottone.state(["!disabled"] if mostra else ["disabled"])

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        if self.app.options is None or self.app.remote is None:
            self._avviso_e_ritorno(
                "Manca un'informazione per iniziare la copia.",
                "Torna al passo «Destinazione» e premi di nuovo «Copia le foto».",
            )
            return
        if self.app.device is None:
            self._avviso_e_ritorno(
                "Il telefono non è più collegato.",
                "Ricollega il telefono e riparti dal primo passo.",
            )
            return
        self.app.set_status("Sto copiando le foto: non scollegare il telefono.", kind="info")
        self.bottone_annulla.state(["!disabled"])
        self.start_transfer()

    def _torna_indietro(self) -> None:
        """Riporta al passo precedente evitando un vicolo cieco senza uscita.

        L'avviso va ripetuto **dopo** il cambio di schermata: `go_to` chiude il banner, quindi
        il messaggio che spiega il motivo del ritorno sparirebbe subito.
        """
        testo, suggerimento = self.app.banner.message_text, self.app.banner.hint_text
        self.app.go_to("options")
        if testo:
            self.app.set_status(testo, hint=suggerimento, kind="avviso")

    def _avviso_e_ritorno(self, testo: str, suggerimento: str) -> None:
        self.app.set_status(testo, hint=suggerimento, kind="avviso")
        self._torna_indietro()

    def _riparti_da_capo(self) -> None:
        """Porta la pagina allo stato «copia appena iniziata» (serve dopo un errore)."""
        self.results = None
        self.report_text = ""
        self._fermata_da_errore = False
        self.stato.configure(text="Preparazione…")
        self.percentuale.configure(text="0 %")
        self.barra_totale.configure(value=0)
        self.barra_file.configure(value=0)
        self.etichetta_file.configure(text="")
        self.dettagli.configure(text="")
        self.riepilogo.configure(text="")
        self.riepilogo_errori.configure(text="")
        self.bottone_indietro.grid_remove()
        self.bottone_annulla.state(["!disabled"])
        self.mostra_altri_pulsanti(False)

    def start_transfer(self) -> None:
        # Un doppio clic (o Invio) su «Copia le foto» non deve far partire due copie insieme.
        # Il segnale conta solo se il lavoro è davvero ancora in corso: se il generatore si è
        # fermato per un errore imprevisto, la copia può ripartire.
        if self._in_corso and self.app.task_in_corso:
            return
        self._riparti_da_capo()
        self.app.cancel_event.clear()
        self.started_at = time.time()
        seriale = self.app.device.serial
        try:
            self.last_plan = self._pianifica(seriale)
        except OSError as errore:
            self._in_corso = False
            self.show_error(
                FotoFacileError(
                    "Non riesco a leggere la cartella di destinazione.",
                    f"Controlla di poter aprire {self.app.options.destination}: {errore}",
                )
            )
            return
        self.app.log(
            f"Da copiare: {self.last_plan.file_count} file "
            f"({format_size(self.last_plan.total_bytes)}); "
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
        self._in_corso = True
        self.app.run_task(generatore, on_done=self.show_summary, on_error=self.show_error)

    def show_error(self, errore) -> None:
        """La copia si è fermata per un errore: si spiega e si offre una via d'uscita."""
        self._in_corso = False
        self._fermata_da_errore = True
        self.stato.configure(text="Copia interrotta.")
        self.riepilogo.configure(text=f"✖ {errore.message}")
        self.riepilogo_errori.configure(text=errore.hint)
        self.bottone_annulla.state(["disabled"])
        self.mostra_altri_pulsanti(True)
        self.bottone_indietro.grid()
        self.app.set_status("La copia si è fermata.", hint="Premi «Indietro» per riprovare.", kind="errore")
        self.app.log(f"Errore durante la copia: {errore.message} {errore.hint}".strip())

    def _pianifica(self, seriale: str) -> TransferPlan:
        return build_plan(
            self.app.media_files,
            self.app.options,
            serial=seriale,
            history=self.app.history(),
        )

    # ── avanzamento ───────────────────────────────────────────────────────
    def update_progress(self, progresso: Progress) -> None:
        percentuale = (progresso.bytes_done * 100 / progresso.bytes_total) if progresso.bytes_total else 0.0
        self.barra_totale.configure(value=min(percentuale, 100.0))
        self.percentuale.configure(text=f"{int(min(percentuale, 100))} %")
        # La seconda barra segue il **singolo file** in corso, non il totale: altrimenti le
        # due barre si muovono insieme e quella «File in corso» non aggiunge nulla.
        if progresso.file_bytes_total:
            percentuale_file = progresso.file_bytes_done * 100 / progresso.file_bytes_total
        else:
            percentuale_file = percentuale
        self.barra_file.configure(value=min(percentuale_file, 100.0))
        self.etichetta_file.configure(text=f"File in corso: {progresso.current_name or '—'}")
        self.dettagli.configure(
            text=(
                f"{progresso.done_files} foto su {progresso.total_files}  •  "
                f"{format_size(progresso.bytes_done)} di {format_size(progresso.bytes_total)}  •  "
                f"{parole_tempo_residuo(progresso.eta_seconds)}"
            )
        )
        self.stato.configure(text="Sto copiando le foto… non scollegare il telefono.")

    # ── fine copia ────────────────────────────────────────────────────────
    def show_summary(self, risultati: TransferResults) -> None:
        self._in_corso = False
        self.results = risultati
        if not risultati.cancelled:
            self.barra_totale.configure(value=100)
            self.percentuale.configure(text="100 %")
        if risultati.cancelled:
            testo = (
                f"⚠ Trasferimento interrotto: ho copiato {len(risultati.copied)} file. "
                "Quelli già copiati sono al sicuro."
            )
        else:
            simbolo = "⚠" if risultati.failed else "✔"
            testo = (
                f"{simbolo} Fatto! Ho copiato {len(risultati.copied)} file "
                f"({format_size(risultati.bytes_copied)}) in {format_duration(risultati.elapsed)}."
            )
            if risultati.skipped:
                testo += f" Ne ho saltati {risultati.skipped} perché erano già presenti."
        self.riepilogo.configure(text=testo)
        righe = []
        if risultati.failed:
            primi = ", ".join(media.name for media, _motivo in risultati.failed[:5])
            righe.append(f"Non copiati ({len(risultati.failed)}): {primi}")
        righe.extend(risultati.warnings)
        self.riepilogo_errori.configure(text="\n".join(righe))
        self.stato.configure(text="Copia conclusa." if not risultati.cancelled else "Copia interrotta.")
        self.report_text = build_report(
            risultati,
            self.last_plan,
            self.app.device or DeviceInfo(serial="—", state="device", model="Telefono", product=""),
            self.started_at,
            self.app.options.destination if self.app.options is not None else Path("."),
        )
        self.mostra_altri_pulsanti(True)
        self.bottone_annulla.state(["disabled"])
        if risultati.cancelled:
            # dopo «Interrompi» si può cambiare idea e tornare alle opzioni, non c'è solo «Chiudi»
            self._fermata_da_errore = True
            self.bottone_indietro.grid()
        self.app.log(self.report_text)

    def azione_principale(self) -> None:
        """Tasto Invio: a copia finita apre la cartella; durante la copia non fa niente."""
        if self.results is not None:
            self.open_folder()

    def azione_indietro(self) -> None:
        """Tasto Esc: durante e dopo una copia riuscita non si torna indietro; dopo un errore o un'interruzione sì."""
        if self._fermata_da_errore:
            self.app.go_to("options")

    def riepilogo_testo(self) -> str:
        return str(self.riepilogo.cget("text"))

    def cancel(self) -> None:
        self.app.cancel_event.set()
        self.stato.configure(text="Interruzione in corso…")
        self.bottone_annulla.state(["disabled"])
        self.app.log("Interruzione richiesta: mi fermo subito. Le foto già copiate restano al sicuro.")

    def open_folder(self) -> None:
        if self.app.options is None:
            return
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
        if not self.report_text or self.app.options is None:
            return
        try:
            percorso = save_report(self.report_text, self.app.options.destination)
        except Exception as errore:
            self.app.set_status(
                getattr(errore, "message", "Non sono riuscito a salvare il resoconto."),
                hint=getattr(
                    errore,
                    "hint",
                    "Copia il testo dall'area «Dettagli» e incollalo in un documento.",
                ),
                kind="avviso",
            )
            return
        self.app.set_status("Resoconto salvato.", hint=f"Lo trovi qui: {percorso}", kind="successo")

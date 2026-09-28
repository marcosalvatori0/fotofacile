"""Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..core.format import format_size, parse_date
from ..core.scanner import DEFAULT_ROOTS, MediaFile, build_scan_command, group_folders
from .theme import COLORI, font


class SelectPage(ttk.Frame):
    """Elenco delle cartelle con caselle di spunta, filtri e totale scelto."""

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        self.folder_vars: dict[str, tk.BooleanVar] = {}
        self.sto_scegliendo_video = tk.BooleanVar(value=True)
        self.data_minima = tk.StringVar(value="")
        self._folders: list = []
        self._files: list[MediaFile] = []
        self._scansione_fatta = False

        ttk.Label(self, text="Scegli cosa copiare", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self,
            text="Queste sono le cartelle trovate sul telefono. Togli la spunta a quelle che non ti servono.",
            style="Sottotitolo.TLabel",
            wraplength=860,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))

        contenitore = ttk.Frame(self)
        contenitore.grid(row=2, column=0, sticky="nsew")
        self.canvas = tk.Canvas(contenitore, highlightthickness=0, background=COLORI["pannello"], height=260)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(contenitore, orient="vertical", command=self.canvas.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=barra.set)
        self.lista = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.lista, anchor="nw")
        contenitore.columnconfigure(0, weight=1)
        contenitore.rowconfigure(0, weight=1)

        opzioni = ttk.Frame(self)
        opzioni.grid(row=3, column=0, sticky="ew", pady=10)
        self.casella_video = ttk.Checkbutton(
            opzioni, text="Includi anche i video", variable=self.sto_scegliendo_video, command=self.start_scan
        )
        self.casella_video.grid(row=0, column=0, sticky="w")
        ttk.Label(opzioni, text="Solo foto dal giorno (AAAA-MM-GG, vuoto = tutte):").grid(
            row=0, column=1, padx=(18, 6)
        )
        campo_data = ttk.Entry(opzioni, textvariable=self.data_minima, width=14)
        campo_data.grid(row=0, column=2)
        campo_data.bind("<KeyRelease>", lambda _evento: self._aggiorna_totale())
        self.bottone_cerca = ttk.Button(
            opzioni, text="Cerca di nuovo", style="Secondary.TButton", command=self.start_scan
        )
        self.bottone_cerca.grid(row=0, column=3, padx=12)

        self.riepilogo = ttk.Label(self, text="", font=font(14, bold=True))
        self.riepilogo.grid(row=4, column=0, sticky="w", pady=(4, 8))

        navigazione = ttk.Frame(self)
        navigazione.grid(row=5, column=0, sticky="ew")
        ttk.Button(
            navigazione, text="←  Indietro", style="Secondary.TButton", command=lambda: self.app.go_to("prev")
        ).grid(row=0, column=0)
        self.bottone_avanti = ttk.Button(navigazione, text="Avanti  →", style="Big.TButton", command=self.go_next)
        self.bottone_avanti.grid(row=0, column=1, sticky="e", padx=(12, 0))
        navigazione.columnconfigure(1, weight=1)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.riepilogo.configure(text="Premi «Cerca di nuovo» per cercare le foto.", foreground=COLORI["tenue"])
        self.bottone_avanti.state(["disabled"])

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        if not self._scansione_fatta and not self.app.task_in_corso:
            self.start_scan()

    # ── ricerca ───────────────────────────────────────────────────────────
    def start_scan(self) -> None:
        if self.app.remote is None:
            self.app.set_status(
                "Manca il collegamento con il telefono.",
                hint="Torna indietro e collega il telefono.",
                kind="avviso",
            )
            return
        self.app.set_status("Sto cercando le foto sul telefono… può richiedere un momento.", kind="info")
        self.bottone_avanti.state(["disabled"])
        self.bottone_cerca.state(["disabled"])
        self.riepilogo.configure(text="Sto cercando…", foreground=COLORI["tenue"])
        seriale = self.app.device.serial if self.app.device is not None else ""
        comando = build_scan_command(DEFAULT_ROOTS, include_videos=self.sto_scegliendo_video.get())
        self.app.run_task(
            self.app.remote.cerca_media(seriale, comando, annulla=self.app.cancel_event),
            on_done=self._scansione_finita,
            on_error=self._scansione_fallita,
        )

    def _scansione_fallita(self, _errore) -> None:
        self.bottone_cerca.state(["!disabled"])
        self.riepilogo.configure(text="Ricerca non riuscita.", foreground=COLORI["avviso"])

    def _scansione_finita(self, file: list[MediaFile]) -> None:
        self._scansione_fatta = True
        self.bottone_cerca.state(["!disabled"])
        self._files = list(file)
        self._folders = group_folders(self._files)
        self.rebuild_list(self._folders)
        if not self._files:
            self.app.set_status(
                "Non ho trovato foto da copiare.",
                hint="Controlla che il telefono sia sbloccato; su alcuni telefoni le foto sono in «Immagini».",
                kind="avviso",
            )
            return
        quanti, peso = self.selected_total()
        self.app.set_status(
            f"Trovate {len(self._files)} foto e video.",
            hint=f"Selezionati: {quanti} file ({format_size(peso)}).",
            kind="successo",
        )

    def rebuild_list(self, folders) -> None:
        """Disegna l'elenco delle cartelle con una casella di spunta per ciascuna."""
        for figlio in self.lista.winfo_children():
            figlio.destroy()
        self.folder_vars.clear()
        for indice, cartella in enumerate(folders):
            variabile = tk.BooleanVar(value=True)
            self.folder_vars[cartella.remote_path] = variabile
            ttk.Checkbutton(
                self.lista,
                text=f"{cartella.label}  —  {cartella.file_count} file, {format_size(cartella.total_size)}",
                variable=variabile,
                command=self._aggiorna_totale,
            ).grid(row=indice, column=0, sticky="w", pady=2, padx=4)
        self.lista.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._aggiorna_totale()

    # ── selezione e totali ────────────────────────────────────────────────
    def selected_labels(self) -> list[str]:
        return [percorso for percorso, variabile in self.folder_vars.items() if variabile.get()]

    def selected_files(self) -> list[MediaFile]:
        scelte = set(self.selected_labels())
        data_minima = parse_date(self.data_minima.get())
        risultato = []
        for file in self._files:
            if file.parent not in scelte:
                continue
            if data_minima is not None and file.mtime < data_minima:
                continue
            risultato.append(file)
        return risultato

    def total_for(self, files) -> tuple[int, int]:
        return len(files), sum(file.size for file in files)

    def selected_total(self) -> tuple[int, int]:
        return self.total_for(self.selected_files())

    def _aggiorna_totale(self) -> None:
        quanti, peso = self.selected_total()
        data_scritta = self.data_minima.get().strip()
        if data_scritta and parse_date(data_scritta) is None:
            self.riepilogo.configure(
                text="La data non è chiara: scrivila come AAAA-MM-GG (per esempio 2024-05-01).",
                foreground=COLORI["avviso"],
            )
            self.bottone_avanti.state(["disabled"])
            return
        self.riepilogo.configure(
            text=f"Hai scelto {quanti} file — circa {format_size(peso)}.",
            foreground=COLORI["testo"] if quanti else COLORI["avviso"],
        )
        self.bottone_avanti.state(["!disabled"] if quanti else ["disabled"])

    def go_next(self) -> None:
        file = self.selected_files()
        if not file:
            self.app.set_status(
                "Non hai scelto nessuna foto da copiare.",
                hint="Metti la spunta ad almeno una cartella, oppure premi «Cerca di nuovo».",
                kind="avviso",
            )
            return
        self.app.media_files = file
        self.app.selected_folders = self.selected_labels()
        self.app.log(f"Selezionati {len(file)} file da copiare.")
        self.app.go_to("options")

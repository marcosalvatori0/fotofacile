"""Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare."""

from __future__ import annotations

import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from ..core.format import format_size, parse_date
from ..core.nomi_cartelle import e_rumore, nomi_distinti
from ..core.scanner import MediaFile, group_folders
from .theme import COLORI, font, tema_tela
from .widgets import TestoAdattivo

#: Voci del menu «Quali foto vuoi?»: (nome mostrato, giorni indietro oppure None per tutte).
PERIODI: tuple[tuple[str, int | None], ...] = (
    ("Tutte le foto", None),
    ("Dell'ultimo mese", 30),
    ("Degli ultimi 3 mesi", 90),
    ("Dell'ultimo anno", 365),
)


class SelectPage(ttk.Frame):
    """Elenco delle cartelle con caselle di spunta, filtri e totale scelto."""

    #: Ogni quanto si ricontrolla se il telefono si è liberato (millisecondi).
    ATTESA_TASK = 120

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        self.folder_vars: dict[str, tk.BooleanVar] = {}
        self.sto_scegliendo_video = tk.BooleanVar(value=True)
        # `data_minima` resta la variabile che filtra i file (AAAA-MM-GG o vuota): la calcola
        # il menu del periodo, l'utente non scrive più nessuna data.
        self.data_minima = tk.StringVar(value="")
        self.periodo = tk.StringVar(value=PERIODI[0][0])
        self.mostra_rumore = tk.BooleanVar(value=False)
        self._folders: list = []
        self._files: list[MediaFile] = []
        self._scansione_fatta = False
        self._scansione_in_corso = False
        self._attesa_id: str | None = None

        ttk.Label(self, text="Scegli le foto", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        TestoAdattivo(
            self, text="Togli la spunta alle cartelle che non ti servono.", style="Sottotitolo.TLabel"
        ).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        opzioni = ttk.Frame(self)
        opzioni.grid(row=2, column=0, sticky="ew", pady=(0, 6))
        self.casella_video = ttk.Checkbutton(
            opzioni, text="Includi anche i video", variable=self.sto_scegliendo_video, command=self.start_scan
        )
        self.casella_video.grid(row=0, column=0, sticky="w")
        ttk.Label(opzioni, text="Quali foto vuoi?").grid(row=0, column=1, padx=(24, 8))
        # l'elenco a tendina del menu è un widget Tk classico: il suo carattere va dato a parte
        self.option_add("*TCombobox*Listbox.font", font(14))
        menu = ttk.Combobox(
            opzioni,
            textvariable=self.periodo,
            values=[nome for nome, _ in PERIODI],
            state="readonly",
            width=22,
            font=font(14),
        )
        menu.grid(row=0, column=2)
        menu.bind("<<ComboboxSelected>>", lambda _evento: self._periodo_cambiato())
        self.casella_rumore = ttk.Checkbutton(
            opzioni, text="Mostra anche miniature e sticker", variable=self.mostra_rumore, command=self._ridisegna
        )
        self.casella_rumore.grid(row=1, column=0, columnspan=3, sticky="w")

        comandi = ttk.Frame(self)
        comandi.grid(row=3, column=0, sticky="ew", pady=(0, 6))
        ttk.Button(
            comandi, text="Seleziona tutte", style="Secondary.TButton", command=lambda: self.seleziona_tutto(True)
        ).grid(row=0, column=0)
        ttk.Button(
            comandi, text="Toglie la selezione", style="Secondary.TButton", command=lambda: self.seleziona_tutto(False)
        ).grid(row=0, column=1, padx=(10, 0))
        self.bottone_cerca = ttk.Button(
            comandi, text="Cerca di nuovo", style="Secondary.TButton", command=self.start_scan
        )
        self.bottone_cerca.grid(row=0, column=2, sticky="e", padx=(10, 0))
        comandi.columnconfigure(2, weight=1)

        contenitore = ttk.Frame(self)
        contenitore.grid(row=4, column=0, sticky="nsew")
        self.canvas = tk.Canvas(contenitore, background=COLORI["pannello"], height=260)
        tema_tela(self.canvas)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(contenitore, orient="vertical", command=self.canvas.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=barra.set)
        self.lista = ttk.Frame(self.canvas)
        self._finestra_lista = self.canvas.create_window((0, 0), window=self.lista, anchor="nw")
        # la lista occupa tutta la larghezza disponibile
        self.canvas.bind(
            "<Configure>", lambda evento: self.canvas.itemconfigure(self._finestra_lista, width=evento.width)
        )
        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind_all(evento, self._rotellina, add="+")
        contenitore.columnconfigure(0, weight=1)
        contenitore.rowconfigure(0, weight=1)

        self.riepilogo = ttk.Label(self, text="", font=font(18, bold=True))
        self.riepilogo.grid(row=5, column=0, sticky="w", pady=(10, 8))

        navigazione = ttk.Frame(self)
        navigazione.grid(row=6, column=0, sticky="ew")
        ttk.Button(
            navigazione, text="←  Indietro", style="Secondary.TButton", command=self.azione_indietro
        ).grid(row=0, column=0)
        self.bottone_avanti = ttk.Button(navigazione, text="Avanti  →", style="Big.TButton", command=self.go_next)
        self.bottone_avanti.grid(row=0, column=1, sticky="e", padx=(12, 0))
        navigazione.columnconfigure(1, weight=1)

        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.riepilogo.configure(text="Premi «Cerca di nuovo» per cercare le foto.", foreground=COLORI["tenue"])
        self.bottone_avanti.state(["disabled"])

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        self._avvia_quando_libero()

    def _avvia_quando_libero(self) -> None:
        """Avvia la ricerca appena il telefono è libero.

        Se all'ingresso in questa schermata c'è ancora un controllo del telefono in corso
        (per esempio il sondaggio del passo 1) si riprova fra poco: senza questo, la
        schermata resterebbe vuota per sempre e l'utente non capirebbe perché.
        """
        self._attesa_id = None
        if self._scansione_in_corso and not self.app.task_in_corso:
            # Il lavoro è stato abbandonato altrove (cambio schermata, altro comando): senza
            # questo azzeramento la schermata resterebbe bloccata per sempre su «Sto cercando…»,
            # con i pulsanti spenti e nessun modo di riprovare.
            self._scansione_in_corso = False
        if self._scansione_fatta or self._scansione_in_corso:
            return
        if self.app.task_in_corso:
            self._attesa_id = self.after(self.ATTESA_TASK, self._avvia_quando_libero)
            return
        self.start_scan()

    def stop_polling(self) -> None:
        """Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)."""
        if self._attesa_id is not None:
            try:
                self.after_cancel(self._attesa_id)
            except (tk.TclError, ValueError):  # finestra già chiusa
                pass
            self._attesa_id = None

    # ── ricerca ───────────────────────────────────────────────────────────
    def start_scan(self) -> None:
        self.stop_polling()
        if self._scansione_in_corso:
            # Premere «Cerca di nuovo» o cambiare la casella dei video mentre una ricerca è
            # già in corso abbandonava il lavoro a metà (processo e file temporanei compresi).
            return
        if self.app.remote is None:
            self.app.set_status(
                "Manca il collegamento con il telefono.",
                hint="Torna indietro e collega il telefono.",
                kind="avviso",
            )
            return
        if self.app.device is None:
            self.app.set_status(
                "Il telefono non è più collegato.",
                hint="Torna al passo «Collega il telefono» e ricollegalo, poi premi «Cerca le foto».",
                kind="avviso",
            )
            self.app.go_to("connect")
            # L'avviso va mostrato **dopo** il cambio di schermata: `go_to` chiude il banner.
            self.app.set_status(
                "Il telefono non è più collegato.",
                hint="Ricollegalo e premi «Avanti» per riprovare.",
                kind="avviso",
            )
            return
        self._scansione_in_corso = True
        self.app.set_status("Sto cercando le foto sul telefono… può richiedere un momento.", kind="info")
        self.bottone_avanti.state(["disabled"])
        self.bottone_cerca.state(["disabled"])
        self.casella_video.state(["disabled"])
        self.riepilogo.configure(text="Sto cercando…", foreground=COLORI["tenue"])
        self.app.run_task(
            self.app.remote.cerca_media(
                self.app.device.serial,
                include_videos=self.sto_scegliendo_video.get(),
                annulla=self.app.cancel_event,
            ),
            on_done=self._scansione_finita,
            on_error=self._scansione_fallita,
        )

    def _scansione_fallita(self, errore) -> None:
        self._scansione_in_corso = False
        self.bottone_cerca.state(["!disabled"])
        self.casella_video.state(["!disabled"])
        self.riepilogo.configure(text="Ricerca non riuscita.", foreground=COLORI["avviso"])
        self.app.set_status(errore.message, hint=errore.hint, kind="errore")
        self.app.log(f"Ricerca non riuscita: {errore.message} {errore.hint}".strip())

    def _scansione_finita(self, file: list[MediaFile]) -> None:
        self._scansione_fatta = True
        self._scansione_in_corso = False
        self.bottone_cerca.state(["!disabled"])
        self.casella_video.state(["!disabled"])
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

    def rebuild_list(self, folders, conserva_spunte: bool = False) -> None:
        """Disegna l'elenco delle cartelle con una casella di spunta per ciascuna.

        Miniature, cache e sticker non compaiono, a meno che la persona non lo chieda.
        """
        folders = self._visibili(folders)
        precedenti = {percorso: variabile.get() for percorso, variabile in self.folder_vars.items()}
        for figlio in self.lista.winfo_children():
            figlio.destroy()
        self.folder_vars.clear()
        nomi = nomi_distinti([cartella.remote_path for cartella in folders])
        for indice, cartella in enumerate(folders):
            valore = precedenti.get(cartella.remote_path, True) if conserva_spunte else True
            variabile = tk.BooleanVar(value=valore)
            self.folder_vars[cartella.remote_path] = variabile
            ttk.Checkbutton(
                self.lista,
                text=f"{nomi[cartella.remote_path]}  —  {cartella.file_count} file, {format_size(cartella.total_size)}",
                variable=variabile,
                command=self._aggiorna_totale,
            ).grid(row=indice, column=0, sticky="w", pady=2, padx=4)
        self.lista.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._aggiorna_totale()

    def _visibili(self, folders) -> list:
        if self.mostra_rumore.get():
            return list(folders)
        return [cartella for cartella in folders if not e_rumore(cartella.remote_path)]

    def _ridisegna(self) -> None:
        self.rebuild_list(self._folders, conserva_spunte=True)

    def _rotellina(self, evento) -> None:
        """La rotellina del mouse (o due dita sul touchpad) scorre l'elenco."""
        if self.app.current_page != "select":
            return
        passo = -1 if getattr(evento, "num", 0) == 4 or getattr(evento, "delta", 0) > 0 else 1
        try:
            self.canvas.yview_scroll(passo, "units")
        except tk.TclError:  # pagina ricostruita: questo elenco non esiste più
            pass

    def seleziona_tutto(self, valore: bool) -> None:
        for variabile in self.folder_vars.values():
            variabile.set(valore)
        self._aggiorna_totale()

    def _periodo_cambiato(self) -> None:
        giorni = dict(PERIODI).get(self.periodo.get())
        if giorni is None:
            self.data_minima.set("")
        else:
            self.data_minima.set(datetime.fromtimestamp(time.time() - giorni * 86400).strftime("%Y-%m-%d"))
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
        self.riepilogo.configure(
            text=f"Hai scelto {quanti} file — circa {format_size(peso)}.",
            foreground=COLORI["testo"] if quanti else COLORI["avviso"],
        )
        self.bottone_avanti.state(["!disabled"] if quanti else ["disabled"])

    def azione_principale(self) -> None:
        """Tasto Invio: come «Avanti»."""
        # Invio è collegato a tutta la finestra e non guarda lo stato dei pulsanti.
        if not self.bottone_avanti.instate(["!disabled"]):
            if self._scansione_in_corso:
                self.app.set_status("Sto ancora cercando le foto.", hint="Aspetta un momento.", kind="info")
            else:
                self.app.set_status(
                    "Non hai scelto nessuna foto da copiare.",
                    hint="Metti la spunta ad almeno una cartella.",
                    kind="avviso",
                )
            return
        self.go_next()

    def azione_indietro(self) -> None:
        """Tasto Esc: torna al passo precedente."""
        self.app.go_to("prev")

    def go_next(self) -> None:
        if self.app.device is None:
            self.app.set_status(
                "Il telefono non è più collegato.",
                hint="Torna al passo «Collega il telefono» e ricollegalo.",
                kind="avviso",
            )
            self.app.go_to("connect")
            return
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

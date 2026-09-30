"""Passo 1: guidare la persona a collegare il telefono.

Questa schermata è la più delicata: il telefono deve funzionare **senza** che l'utente attivi
qualcosa di speciale. Il programma sceglie da sé il collegamento migliore disponibile
(vedi :mod:`fotofacile.core.trasporto`) e qui si spiega solo cosa fare col cavo.

Le istruzioni per attivare il «Debug USB» esistono ancora, ma sono l'**ultima spiaggia**: si
mostrano solo se nessun altro collegamento dà risultati.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..core.devices import STATE_MESSAGE
from ..core.installer import installa_a_passi
from .theme import COLORI, font, tema_finestra, tema_testo

PASSI_SAMSUNG = [
    "Apri «Impostazioni».",
    "Vai in «Info sul telefono» e tocca «Informazioni sul software».",
    "Tocca «Numero di build» 7 volte: apparirà la voce «Opzioni sviluppatore».",
    "Torna in «Impostazioni» → «Opzioni sviluppatore» e attiva «Debug USB».",
]
PASSI_XIAOMI = [
    "Apri «Impostazioni» → «Info sul telefono».",
    "Tocca «Versione MIUI» (o «Numero di build») 7 volte.",
    "Apri «Impostazioni» → «Impostazioni aggiuntive» → «Opzioni sviluppatore».",
    "Attiva «Debug USB».",
]
PASSI_GOOGLE = [
    "Apri «Impostazioni» → «Info sul telefono».",
    "Tocca «Numero di build» 7 volte.",
    "Apri «Impostazioni» → «Sistema» → «Opzioni sviluppatore».",
    "Attiva «Debug USB».",
]
PASSI_HUAWEI = [
    "Apri «Impostazioni» → «Info sul telefono».",
    "Tocca «Numero di build» 7 volte.",
    "Apri «Impostazioni» → «Sistema e aggiornamenti» → «Opzioni sviluppatore».",
    "Attiva «Debug USB».",
]
PASSI_OPPO = [
    "Apri «Impostazioni» → «Info sul telefono» → «Versione».",
    "Tocca «Numero di build» 7 volte.",
    "Apri «Impostazioni» → «Sistema» → «Opzioni sviluppatore».",
    "Attiva «Debug USB».",
]
PASSI_GENERICI = [
    "Apri «Impostazioni» sul telefono.",
    "Cerca la voce «Info sul telefono» (a volte si chiama «Info dispositivo»).",
    "Tocca «Numero di build» 7 volte di seguito.",
    "Torna indietro: apparirà «Opzioni sviluppatore» (a volte sotto «Sistema»).",
    "Attiva «Debug USB».",
]

BRAND_SCONOSCIUTO = "Altro"
# Ogni marca si trova cercandola per nome; il menù mostra solo le voci principali.
HELP_BRANDS: dict[str, list[str]] = {
    "Samsung": PASSI_SAMSUNG,
    "Xiaomi": PASSI_XIAOMI,
    "Redmi": PASSI_XIAOMI,
    "POCO": PASSI_XIAOMI,
    "Google": PASSI_GOOGLE,
    "Pixel": PASSI_GOOGLE,
    "Huawei": PASSI_HUAWEI,
    "Honor": PASSI_HUAWEI,
    "Oppo": PASSI_OPPO,
    "Realme": PASSI_OPPO,
    "OnePlus": PASSI_OPPO,
    BRAND_SCONOSCIUTO: PASSI_GENERICI,
}
BRANDS_ORDINE = ("Samsung", "Xiaomi", "Google", "Huawei", "Oppo", BRAND_SCONOSCIUTO)

CONSIGLI_FINALI = (
    "",
    "Quando lo schermo del telefono chiede «Consentire il debug USB?», tocca «Consenti».",
    "",
    "Se il telefono non viene riconosciuto:",
    "• prova un altro cavo USB (alcuni cavi servono solo per ricaricare);",
    "• sblocca lo schermo del telefono e lascialo sbloccato durante la copia;",
    "• scollega e ricollega il cavo dopo aver attivato il «Debug USB».",
)

#: Testo mostrato quando nessun collegamento funziona: prima le cose semplici, il Debug USB
#: solo alla fine, perché non deve mai sembrare obbligatorio.
CONSIGLI_SENZA_DEBUG = (
    "Il telefono non viene riconosciuto.",
    "",
    "Prova in quest'ordine:",
    "1. usa un altro cavo USB (alcuni cavi servono solo per ricaricare);",
    "2. cambia porta del computer (evita gli adattatori e gli hub);",
    "3. sblocca lo schermo del telefono e rispondi «Consenti» se compare una richiesta;",
    "4. scollega e ricollega il cavo tenendo il telefono sbloccato.",
    "",
    "Se non basta, l'ultima possibilità è attivare il «Debug USB»: scegli la marca del"
    " telefono qui sopra e segui i passaggi.",
)


def build_help_text(brand: str) -> str:
    """Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca."""
    passi = HELP_BRANDS.get(brand, PASSI_GENERICI)
    righe = [
        f"Come attivare il «Debug USB» — {brand}",
        "",
        "Serve solo se il telefono non viene riconosciuto in nessun altro modo:",
        "di solito non è necessario.",
        "",
    ]
    righe.extend(f"{indice}. {passo}" for indice, passo in enumerate(passi, start=1))
    righe.extend(CONSIGLI_FINALI)
    return "\n".join(righe)


def build_help_text_generico() -> str:
    """Cosa provare **prima** di pensare al Debug USB."""
    return "\n".join(CONSIGLI_SENZA_DEBUG)


class ConnectPage(ttk.Frame):
    """Prima schermata: collega il telefono, con aiuto, installazione e prova demo."""

    INTERVALLO_SONDAGGIO = 2000

    def __init__(self, parent) -> None:
        # le pagine vivono dentro app.container: la finestra resta libera per
        # intestazione (indicatore dei passi), avvisi e dettagli
        super().__init__(parent.container)
        self.app = parent
        self.message = ""
        self._polling = False
        #: Identificativo del prossimo controllo programmato: annullarlo è l'unico modo
        #: per non lasciare in giro catene di `after` che continuano a interrogare il telefono.
        self._tick_id: str | None = None
        self._finestra_aiuto: tk.Toplevel | None = None
        self._ultimo_stato = ("", 0, 0)

        ttk.Label(self, text="Collega il telefono al computer", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 2)
        )
        ttk.Label(
            self,
            text=(
                "Usa il cavo USB e tieni lo schermo del telefono sbloccato. "
                "Non devi attivare nessuna impostazione: il programma trova da s\u00e9 il modo di leggere le foto."
            ),
            style="Sottotitolo.TLabel",
            wraplength=860,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.indicatore = ttk.Label(self, text="", font=font(16, bold=True), wraplength=880, justify="left")
        self.indicatore.grid(row=2, column=0, sticky="w", pady=(6, 2))
        self.dettaglio = ttk.Label(
            self, text="", style="Tenue.TLabel", font=font(12), wraplength=880, justify="left"
        )
        self.dettaglio.grid(row=3, column=0, sticky="w")

        pulsanti = ttk.Frame(self)
        pulsanti.grid(row=4, column=0, sticky="w", pady=14)
        self.bottone_aiuto = ttk.Button(
            pulsanti,
            text="Il telefono non viene riconosciuto?",
            style="Secondary.TButton",
            command=self.show_help,
        )
        self.bottone_aiuto.grid(row=0, column=0, padx=(0, 8))
        self.bottone_installa = ttk.Button(
            pulsanti,
            text="Installa componente mancante",
            style="Secondary.TButton",
            command=self.install_component,
        )
        self.bottone_installa.grid(row=0, column=1, padx=8)
        self.bottone_ricarica = ttk.Button(
            pulsanti, text="Riprova il collegamento", style="Secondary.TButton", command=self.restart_connection
        )
        self.bottone_ricarica.grid(row=0, column=2, padx=8)

        navigazione = ttk.Frame(self)
        navigazione.grid(row=5, column=0, sticky="ew", pady=(6, 0))
        self.bottone_avanti = ttk.Button(navigazione, text="Avanti  →", style="Big.TButton", command=self._avanti)
        self.bottone_avanti.grid(row=0, column=1, sticky="e")
        navigazione.columnconfigure(1, weight=1)

        ttk.Button(
            self,
            text="Prova il programma senza telefono (demo)",
            style="Secondary.TButton",
            command=self.enable_demo,
        ).grid(row=6, column=0, sticky="w", pady=(22, 0))
        ttk.Label(
            self,
            text="Nella modalità demo viene usato un telefono finto: serve solo per vedere come funziona.",
            style="Tenue.TLabel",
            font=font(11),
        ).grid(row=7, column=0, sticky="w")

        self.columnconfigure(0, weight=1)
        self._aggiorna_bottone_installa()
        self.set_message("Collega il telefono con il cavo e sbloccalo.")
        self.bottone_avanti.state(["disabled"])

    # ── messaggi ──────────────────────────────────────────────────────────
    def set_message(self, testo: str, tono: str = "info") -> None:
        self.message = testo
        colori = {"info": COLORI["testo"], "successo": COLORI["successo"], "avviso": COLORI["avviso"]}
        self.indicatore.configure(text=testo, foreground=colori.get(tono, COLORI["testo"]))

    def _aggiorna_bottone_installa(self) -> None:
        # Il pulsante compare solo quando **nessun** collegamento è disponibile: con il
        # collegamento diretto non serve installare niente.
        serve = self.app.component_mancante
        self.bottone_installa.state(["!disabled"] if serve else ["disabled"])

    # ── ciclo di vita e sondaggio ─────────────────────────────────────────
    def on_show(self) -> None:
        self.start_polling()

    def start_polling(self) -> None:
        # Si riparte sempre da zero: senza l'annullamento del controllo precedente ogni
        # ritorno a questa schermata aggiungeva una catena di `after` in più, e il telefono
        # veniva interrogato due, tre, quattro volte ogni due secondi.
        self.stop_polling()
        self._polling = True
        self.check_now()
        self._tick_id = self.after(self.INTERVALLO_SONDAGGIO, self._tick)

    def stop_polling(self) -> None:
        self._polling = False
        if self._tick_id is not None:
            try:
                self.after_cancel(self._tick_id)
            except (tk.TclError, ValueError):  # finestra già chiusa
                pass
            self._tick_id = None
        self._ultimo_stato = ("", 0, 0)

    def _tick(self) -> None:
        self._tick_id = None
        if not self._polling:
            return
        self.check_now()
        self._tick_id = self.after(self.INTERVALLO_SONDAGGIO, self._tick)

    def check_now(self) -> None:
        """Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale."""
        self._aggiorna_bottone_installa()
        if self.app.remote is None:
            # Su questo computer non esiste nessun modo di collegarsi: è una condizione di
            # partenza, non qualcosa che cambia da sola. Lo si dice una volta sola, indicando
            # l'unica azione che può davvero aiutare.
            self.set_message("Su questo computer non riesco a collegarmi al telefono.", tono="avviso")
            self.dettaglio.configure(
                text="Premi «Installa componente mancante», oppure apri la diagnosi con «doctor»."
            )
            return
        if self.app.task_in_corso:
            return  # c'è già un controllo in corso
        self.app.run_task(
            self.app.remote.dispositivi(),
            on_done=self._dispositivi_ricevuti,
            on_error=self._controllo_fallito,
        )

    def _controllo_fallito(self, errore) -> None:
        """Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se c'è.

        Una sola volta per modo: se anche l'ultimo disponibile fallisce, si mostra l'errore
        invece di riprovare all'infinito.
        """
        if not self.app.demo_mode and self.app.cambia_collegamento():
            self.app.log(f"Cambio collegamento: {errore.message}")
            self._aggiorna_bottone_installa()
            self.check_now()
            return
        self.set_message(errore.message, tono="avviso")
        self.dettaglio.configure(text=errore.hint or "Premi «Riprova il collegamento» e riprova.")

    def _dispositivi_ricevuti(self, dispositivi) -> None:
        pronti = [dispositivo for dispositivo in dispositivi if dispositivo.is_ready]
        pronto = pronti[0] if pronti else None
        if pronto is not None:
            if len(pronti) > 1:
                nomi = ", ".join(dispositivo.display_name for dispositivo in pronti)
                if self._ultimo_stato[1] != len(pronti):
                    self.app.log(f"Più telefoni collegati ({nomi}): uso {pronto.display_name}.")
            self.app.device = pronto
            self.set_message(f"Perfetto! Telefono collegato: {pronto.display_name}", tono="successo")
            self.dettaglio.configure(text="Premi «Avanti» per scegliere quali foto copiare.")
            self._ultimo_stato = ("device", len(pronti), 0)
            self.bottone_avanti.state(["!disabled"])
            self.stop_polling()
            return
        self.app.device = None
        self.bottone_avanti.state(["disabled"])
        if not dispositivi:
            self.set_message("Non vedo ancora nessun telefono: collegalo con il cavo e sbloccalo.")
            self.dettaglio.configure(
                text="Se il cavo è già collegato, prova un altro cavo USB o un'altra porta del computer."
            )
            return
        stato = dispositivi[0].state
        messaggio, suggerimento = STATE_MESSAGE.get(
            stato, ("Il telefono non è pronto.", "Aspetta qualche secondo e riprova.")
        )
        self.set_message(messaggio, tono="avviso")
        self.dettaglio.configure(text=suggerimento)
        firma = (stato, len(dispositivi), 0)
        if firma != self._ultimo_stato:  # nel registro solo quando la situazione cambia
            self.app.log(f"Telefono: {stato}.")
            self._ultimo_stato = firma

    # ── azioni ────────────────────────────────────────────────────────────
    def _avanti(self) -> None:
        if self.app.device is None:
            self.set_message("Prima collega il telefono e sblocca lo schermo.", tono="avviso")
            return
        self.stop_polling()
        self.app.go_to("select")

    def show_help(self) -> None:
        """Cosa provare quando il telefono non viene riconosciuto.

        Prima le cose semplici (cavo, porta, schermo sbloccato); il «Debug USB» è in fondo,
        presentato come ultima possibilità e non come passaggio obbligato. La finestra viene
        riusata, non moltiplicata a ogni clic.
        """
        if self._finestra_aiuto is not None and self._finestra_aiuto.winfo_exists():
            self._finestra_aiuto.deiconify()
            self._finestra_aiuto.lift()
            self._finestra_aiuto.focus_set()
            return

        finestra = tk.Toplevel(self)
        self._finestra_aiuto = finestra
        finestra.title("Il telefono non viene riconosciuto")
        finestra.geometry("700x580")
        finestra.transient(self.winfo_toplevel())
        tema_finestra(finestra)
        marca = tk.StringVar(value="Samsung")

        testo = tk.Text(finestra, wrap="word", font=font(12), height=16)
        tema_testo(testo)
        testo.grid(row=0, column=0, sticky="nsew", padx=14, pady=(12, 6))

        def mostra(con_marca: bool, *_args) -> None:
            testo.configure(state="normal")
            testo.delete("1.0", "end")
            testo.insert("1.0", build_help_text(marca.get()) if con_marca else build_help_text_generico())
            testo.configure(state="disabled")
            testo.see("1.0")

        ttk.Button(
            finestra, text="Cosa provare adesso", style="Secondary.TButton", command=lambda: mostra(False)
        ).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 6))
        ttk.Label(finestra, text="Oppure, come ultima possibilità, attiva il Debug USB:").grid(
            row=2, column=0, sticky="w", padx=14
        )
        selettore = ttk.Combobox(finestra, textvariable=marca, values=list(BRANDS_ORDINE), state="readonly")
        selettore.grid(row=3, column=0, sticky="ew", padx=14, pady=(2, 8))
        selettore.bind("<<ComboboxSelected>>", lambda _evento: mostra(True))
        ttk.Button(finestra, text="Ho capito", style="Secondary.TButton", command=finestra.destroy).grid(
            row=4, column=0, pady=(0, 12)
        )
        finestra.columnconfigure(0, weight=1)
        finestra.rowconfigure(0, weight=1)
        mostra(False)

    def install_component(self) -> None:
        """Scarica il componente mancante mostrando l'avanzamento nel registro."""
        self.app.set_status("Sto scaricando il componente di collegamento…", kind="info")
        self.bottone_installa.state(["disabled"])
        self.app.log("Download del componente di collegamento in corso…")
        # L'evento di annullamento è condiviso con le altre operazioni: qui va azzerato,
        # altrimenti un annullamento precedente interromperebbe subito il download.
        self.app.cancel_event.clear()

        def progresso(info: dict) -> None:
            totale = info.get("totale") or 0
            percentuale = f" ({info['ricevuti'] * 100 // totale}%)" if totale else ""
            self.app.log(f"  scaricati {info['ricevuti'] // 1024} KB{percentuale}")

        self.app.run_task(
            installa_a_passi(on_progress=progresso, annulla=self.app.cancel_event),
            on_done=self._componente_pronto,
            on_error=self._componente_fallito,
        )

    def _componente_fallito(self, errore) -> None:
        """Il download non è riuscito: il pulsante torna subito utilizzabile."""
        self._aggiorna_bottone_installa()
        self.set_message(errore.message, tono="avviso")
        self.dettaglio.configure(text=errore.hint or "Riprova il download.")

    def _componente_pronto(self, percorso) -> None:
        self.app.log(f"Componente pronto: {percorso}")
        self.app.usa_telefono_vero(str(percorso))
        self.app.set_status("Componente installato. Ora collega il telefono.", kind="successo")
        self._aggiorna_bottone_installa()
        self.check_now()

    def restart_connection(self) -> None:
        """Riprova il collegamento: prima si ricontrolla quali modi sono disponibili.

        È il primo rimedio da provare e non presuppone nessuna impostazione sul telefono: con
        il collegamento diretto serve solo a scollegare e ricollegare il cavo.
        """
        if self.app.remote is None:
            if not self.app.usa_collegamento_migliore():
                self.app.set_status(
                    "Non c'è nessun collegamento da riprovare su questo computer.",
                    hint="Apri la diagnosi con «doctor» e segnala il risultato.",
                    kind="avviso",
                )
                return
            self._aggiorna_bottone_installa()
        self.app.set_status("Sto riprovando il collegamento…", kind="info")
        self.app.log("Collegamento riprovato.")
        self.app.run_task(self.app.remote.riavvia(), on_done=lambda _esito: self.check_now())

    def enable_demo(self) -> None:
        """Telefono finto: permette di provare tutta la procedura senza dispositivo."""
        self.app.attiva_demo()
        self._aggiorna_bottone_installa()
        self.set_message("Modalità demo: telefono finto collegato.", tono="successo")
        self.check_now()

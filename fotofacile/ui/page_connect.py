"""Passo 1: guidare la persona a collegare il telefono e autorizzare il computer.

Questa schermata è la più delicata: se il telefono non viene riconosciuto, l'utente deve
capire *cosa fare adesso*, senza gergo tecnico.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..core.devices import STATE_MESSAGE
from ..core.installer import installa_a_passi, is_installed
from .theme import COLORI, font

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
    "• su Windows, installa il driver USB del produttore del telefono;",
    "• scollega e ricollega il cavo dopo aver attivato il «Debug USB».",
)


def build_help_text(brand: str) -> str:
    """Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca."""
    passi = HELP_BRANDS.get(brand, PASSI_GENERICI)
    righe = [
        f"Come attivare il «Debug USB» — {brand}",
        "",
        "Il telefono deve autorizzare il computer: è una procedura da fare una volta sola.",
        "",
    ]
    righe.extend(f"{indice}. {passo}" for indice, passo in enumerate(passi, start=1))
    righe.extend(CONSIGLI_FINALI)
    return "\n".join(righe)


class ConnectPage(ttk.Frame):
    """Prima schermata: collega il telefono, con aiuto, installazione e prova demo."""

    INTERVALLO_SONDAGGIO = 2000

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.message = ""
        self._polling = False
        self._controllo_in_corso = False

        ttk.Label(self, text="Collega il telefono al computer", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 2)
        )
        ttk.Label(
            self,
            text="Usa il cavo USB e tieni il telefono sbloccato: ti chiederà di autorizzare il computer.",
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
            pulsanti, text="Come si attiva il Debug USB?", style="Secondary.TButton", command=self.show_help
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
            pulsanti, text="Riavvia collegamento", style="Secondary.TButton", command=self.restart_connection
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
        serve = self.app.component_mancante
        self.bottone_installa.state(["!disabled"] if serve else ["disabled"])

    # ── ciclo di vita e sondaggio ─────────────────────────────────────────
    def on_show(self) -> None:
        self.start_polling()

    def start_polling(self) -> None:
        if self._polling:
            return
        self._polling = True
        self.check_now()
        self.after(self.INTERVALLO_SONDAGGIO, self._tick)

    def stop_polling(self) -> None:
        self._polling = False

    def _tick(self) -> None:
        if not self._polling:
            return
        self.check_now()
        self.after(self.INTERVALLO_SONDAGGIO, self._tick)

    def check_now(self) -> None:
        """Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale."""
        self._aggiorna_bottone_installa()
        if self.app.remote is None:
            self.set_message("Manca il componente di collegamento.", tono="avviso")
            self.dettaglio.configure(text="Premi «Installa componente mancante»: lo scarico io da internet.")
            return
        if self._controllo_in_corso:
            return
        self._controllo_in_corso = True
        self.app.run_task(self.app.remote.dispositivi(), on_done=self._dispositivi_ricevuti)

    def _dispositivi_ricevuti(self, dispositivi) -> None:
        self._controllo_in_corso = False
        pronto = next((dispositivo for dispositivo in dispositivi if dispositivo.is_ready), None)
        if pronto is not None:
            self.app.device = pronto
            self.set_message(f"Perfetto! Telefono collegato: {pronto.display_name}", tono="successo")
            self.dettaglio.configure(text="Premi «Avanti» per scegliere quali foto copiare.")
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

    # ── azioni ────────────────────────────────────────────────────────────
    def _avanti(self) -> None:
        if self.app.device is None:
            self.set_message("Prima collega il telefono e autorizza il computer.", tono="avviso")
            return
        self.stop_polling()
        self.app.go_to("select")

    def show_help(self) -> None:
        """Istruzioni per marca, con menù a tendina."""
        finestra = tk.Toplevel(self)
        finestra.title("Come attivare il Debug USB")
        finestra.geometry("660x540")
        marca = tk.StringVar(value="Samsung")
        testo = tk.Text(finestra, wrap="word", font=font(12), height=16, background=COLORI["pannello"])
        testo.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))

        def aggiorna(*_args) -> None:
            testo.configure(state="normal")
            testo.delete("1.0", "end")
            testo.insert("1.0", build_help_text(marca.get()))
            testo.configure(state="disabled")

        selettore = ttk.Combobox(finestra, textvariable=marca, values=list(BRANDS_ORDINE), state="readonly")
        selettore.grid(row=0, column=0, sticky="ew", padx=14, pady=12)
        selettore.bind("<<ComboboxSelected>>", aggiorna)
        ttk.Button(finestra, text="Ho capito", style="Secondary.TButton", command=finestra.destroy).grid(
            row=2, column=0, pady=(0, 12)
        )
        finestra.columnconfigure(0, weight=1)
        finestra.rowconfigure(1, weight=1)
        aggiorna()

    def install_component(self) -> None:
        """Scarica il componente mancante mostrando l'avanzamento nel registro."""
        self.app.set_status("Sto scaricando il componente di collegamento…", kind="info")
        self.bottone_installa.state(["disabled"])
        self.app.log("Download del componente di collegamento in corso…")

        def progresso(info: dict) -> None:
            totale = info.get("totale") or 0
            percentuale = f" ({info['ricevuti'] * 100 // totale}%)" if totale else ""
            self.app.log(f"  scaricati {info['ricevuti'] // 1024} KB{percentuale}")

        self.app.run_task(installa_a_passi(on_progress=progresso), on_done=self._componente_pronto)

    def _componente_pronto(self, percorso) -> None:
        self.app.log(f"Componente pronto: {percorso}")
        self.app.usa_telefono_vero(str(percorso))
        self.app.set_status("Componente installato. Ora collega il telefono.", kind="successo")
        self._aggiorna_bottone_installa()
        self.check_now()

    def restart_connection(self) -> None:
        if self.app.remote is None:
            self.app.set_status(
                "Prima serve il componente di collegamento.",
                hint="Premi «Installa componente mancante».",
                kind="avviso",
            )
            return
        self.app.set_status("Sto riavviando il collegamento…", kind="info")
        self.app.log("Riavvio del collegamento richiesto.")
        self.app.run_task(self.app.remote.riavvia(), on_done=lambda _esito: self.check_now())

    def enable_demo(self) -> None:
        """Telefono finto: permette di provare tutta la procedura senza dispositivo."""
        self.app.attiva_demo()
        self._aggiorna_bottone_installa()
        self.set_message("Modalità demo: telefono finto collegato.", tono="successo")
        self.check_now()

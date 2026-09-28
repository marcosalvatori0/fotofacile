"""Componenti grafici riusabili: nessuna logica di business, solo presentazione."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk
from typing import Callable, Sequence

from .theme import COLORI, font


_TK_DISPONIBILE: bool | None = None


def tk_available(timeout: float = 8.0) -> bool:
    """True se questa macchina riesce davvero ad aprire una finestra.

    La verifica viene fatta in un processo separato con un tempo massimo: su alcuni sistemi
    (per esempio dentro strumenti di automazione senza sessione grafica) la creazione della
    finestra si blocca, e in quel caso è meglio saperlo subito invece di restare appesi.
    Il risultato viene ricordato.
    """
    global _TK_DISPONIBILE
    if _TK_DISPONIBILE is None:
        if tk._default_root is not None:
            _TK_DISPONIBILE = True
        else:
            _TK_DISPONIBILE = _prova_finestra(timeout)
    return _TK_DISPONIBILE


def _prova_finestra(timeout: float) -> bool:
    import subprocess
    import sys

    codice = "import tkinter as tk; r=tk.Tk(); r.withdraw(); r.update(); r.destroy()"
    try:
        esito = subprocess.run(
            [sys.executable, "-c", codice],
            capture_output=True,
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError):
        return False
    return esito.returncode == 0


class StepIndicator(ttk.Frame):
    """Barra dei passi della procedura guidata, con quello attuale evidenziato."""

    def __init__(self, parent: tk.Misc, steps: Sequence[str]) -> None:
        super().__init__(parent)
        self.steps = list(steps)
        self.current = 0
        self._etichette: list[ttk.Label] = []
        for indice, nome in enumerate(self.steps, start=1):
            etichetta = ttk.Label(self, text=f"{indice}. {nome}", padding=(8, 4))
            etichetta.grid(row=0, column=indice, padx=6)
            self._etichette.append(etichetta)
        self.set_step(0)

    def set_step(self, index: int) -> None:
        self.current = max(0, min(index, len(self.steps) - 1))
        for posizione, etichetta in enumerate(self._etichette):
            if posizione == self.current:
                etichetta.configure(foreground=COLORI["primario"], font=font(12, bold=True))
            elif posizione < self.current:
                etichetta.configure(foreground=COLORI["successo"], font=font(12))
            else:
                etichetta.configure(foreground=COLORI["tenue"], font=font(12))


class LogPane(ttk.Frame):
    """Area di testo scorrevole con il dettaglio di quello che succede."""

    def __init__(self, parent: tk.Misc, height: int = 8) -> None:
        super().__init__(parent)
        self.text = tk.Text(
            self, height=height, wrap="word", state="disabled", font=font(11), background=COLORI["pannello"]
        )
        self.text.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=barra.set)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def append(self, testo: str) -> None:
        self.text.configure(state="normal")
        self.text.insert("end", testo.rstrip("\n") + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def get_text(self) -> str:
        return self.text.get("1.0", "end").strip()


class Banner(ttk.Frame):
    """Messaggio grande con suggerimento: è il modo principale con cui l'app parla all'utente."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.message_text = ""
        self.hint_text = ""
        self.kind = "info"
        self.visible = False
        self._messaggio = ttk.Label(
            self, text="", font=font(15, bold=True), wraplength=860, justify="left"
        )
        self._suggerimento = ttk.Label(self, text="", font=font(12), wraplength=860, justify="left")
        self._messaggio.grid(row=0, column=0, sticky="w")
        self._suggerimento.grid(row=1, column=0, sticky="w")
        self.columnconfigure(0, weight=1)

    def show(self, message: str, hint: str = "", kind: str = "info") -> None:
        self.message_text, self.hint_text, self.kind = message, hint, kind
        colore = {
            "info": COLORI["testo"],
            "successo": COLORI["successo"],
            "avviso": COLORI["avviso"],
            "errore": COLORI["errore"],
        }.get(kind, COLORI["testo"])
        self._messaggio.configure(text=message, foreground=colore)
        self._suggerimento.configure(text=hint, foreground=COLORI["tenue"])
        self.visible = True
        self.grid()

    def hide(self) -> None:
        self.visible = False
        self.grid_remove()


class PathChooser(ttk.Frame):
    """Riquadro con il percorso scelto e il pulsante «Sfoglia…»."""

    def __init__(self, parent: tk.Misc, on_change: Callable[[str], None] | None = None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._variabile = tk.StringVar()
        self.campo = ttk.Entry(self, textvariable=self._variabile, font=font(12))
        self.campo.grid(row=0, column=0, sticky="ew")
        self.bottone = ttk.Button(self, text="Sfoglia…", style="Secondary.TButton", command=self.browse)
        self.bottone.grid(row=0, column=1, padx=6)
        self.columnconfigure(0, weight=1)

    def get(self) -> str:
        return self._variabile.get()

    def set(self, path: str) -> None:
        self._variabile.set(path)
        if self._on_change is not None:
            self._on_change(path)

    def browse(self) -> None:
        scelta = filedialog.askdirectory(
            initialdir=self.get() or None, title="Scegli dove salvare le foto"
        )
        if scelta:
            self.set(scelta)

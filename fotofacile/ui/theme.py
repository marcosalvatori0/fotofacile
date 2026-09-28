"""Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma."""

from __future__ import annotations

import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

FONT_PREFERITI = ("Segoe UI", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", "Arial")
COLORI = {
    "sfondo": "#f2f4f7",
    "pannello": "#ffffff",
    "testo": "#1f2430",
    "tenue": "#5b6472",
    "primario": "#1565c0",
    "primario_attivo": "#0d47a1",
    "successo": "#1b7f4b",
    "avviso": "#b26a00",
    "errore": "#b3261e",
    "bordo": "#d4d8e0",
}
_FAMIGLIA = FONT_PREFERITI[-1]


def pick_font_family(available: set[str] | None = None) -> str:
    """Scegliе il primo font preferito presente sul sistema (Windows, macOS o Linux)."""
    if available is None:
        try:
            available = set(tkfont.families())
        except (AttributeError, tk.TclError):  # pragma: no cover - ambienti senza schermo
            available = set()
    for preferito in FONT_PREFERITI:
        if preferito in available:
            return preferito
    return FONT_PREFERITI[-1]


def font(size: int = 12, bold: bool = False) -> tuple:
    """Tupla (famiglia, dimensione[, stile]) usabile da Tkinter."""
    return (_FAMIGLIA, size, "bold") if bold else (_FAMIGLIA, size)


def _tema_disponibile(root: tk.Misc) -> str:
    stile = ttk.Style(root)
    disponibili = set(stile.theme_names())
    preferiti = ["vista", "aqua", "clam"] if sys.platform == "win32" else ["aqua", "clam", "vista"]
    for nome in preferiti:
        if nome in disponibili:
            return nome
    return stile.theme_use()  # pragma: no cover - Tk ha sempre un tema attivo


def apply_theme(root: tk.Misc, available_families: set[str] | None = None) -> None:
    """Applica tema e stile: vista su Windows, aqua su macOS, clam su Linux."""
    global _FAMIGLIA
    _FAMIGLIA = pick_font_family(available_families)
    stile = ttk.Style(root)
    stile.theme_use(_tema_disponibile(root))
    root.configure(background=COLORI["sfondo"])
    stile.configure(".", background=COLORI["sfondo"], foreground=COLORI["testo"], font=font(12))
    stile.configure("TFrame", background=COLORI["sfondo"])
    stile.configure("TLabel", background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.configure("Titolo.TLabel", font=font(22, bold=True))
    stile.configure("Sottotitolo.TLabel", font=font(14), foreground=COLORI["tenue"])
    stile.configure("Tenue.TLabel", foreground=COLORI["tenue"])
    stile.configure("Successo.TLabel", foreground=COLORI["successo"], font=font(14, bold=True))
    stile.configure("Avviso.TLabel", foreground=COLORI["avviso"])
    stile.configure("Errore.TLabel", foreground=COLORI["errore"])
    stile.configure("Big.TButton", font=font(14, bold=True), padding=(18, 12))
    stile.configure("Secondary.TButton", font=font(12), padding=(10, 6))
    stile.configure("Barra.Horizontal.TProgressbar", troughcolor=COLORI["bordo"])

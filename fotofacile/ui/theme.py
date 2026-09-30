"""Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.

Perché il tema `clam` e non `aqua`/`vista`: i temi nativi di macOS e Windows **ignorano**
i colori impostati (sfondo dei testi compreso). In modalità scura questo produceva testo
scuro su fondo scuro, cioè una finestra praticamente illeggibile. `clam` è disegnato da Tk
e rispetta sempre la tavolozza scelta: l'aspetto resta coerente e leggibile su Windows,
macOS e Linux, in modalità chiara e scura.
"""

from __future__ import annotations

import subprocess
import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from typing import Callable

FONT_PREFERITI = ("Segoe UI", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", "Arial")

PALETTE: dict[str, dict[str, str]] = {
    "chiaro": {
        "sfondo": "#f2f4f7",
        "pannello": "#ffffff",
        "testo": "#1f2430",
        "tenue": "#5b6472",
        "primario": "#1565c0",
        "primario_attivo": "#0d47a1",
        "successo": "#146c43",
        "avviso": "#8a5200",
        "errore": "#b3261e",
        "bordo": "#d4d8e0",
        "campo": "#ffffff",
        "selezione": "#cdd9f0",
        "barra": "#dbe2ef",
    },
    "scuro": {
        "sfondo": "#1c2128",
        "pannello": "#242b35",
        "testo": "#f2f5f9",
        "tenue": "#b6c0cd",
        "primario": "#6aa9f0",
        "primario_attivo": "#8cc0f7",
        "successo": "#7fd39b",
        "avviso": "#f0c268",
        "errore": "#ff9a92",
        "bordo": "#3a4653",
        "campo": "#2d3540",
        "selezione": "#33507a",
        "barra": "#2d3540",
    },
}
# Tavolozza attiva: viene aggiornata **in loco** da apply_theme, così chi ha già
# importato COLORI vede subito i colori giusti.
COLORI: dict[str, str] = dict(PALETTE["chiaro"])
_FAMIGLIA = FONT_PREFERITI[-1]
_SCURO = False


def _canale(valore: float) -> float:
    valore = valore / 255
    return valore / 12.92 if valore <= 0.03928 else ((valore + 0.055) / 1.055) ** 2.4


def luminanza(colore: str) -> float:
    """Luminanza relativa di un colore «#rrggbb» (formula WCAG)."""
    rosso, verde, blu = (int(colore[i : i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _canale(rosso) + 0.7152 * _canale(verde) + 0.0722 * _canale(blu)


def contrasto(primo: str, secondo: str) -> float:
    """Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono)."""
    chiaro, scuro = sorted((luminanza(primo), luminanza(secondo)), reverse=True)
    return (chiaro + 0.05) / (scuro + 0.05)


def sistema_scuro(system: str | None = None, runner: Callable[..., object] | None = None) -> bool:
    """True se il sistema è in modalità scura (Windows, macOS o Linux)."""
    sistema = system or sys.platform
    esegui = runner or subprocess.run
    try:
        if sistema == "darwin":
            esito = esegui(["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True, text=True)
            return "dark" in str(getattr(esito, "stdout", "") or "").lower()
        if sistema == "win32":  # pragma: no cover - verificato solo su Windows
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            ) as chiave:
                valore, _ = winreg.QueryValueEx(chiave, "AppsUseLightTheme")
            return valore == 0
        if sistema == "linux":  # pragma: no cover - verificato solo su Linux
            esito = esegui(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True,
                text=True,
            )
            return "dark" in str(getattr(esito, "stdout", "") or "").lower()
    except Exception:
        return False
    return False


def pick_font_family(available: set[str] | None = None) -> str:
    """Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)."""
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


def apply_theme(
    root: tk.Misc,
    available_families: set[str] | None = None,
    scuro: bool | None = None,
) -> None:
    """Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra."""
    global _FAMIGLIA, _SCURO
    modalita = sistema_scuro() if scuro is None else scuro
    _SCURO = modalita
    tavolozza = PALETTE["scuro" if modalita else "chiaro"]
    COLORI.clear()
    COLORI.update(tavolozza)

    _FAMIGLIA = pick_font_family(available_families)
    stile = ttk.Style(root)
    stile.theme_use("clam")  # unico tema che rispetta i colori su tutti i sistemi
    root.configure(background=COLORI["sfondo"])

    stile.configure(".", background=COLORI["sfondo"], foreground=COLORI["testo"], font=font(12))
    for stile_base in ("TFrame", "TLabelframe", "TLabelframe.Label"):
        stile.configure(stile_base, background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.configure("TLabel", background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.configure(
        "Titolo.TLabel", font=font(22, bold=True), background=COLORI["sfondo"], foreground=COLORI["testo"]
    )
    stile.configure("Sottotitolo.TLabel", font=font(14), background=COLORI["sfondo"], foreground=COLORI["tenue"])
    stile.configure("Tenue.TLabel", background=COLORI["sfondo"], foreground=COLORI["tenue"])
    stile.configure(
        "Successo.TLabel", background=COLORI["sfondo"], foreground=COLORI["successo"], font=font(14, bold=True)
    )
    stile.configure("Avviso.TLabel", background=COLORI["sfondo"], foreground=COLORI["avviso"])
    stile.configure("Errore.TLabel", background=COLORI["sfondo"], foreground=COLORI["errore"])

    stile.configure(
        "Big.TButton",
        font=font(14, bold=True),
        padding=(18, 12),
        background=COLORI["primario"],
        foreground=COLORI["pannello"] if not modalita else COLORI["sfondo"],
    )
    stile.map("Big.TButton", background=[("active", COLORI["primario_attivo"])])
    stile.configure("Secondary.TButton", font=font(12), padding=(10, 6))
    stile.map("Secondary.TButton", background=[("active", COLORI["selezione"])])
    stile.configure("TCheckbutton", background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.map("TCheckbutton", background=[("active", COLORI["sfondo"])])
    stile.configure(
        "TEntry",
        fieldbackground=COLORI["campo"],
        foreground=COLORI["testo"],
        insertcolor=COLORI["testo"],
        bordercolor=COLORI["bordo"],
    )
    stile.configure(
        "TCombobox",
        fieldbackground=COLORI["campo"],
        background=COLORI["campo"],
        foreground=COLORI["testo"],
        arrowcolor=COLORI["testo"],
    )
    stile.map("TCombobox", fieldbackground=[("readonly", COLORI["campo"])])
    stile.configure(
        "Barra.Horizontal.TProgressbar",
        troughcolor=COLORI["barra"],
        background=COLORI["primario"],
        bordercolor=COLORI["bordo"],
        lightcolor=COLORI["primario"],
        darkcolor=COLORI["primario"],
    )
    stile.configure("TScrollbar", background=COLORI["barra"], troughcolor=COLORI["sfondo"], arrowcolor=COLORI["testo"])


# ── widget Tk «classici» ──────────────────────────────────────────────────
# Text, Canvas e Listbox non sono ttk: gli stili di `apply_theme` non li toccano. Se si
# imposta solo lo sfondo, il testo resta nero su un pannello scuro — cioè invisibile.
# Queste funzioni sono l'unico posto dove si colorano.


def tema_testo(testo: tk.Text) -> None:
    """Colora un'area di testo classica: sfondo **e** testo, cursore e selezione compresi."""
    testo.configure(
        background=COLORI["campo"],
        foreground=COLORI["testo"],
        insertbackground=COLORI["testo"],
        selectbackground=COLORI["selezione"],
        selectforeground=COLORI["testo"],
        highlightthickness=1,
        highlightbackground=COLORI["bordo"],
        highlightcolor=COLORI["primario"],
        borderwidth=0,
    )


def tema_tela(tela: tk.Canvas) -> None:
    """Colora una superficie di disegno, allineandola al pannello."""
    tela.configure(background=COLORI["pannello"], highlightthickness=0)


def tema_finestra(finestra: tk.Misc) -> None:
    """Colora una finestra secondaria come quella principale.

    Serve a evitare il bordo grigio chiaro attorno a una finestra scura su macOS e Windows:
    il `Toplevel` di Tk usa i colori di sistema finché non glieli si impone.
    """
    finestra.configure(background=COLORI["sfondo"])

"""Passo 2: scelta delle foto (contenuto in arrivo)."""

from __future__ import annotations

from tkinter import ttk


class SelectPage(ttk.Frame):
    """Seconda schermata della procedura guidata."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        ttk.Label(self, text="Scegli cosa copiare", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")

    def on_show(self) -> None:
        pass

"""Passo 4: copia e resoconto (contenuto in arrivo)."""

from __future__ import annotations

from tkinter import ttk


class TransferPage(ttk.Frame):
    """Quarta schermata della procedura guidata."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        ttk.Label(self, text="Copia in corso", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")

    def on_show(self) -> None:
        pass

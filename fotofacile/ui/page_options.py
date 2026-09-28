"""Passo 3: destinazione e opzioni (contenuto in arrivo)."""

from __future__ import annotations

from tkinter import ttk


class OptionsPage(ttk.Frame):
    """Terza schermata della procedura guidata."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        ttk.Label(self, text="Dove vuoi salvare le foto?", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w"
        )

    def on_show(self) -> None:
        pass

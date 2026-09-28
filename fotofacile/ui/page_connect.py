"""Passo 1: guidare la persona a collegare il telefono (contenuto in arrivo)."""

from __future__ import annotations

from tkinter import ttk


class ConnectPage(ttk.Frame):
    """Prima schermata della procedura guidata."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.message = ""
        self._polling = False
        ttk.Label(self, text="Collega il telefono al computer", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w"
        )

    def on_show(self) -> None:
        pass

    def start_polling(self) -> None:
        self._polling = True

    def stop_polling(self) -> None:
        self._polling = False

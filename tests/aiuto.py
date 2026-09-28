"""Funzioni di appoggio per i test della grafica."""

from __future__ import annotations

import time


def attendi(applicazione, condizione, passi: int = 200, pausa: float = 0.002) -> bool:
    """Fa girare il ciclo della grafica finché la condizione non è vera (o scade)."""
    for _ in range(passi):
        applicazione.update()
        if condizione():
            return True
        time.sleep(pausa)
    return False

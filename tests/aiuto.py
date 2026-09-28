"""Funzioni di appoggio per i test della grafica."""

from __future__ import annotations


def attendi(applicazione, condizione, passi: int = 100) -> bool:
    """Fa girare il ciclo della grafica finché la condizione non è vera (o scade)."""
    for _ in range(passi):
        applicazione.update()
        applicazione.pump_events()
        if condizione():
            return True
    return False

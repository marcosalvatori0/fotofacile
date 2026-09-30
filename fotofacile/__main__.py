"""Avvio del programma con «python -m fotofacile».

Serve ai processi figli (l'aiutante che parla con il telefono, la prova che la finestra si
apra) quando il programma non è impacchettato: così si possono avviare senza sapere dove si
trova il file di avvio del progetto.

    python -m fotofacile
    python -m fotofacile doctor
    python -m fotofacile --aiutante ptp_mac elenca
"""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

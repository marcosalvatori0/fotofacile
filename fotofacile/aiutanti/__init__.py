"""Programmi aiutanti: un modo di parlare con il telefono per ogni sistema operativo.

Il programma principale non conosce i dettagli di nessun sistema: avvia l'aiutante adatto,
gli parla sempre allo stesso modo (righe JSON) e legge il risultato. Per sapere *quale*
aiutante usare, e se è utilizzabile, guarda :mod:`fotofacile.core.trasporto`.

Gli aiutanti non vengono mai importati all'avvio: su macOS importare PyObjC è costoso e
inutile se il collegamento diretto non serve.
"""

from __future__ import annotations

import importlib
import importlib.util
from typing import Sequence

#: Nome dell'aiutante → modulo Python che lo implementa.
MODULI = {
    "ptp_mac": "fotofacile.aiutanti.ptp_mac",
    "mtp_linux": "fotofacile.aiutanti.mtp_linux",
    "wpd_win": "fotofacile.aiutanti.wpd_win",
}


def modulo_disponibile(nome: str) -> bool:
    """True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio."""
    percorso = MODULI.get(nome)
    if percorso is None:
        return False
    try:
        return importlib.util.find_spec(percorso) is not None
    except (ImportError, ValueError):  # pragma: no cover - difensivo
        return False


def carica(nome: str):
    """Importa il modulo dell'aiutante, o solleva KeyError se non esiste."""
    percorso = MODULI.get(nome)
    if percorso is None:
        raise KeyError(nome)
    return importlib.import_module(percorso)


def esegui(nome: str, argomenti: Sequence[str]) -> int:
    """Esegue un aiutante e restituisce il suo codice di uscita."""
    return carica(nome).main(list(argomenti))

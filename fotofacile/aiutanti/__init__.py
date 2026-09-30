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
from typing import Callable, Sequence

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
    modulo = carica(nome)
    ripristina = _termina_con_ordine()
    try:
        return modulo.main(list(argomenti))
    finally:
        ripristina()


def _termina_con_ordine() -> Callable[[], object]:
    """Trasforma la richiesta di terminare (SIGTERM) in un'uscita ordinata.

    Il programma principale ferma l'aiutante con SIGTERM (annullo, tempo scaduto,
    chiusura della finestra). Senza un gestore Python muore all'istante e nessun
    ``finally`` scatta: restavano la cartella temporanea con la foto scaricata (macOS) e i
    comandi figli vivi e orfani, come ``jmtpfs`` o ``gio mount`` (Linux). Con
    ``SystemExit`` le pulizie scattano e ``subprocess.run`` uccide il comando figlio.
    Su Windows il segnale non arriva (l'aiutante viene chiuso di netto): lì provvede la
    sorveglianza di PowerShell (``-PidSupervisionato``).
    """
    import signal

    def interrompi(_numero, _quadro):
        raise SystemExit(2)

    try:
        precedente = signal.signal(signal.SIGTERM, interrompi)
    except (AttributeError, OSError, ValueError):  # pragma: no cover - sistema senza SIGTERM
        return lambda: None
    if precedente is None:  # pragma: no cover - gestore installato fuori da Python
        precedente = signal.SIG_DFL
    return lambda: signal.signal(signal.SIGTERM, precedente)

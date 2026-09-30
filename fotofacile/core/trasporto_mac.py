"""Collegamento diretto su macOS: PTP/MTP tramite ImageCaptureCore.

macOS non ha un modo di leggere i telefoni Android come dischi. Il telefono però si presenta
sempre anche come «fotocamera», e questo macOS lo sa leggere — è lo stesso meccanismo
dell'applicazione «Acquisizione immagini». Non serve attivare niente.

Tutto il lavoro delicato (ciclo di eventi Cocoa, sessioni, lettura a blocchi) sta
nell'aiutante :mod:`fotofacile.aiutanti.ptp_mac`, che gira in un processo separato: così non
può bloccare la finestra.
"""

from __future__ import annotations


from .osutil import chiave_sistema
from .trasporto_aiutante import TrasportoAiutante


class TrasportoPtpMac(TrasportoAiutante):
    """Telefono collegato via cavo su macOS, senza Debug USB."""

    nome = "Collegamento diretto"
    spiegazione = (
        "Uso il collegamento normale del telefono: non serve attivare il Debug USB."
    )
    aiutante = "ptp_mac"

    def disponibile(self) -> bool:
        """True se siamo su macOS e il componente di sistema è raggiungibile.

        Il controllo non importa PyObjC (è costoso): si limita a verificare che i moduli ci
        siano. L'import vero avviene solo nel processo aiutante.
        """
        if chiave_sistema() != "darwin":
            return False
        import importlib.util

        for modulo in ("objc", "ImageCaptureCore"):
            try:
                if importlib.util.find_spec(modulo) is None:
                    return False
            except (ImportError, ValueError):  # pragma: no cover - difensivo
                return False
        return True

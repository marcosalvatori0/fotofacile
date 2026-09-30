"""Collegamento diretto su Linux: MTP tramite ``gio``/gvfs, con ``jmtpfs`` di ripiego.

Il desktop Linux sa già leggere i telefoni MTP: è lo stesso meccanismo del gestore file
(«File»/Nautilus), che si appoggia a ``gio`` e ai montaggi gvfs. Anche qui tutto il lavoro
delicato sta in un aiutante separato (:mod:`fotofacile.aiutanti.mtp_linux`), per due
motivi: ``gio mount`` può chiedere un'autorizzazione al desktop e, con un telefono
bloccato, può restare appeso; in un processo a parte si può interrompere senza mai
bloccare la finestra. Il montaggio però non è del processo ma del desktop, quindi resta
vivo fra un comando e l'altro (come quando si apre il telefono da «File») e non si rimonta
per ogni foto.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable, Generator

from .osutil import flag_nascosta, chiave_sistema
from .scanner import MediaFile
from .trasporto_aiutante import INTERVALLO, TrasportoAiutante

#: Alla chiusura non si può restare appesi a un telefono bloccato.
TIMEOUT_SMONTA = 15.0


def _eseguibile(nome: str) -> str | None:
    """Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei test)."""
    import shutil

    return shutil.which(nome)


class TrasportoMtpLinux(TrasportoAiutante):
    """Telefono collegato via cavo su Linux, senza Debug USB."""

    nome = "Collegamento diretto"
    spiegazione = (
        "Uso il collegamento del desktop al telefono (lo stesso di «File»): "
        "non serve attivare il Debug USB."
    )
    aiutante = "mtp_linux"

    def __init__(self, env=None, intervallo: float = INTERVALLO) -> None:
        super().__init__(env=env, intervallo=intervallo)
        #: I telefoni usati in questa sessione: vanno smontati alla chiusura.
        self._usati: set[str] = set()

    def disponibile(self) -> bool:
        """True solo su Linux e solo se c'è un modo per montare l'MTP."""
        if chiave_sistema() != "linux":
            return False
        return _eseguibile("gio") is not None or _eseguibile("jmtpfs") is not None

    # ── le operazioni segnano il telefono usato ───────────────────────────
    # Il montaggio è del desktop (gvfs) e sopravvive a questo oggetto: per poterlo
    # smontare alla chiusura bisogna ricordarsi quali telefoni sono stati toccati.

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        self._usati.add(serial)
        return (
            yield from super().cerca_media(
                serial, include_videos=include_videos, annulla=annulla
            )
        )

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        self._usati.add(serial)
        return (
            yield from super().copia(
                serial,
                remoto,
                destinazione,
                on_scritti=on_scritti,
                annulla=annulla,
                remoto_dimensione=remoto_dimensione,
            )
        )

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        self._usati.add(serial)
        return (yield from super().cancella(serial, remoto))

    def pulisci(self) -> None:
        """Chiude i processi rimasti e smonta i telefoni usati.

        Smontare alla chiusura libera il telefono: se restasse montato, la Galleria e gli
        altri programmi del computer lo vedrebbero «occupato». È quello che fa anche il
        gestore file quando si chiude la finestra del telefono. La pulizia non deve mai
        bloccare la chiusura: ogni errore viene ignorato.
        """
        super().pulisci()
        for seriale in list(self._usati):
            try:
                subprocess.run(
                    [*self.base(), "smonta", "--seriale", seriale],
                    timeout=TIMEOUT_SMONTA,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=flag_nascosta(),
                )
            except (OSError, subprocess.TimeoutExpired):
                continue
        self._usati.clear()

"""Collegamento diretto su Windows: WPD tramite ``Shell.Application``.

Windows non mostra i telefoni Android come dischi, ma come «dispositivi portatili» dentro
«Questo PC»: è lo stesso meccanismo di Esplora file. Il lavoro delicato (componente COM,
copie asincrone, enumerazione) sta nell'aiutante :mod:`fotofacile.aiutanti.wpd_win`, che
gira in un processo separato: così una copia lenta o un telefono bloccato non possono
fermare la finestra.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Callable, Generator

from .adb_passi import _controlla_spazio, _esito_di_copia, percorso_temporaneo
from .errors import FotoFacileError, traduci_errore_file
from .ops import Annullato
from .osutil import chiave_sistema
from .trasporto_aiutante import (
    TIMEOUT_COPIA,
    TrasportoAiutante,
    _dimensione,
    _rallenta_scrittura,
)

#: Quanti tentativi (da 0,1 s) per togliere il file «a metà» tenuto aperto dall'aiutante.
TENTATIVI_RIMOZIONE = 15


def _rimuovi_con_pazienza(percorso: Path) -> None:
    """Toglie il file «a metà» anche se l'aiutante di Windows lo tiene ancora aperto.

    Su Windows un file aperto non si può cancellare: quando l'utente annulla, il processo
    dell'aiutante muore subito, ma PowerShell (che è un processo figlio) se ne accorge
    entro un istante e chiude il file. Riprovare per un breve periodo evita di lasciare un
    ``.part`` nella cartella delle foto.
    """
    for tentativo in range(TENTATIVI_RIMOZIONE):
        try:
            percorso.unlink(missing_ok=True)
            return
        except OSError:
            if tentativo == TENTATIVI_RIMOZIONE - 1:
                return  # non è un buon motivo per far fallire l'operazione
            time.sleep(0.1)


def _rimuovi_cartella_con_pazienza(percorso: Path) -> None:
    """Toglie la cartella di appoggio, anche se contiene un file ancora aperto.

    La cartella è nostra (creata con :func:`tempfile.mkdtemp`): l'aiutante non la cancella
    da sé, perché se il suo processo venisse interrotto di netto il ``finally`` non
    scatterebbe comunque. Così invece è il programma principale a ripulire, sempre.
    """
    for tentativo in range(TENTATIVI_RIMOZIONE):
        shutil.rmtree(percorso, ignore_errors=True)
        if not percorso.exists():
            return
        if tentativo < TENTATIVI_RIMOZIONE - 1:
            time.sleep(0.1)


class TrasportoWpdWindows(TrasportoAiutante):
    """Telefono collegato via cavo su Windows, senza Debug USB."""

    nome = "Collegamento diretto"
    spiegazione = (
        "Uso il collegamento di Windows al telefono (lo stesso di Esplora file): "
        "non serve attivare il Debug USB."
    )
    aiutante = "wpd_win"

    def disponibile(self) -> bool:
        """True solo su Windows: l'aiutante è uno script PowerShell di Windows."""
        return chiave_sistema() == "win32"

    # ── copia ─────────────────────────────────────────────────────────────
    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        """Copia un file passando dal file di appoggio che l'aiutante prepara.

        Perché questa è l'unica operazione riscritta invece di usare quella condivisa:
        ``CopyHere``, l'unica copia offerta da Windows per i dispositivi portatili, è
        asincrona e non sa scrivere su un flusso. Quindi l'aiutante copia prima il file in
        una cartella di appoggio (creata qui dentro la destinazione scelta dall'utente e
        indicata con ``--destinazione``) e poi ce lo consegna byte per byte sull'uscita
        standard. La cartella di appoggio è creata e cancellata da questo file, non
        dall'aiutante: se Windows interrompe di netto il processo dell'aiutante, non
        resta mezza foto nella cartella delle foto. Per il resto non cambia niente: i byte
        arrivano in ordine, il ``.part`` è gestito come sugli altri sistemi e lo spazio su
        disco è controllato prima di iniziare.
        """
        destinazione = Path(destinazione)
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
        except OSError as errore:
            raise traduci_errore_file(errore, destinazione) from errore
        _controlla_spazio(destinazione)
        temporaneo = percorso_temporaneo(destinazione)
        try:
            appoggio = Path(
                tempfile.mkdtemp(prefix="fotofacile-appoggio-", dir=str(destinazione.parent))
            )
        except OSError as errore:
            raise traduci_errore_file(errore, destinazione) from errore
        scritti = 0
        completato = False
        processo = None
        try:
            processo = self._avvia(
                [
                    "copia",
                    "--seriale",
                    serial,
                    "--percorso",
                    remoto,
                    "--destinazione",
                    str(appoggio),
                ],
                TIMEOUT_COPIA,
                f"Non sono riuscito a copiare {destinazione.name}.",
                "Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
                output_file=temporaneo,
            )
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    raise Annullato()
                if processo.scaduto():
                    raise FotoFacileError(
                        f"La copia di {destinazione.name} è durata troppo tempo.",
                        hint="Riprova: se succede sempre con i video, prova un altro cavo USB.",
                    )
                scritti = _dimensione(temporaneo, scritti, on_scritti)
                yield self.intervallo
            scritti = _dimensione(temporaneo, scritti, on_scritti)
            _esito_di_copia(processo, destinazione)
            _rallenta_scrittura(temporaneo)
            try:
                os.replace(temporaneo, destinazione)
            except OSError as errore:
                raise traduci_errore_file(errore, destinazione) from errore
            completato = True
        finally:
            if processo is not None:
                processo.termina()
            if not completato:
                _rimuovi_con_pazienza(temporaneo)
            _rimuovi_cartella_con_pazienza(appoggio)
        return scritti

    # ── cancellazione ─────────────────────────────────────────────────────
    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        """Spiega con calma che con WPD la cancellazione non è disponibile.

        L'aiutante termina sempre con codice 2 per questo comando: ``Shell.Application``
        (l'unico accesso non amministrativo ai dispositivi portatili) offre solo
        ``InvokeVerb("delete")``, che apre una richiesta di conferma. Con
        ``-NonInteractive`` quella richiesta resterebbe appesa per sempre, quindi si
        preferisce dire la verità invece di rischiare un blocco. Il Debug USB, se è già
        attivo, sa cancellare i file senza problemi.
        """
        try:
            yield from super().cancella(serial, remoto)
        except FotoFacileError as errore:
            raise FotoFacileError(
                "Con il collegamento di Windows non riesco a cancellare i file dal telefono.",
                hint=(
                    "Il file resta sul telefono: puoi cancellarlo dalla Galleria. "
                    "Se vuoi cancellarlo da qui, attiva il Debug USB sul telefono e riprova."
                ),
            ) from errore

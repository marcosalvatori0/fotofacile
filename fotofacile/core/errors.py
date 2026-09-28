"""Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento."""

from __future__ import annotations

from pathlib import Path


class FotoFacileError(Exception):
    """Errore con messaggio per l'utente e un suggerimento su come procedere."""

    #: True solo per gli errori che ha senso ritentare (per esempio il cavo mosso).
    ritentabile = False

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        return self.message if not self.hint else f"{self.message} {self.hint}"


class AdbError(FotoFacileError):
    """Errore di comunicazione con il telefono: spesso basta riprovare."""

    ritentabile = True


class TransferError(FotoFacileError):
    """Errore durante la copia di un file."""


def traduci_errore_file(errore: Exception, destinazione: Path) -> FotoFacileError:
    """Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile."""
    codice = getattr(errore, "errno", None)
    testo = str(errore).lower()
    if "no space" in testo or "disk full" in testo or codice == 28:
        return FotoFacileError(
            f"Non c'è più spazio sul disco mentre copiavo {destinazione.name}.",
            hint="Libera spazio e riprova: le foto già copiate sono al sicuro.",
        )
    if "permission" in testo or codice == 13:
        return FotoFacileError(
            f"Non ho il permesso di scrivere {destinazione.name} nella cartella scelta.",
            hint="Scegli un'altra cartella (per esempio Immagini) e riprova.",
        )
    if "read-only" in testo or codice == 30:
        return FotoFacileError(
            f"La cartella {destinazione.parent} è in sola lettura.",
            hint="Scegli un'altra cartella dove salvare le foto.",
        )
    return FotoFacileError(
        f"Non sono riuscito a copiare {destinazione.name}.",
        hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
    )

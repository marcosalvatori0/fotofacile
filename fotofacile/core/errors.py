"""Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento."""


class FotoFacileError(Exception):
    """Errore con messaggio per l'utente e un suggerimento su come procedere."""

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        return self.message if not self.hint else f"{self.message} {self.hint}"


class AdbError(FotoFacileError):
    """Errore di comunicazione con il telefono."""


class TransferError(FotoFacileError):
    """Errore durante la copia di un file."""

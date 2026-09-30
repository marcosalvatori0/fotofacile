"""Impostazioni personali (per ora: la dimensione del testo), salvate fra un avvio e l'altro."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from .osutil import app_dir

SCALE_AMMESSE = (1.0, 1.25, 1.5)
SCALA_PREDEFINITA = 1.25  # gli anziani sono il pubblico principale: si parte già «grande»


def scala_vicina(valore: object) -> float:
    """Riporta un valore qualunque alla scala ammessa più vicina (o al predefinito)."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        return SCALA_PREDEFINITA
    try:
        numero = float(valore)
    except OverflowError:  # un intero enorme nel file
        return SCALA_PREDEFINITA
    if not math.isfinite(numero):  # NaN o infinito
        return SCALA_PREDEFINITA
    return min(SCALE_AMMESSE, key=lambda ammessa: abs(ammessa - numero))


def percorso_impostazioni() -> Path:
    return app_dir() / "impostazioni.json"


@dataclass
class Impostazioni:
    scala_testo: float = SCALA_PREDEFINITA

    @classmethod
    def carica(cls, percorso: Path | None = None) -> "Impostazioni":
        """Legge le impostazioni; qualunque problema porta ai valori predefiniti."""
        destinazione = Path(percorso) if percorso is not None else percorso_impostazioni()
        try:
            contenuto = json.loads(destinazione.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        if not isinstance(contenuto, dict):
            return cls()
        return cls(scala_testo=scala_vicina(contenuto.get("scala_testo")))

    def salva(self, percorso: Path | None = None) -> None:
        """Scrive le impostazioni; se non si può, pazienza (non è mai un errore per l'utente)."""
        destinazione = Path(percorso) if percorso is not None else percorso_impostazioni()
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
            destinazione.write_text(json.dumps({"scala_testo": self.scala_testo}), encoding="utf-8")
        except OSError:
            pass

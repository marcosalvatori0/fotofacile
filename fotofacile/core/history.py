"""Archivio dei file già copiati, per non ricopiarli una seconda volta.

Separato per dispositivo: due telefoni diversi possono avere foto con lo stesso nome.
La scrittura è atomica e un file corrotto viene messo da parte invece di far crashare l'app.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from .osutil import app_dir

VERSIONE = 1


def default_path() -> Path:
    return app_dir() / "history.json"


class History:
    """Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_path()
        self._dati: dict[str, dict[str, dict]] = {}
        self._caricato = False

    # ── lettura e scrittura ───────────────────────────────────────────────
    def load(self) -> None:
        """Carica la cronologia; un file corrotto o malformato viene messo da parte, mai un errore."""
        self._dati = {}
        if self.path.is_file():
            try:
                contenuto = json.loads(self.path.read_text(encoding="utf-8"))
                dispositivi = contenuto.get("devices", {})
                if isinstance(dispositivi, dict):
                    self._dati = _solo_voci_valide(dispositivi)
            except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError):
                self._metti_da_parte_file_corrotto()
                self._dati = {}
            except OSError:
                # Il file c'è ma non si può leggere (permessi, disco di rete): si riparte da
                # una cronologia vuota, senza toccare il file dell'utente.
                self._dati = {}
        self._caricato = True

    def _metti_da_parte_file_corrotto(self) -> None:
        backup = self.path.with_name(f"{self.path.name}.corrupt-{int(time.time())}")
        try:
            self.path.replace(backup)
        except OSError:  # pragma: no cover - non deve mai bloccare l'utente
            pass

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Un'altra copia del programma può aver scritto nel frattempo: si riparte da ciò che
        # c'è su disco e si sovrappongono le voci di questa sessione (vincono le più recenti).
        su_disco = History(self.path)
        su_disco.load()
        for seriale, voci in self._dati.items():
            su_disco._dati.setdefault(seriale, {}).update(voci)
        self._dati = su_disco._dati
        temporaneo = self.path.with_name(self.path.name + ".tmp")
        contenuto = {"version": VERSIONE, "devices": self._dati}
        temporaneo.write_text(json.dumps(contenuto, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(temporaneo, self.path)

    # ── interrogazioni ────────────────────────────────────────────────────
    def contains(self, serial: str, rel_path: str, size: int, mtime: int) -> bool:
        """True se quel file, con la stessa dimensione e data, è già stato copiato."""
        voce = self._dati.get(serial, {}).get(rel_path)
        if not isinstance(voce, dict):
            # Voce malformata (file modificato a mano o di un'altra versione): si considera
            # «non copiato» invece di far saltare la pianificazione con un AttributeError.
            return False
        return voce.get("size") == size and voce.get("mtime") == mtime

    def record(self, serial: str, rel_path: str, size: int, mtime: int, dest: str) -> None:
        self._dati.setdefault(serial, {})[rel_path] = {"size": size, "mtime": mtime, "dest": dest}

    def count(self, serial: str) -> int:
        return len(self._dati.get(serial, {}))


def _solo_voci_valide(dispositivi: dict) -> dict[str, dict[str, dict]]:
    """Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in silenzio.

    Un file JSON può essere valido ma avere la struttura sbagliata (per esempio
    ``{"S1": {"/DCIM/a.jpg": 5}}``): senza questo controllo il programma si romperebbe più
    tardi, in un punto lontano e difficile da capire.
    """
    risultato: dict[str, dict[str, dict]] = {}
    for seriale, voci in dispositivi.items():
        if not isinstance(voci, dict):
            continue
        pulite: dict[str, dict] = {}
        for percorso, voce in voci.items():
            if not isinstance(voce, dict):
                continue
            if not isinstance(voce.get("size"), int) or not isinstance(voce.get("mtime"), int):
                continue
            pulite[str(percorso)] = voce
        if pulite:
            risultato[str(seriale)] = pulite
    return risultato

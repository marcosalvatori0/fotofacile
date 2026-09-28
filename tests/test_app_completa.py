"""Collaudo completo dell'applicazione vera (avvio → copia → resoconto).

Il collaudo gira in un **processo separato**: così la creazione della finestra non blocca la
suite di test e, sui computer senza sessione grafica (per esempio gli strumenti di
automazione), il test viene saltato con un motivo chiaro invece di restare appeso.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from fotofacile.ui.widgets import tk_available

RADICE = Path(__file__).resolve().parent.parent

pytestmark = pytest.mark.skipif(
    not tk_available(), reason="questo ambiente non riesce ad aprire finestre"
)


def test_app_completa_la_copia_in_modalita_demo(tmp_path):
    destinazione = tmp_path / "foto"
    esito_file = tmp_path / "esito.json"
    ambiente = {
        **os.environ,
        "HOME": str(tmp_path),
        "USERPROFILE": str(tmp_path),
        "FF_DEST": str(destinazione),
        "FF_ESITO": str(esito_file),
        "FF_SCADENZA": "120",
        "FF_PAUSA_MS": "100",
    }
    esito = subprocess.run(
        [sys.executable, str(RADICE / "tests" / "pilota_app.py")],
        capture_output=True,
        text=True,
        timeout=180,
        env=ambiente,
        cwd=RADICE,
    )
    assert esito_file.is_file(), f"nessun esito prodotto. stdout={esito.stdout} stderr={esito.stderr}"
    dati = json.loads(esito_file.read_text())
    assert dati["ok"] is True, dati
    assert dati["copiati"] >= 10
    assert dati["errori"] == []
    assert "Copiate" in dati["resoconto"]
    for percorso in dati["file"]:
        assert Path(percorso).is_file()
    copiati = sorted(destinazione.rglob("*"))
    scritti = [percorso for percorso in copiati if percorso.is_file()]
    assert len(scritti) >= 10
    assert not list(destinazione.rglob("*.part"))


def test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema(tmp_path):
    """Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice."""
    esito = subprocess.run(
        [sys.executable, "fotofacile.py", "doctor"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=RADICE,
        env={**os.environ, "HOME": str(tmp_path)},
    )
    assert esito.returncode == 0
    assert "FotoFacile" in esito.stdout
    assert "Tkinter:" in esito.stdout

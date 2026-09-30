"""L'aiutante per Windows (`wpd_win.ps1`) deve restare completo e avviabile.

Prima questi controlli stavano nei test della «cartella pronta per Windows»: con il
`Setup.exe` quella cartella non esiste più, ma l'aiutante che parla con il telefono (senza
Debug USB) è ancora indispensabile e va protetto lo stesso.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent


def test_il_progetto_porta_l_aiutante_per_windows():
    """Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non chiede
    il Debug USB — non può funzionare nella versione distribuita."""
    script = RADICE / "fotofacile" / "aiutanti" / "wpd_win.ps1"
    assert script.is_file(), "manca l'aiutante wpd_win.ps1"
    assert script.read_bytes().startswith(b"\xef\xbb\xbf"), "gli script .ps1 devono avere il BOM UTF-8"
    assert (RADICE / "fotofacile" / "aiutanti" / "wpd_win.py").is_file()
    for modulo in ("trasporto.py", "trasporto_aiutante.py", "trasporto_win.py"):
        assert (RADICE / "fotofacile" / "core" / modulo).is_file(), f"manca {modulo}"


def test_il_punto_di_avvio_esegue_la_diagnosi(tmp_path):
    """`python fotofacile.py doctor` (e quindi `FotoFacile.exe doctor`) arriva alla diagnosi,
    senza aprire la finestra. Qui lo si esegue davvero, in un processo separato."""
    esito = subprocess.run(
        [sys.executable, "fotofacile.py", "doctor"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=RADICE,
        env={
            "HOME": str(tmp_path),
            "USERPROFILE": str(tmp_path),
            "PATH": "",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )
    assert esito.returncode == 0, esito.stderr
    assert "FotoFacile" in esito.stdout
    assert "Sistema:" in esito.stdout

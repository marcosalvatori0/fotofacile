import re
import subprocess
import sys
from pathlib import Path

import pytest

import fotofacile

RADICE = Path(__file__).resolve().parent.parent


def test_la_versione_ha_la_forma_giusta():
    assert re.fullmatch(r"\d+\.\d+\.\d+", fotofacile.__version__)


def test_lo_script_stampa_la_stessa_versione():
    esito = subprocess.run([sys.executable, str(RADICE / "scripts" / "leggi_versione.py")],
                           capture_output=True, text=True, check=True)
    assert esito.stdout.strip() == fotofacile.__version__


@pytest.mark.xfail(reason="serve il Task D1")
def test_lo_script_iss_non_ha_una_versione_scritta_a_mano_diversa():
    iss = (RADICE / "installer" / "windows" / "FotoFacile.iss").read_text(encoding="utf-8-sig")
    # la versione arriva da /DVersione=…; il valore di ripiego deve coincidere con quello vero
    trovata = re.search(r'#define Versione "([^"]+)"', iss)
    assert trovata and trovata.group(1) == fotofacile.__version__

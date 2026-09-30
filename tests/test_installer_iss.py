import re
from pathlib import Path

import pytest

import fotofacile

RADICE = Path(__file__).resolve().parent.parent
ISS = RADICE / "installer" / "windows" / "FotoFacile.iss"


@pytest.fixture(scope="module")
def iss() -> str:
    return ISS.read_text(encoding="utf-8-sig")


def _direttiva(iss: str, nome: str) -> str:
    trovata = re.search(rf"^{nome}=(.*)$", iss, re.MULTILINE)
    assert trovata, f"manca {nome}="
    return trovata.group(1).strip()


def test_versione_di_ripiego_uguale_a_quella_del_programma(iss):
    assert re.search(rf'#define Versione "{re.escape(fotofacile.__version__)}"', iss)
    assert "#ifndef Versione" in iss  # la pipeline può passarla con /DVersione=


def test_l_id_dell_applicazione_non_cambia_mai(iss):
    # cambiarlo farebbe installare la 0.2 accanto alla 0.1 invece di aggiornarla
    assert "AppId={{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}" in iss


def test_installa_senza_amministratore_e_senza_finestra_di_scelta(iss):
    assert _direttiva(iss, "PrivilegesRequired") == "lowest"
    assert "PrivilegesRequiredOverridesAllowed" not in iss  # niente domanda incomprensibile


def test_finestra_ingrandita_e_stile_moderno(iss):
    assert _direttiva(iss, "WizardStyle") == "modern"
    assert int(_direttiva(iss, "WizardSizePercent").split(",")[0]) >= 120


def test_solo_windows_10_o_successivo_a_64_bit(iss):
    assert _direttiva(iss, "MinVersion") == "10.0"
    assert _direttiva(iss, "ArchitecturesAllowed") == "x64compatible"
    assert _direttiva(iss, "ArchitecturesInstallIn64BitMode") == "x64compatible"


def test_lingua_italiana(iss):
    assert 'MessagesFile: "compiler:Languages\\Italian.isl"' in iss


def test_niente_bat_ne_powershell_per_l_utente(iss):
    assert ".bat" not in iss.lower()
    assert ".ps1" not in iss.lower()


def test_i_file_di_testo_con_accenti_hanno_il_bom():
    grezzo = (RADICE / "installer" / "windows" / "Benvenuto.txt").read_bytes()
    assert grezzo.startswith(b"\xef\xbb\xbf"), "Inno Setup legge come ANSI i testi senza BOM"


def test_c_e_il_collegamento_alla_diagnosi(iss):
    assert 'Parameters: "doctor"' in iss


def test_disinstallazione_chiede_prima_di_togliere_i_dati_personali(iss):
    assert "[Code]" in iss and "MsgBox" in iss and ".fotofacile" in iss

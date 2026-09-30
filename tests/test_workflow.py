from pathlib import Path

import pytest
import yaml

RADICE = Path(__file__).resolve().parent.parent
FLUSSO = RADICE / ".github" / "workflows" / "build-installers.yml"
PROVA = RADICE / "installer" / "windows" / "prova-installazione.ps1"
VERIFICA = RADICE / "installer" / "windows" / "verifica-eseguibile.ps1"


@pytest.fixture(scope="module")
def testo() -> str:
    return FLUSSO.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def flusso(testo) -> dict:
    return yaml.safe_load(testo)


def _passi(flusso: dict, lavoro: str) -> list[dict]:
    return flusso["jobs"][lavoro]["steps"]


def test_la_versione_arriva_dal_codice_non_da_un_numero_scritto_due_volte(testo):
    assert "scripts/leggi_versione.py" in testo
    assert "/DVersione=" in testo


def test_l_installer_viene_provato_davvero_su_windows(testo):
    assert "/VERYSILENT" in PROVA.read_text(encoding="utf-8-sig")
    assert "prova-installazione.ps1" in testo


def test_ci_sono_i_checksum_e_il_log(testo):
    assert "SHA256SUMS.txt" in testo
    assert "log-installazione.txt" in testo


def test_pillow_e_nel_pacchetto_windows(testo):
    assert "pillow" in testo.lower()


def test_il_file_yaml_e_valido_e_ha_i_tre_lavori(flusso):
    assert set(flusso["jobs"]) == {"macos", "windows", "release"}


def test_la_release_parte_solo_da_un_tag_mai_da_push_o_pull_request(flusso):
    # «on» in YAML 1.1 diventa True: PyYAML lo legge così
    attivazioni = flusso.get("on", flusso.get(True))
    assert set(attivazioni) == {"push", "workflow_dispatch"}
    assert attivazioni["push"] == {"tags": ["v*"]}  # nessun ramo: i push normali non fanno nulla
    assert flusso["jobs"]["release"]["if"] == "startsWith(github.ref, 'refs/tags/v')"
    assert set(flusso["jobs"]["release"]["needs"]) == {"macos", "windows"}


def test_l_autocollaudo_di_macos_non_viene_mascherato(testo):
    assert "|| echo" not in testo  # un «|| echo» dopo un comando lo fa passare anche se fallisce


def test_windows_legge_l_esito_dai_file_non_dal_codice_di_uscita(flusso):
    """L'exe senza finestra nera non scrive su stdout: l'esito sta in selftest.txt."""
    verifica = VERIFICA.read_text(encoding="utf-8-sig")
    assert "selftest.txt" in verifica and "diagnosi.txt" in verifica
    assert "ConvertFrom-Json" in verifica
    assert "FOTOFACILE_NO_OPEN" in verifica  # niente Blocco note che tiene bloccato il runner
    assert "wpd_win.ps1" in verifica  # lo script del collegamento diretto è nel pacchetto
    assert "Conversione WebP: disponibile" in verifica  # Pillow è nel pacchetto
    comandi = "\n".join(p.get("run", "") for p in _passi(flusso, "windows"))
    assert "verifica-eseguibile.ps1" in comandi
    assert "dist\\FotoFacile\\FotoFacile.exe --selftest" not in comandi


def test_la_prova_dell_installatore_riusa_la_verifica_e_aspetta_la_disinstallazione():
    prova = PROVA.read_text(encoding="utf-8-sig")
    assert "verifica-eseguibile.ps1" in prova
    assert "unins000.exe" in prova
    assert "{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}_is1" in prova  # lo stesso AppId del .iss


@pytest.mark.parametrize("script", [PROVA, VERIFICA])
def test_gli_script_powershell_hanno_il_bom(script):
    assert script.read_bytes().startswith(b"\xef\xbb\xbf")


def test_il_lavoro_windows_costruisce_installa_e_carica_i_file_giusti(flusso):
    nomi = [p.get("name", "") for p in _passi(flusso, "windows")]
    ordine = [
        next(i for i, n in enumerate(nomi) if chiave in n)
        for chiave in ("Crea l'eseguibile", "Verifica l'eseguibile", "portatile", "Inno Setup",
                       "programma di installazione", "Prova davvero", "Somme di controllo", "Carica")
    ]
    assert ordine == sorted(ordine)
    carica = _passi(flusso, "windows")[-1]
    percorsi = carica["with"]["path"]
    for atteso in ("dist/installer/*.exe", "dist/*.zip", "dist/SHA256SUMS.txt", "log-installazione.txt"):
        assert atteso in percorsi
    assert carica["if"] == "always()"  # il log serve proprio quando la prova fallisce


def test_il_testo_della_release_non_parla_piu_di_debug_usb(flusso):
    passo = next(p for p in _passi(flusso, "release") if "softprops" in p.get("uses", ""))
    corpo = passo["with"]["body"]
    assert "Debug USB" not in corpo and "debug USB" not in corpo
    assert "Trasferimento file" in corpo
    assert "Esegui comunque" in corpo and "Ulteriori informazioni" in corpo
    assert "artefatti/**/SHA256SUMS.txt" in passo["with"]["files"]

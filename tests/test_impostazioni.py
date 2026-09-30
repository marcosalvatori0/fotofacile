from fotofacile.core.impostazioni import (
    SCALA_PREDEFINITA,
    SCALE_AMMESSE,
    Impostazioni,
    scala_vicina,
)


def test_predefinito_quando_il_file_non_esiste(tmp_path):
    assert Impostazioni.carica(tmp_path / "no.json").scala_testo == SCALA_PREDEFINITA


def test_salva_e_ricarica(tmp_path):
    percorso = tmp_path / "i.json"
    Impostazioni(scala_testo=1.5).salva(percorso)
    assert Impostazioni.carica(percorso).scala_testo == 1.5


def test_file_rovinato_o_valori_strani_non_rompono_niente(tmp_path):
    percorso = tmp_path / "i.json"
    percorso.write_text("{non è json", encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA
    percorso.write_text('{"scala_testo": "enorme"}', encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA
    percorso.write_text("[1, 2]", encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA


def test_la_scala_si_riporta_alla_piu_vicina_ammessa():
    assert scala_vicina(1.3) == 1.25
    assert scala_vicina(9) == SCALE_AMMESSE[-1]
    assert scala_vicina(0) == SCALE_AMMESSE[0]
    assert scala_vicina(None) == SCALA_PREDEFINITA


def test_salvataggio_in_cartella_non_scrivibile_non_solleva(tmp_path):
    bloccato = tmp_path / "file"
    bloccato.write_text("x")
    Impostazioni(scala_testo=1.0).salva(bloccato / "dentro.json")  # «file» non è una cartella


def test_valori_non_numeri_veri_tornano_al_predefinito(tmp_path):
    assert scala_vicina(True) == SCALA_PREDEFINITA
    assert scala_vicina(float("nan")) == SCALA_PREDEFINITA
    assert scala_vicina(float("inf")) == SCALA_PREDEFINITA
    assert scala_vicina(10**400) == SCALA_PREDEFINITA
    percorso = tmp_path / "i.json"
    percorso.write_text('{"scala_testo": 1' + "0" * 400 + "}", encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA

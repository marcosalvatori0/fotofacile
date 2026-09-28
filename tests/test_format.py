import pytest

from fotofacile.core.format import (
    format_date,
    format_duration,
    format_eta,
    format_size,
    format_speed,
    parse_date,
)


@pytest.mark.parametrize(
    ("byte", "atteso"),
    [
        (0, "0 B"),
        (512, "512 B"),
        (1024, "1,0 KB"),
        (1536, "1,5 KB"),
        (10 * 1024**2, "10,0 MB"),
        (3_650_722_022, "3,4 GB"),
        (-5, "0 B"),
    ],
)
def test_formato_dimensione(byte, atteso):
    assert format_size(byte) == atteso


def test_formato_velocita():
    assert format_speed(2 * 1024**2) == "2,0 MB/s"
    assert format_speed(0) == "—"
    assert format_speed(-1) == "—"


def test_formato_durata_e_tempo_rimanente():
    assert format_duration(45) == "45 secondi"
    assert format_duration(1) == "1 secondo"
    assert format_duration(60) == "1 minuto"
    assert format_duration(90) == "1 minuto e 30 secondi"
    assert format_duration(3725) == "1 ora e 2 minuti"
    assert format_eta(None) == "calcolo in corso…"
    assert format_eta(0) == "meno di un secondo"
    assert format_eta(90) == "circa 1 minuto e 30 secondi"


def test_formato_data_italiana():
    assert format_date(1_700_000_000) == "14/11/2023"


def test_parse_date_accetta_formati_comodi():
    assert parse_date("2024-05-01") is not None
    assert parse_date("01/05/2024") is not None
    assert parse_date("2024-05-01") == parse_date("01/05/2024")
    assert parse_date("2024-05-01") < parse_date("2024-05-02")


def test_parse_date_rifiuta_input_non_validi():
    assert parse_date("") is None
    assert parse_date("   ") is None
    assert parse_date("non una data") is None
    assert parse_date("2024-13-45") is None

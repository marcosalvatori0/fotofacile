from fotofacile.ui.theme import COLORI, FONT_PREFERITI, font, pick_font_family


def test_sceglie_il_primo_font_disponibile():
    assert pick_font_family({"DejaVu Sans", "Arial"}) == "DejaVu Sans"
    assert pick_font_family({"Segoe UI"}) == "Segoe UI"
    assert pick_font_family({"Helvetica Neue", "DejaVu Sans"}) == "Helvetica Neue"


def test_ricade_su_un_font_generico_se_nessuno_disponibile():
    assert pick_font_family(set()) == FONT_PREFERITI[-1]


def test_palette_completa_e_coerente():
    for chiave in ("sfondo", "testo", "primario", "successo", "errore", "avviso", "tenue", "pannello", "bordo"):
        assert COLORI[chiave].startswith("#")
        assert len(COLORI[chiave]) == 7


def test_font_restituisce_tupla_usabile_da_tkinter():
    normale = font(14)
    grassetto = font(14, bold=True)
    assert normale[1] == 14
    assert grassetto[2] == "bold"
    assert normale[0] == grassetto[0]
    assert len(normale) == 2


def test_tema_applicato_sceglie_un_font_del_sistema():
    import tkinter as tk

    from fotofacile.ui.theme import apply_theme
    from fotofacile.ui.widgets import tk_available
    import pytest

    if not tk_available():
        pytest.skip("serve un ambiente grafico")
    finestra = tk.Tk()
    finestra.withdraw()
    try:
        apply_theme(finestra)
        famiglia = font(12)[0]
        assert famiglia in FONT_PREFERITI
        assert famiglia != ""
    finally:
        finestra.destroy()

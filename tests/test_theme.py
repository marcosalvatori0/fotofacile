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


# ── modalità scura e chiara ──────────────────────────────────────────────
def test_riconosce_la_modalita_scura_di_macos():
    from fotofacile.ui.theme import sistema_scuro

    def runner(comando, **_kwargs):
        import subprocess

        return subprocess.CompletedProcess(comando, 0, stdout="Dark\n", stderr="")

    assert sistema_scuro(system="darwin", runner=runner) is True

    def runner_chiaro(comando, **_kwargs):
        import subprocess

        return subprocess.CompletedProcess(comando, 1, stdout="", stderr="")

    assert sistema_scuro(system="darwin", runner=runner_chiaro) is False


def test_modalita_scura_su_linux():
    from fotofacile.ui.theme import sistema_scuro

    def runner(comando, **_kwargs):
        import subprocess

        return subprocess.CompletedProcess(comando, 0, stdout="'prefer-dark'\n", stderr="")

    assert sistema_scuro(system="linux", runner=runner) is True


def test_modalita_scura_non_impedisce_l_avvio_se_il_comando_manca():
    from fotofacile.ui.theme import sistema_scuro

    def runner(comando, **_kwargs):
        raise FileNotFoundError("nessun comando")

    assert sistema_scuro(system="darwin", runner=runner) is False
    assert sistema_scuro(system="pianeta-x", runner=runner) is False


def test_tavolozza_chiara_e_scura_hanno_gli_stessi_nomi():
    from fotofacile.ui.theme import PALETTE

    assert set(PALETTE["chiaro"]) == set(PALETTE["scuro"])
    for tavolozza in PALETTE.values():
        for chiave in ("sfondo", "pannello", "testo", "tenue", "bordo", "primario"):
            assert tavolozza[chiave].startswith("#")


def test_modalita_scura_ha_contrasto_leggibile():
    """Il testo deve essere chiaro su sfondo scuro: era il difetto che rendeva l'app illeggibile."""
    from fotofacile.ui.theme import contrasto, PALETTE

    scuro = PALETTE["scuro"]
    chiaro = PALETTE["chiaro"]
    assert contrasto(scuro["testo"], scuro["sfondo"]) >= 7
    assert contrasto(scuro["testo"], scuro["pannello"]) >= 7
    assert contrasto(chiaro["testo"], chiaro["sfondo"]) >= 7
    assert contrasto(scuro["tenue"], scuro["sfondo"]) >= 4.5
    assert contrasto(scuro["errore"], scuro["sfondo"]) >= 4.5
    assert contrasto(scuro["successo"], scuro["sfondo"]) >= 4.5


def test_tema_rispetta_i_colori_in_modalita_scura():
    import tkinter as tk
    from tkinter import ttk

    from fotofacile.ui.theme import COLORI, PALETTE, apply_theme
    from fotofacile.ui.widgets import tk_available

    if not tk_available():
        import pytest

        pytest.skip("serve un ambiente grafico")
    finestra = tk.Tk()
    finestra.withdraw()
    try:
        apply_theme(finestra, scuro=True)
        stile = ttk.Style(finestra)
        # «clam» disegna i widget rispettando i colori scelti; «aqua» li ignorerebbe
        assert stile.theme_use() == "clam"
        assert stile.lookup("TLabel", "background") == PALETTE["scuro"]["sfondo"]
        assert stile.lookup("TLabel", "foreground") == PALETTE["scuro"]["testo"]
        assert stile.lookup("TFrame", "background") == PALETTE["scuro"]["sfondo"]
        assert COLORI["sfondo"] == PALETTE["scuro"]["sfondo"]
    finally:
        finestra.destroy()


def test_tema_in_modalita_chiara_ha_colori_chiari():
    import tkinter as tk
    from tkinter import ttk

    from fotofacile.ui.theme import COLORI, PALETTE, apply_theme
    from fotofacile.ui.widgets import tk_available

    if not tk_available():
        import pytest

        pytest.skip("serve un ambiente grafico")
    finestra = tk.Tk()
    finestra.withdraw()
    try:
        apply_theme(finestra, scuro=False)
        assert ttk.Style(finestra).lookup("TLabel", "background") == PALETTE["chiaro"]["sfondo"]
        assert COLORI["pannello"] == PALETTE["chiaro"]["pannello"]
    finally:
        finestra.destroy()


def test_la_scala_ingrandisce_i_font():
    from fotofacile.ui import theme

    try:
        theme.imposta_scala(1.0)
        base = theme.font(14)[1]
        theme.imposta_scala(1.5)
        assert theme.font(14)[1] == round(base * 1.5)
        assert theme.scala_attuale() == 1.5
    finally:
        theme.imposta_scala(1.0)


def test_scala_fuori_dai_limiti_viene_riportata():
    from fotofacile.ui import theme

    try:
        theme.imposta_scala(9)
        assert theme.scala_attuale() == 1.5
        theme.imposta_scala(0.1)
        assert theme.scala_attuale() == 1.0
    finally:
        theme.imposta_scala(1.0)


def test_nessun_testo_sotto_14_punti_a_scala_normale():
    from fotofacile.ui import theme

    theme.imposta_scala(1.0)
    for usato in (theme.font(14), theme.font(14, bold=True), theme.font(28, bold=True)):
        assert usato[1] >= 14

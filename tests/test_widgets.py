import pytest

from fotofacile.ui.widgets import Banner, LogPane, PathChooser, StepIndicator, tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


def test_indicatore_passi(root):
    indicatore = StepIndicator(root, ["Collega", "Scegli", "Opzioni", "Copia"])
    try:
        indicatore.set_step(0)
        assert indicatore.current == 0
        indicatore.set_step(3)
        assert indicatore.current == 3
        indicatore.set_step(99)
        assert indicatore.current == 3
        indicatore.set_step(-5)
        assert indicatore.current == 0
    finally:
        indicatore.destroy()


def test_pannello_registro(root):
    pannello = LogPane(root)
    try:
        pannello.append("prima riga")
        pannello.append("seconda riga")
        assert "prima riga" in pannello.get_text()
        assert "seconda riga" in pannello.get_text()
        pannello.clear()
        assert pannello.get_text() == ""
    finally:
        pannello.destroy()


def test_banner_mostra_messaggio_e_suggerimento(root):
    banner = Banner(root)
    try:
        banner.show("Telefono non collegato", hint="Controlla il cavo", kind="avviso")
        assert banner.visible is True
        assert "Telefono non collegato" in banner.message_text
        assert "Controlla il cavo" in banner.hint_text
        assert banner.kind == "avviso"
        banner.hide()
        assert banner.visible is False
    finally:
        banner.destroy()


def test_banner_accetta_tutti_i_toni(root):
    banner = Banner(root)
    try:
        for tono in ("info", "successo", "avviso", "errore"):
            banner.show("messaggio", kind=tono)
            assert banner.kind == tono
    finally:
        banner.destroy()


def test_scelta_cartella_aggiorna_il_valore(root, tmp_path):
    cambi = []
    chooser = PathChooser(root, on_change=cambi.append)
    try:
        chooser.set(str(tmp_path))
        assert chooser.get() == str(tmp_path)
        assert cambi == [str(tmp_path)]
    finally:
        chooser.destroy()


def test_scelta_cartella_senza_callback(root, tmp_path):
    chooser = PathChooser(root)
    try:
        chooser.set(str(tmp_path))
        assert chooser.get() == str(tmp_path)
    finally:
        chooser.destroy()

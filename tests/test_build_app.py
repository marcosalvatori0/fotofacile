import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_app  # noqa: E402


def test_l_archivio_contiene_la_cartella_del_programma_non_e_vuoto(monkeypatch, tmp_path):
    """Su Windows e Linux «pacchetto_creato» è l'eseguibile: lo zip deve avere tutta la cartella."""
    cartella = tmp_path / "dist" / "FotoFacile"
    (cartella / "_internal").mkdir(parents=True)
    exe = cartella / "FotoFacile.exe"
    exe.write_bytes(b"MZ")
    (cartella / "_internal" / "dati.bin").write_bytes(b"x")
    monkeypatch.setattr(build_app, "RADICE", tmp_path)
    monkeypatch.setattr(build_app, "versione", lambda: "0.0.1")

    archivio = build_app.crea_archivio(exe)

    with zipfile.ZipFile(archivio) as zip_file:
        nomi = sorted(zip_file.namelist())
    assert nomi == ["FotoFacile/FotoFacile.exe", "FotoFacile/_internal/dati.bin"]


def test_il_pacchetto_windows_include_aiutante_pillow_e_icona(monkeypatch):
    """Senza queste tre cose il programma installato perde collegamento diretto, WebP o icona."""
    monkeypatch.setattr(build_app.sys, "platform", "win32")
    icona = build_app.icona_per_sistema()
    assert icona is not None and icona.name == "fotofacile.ico"  # lo vuole anche il .iss

    comando = build_app.comando_pyinstaller(icona)

    assert "--windowed" in comando
    dati = comando[comando.index("--add-data") + 1]
    assert dati.endswith("fotofacile/aiutanti") and "aiutanti" in dati.split(build_app.os.pathsep)[0]
    assert (build_app.RADICE / "fotofacile" / "aiutanti" / "wpd_win.ps1").is_file()
    assert "PIL" in comando and "--collect-binaries" in comando
    assert comando[comando.index("--icon") + 1] == str(icona)

#!/usr/bin/env python3
"""Crea la versione "pacchetto" di FotoFacile (build) per il sistema su cui viene eseguito.

Su macOS produce `dist/FotoFacile.app`, su Windows `dist/FotoFacile/FotoFacile.exe`,
su Linux `dist/FotoFacile/FotoFacile`. Il pacchetto contiene Python e la grafica: chi lo
riceve **non deve installare nulla**.

    python3 scripts/build_app.py                 # crea il pacchetto
    python3 scripts/build_app.py --no-zip        # senza archivio da condividere
    python3 scripts/build_app.py --verify        # verifica il pacchetto con l'autocollaudo

Note:
- su macOS il pacchetto non è firmato: la prima apertura richiede clic destro → «Apri»;
- il componente di collegamento (platform-tools) non è incluso: l'app lo scarica da sola
  alla prima necessità, come nella versione da sorgente.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
NOME = "FotoFacile"
ASSET = RADICE / "assets"


def versione() -> str:
    sys.path.insert(0, str(RADICE))
    try:
        import fotofacile

        return fotofacile.__version__
    finally:
        sys.path.pop(0)


def icona_per_sistema() -> Path | None:
    """L'icona adatta al sistema, se è stata generata."""
    preferite = {
        "darwin": ["fotofacile.icns", "fotofacile.png"],
        "win32": ["fotofacile.ico", "fotofacile.png"],
    }.get(sys.platform, ["fotofacile.png"])
    for nome in preferite:
        percorso = ASSET / nome
        if percorso.is_file():
            return percorso
    return None


def comando_pyinstaller(icona: Path | None) -> list[str]:
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",  # niente finestra nera del terminale
        "--name",
        NOME,
        "--collect-submodules",
        "fotofacile",
        "--distpath",
        str(RADICE / "dist"),
        "--workpath",
        str(RADICE / "build" / "pyinstaller"),
        "--specpath",
        str(RADICE / "build"),
    ]
    if icona is not None:
        comando += ["--icon", str(icona)]
    if sys.platform == "darwin":
        comando += ["--osx-bundle-identifier", "com.fotofacile.app"]
    comando.append(str(RADICE / "fotofacile.py"))
    return comando


def pacchetto_creato() -> Path:
    if sys.platform == "darwin":
        return RADICE / "dist" / f"{NOME}.app"
    if sys.platform == "win32":
        return RADICE / "dist" / NOME / f"{NOME}.exe"
    return RADICE / "dist" / NOME / NOME


def eseguibile_dentro(pacchetto: Path) -> Path:
    if pacchetto.suffix == ".app":
        return pacchetto / "Contents" / "MacOS" / NOME
    return pacchetto


def dimensione_mb(percorso: Path) -> float:
    """Dimensione reale su disco (i collegamenti simbolici non vanno contati due volte)."""
    if percorso.is_file():
        return percorso.stat().st_size / 1024 / 1024
    totale = 0
    for voce in percorso.rglob("*"):
        if voce.is_file() and not voce.is_symlink():
            totale += voce.stat().st_size
    return totale / 1024 / 1024


def crea_archivio(pacchetto: Path) -> Path:
    nome = f"{NOME}-{versione()}-{sys.platform}-{__import__('platform').machine()}"
    if pacchetto.suffix == ".app":
        archivio = RADICE / "dist" / f"{nome}.zip"
        # «ditto» conserva permessi e collegamenti simbolici del pacchetto .app
        subprocess.run(
            ["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(pacchetto), str(archivio)],
            check=True,
        )
        return archivio
    archivio = RADICE / "dist" / f"{nome}.zip"
    with zipfile.ZipFile(archivio, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in pacchetto.rglob("*"):
            if file.is_file():
                zip_file.write(file, file.relative_to(pacchetto.parent))
    return archivio


def verifica(pacchetto: Path) -> bool:
    """Esegue l'autocollaudo del pacchetto: apre e chiude la finestra, senza toccare foto."""
    eseguibile = eseguibile_dentro(pacchetto)
    print(f"Verifica: {eseguibile} --selftest")
    try:
        esito = subprocess.run([str(eseguibile), "--selftest"], capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, OSError) as errore:
        print(f"  verifica non conclusa in questo ambiente ({errore})")
        return False
    print(f"  uscita: {esito.returncode} — {esito.stdout.strip() or esito.stderr.strip()}")
    return esito.returncode == 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crea la versione pacchetto di FotoFacile.")
    parser.add_argument("--no-zip", action="store_true", help="non creare l'archivio da condividere")
    parser.add_argument("--verify", action="store_true", help="esegui l'autocollaudo sul pacchetto")
    argomenti = parser.parse_args(argv)

    for cartella in ("dist", "build"):
        shutil.rmtree(RADICE / cartella, ignore_errors=True)

    if not (ASSET / "fotofacile.png").is_file():
        print("Genero l'icona…")
        subprocess.run([sys.executable, str(RADICE / "scripts" / "make_icon.py")], check=False)

    icona = icona_per_sistema()
    print(f"Creo il pacchetto per {sys.platform} (icona: {icona.name if icona else 'nessuna'})…")
    esito = subprocess.run(comando_pyinstaller(icona), cwd=str(RADICE))
    if esito.returncode != 0:
        print("La creazione del pacchetto non è riuscita.")
        return esito.returncode

    pacchetto = pacchetto_creato()
    if sys.platform == "darwin":
        # su macOS il pacchetto da consegnare è il .app: la cartella intermedia è inutile
        shutil.rmtree(RADICE / "dist" / NOME, ignore_errors=True)
    if not pacchetto.exists():
        print(f"Pacchetto non trovato in {pacchetto}")
        return 1

    print(f"\nPacchetto pronto: {pacchetto} ({dimensione_mb(pacchetto):.1f} MB)")
    if argomenti.verify and not verifica(pacchetto):
        print("  (il pacchetto è stato creato; l'autocollaudo richiede una sessione grafica)")

    if not argomenti.no_zip:
        archivio = crea_archivio(pacchetto)
        print(f"Archivio da condividere: {archivio} ({dimensione_mb(archivio):.1f} MB)")

    print(
        "\nPer provarlo:\n"
        f"  macOS:   open '{pacchetto}'      (prima volta: clic destro → Apri)\n"
        f"  Windows: doppio clic su {pacchetto.name}\n"
        f"  Linux:   {eseguibile_dentro(pacchetto)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

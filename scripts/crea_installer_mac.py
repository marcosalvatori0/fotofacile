#!/usr/bin/env python3
"""Crea l'installatore macOS (.dmg) di FotoFacile: si apre, si trascina l'app in Applicazioni.

È un installatore vero: dentro il disco virtuale ci sono l'applicazione e la scorciatoia ad
«Applicazioni», più un file LEGGIMI con le istruzioni per il primo avvio.

    python3 scripts/crea_installer_mac.py                 # usa dist/FotoFacile.app
    python3 scripts/crea_installer_mac.py --fonte <app>   # usa un'app diversa (per i test)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
NOME = "FotoFacile"

LEGGIMI = """FotoFacile — installazione su macOS
=====================================

1. Trascina l'icona di FotoFacile nella cartella «Applicazioni».
2. Apri FotoFacile da «Applicazioni»: la prima volta fai clic destro sull'icona e scegli
   «Apri» (il programma non è firmato: macOS chiede conferma solo la prima volta).
3. Collega il telefono Android con il cavo USB, sblocca lo schermo e segui i quattro passi.

Se il telefono non viene riconosciuto: sul telefono scegli «Trasferimento file» (tocca «Consenti» se lo chiede) e nel
programma premi «Serve aiuto?». Prova anche un altro cavo USB (alcuni ricaricano soltanto).

Diagnosi (dal Terminale):
    /Applications/FotoFacile.app/Contents/MacOS/FotoFacile doctor
    /Applications/FotoFacile.app/Contents/MacOS/FotoFacile --selftest

Il programma non invia nulla su internet: la usa solo, se manca, per scaricare il componente
di collegamento ufficiale di Google.
"""


def versione() -> str:
    sys.path.insert(0, str(RADICE))
    try:
        import fotofacile

        return fotofacile.__version__
    finally:
        sys.path.pop(0)


def _esegui(comando: list[str], **kwargs) -> subprocess.CompletedProcess:
    esito = subprocess.run(comando, capture_output=True, text=True, **kwargs)
    if esito.returncode != 0:
        raise RuntimeError(f"{comando[0]} è fallito: {esito.stderr.strip() or esito.stdout.strip()}")
    return esito


def crea_dmg(fonte: Path, destinazione: Path, nome_volume: str = NOME) -> Path:
    """Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il LEGGIMI."""
    if sys.platform != "darwin":  # pragma: no cover - solo macOS sa creare i .dmg
        raise RuntimeError("Il disco di installazione per macOS si può creare solo da macOS.")
    if not fonte.exists():
        raise FileNotFoundError(f"Applicazione non trovata: {fonte}")

    destinazione.parent.mkdir(parents=True, exist_ok=True)
    destinazione.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="fotofacile-dmg-") as temporanea:
        scena = Path(temporanea) / "scena"
        scena.mkdir()
        if fonte.is_dir() and fonte.suffix == ".app":
            _esegui(["ditto", str(fonte), str(scena / fonte.name)])
        else:
            shutil.copy2(fonte, scena / fonte.name)
        (scena / "LEGGIMI - macOS.txt").write_text(LEGGIMI, encoding="utf-8")
        (scena / "Applicazioni").symlink_to("/Applications")
        _esegui(
            [
                "hdiutil",
                "create",
                "-volname",
                nome_volume,
                "-srcfolder",
                str(scena),
                "-ov",
                "-format",
                "UDZO",
                str(destinazione),
            ]
        )
    return destinazione


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crea l'installatore .dmg per macOS.")
    parser.add_argument("--fonte", type=Path, default=RADICE / "dist" / f"{NOME}.app")
    parser.add_argument("--uscita", type=Path, default=None)
    argomenti = parser.parse_args(argv)

    uscita = argomenti.uscita or RADICE / "dist" / f"{NOME}-{versione()}.dmg"
    try:
        percorso = crea_dmg(argomenti.fonte, uscita)
    except (RuntimeError, FileNotFoundError) as errore:
        print(f"Non ho potuto creare il .dmg: {errore}")
        print("Suggerimento: crea prima l'app con:  python3 scripts/build_app.py")
        return 1
    print(f"Installatore pronto: {percorso} ({percorso.stat().st_size / 1024 / 1024:.1f} MB)")
    print("Per provarlo: apri il file .dmg e trascina FotoFacile in Applicazioni.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

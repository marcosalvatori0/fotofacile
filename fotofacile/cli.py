"""Avvio del programma: interfaccia grafica, modalità demo e diagnosi."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Mapping, Sequence

from . import __version__
from .core.adb import find_adb
from .core.devices import get_devices
from .core.osutil import app_dir


def build_doctor_report(
    adb_path: str | None,
    adb_version: str,
    system: str,
    python_version: str,
    tk_version: str,
    devices: Sequence[tuple[str, str]],
    app_folder: str,
    writing_ok: bool,
) -> str:
    """Testo della diagnosi: serve al supporto per capire cosa non va su un computer."""
    righe = [
        "FotoFacile — diagnosi",
        "──────────────────────────────",
        f"Sistema: {system}",
        f"Python: {python_version}",
        f"Tkinter: {tk_version}",
        f"Componente: {adb_path or 'non trovato'}",
    ]
    if adb_version:
        righe.append(f"Versione componente: {adb_version}")
    if devices:
        righe.append(
            "Telefoni collegati: " + ", ".join(f"{seriale} ({stato})" for seriale, stato in devices)
        )
    else:
        righe.append("Telefoni collegati: nessuno")
    righe.append(f"Cartella dati: {app_folder}")
    righe.append(f"Scrittura: {'ok' if writing_ok else 'problema'}")
    if not adb_path:
        righe.extend(
            [
                "",
                "Suggerimento: apri FotoFacile senza argomenti e premi «Installa componente».",
            ]
        )
    if not devices:
        righe.extend(["", "Suggerimento: collega il telefono con il cavo e sbloccalo."])
    return "\n".join(righe) + "\n"


def doctor(env: Mapping[str, str] | None = None) -> int:
    """Stampa una diagnosi completa dello stato del computer e del collegamento."""
    ambiente = dict(env if env is not None else os.environ)
    percorso_adb = find_adb(env=ambiente)
    versione = ""
    dispositivi: list[tuple[str, str]] = []
    if percorso_adb:
        try:
            from .core.adb import RealAdbBackend

            backend = RealAdbBackend(percorso_adb)
            versione = backend.check()
            dispositivi = [(dispositivo.serial, dispositivo.state) for dispositivo in get_devices(backend)]
        except Exception as errore:  # pragma: no cover - diagnosi "best effort"
            versione = f"non utilizzabile ({errore})"
    cartella = app_dir(ambiente)
    try:
        cartella.mkdir(parents=True, exist_ok=True)
        prova = cartella / ".prova-scrittura"
        prova.write_text("ok", encoding="utf-8")
        prova.unlink()
        scrittura = True
    except OSError:
        scrittura = False
    try:
        import tkinter

        versione_tk = str(tkinter.TkVersion)
    except Exception:  # pragma: no cover - Tkinter assente
        versione_tk = "non disponibile"
    print(
        build_doctor_report(
            adb_path=percorso_adb,
            adb_version=versione,
            system=sys.platform,
            python_version=sys.version.split()[0],
            tk_version=versione_tk,
            devices=dispositivi,
            app_folder=str(cartella),
            writing_ok=scrittura,
        )
    )
    return 0


def selftest() -> int:
    """Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude.

    Serve soprattutto a verificare una versione impacchettata (build): dice in una riga
    se la parte grafica funziona su questo computer, senza toccare nessuna foto.
    """
    import json

    dati: dict = {"ok": False, "motivo": ""}
    try:
        from .ui.app import App

        applicazione = App(demo_mode=True)
        applicazione.withdraw()
        for _ in range(5):
            applicazione.update()
        dati = {
            "ok": True,
            "pagina": applicazione.current_page,
            "pagine": sorted(applicazione.pages),
            "motivo": "",
        }
        applicazione.stop_all_polling()
        applicazione.destroy()
    except Exception as errore:  # qualunque problema va riportato, non nascosto
        dati = {"ok": False, "motivo": f"{type(errore).__name__}: {errore}"}
    print(json.dumps(dati, ensure_ascii=False))
    return 0 if dati["ok"] else 1


def start_gui(demo: bool = False) -> int:
    """Apre la finestra principale; se la grafica non è disponibile lo spiega con calma."""
    import tkinter as tk

    from .ui.app import App

    try:
        applicazione = App(demo_mode=demo)
    except tk.TclError as errore:
        print(
            "Non riesco ad aprire la finestra del programma.\n"
            f"Motivo tecnico: {errore}\n"
            "Su Linux serve il pacchetto della grafica (per esempio «python3-tk»);\n"
            "su macOS e Windows reinstalla Python dalle impostazioni consigliate.\n"
            "Per controllare il computer puoi usare:  fotofacile doctor"
        )
        return 1
    applicazione.mainloop()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fotofacile",
        description="Copia le foto dal telefono Android al computer, passo per passo.",
        epilog="Esempi:  py fotofacile.py        (Windows)\n"
        "         python3 fotofacile.py    (macOS e Linux)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--demo", action="store_true", help="prova il programma senza telefono")
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="apre e chiude la finestra per verificare che tutto funzioni",
    )
    parser.add_argument("--version", action="version", version=f"FotoFacile {__version__}")
    parser.add_argument(
        "comando",
        nargs="?",
        choices=["doctor"],
        help="«doctor» mostra la diagnosi del sistema e del collegamento",
    )
    return parser


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    argomenti = build_parser().parse_args(list(argv) if argv is not None else None)
    if argomenti.comando == "doctor":
        return doctor(env)
    if argomenti.selftest:
        return selftest()
    return start_gui(demo=argomenti.demo)

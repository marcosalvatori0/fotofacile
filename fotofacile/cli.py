"""Avvio del programma: interfaccia grafica, modalità demo e diagnosi."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Mapping, Sequence

from . import __version__
from .core.adb import find_adb
from .core.devices import get_devices
from .core.osutil import app_dir, comando_se_stesso, flag_nascosta


def build_doctor_report(
    adb_path: str | None,
    adb_version: str,
    system: str,
    python_version: str,
    tk_version: str,
    devices: Sequence[tuple[str, str]],
    app_folder: str,
    writing_ok: bool,
    modi: Sequence[tuple[str, bool]] = (),
) -> str:
    """Testo della diagnosi: serve al supporto per capire cosa non va su un computer."""
    righe = [
        "FotoFacile — diagnosi",
        "──────────────────────────────",
        f"Sistema: {system}",
        f"Python: {python_version}",
        f"Tkinter: {tk_version}",
    ]
    if modi:
        righe.append("Modi di collegamento:")
        for nome, attivo in modi:
            righe.append(f"  • {nome} — {'disponibile' if attivo else 'non disponibile'}")
    righe.append(f"Componente aggiuntivo (adb): {adb_path or 'non trovato'}")
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
    if not adb_path and not modi:
        righe.extend(
            [
                "",
                "Suggerimento: apri FotoFacile senza argomenti e premi «Installa componente».",
            ]
        )
    if not devices:
        righe.extend(
            [
                "",
                "Suggerimento: collega il telefono con il cavo e sblocca lo schermo.",
                "Non serve attivare il Debug USB: il programma usa il collegamento normale.",
            ]
        )
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
            modi=elenco_modi(ambiente),
        )
    )
    return 0


def elenco_modi(ambiente: Mapping[str, str] | None = None) -> list[tuple[str, bool]]:
    """Quali modi di collegamento al telefono sono utilizzabili su questo computer.

    È la riga più utile della diagnosi: dice subito se il collegamento **senza Debug USB**
    è disponibile, o se l'unica possibilità è il collegamento rapido.
    """
    try:
        from .core.trasporto import trasporti_disponibili

        return [
            (trasporto.nome, trasporto.disponibile())
            for trasporto in trasporti_disponibili(env=ambiente)
        ]
    except Exception as errore:  # diagnosi «best effort»: non deve mai fallire
        return [(f"errore nella verifica: {errore}", False)]


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


def scrivi_log_avvio(testo: str, env: Mapping[str, str] | None = None) -> Path:
    """Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log).

    Se il programma non si apre, questo file dice sempre cosa è successo.
    """
    from datetime import datetime

    percorso = app_dir(env) / "avvio.log"
    path_obj = Path(percorso)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with path_obj.open("a", encoding="utf-8") as uscita:
        uscita.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  {testo}\n")
    return path_obj


def contesto_grafico_dubbio(env: Mapping[str, str] | None = None, system: str | None = None) -> bool:
    """True se non ci sono segnali di una sessione grafica (automazione, servizi, ssh).

    Serve a non restare appesi in silenzio: se il contesto è dubbio si fa una prova rapida
    e, se fallisce, si spiega all'utente cosa fare.
    """
    ambiente = dict(env if env is not None else os.environ)
    sistema = system or sys.platform
    if sistema != "darwin":
        return False
    return not (ambiente.get("TERM_PROGRAM") or ambiente.get("__CFBundleIdentifier"))


def prova_finestra(timeout: float = 10.0) -> bool:
    """Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.

    Nel pacchetto (PyInstaller) non si possono passare opzioni come ``-c`` all'eseguibile:
    si richiama sé stesso con l'opzione interna ``--prova-finestra``. Il richiamo funziona
    identico dal sorgente e dal programma impacchettato (vedi ``osutil.comando_se_stesso``).
    """
    return _processo_finestra(comando_se_stesso("--prova-finestra"), timeout)


def _processo_finestra(comando: list[str], timeout: float) -> bool:
    import subprocess

    try:
        esito = subprocess.run(
            comando,
            capture_output=True,
            timeout=timeout,
            creationflags=flag_nascosta(),
        )
    except (subprocess.TimeoutExpired, OSError):
        return False
    return esito.returncode == 0


def prova_finestra_diretta() -> int:
    """Apre e chiude una finestra vuota: è il corpo di ``--prova-finestra``."""
    try:
        import tkinter as tk

        radice = tk.Tk()
        radice.withdraw()
        radice.update()
        radice.destroy()
    except Exception:
        return 1
    return 0


def avviso_visibile(
    testo: str,
    env: Mapping[str, str] | None = None,
    system: str | None = None,
    runner=None,
) -> None:
    """Fa vedere un avviso anche quando la finestra del programma non può aprirsi."""
    import json
    import subprocess

    sistema = system or sys.platform
    scrivi_log_avvio(testo.replace("\n", " | "), env)
    print(testo)
    if sistema == "darwin":
        esegui = runner or subprocess.run
        script = f'display alert "FotoFacile" message {json.dumps(testo)} as critical'
        try:
            esegui(["osascript", "-e", script], capture_output=True, creationflags=flag_nascosta())
        except OSError:  # pragma: no cover - osascript sempre presente su macOS
            pass


def start_gui(demo: bool = False) -> int:
    """Apre la finestra principale; se la grafica non è disponibile lo spiega con calma."""
    import tkinter as tk

    from .ui.app import App

    scrivi_log_avvio("avvio dell'interfaccia grafica" + (" (modalità demo)" if demo else ""))
    if contesto_grafico_dubbio() and not prova_finestra():
        messaggio = (
            "Non riesco ad aprire la finestra di FotoFacile in questo contesto.\n"
            "Avvia il programma dalla sessione grafica del computer:\n"
            "• doppio clic su FotoFacile.app, oppure\n"
            "• dal Terminale: python3 fotofacile.py\n"
            "Per la diagnosi completa: fotofacile doctor"
        )
        avviso_visibile(messaggio)
        return 1
    from .core.osutil import rendi_consapevole_dpi

    rendi_consapevole_dpi()
    try:
        applicazione = App(demo_mode=demo)
    except tk.TclError as errore:
        messaggio = (
            "Non riesco ad aprire la finestra del programma.\n"
            f"Motivo tecnico: {errore}\n"
            "Su Linux serve il pacchetto della grafica (per esempio «python3-tk»);\n"
            "su macOS e Windows reinstalla Python dalle impostazioni consigliate.\n"
            "Per controllare il computer puoi usare:  fotofacile doctor"
        )
        avviso_visibile(messaggio)
        return 1
    applicazione.mainloop()
    scrivi_log_avvio("finestra chiusa")
    return 0


def esegui_aiutante(argomenti: Sequence[str]) -> int:
    """Modalità interna: il programma richiama sé stesso per parlare con il telefono.

    Non è pensata per essere usata a mano: serve a :mod:`fotofacile.core.trasporto_aiutante`,
    che avvia un processo separato perché il collegamento diretto (ImageCaptureCore su macOS,
    WPD su Windows, gio su Linux) ha bisogno di un ciclo di eventi tutto suo, che non si può
    mescolare con la finestra.
    """
    from .aiutanti import esegui

    elenco = list(argomenti)
    if not elenco:
        print("Serve il nome dell'aiutante.", file=sys.stderr)
        return 2
    nome, resto = elenco[0], elenco[1:]
    try:
        return esegui(nome, resto)
    except KeyError:
        print(f"Aiutante sconosciuto: {nome}", file=sys.stderr)
        return 2
    except ImportError as errore:
        print(f"L'aiutante {nome} non è disponibile su questo computer: {errore}", file=sys.stderr)
        return 2


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
        "--prova-finestra",
        dest="prova_finestra",
        action="store_true",
        help=argparse.SUPPRESS,  # uso interno: verifica che la grafica si apra davvero
    )
    parser.add_argument(
        "comando",
        nargs="?",
        choices=["doctor"],
        help="«doctor» mostra la diagnosi del sistema e del collegamento",
    )
    return parser


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    argomenti = list(argv) if argv is not None else sys.argv[1:]
    # L'opzione interna va intercettata **prima** di argparse: gli argomenti dopo di essa
    # appartengono all'aiutante, non a FotoFacile.
    if argomenti[:1] == ["--aiutante"]:
        return esegui_aiutante(argomenti[1:])
    argomenti_letti = build_parser().parse_args(argomenti)
    if argomenti_letti.prova_finestra:
        return prova_finestra_diretta()
    if argomenti_letti.comando == "doctor":
        return doctor(env)
    if argomenti_letti.selftest:
        return selftest()
    return start_gui(demo=argomenti_letti.demo)

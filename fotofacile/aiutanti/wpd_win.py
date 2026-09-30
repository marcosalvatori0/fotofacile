"""Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).

Perché un passaggio in più rispetto agli altri sistemi: su Windows l'unico modo per
raggiungere i telefoni collegati senza Debug USB è il componente ``Shell.Application``,
che è un oggetto COM. Python non lo vede, PowerShell sì, e PowerShell è presente su ogni
Windows. Questo file fa da traduttore: riceve i comandi del contratto, chiama PowerShell
e lascia passare l'uscita così com'è.

L'uscita standard (i byte delle foto) non viene mai toccata: si lascia che PowerShell
scriva direttamente sullo stesso flusso, così un video da 4 GB non passa mai dalla memoria
di Python. I messaggi per la persona restano sull'uscita degli errori.

Uso (dall'esterno non si chiama mai a mano, lo fa :mod:`fotofacile.core.trasporto_aiutante`)::

    python -m fotofacile.aiutanti.wpd_win dispositivi
    python -m fotofacile.aiutanti.wpd_win elenca [--seriale S] [--solo-foto]
    python -m fotofacile.aiutanti.wpd_win copia --seriale S --percorso P --destinazione D
    python -m fotofacile.aiutanti.wpd_win cancella --seriale S --percorso P
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from ..core.osutil import flag_nascosta

USCITA_OK = 0
USCITA_ERRORE = 2
USCITA_NESSUN_TELEFONO = 3

#: Nome del comando di PowerShell: «powershell» è presente su ogni Windows dal 7 in poi.
POWERSHELL = "powershell"

#: I comandi che il contratto prevede per tutti gli aiutanti.
COMANDI = ("dispositivi", "elenca", "copia", "cancella")

#: Tempi massimi, un po' più corti di quelli del programma principale (30 s, 300 s,
#: 1800 s): così è questo aiutante a uccidere PowerShell e a raccontare con calma che il
#: telefono non risponde, invece di farsi interrompere dal programma principale mentre
#: PowerShell tiene ancora aperto il file di uscita (su Windows non si può cancellare un
#: file aperto, e l'errore vero verrebbe sostituito da uno incomprensibile).
TIMEOUT_POWERSHELL = {
    "dispositivi": 25.0,
    "elenca": 280.0,
    "copia": 1750.0,
    "cancella": 60.0,
}


def percorso_script() -> Path:
    """Il file PowerShell che fa il lavoro vero, accanto a questo modulo."""
    return Path(__file__).with_name("wpd_win.ps1")


def _valore(argomenti: Sequence[str], chiave: str, predefinito: str = "") -> str:
    elenco = list(argomenti)
    if chiave in elenco:
        posizione = elenco.index(chiave)
        if posizione + 1 < len(elenco):
            return elenco[posizione + 1]
    return predefinito


def comando_powershell(
    script: Path,
    comando: str,
    seriale: str = "",
    percorso: str = "",
    destinazione: str = "",
    solo_foto: bool = False,
) -> list[str]:
    """Costruisce la riga di comando per PowerShell, con i soli argomenti utili.

    ``-NoProfile`` evita che un profilo dell'utente cambi il comportamento;
    ``-NonInteractive`` garantisce che non compaia nessuna richiesta di conferma (una
    richiesta appesa bloccherebbe il programma per sempre); ``-ExecutionPolicy Bypass``
    serve perché lo script è nostro e non deve essere rifiutato dalla politica di sistema.
    ``-PidSupervisionato`` è il numero di questo processo: se l'app annulla un'operazione
    e uccide l'aiutante, PowerShell se ne accorge e smette di copiare, invece di restare
    vivo a lavorare per nessuno.
    """
    argomenti = [
        POWERSHELL,
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-Comando",
        comando,
        "-PidSupervisionato",
        str(os.getpid()),
    ]
    if seriale:
        argomenti += ["-Seriale", seriale]
    if percorso:
        argomenti += ["-Percorso", percorso]
    if destinazione:
        argomenti += ["-Destinazione", destinazione]
    if solo_foto:
        argomenti.append("-SoloFoto")
    return argomenti


def _codice_di_uscita(codice: int) -> int:
    """Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)."""
    if codice == USCITA_OK:
        return USCITA_OK
    if codice == USCITA_NESSUN_TELEFONO:
        return USCITA_NESSUN_TELEFONO
    if codice != USCITA_ERRORE:
        # Un codice inatteso (per esempio un errore di sintassi di PowerShell, che esce
        # con 1): si aggiunge una riga italiana, perché il messaggio di PowerShell può
        # essere tecnico, in inglese o del tutto assente.
        sys.stderr.write(
            f"PowerShell non è riuscito a parlare con il telefono (codice {codice}).\n"
        )
        sys.stderr.write("Scollega e ricollega il cavo del telefono, poi riprova.\n")
    return USCITA_ERRORE


def main(argv: Sequence[str] | None = None) -> int:
    argomenti = list(sys.argv[1:] if argv is None else argv)
    if not argomenti:
        sys.stderr.write("Serve un comando: dispositivi, elenca, copia, cancella.\n")
        return USCITA_ERRORE
    comando, resto = argomenti[0], argomenti[1:]
    if comando not in COMANDI:
        sys.stderr.write(f"Comando sconosciuto: {comando}\n")
        return USCITA_ERRORE

    script = percorso_script()
    if not script.is_file():
        # Senza il file PowerShell non c'è niente da provare: meglio dirlo chiaramente
        # che far fallire PowerShell con un errore incomprensibile.
        sys.stderr.write(
            "Manca il componente per Windows (wpd_win.ps1): reinstalla FotoFacile.\n"
        )
        return USCITA_ERRORE

    riga = comando_powershell(
        script,
        comando,
        seriale=_valore(resto, "--seriale"),
        percorso=_valore(resto, "--percorso"),
        destinazione=_valore(resto, "--destinazione"),
        solo_foto="--solo-foto" in resto,
    )
    try:
        # I flussi non si toccano: PowerShell scrive i byte delle foto e i messaggi
        # direttamente sugli stessi flussi del contratto (uscita standard per i dati,
        # uscita degli errori per le spiegazioni). Mettersi in mezzo significherebbe far
        # passare un video da 4 GB dalla memoria di Python.
        esito = subprocess.run(
            riga,
            stdin=subprocess.DEVNULL,
            creationflags=flag_nascosta(),
            timeout=TIMEOUT_POWERSHELL[comando],
        )
    except subprocess.TimeoutExpired:
        sys.stderr.write("Il telefono non ha risposto in tempo.\n")
        sys.stderr.write("Sblocca il telefono e riprova; se serve, scollega e ricollega il cavo.\n")
        return USCITA_ERRORE
    except OSError as errore:
        sys.stderr.write(f"Non riesco ad avviare PowerShell: {errore}\n")
        sys.stderr.write("Apri il Prompt dei comandi e prova a scrivere «powershell».\n")
        return USCITA_ERRORE
    return _codice_di_uscita(int(esito.returncode))


if __name__ == "__main__":  # pragma: no cover - avvio diretto
    raise SystemExit(main())

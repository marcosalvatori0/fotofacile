#!/usr/bin/env python3
"""Crea la cartella «FotoFacile per Windows» pronta da copiare su un PC Windows.

Perché una cartella e non direttamente un `.exe`: **PyInstaller non compila per Windows
da macOS** — un eseguibile Windows si può creare e collaudare solo su Windows. Questa
cartella risolve il problema in due modi:

1. `Avvia FotoFacile.bat` fa partire il programma **subito** su Windows; se Python non c'è,
   lo installa da solo (winget) e in alternativa spiega come fare.
2. `Crea l'eseguibile per Windows.bat` crea `dist\\FotoFacile\\FotoFacile.exe` con un doppio
   clic, e lo verifica subito con l'autocollaudo: quell'eseguibile poi funziona su qualsiasi
   PC Windows **senza installare nulla**.

    python3 scripts/crea_pacchetto_windows.py [--force] [cartella_destinazione]

Con `--force` si accetta di cancellare una cartella esistente che non sembra un pacchetto
creato in precedenza: senza di esso il programma si ferma invece di rischiare di cancellare
per sbaglio dei dati dell'utente (vedi `_controlla_destinazione`).
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
NOME_CARTELLA = "FotoFacile per Windows"
# File/cartelle presenti in un pacchetto già creato: servono a riconoscerlo prima di
# cancellarlo, così non si rischia di distruggere la cartella di lavoro di qualcun altro.
MARCATORI_PACCHETTO = ("Avvia FotoFacile.bat", "LEGGIMI - Windows.txt", "fotofacile")
CARTELLE_DA_COPIARE = ("fotofacile",)
FILE_DA_COPIARE = (
    "fotofacile.py",
    "README.md",
    "requirements-dev.txt",
    "requirements.txt",
    "scripts/build_app.py",
    "scripts/make_icon.py",
    "assets/fotofacile.ico",
    "assets/fotofacile.png",
)

AVVIO_BAT = r"""@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title FotoFacile - copia le foto dal telefono

echo ============================================================
echo   FotoFacile - copia le foto dal telefono al computer
echo ============================================================
echo.

set "PY="
call :trova_python
if defined PY goto avvia

echo Non ho trovato Python su questo computer.
call :diagnostica
echo.
where winget >nul 2>nul
if errorlevel 1 goto istruzioni

echo Posso installarlo io adesso con winget: serve internet e qualche minuto.
echo.
set /p scelta="Installo Python 3.13 adesso? [S/n] "
if /i "%scelta%"=="n" goto istruzioni
echo.
echo Installazione di Python in corso...
winget install -e --id Python.Python.3.13 --accept-package-agreements --accept-source-agreements
call :trova_python
if not defined PY goto istruzioni
goto avvia

:istruzioni
echo.
echo ------------------------------------------------------------
echo  COSA FARE ADESSO
echo ------------------------------------------------------------
echo  1) Apri il Microsoft Store, cerca "Python 3.13" e installalo.
echo     In alternativa: https://www.python.org/downloads/windows/
echo  2) Durante l'installazione spunta "Add python.exe to PATH".
echo  3) Poi fai di nuovo doppio clic su "Avvia FotoFacile.bat".
echo.
echo  Oppure usa "Installa FotoFacile.bat": installa il programma
echo  e, se serve, Python; in piu' crea i collegamenti sul Desktop.
echo ------------------------------------------------------------
echo.
pause
exit /b 1

:avvia
echo Uso Python con: %PY%
%PY% -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
if errorlevel 1 (
  echo.
  echo Questo Python non ha la grafica ^(tkinter^): reinstallalo dal sito python.org
  echo scegliendo la versione completa.
  echo.
  pause
  exit /b 1
)

echo Avvio del programma...
echo.
%PY% fotofacile.py
set "CODICE=%ERRORLEVEL%"
if not "%CODICE%"=="0" (
  echo.
  echo ------------------------------------------------------------
  echo  Il programma si e' chiuso con un problema: ecco la diagnosi
  echo ------------------------------------------------------------
  %PY% fotofacile.py doctor
  echo.
  echo Registro di avvio: %USERPROFILE%\.fotofacile\avvio.log
  call :diagnostica
)
echo.
pause
exit /b 0

:trova_python
rem --- 1) il launcher ufficiale «py» (il piu' affidabile su Windows) ---
py -3 -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
if not errorlevel 1 (
  set "PY=py -3"
  exit /b 0
)
rem --- 2) installazioni nei percorsi tipici (PATH non aggiornato) ---
for %%B in ("%LOCALAPPDATA%\Programs\Python" "%ProgramFiles%\Python" "%ProgramFiles(x86)%\Python" "C:\Python3") do (
  for /d %%V in ("%%~B\Python3*") do (
    if exist "%%~V\python.exe" (
      "%%~V\python.exe" -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
      if not errorlevel 1 (
        set "PY=%%~V\python.exe"
        exit /b 0
      )
    )
  )
)
rem --- 3) python / python3 presenti nel PATH ---
for %%C in (python python3) do (
  %%C -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
  if not errorlevel 1 (
    set "PY=%%C"
    exit /b 0
  )
)
rem --- 4) elenco del launcher «py»: dice dove sono le versioni installate ---
where py >nul 2>nul
if not errorlevel 1 (
  for /f "delims=" %%L in ('py -0p 2^>nul') do (
    for %%P in (%%L) do set "CANDIDATO=%%P"
    if exist "!CANDIDATO!" (
      "!CANDIDATO!" -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
      if not errorlevel 1 (
        set "PY=!CANDIDATO!"
        exit /b 0
      )
    )
  )
)
exit /b 0

:diagnostica
rem Dice esattamente cosa e' stato trovato: serve a capire perche' non parte.
echo --- Cosa ho trovato su questo computer ---
where python 2>nul || echo   python nel PATH: non trovato
where py 2>nul || echo   launcher "py": non trovato
py --version 2>&1
py -0p 2>nul
echo --------------------------------------------
"""

ESEGUIBILE_BAT = r"""@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title FotoFacile - crea l'eseguibile

echo ============================================================
echo   Creo l'eseguibile di FotoFacile per Windows
echo ============================================================
echo.

set "PY="
call :trova_python
if not defined PY (
  echo Serve Python per creare l'eseguibile: ecco cosa ho trovato.
  call :diagnostica
  echo.
  echo Fai prima doppio clic su "Avvia FotoFacile.bat" oppure su
  echo "Installa FotoFacile.bat": installano Python se manca.
  echo.
  pause
  exit /b 1
)

echo Uso Python con: %PY%
echo.
echo 1 di 2 - installo/aggiorno PyInstaller...
%PY% -m pip install --upgrade pip pyinstaller
if errorlevel 1 (
  echo.
  echo Non sono riuscito a installare PyInstaller: controlla la connessione a internet.
  pause
  exit /b 1
)

echo.
echo 2 di 2 - creo l'eseguibile (puo' richiedere 1-2 minuti)...
%PY% scripts\build_app.py
if errorlevel 1 (
  echo.
  echo La creazione non e' riuscita: il messaggio sopra dice il motivo.
  pause
  exit /b 1
)

echo.
echo Provo l'eseguibile appena creato...
dist\FotoFacile\FotoFacile.exe --selftest
echo.
echo ------------------------------------------------------------
echo  FATTO
echo ------------------------------------------------------------
echo  Eseguibile:  dist\FotoFacile\FotoFacile.exe
echo  Archivio:    guarda il file .zip dentro la cartella "dist"
echo.
echo  Per usarlo su un altro computer: copia tutta la cartella
echo  "dist\FotoFacile" (oppure il file .zip): non serve installare Python.
echo.
echo  Se Windows mostra un avviso di sicurezza la prima volta:
echo  clic su "Ulteriori informazioni" e poi "Esegui comunque".
echo ------------------------------------------------------------
echo.
pause
exit /b 0

:trova_python
rem --- 1) il launcher ufficiale «py» (il piu' affidabile su Windows) ---
py -3 -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
if not errorlevel 1 (
  set "PY=py -3"
  exit /b 0
)
rem --- 2) installazioni nei percorsi tipici (PATH non aggiornato) ---
for %%B in ("%LOCALAPPDATA%\Programs\Python" "%ProgramFiles%\Python" "%ProgramFiles(x86)%\Python" "C:\Python3") do (
  for /d %%V in ("%%~B\Python3*") do (
    if exist "%%~V\python.exe" (
      "%%~V\python.exe" -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
      if not errorlevel 1 (
        set "PY=%%~V\python.exe"
        exit /b 0
      )
    )
  )
)
rem --- 3) python / python3 presenti nel PATH ---
for %%C in (python python3) do (
  %%C -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
  if not errorlevel 1 (
    set "PY=%%C"
    exit /b 0
  )
)
rem --- 4) elenco del launcher «py»: dice dove sono le versioni installate ---
where py >nul 2>nul
if not errorlevel 1 (
  for /f "delims=" %%L in ('py -0p 2^>nul') do (
    for %%P in (%%L) do set "CANDIDATO=%%P"
    if exist "!CANDIDATO!" (
      "!CANDIDATO!" -c "import sys, tkinter; sys.exit(0 if sys.version_info[:2] >= (3, 9) else 2)" >nul 2>nul
      if not errorlevel 1 (
        set "PY=!CANDIDATO!"
        exit /b 0
      )
    )
  )
)
exit /b 0

:diagnostica
rem Dice esattamente cosa e' stato trovato: serve a capire perche' non parte.
echo --- Cosa ho trovato su questo computer ---
where python 2>nul || echo   python nel PATH: non trovato
where py 2>nul || echo   launcher "py": non trovato
py --version 2>&1
py -0p 2>nul
echo --------------------------------------------
"""

LEGGIMI = """FotoFacile per Windows - istruzioni
====================================

Questa cartella contiene il programma completo per copiare le foto dal telefono Android
al computer, con una procedura guidata in italiano.

Ci sono due modi di usarla. Scegli quello che ti serve.


1) USARE SUBITO IL PROGRAMMA  (doppio clic su: Avvia FotoFacile.bat)
--------------------------------------------------------------------
- Se il computer ha gia' Python, il programma parte subito.
- Se Python non c'e', il file te lo fa installare da solo (serve internet) oppure ti
  spiega come installarlo in due passi: dal Microsoft Store cercando "Python 3.13",
  oppure scaricandolo da https://www.python.org/downloads/windows/
  (durante l'installazione spunta "Add python.exe to PATH").
- La finestra nera che si apre serve ad avviare il programma: e' normale, non chiuderla
  finche' usi FotoFacile.


2) CREARE L'ESEGUIBILE CHE NON RICHIEDE PYTHON  (doppio clic su: Crea l'eseguibile per Windows.bat)
----------------------------------------------------------------------------------------------------
- Crea il file:  dist\\FotoFacile\\FotoFacile.exe
- Alla fine lo prova da solo e ti dice se funziona (autocollaudo).
- Per regalarlo: copia tutta la cartella "dist\\FotoFacile" (o il file .zip che trovi in
  "dist") su una chiavetta. Su quel computer non serve installare nulla.
- Nota: l'eseguibile si crea solo su Windows. Da Mac non si puo': questo file e' il modo
  piu' semplice per farlo con un doppio clic.


COLLEGARE IL TELEFONO (non serve attivare niente)
-------------------------------------------------
1. Collega il telefono con il cavo USB e sblocca lo schermo.
2. Aspetta qualche secondo: il programma scrive "Perfetto! Telefono collegato".
3. Premi Avanti e scegli quali foto e video copiare.

NON devi attivare il Debug USB e non devi cambiare nessuna impostazione: il programma usa
il collegamento normale del telefono, lo stesso che vede Esplora file quando apri "Questo PC".
Le foto arrivano direttamente nella cartella che scegli, senza ricreare le cartelle del
telefono (se le vuoi, c'e' una casella per riattivarle).

Se il telefono non viene riconosciuto, prova in quest'ordine:
1. usa un altro cavo USB (alcuni cavi servono solo per ricaricare);
2. cambia porta del computer (evita adattatori e hub);
3. sblocca lo schermo del telefono e rispondi "Consenti" se compare una richiesta;
4. scollega e ricollega il cavo tenendo il telefono sbloccato;
5. se non basta, nel programma premi "Il telefono non viene riconosciuto?": spiega cos'e'
   il Debug USB (e' l'ultima possibilita', non un passaggio obbligato);
6. su Windows, se ancora niente: installa il driver USB del produttore del telefono
   (Samsung, Xiaomi, Huawei... lo hanno sul loro sito).


SE QUALCOSA NON FUNZIONA
------------------------
- Diagnosi completa: apri il prompt dei comandi in questa cartella e scrivi
      py fotofacile.py doctor
  (oppure: python fotofacile.py doctor)
  Nella riga "Modi di collegamento" vedi se il collegamento diretto e' disponibile:
  se lo e', il Debug USB non serve assolutamente a niente.
- Controllo della grafica:
      py fotofacile.py --selftest
  Se risponde {"ok": true, ...} la finestra funziona.
- Registro di avvio (dice sempre perche' il programma non si e' aperto):
      %USERPROFILE%\\.fotofacile\\avvio.log
- Se Windows avvisa che l'eseguibile non e' firmato ("SmartScreen"): clic su
  "Ulteriori informazioni" e poi "Esegui comunque". Succede con tutti i programmi
  appena creati e non firmati.
- Se l'antivirus segnala l'eseguibile: e' un falso allarme tipico dei programmi creati con
  PyInstaller; puoi aggiungere la cartella alle eccezioni oppure usare il modo 1.

Il programma non ha bisogno di internet per funzionare: lo usa solo (una volta, se manca)
per scaricare il componente di collegamento ufficiale di Google e, se lo chiedi, Python.
"""


def _copia_albero(sorgente: Path, destinazione: Path) -> None:
    destinazione.mkdir(parents=True, exist_ok=True)
    for voce in sorted(sorgente.rglob("*")):
        if "__pycache__" in voce.parts or voce.name == ".DS_Store":
            continue
        relativo = voce.relative_to(sorgente)
        if voce.is_dir():
            (destinazione / relativo).mkdir(parents=True, exist_ok=True)
        elif voce.suffix in (".py", ".md", ".txt", ".ico", ".png", ".ps1", ".json"):
            # `.ps1` è indispensabile: è l'aiutante che permette di leggere il telefono
            # **senza Debug USB** su Windows. Senza di esso il pacchetto non funziona.
            shutil.copy2(voce, destinazione / relativo)


def _scrivi_testo(percorso: Path, contenuto: str) -> Path:
    """Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe."""
    righe = contenuto.replace("\r\n", "\n").split("\n")
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_bytes("\r\n".join(righe).encode("utf-8"))
    return percorso


def _controlla_destinazione(cartella: Path, forza: bool) -> None:
    """Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la destinazione."""
    if not cartella.exists():
        return
    risolta = cartella.resolve()
    radice_repo = RADICE.resolve()
    if (
        risolta == Path(risolta.anchor)  # radice del disco («/» oppure «C:\»)
        or risolta == Path.cwd().resolve()  # cartella corrente
        or risolta == Path.home().resolve()  # cartella personale
        or risolta == radice_repo  # il progetto stesso
        or risolta in radice_repo.parents  # una cartella che contiene il progetto
    ):
        raise SystemExit(
            f"Errore: non cancello «{risolta}» per sicurezza "
            "(è la radice del disco, la cartella corrente, la cartella personale "
            "o una cartella che contiene il progetto FotoFacile).\n"
            "Scegli una destinazione diversa, per esempio:\n"
            "  python3 scripts/crea_pacchetto_windows.py ~/Desktop/FotoFacile-per-Windows"
        )
    if not forza and not any((risolta / nome).exists() for nome in MARCATORI_PACCHETTO):
        raise SystemExit(
            f"Errore: «{risolta}» esiste già e non sembra un pacchetto di FotoFacile "
            "(mancano «Avvia FotoFacile.bat», «LEGGIMI - Windows.txt» e la cartella «fotofacile»).\n"
            "Se sei sicuro di volerla cancellare, ripeti con --force:\n"
            f'  python3 scripts/crea_pacchetto_windows.py --force "{risolta}"'
        )


def crea_pacchetto(destinazione: Path | None = None, forza: bool = False) -> Path:
    """Crea la cartella pronta per Windows e restituisce il percorso.

    `forza` permette di cancellare una cartella esistente che non sembra un pacchetto di
    FotoFacile; senza di esso ci si ferma, per non cancellare per sbaglio dati altrui.
    """
    cartella = Path(destinazione) if destinazione is not None else Path.home() / "Desktop" / NOME_CARTELLA
    _controlla_destinazione(cartella, forza)
    if cartella.exists():
        shutil.rmtree(cartella)
    cartella.mkdir(parents=True, exist_ok=True)

    for nome in FILE_DA_COPIARE:
        origine = RADICE / nome
        if origine.is_file():
            (cartella / nome).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origine, cartella / nome)
    for nome in CARTELLE_DA_COPIARE:
        _copia_albero(RADICE / nome, cartella / nome)

    _scrivi_testo(cartella / "Avvia FotoFacile.bat", AVVIO_BAT)
    _scrivi_testo(cartella / "Crea l'eseguibile per Windows.bat", ESEGUIBILE_BAT)
    _scrivi_testo(cartella / "LEGGIMI - Windows.txt", LEGGIMI)

    # installer vero: avvio dal pacchetto + script PowerShell accanto
    origine_installer = RADICE / "installer" / "windows"
    _scrivi_testo(
        cartella / "Installa FotoFacile.bat",
        (origine_installer / "Installa Foto Facile.bat").read_text(encoding="utf-8")
        if (origine_installer / "Installa Foto Facile.bat").is_file()
        else (origine_installer / "Installa FotoFacile.bat").read_text(encoding="utf-8"),
    )
    for nome in ("InstallaFotoFacile.ps1", "DisinstallaFotoFacile.ps1", "FotoFacile.iss"):
        sorgente = origine_installer / nome
        if sorgente.is_file():
            _scrivi_testo(cartella / "installer" / "windows" / nome, sorgente.read_text(encoding="utf-8"))

    # pulizia finale: Finder crea da solo file .DS_Store che su Windows non servono
    for residuo in cartella.rglob(".DS_Store"):
        residuo.unlink(missing_ok=True)
    return cartella


def main(destinazione: str | None = None, forza: bool = False) -> int:
    cartella = crea_pacchetto(Path(destinazione) if destinazione else None, forza=forza)
    file_totali = sum(1 for _ in cartella.rglob("*") if _.is_file())
    peso = sum(_.stat().st_size for _ in cartella.rglob("*") if _.is_file()) / 1024 / 1024
    print(f"Cartella pronta: {cartella}")
    print(f"  {file_totali} file, {peso:.2f} MB")
    print("\nSu Windows:")
    print("  1. doppio clic su «Avvia FotoFacile.bat»               → usa subito il programma")
    print("  2. doppio clic su «Crea l'eseguibile per Windows.bat»   → crea FotoFacile.exe")
    print("  3. copia la cartella dist\\FotoFacile su chiavetta       → funziona senza Python")
    return 0


if __name__ == "__main__":
    argomenti = [argomento for argomento in sys.argv[1:] if argomento != "--force"]
    raise SystemExit(main(argomenti[0] if argomenti else None, forza="--force" in sys.argv[1:]))

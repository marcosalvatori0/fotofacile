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

    python3 scripts/crea_pacchetto_windows.py [cartella_destinazione]
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
NOME_CARTELLA = "FotoFacile per Windows"
CARTELLE_DA_COPIARE = ("fotofacile",)
FILE_DA_COPIARE = (
    "fotofacile.py",
    "README.md",
    "requirements-dev.txt",
    "scripts/build_app.py",
    "scripts/make_icon.py",
    "assets/fotofacile.ico",
    "assets/fotofacile.png",
)

AVVIO_BAT = r"""@echo off
chcp 65001 >nul
setlocal EnableExtensions
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
echo     In alternativa scaricalo da: https://www.python.org/downloads/windows/
echo  2) Durante l'installazione spunta "Add python.exe to PATH".
echo  3) Poi fai di nuovo doppio clic su "Avvia FotoFacile.bat".
echo.
echo  Oppure, per avere un eseguibile che non richiede Python:
echo  fai doppio clic su "Crea l'eseguibile per Windows.bat".
echo ------------------------------------------------------------
echo.
pause
exit /b 1

:avvia
echo Uso Python con: %PY%
%PY% -c "import tkinter" >nul 2>nul
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
)
echo.
pause
exit /b 0

:trova_python
rem preferisce il launcher ufficiale "py" con Python 3, poi "python", poi "python3"
for %%C in ("py -3" "python" "python3") do (
  %%~C -c "import sys; raise SystemExit(0 if sys.version_info ^>= (3, 9) else 1)" >nul 2>nul
  if not errorlevel 1 (
    set "PY=%%~C"
    exit /b 0
  )
)
exit /b 0
"""

ESEGUIBILE_BAT = r"""@echo off
chcp 65001 >nul
setlocal EnableExtensions
cd /d "%~dp0"
title FotoFacile - crea l'eseguibile

echo ============================================================
echo   Creo l'eseguibile di FotoFacile per Windows
echo ============================================================
echo.

set "PY="
call :trova_python
if not defined PY (
  echo Serve Python per creare l'eseguibile.
  echo Fai prima doppio clic su "Avvia FotoFacile.bat": installa Python se manca.
  echo.
  pause
  exit /b 1
)

echo Uso Python con: %PY%
echo.
echo 1 di 3 - installo/aggiorno PyInstaller...
%PY% -m pip install --upgrade pip pyinstaller
if errorlevel 1 (
  echo.
  echo Non sono riuscito a installare PyInstaller: controlla la connessione a internet.
  pause
  exit /b 1
)

echo.
echo 2 di 3 - creo l'eseguibile (puo' richiedere 1-2 minuti)...
%PY% scripts\build_app.py
if errorlevel 1 (
  echo.
  echo La creazione non e' riuscita: il messaggio sopra dice il motivo.
  pause
  exit /b 1
)

echo.
echo 3 di 3 - provo l'eseguibile appena creato...
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
for %%C in ("py -3" "python" "python3") do (
  %%~C -c "import sys; raise SystemExit(0 if sys.version_info ^>= (3, 9) else 1)" >nul 2>nul
  if not errorlevel 1 (
    set "PY=%%~C"
    exit /b 0
  )
)
exit /b 0
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


PRIMA VOLTA: fai autorizzare il telefono (una volta sola)
---------------------------------------------------------
1. Collega il telefono con il cavo USB e sblocca lo schermo.
2. Nel programma premi "Come si attiva il Debug USB?" e segui i passi della tua marca
   (Samsung, Xiaomi, Google, Huawei, Oppo...).
3. Quando il telefono chiede "Consentire il debug USB?", tocca "Consenti".
4. Il programma scrive "Perfetto! Telefono collegato": premi Avanti e scegli le foto.

Se il telefono non viene riconosciuto: prova un altro cavo USB (alcuni ricaricano soltanto),
un'altra porta, e installa il driver USB del produttore del telefono.


SE QUALCOSA NON FUNZIONA
------------------------
- Diagnosi completa: apri il prompt dei comandi in questa cartella e scrivi
      py fotofacile.py doctor
  (oppure: python fotofacile.py doctor)
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
        elif voce.suffix in (".py", ".md", ".txt", ".ico", ".png"):
            shutil.copy2(voce, destinazione / relativo)


def _scrivi_testo(percorso: Path, contenuto: str) -> Path:
    """Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe."""
    righe = contenuto.replace("\r\n", "\n").split("\n")
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_bytes("\r\n".join(righe).encode("utf-8"))
    return percorso


def crea_pacchetto(destinazione: Path | None = None) -> Path:
    """Crea la cartella pronta per Windows e restituisce il percorso."""
    cartella = Path(destinazione) if destinazione is not None else Path.home() / "Desktop" / NOME_CARTELLA
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

    # pulizia finale: Finder crea da solo file .DS_Store che su Windows non servono
    for residuo in cartella.rglob(".DS_Store"):
        residuo.unlink(missing_ok=True)
    return cartella


def main(destinazione: str | None = None) -> int:
    cartella = crea_pacchetto(Path(destinazione) if destinazione else None)
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
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))

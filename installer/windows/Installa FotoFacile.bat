@echo off
chcp 65001 >nul
setlocal EnableExtensions
cd /d "%~dp0"
title FotoFacile - installazione

echo ============================================================
echo   Installazione di FotoFacile su questo computer
echo ============================================================
echo.
echo Il programma verra' installato nella cartella personale
echo (non servono privilegi di amministratore) e comparira' nel
echo menu Start e, se vuoi, sul Desktop.
echo.
echo Per disinstallarlo: Impostazioni - App - FotoFacile, oppure il
echo file "Disinstalla FotoFacile.bat" nella cartella del programma.
echo.

where powershell >nul 2>nul
if errorlevel 1 goto niente_powershell

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer\windows\InstallaFotoFacile.ps1" %*
set "CODICE=%ERRORLEVEL%"
echo.
if not "%CODICE%"=="0" (
  echo ------------------------------------------------------------
  echo  L'installazione non e' riuscita ^(codice %CODICE%^).
  echo  Prova a eseguire come amministratore, oppure usa il pacchetto
  echo  "Avvia FotoFacile.bat" senza installare nulla.
  echo ------------------------------------------------------------
)
pause
exit /b %CODICE%

:niente_powershell
echo Non trovo PowerShell su questo computer: usa "Avvia FotoFacile.bat".
pause
exit /b 1

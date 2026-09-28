# FotoFacile — programma di installazione per Windows (PowerShell)
#
# Installa FotoFacile per l'utente corrente, senza chiedere privilegi di amministratore:
#   * copia i file in %LOCALAPPDATA%\Programs\FotoFacile
#   * crea il collegamento sul Desktop e nel menu Start
#   * registra la voce in «App e funzionalità» con il comando di disinstallazione
#
# Funziona in due modi:
#   1. con l'eseguibile già creato (cartella «dist\FotoFacile» accanto a questo file);
#   2. senza eseguibile, installando i sorgenti e usando Python (che il programma di
#      installazione verifica o installa con winget).
#
# Uso:  powershell -NoProfile -ExecutionPolicy Bypass -File InstallaFotoFacile.ps1

param(
    [string]$Sorgente = "",
    [string]$Versione = "0.1.0",
    [switch]$Silenzioso
)

$ErrorActionPreference = "Stop"
$Nome = "FotoFacile"
$Destinazione = Join-Path $env:LOCALAPPDATA "Programs\$Nome"
$Chiave = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$Nome"
$CartellaScript = Split-Path -Parent $MyInvocation.MyCommand.Path
$Radice = Split-Path -Parent (Split-Path -Parent $CartellaScript)

function Scrivi($testo, $colore = "Gray") {
    Write-Host $testo -ForegroundColor $colore
}

function Trova-Eseguibile {
    $possibili = @(
        (Join-Path $Radice "dist\FotoFacile\$Nome.exe"),
        (Join-Path $Radice "installer\FotoFacile.exe"),
        (Join-Path $Radice "$Nome.exe")
    )
    foreach ($percorso in $possibili) {
        if (Test-Path $percorso) { return $percorso }
    }
    return $null
}

function Trova-Python {
    foreach ($candidato in @(@("py", "-3"), @("python"), @("python3"))) {
        try {
            $esito = & $candidato[0] $candidato[1..($candidato.Count - 1)] -c "import sys,tkinter; raise SystemExit(0 if sys.version_info >= (3,9) else 1)" 2>$null
            if ($LASTEXITCODE -eq 0) { return ($candidato -join " ") }
        } catch { }
    }
    return $null
}

function Crea-Collegamento($percorso, $destinazione, $icona) {
    $shell = New-Object -ComObject WScript.Shell
    $collegamento = $shell.CreateShortcut($percorso)
    $collegamento.TargetPath = $destinazione
    $collegamento.WorkingDirectory = (Split-Path -Parent $destinazione)
    $collegamento.Description = "Copia le foto dal telefono Android al computer"
    if ($icona -and (Test-Path $icona)) { $collegamento.IconLocation = $icona }
    $collegamento.Save()
}

Scrivi ""
Scrivi "==========================================================" "Cyan"
Scrivi "  Installazione di $Nome $Versione" "Cyan"
Scrivi "==========================================================" "Cyan"
Scrivi ""

$eseguibile = if ($Sorgente -and (Test-Path $Sorgente)) { $Sorgente } else { Trova-Eseguibile }
$modalitaSorgente = $false
if (-not $eseguibile) {
    Scrivi "Non trovo l'eseguibile: installerò la versione che usa Python." "Yellow"
    $modalitaSorgente = $true
    $python = Trova-Python
    if (-not $python) {
        Scrivi ""
        Scrivi "Python non è installato. Posso installarlo io con winget." "Yellow"
        $risposta = Read-Host "Installo Python 3.13 adesso? [S/n]"
        if ($risposta -ne "n" -and $risposta -ne "N") {
            if (Get-Command winget -ErrorAction SilentlyContinue) {
                winget install -e --id Python.Python.3.13 --accept-package-agreements --accept-source-agreements
                $python = Trova-Python
            }
        }
    }
    if (-not $python) {
        Scrivi ""
        Scrivi "Per finire l'installazione serve Python 3.9 o successivo:" "Red"
        Scrivi "  https://www.python.org/downloads/windows/  (spunta «Add python.exe to PATH»)" "Red"
        Scrivi "oppure, per non installare nulla, prova «Crea l'eseguibile per Windows.bat»." "Red"
        exit 1
    }
    Scrivi "Userò Python con: $python" "DarkGray"
}

if (Test-Path $Destinazione) {
    Scrivi "Aggiorno l'installazione esistente in $Destinazione" "DarkGray"
    Remove-Item -Recurse -Force $Destinazione
}
New-Item -ItemType Directory -Force -Path $Destinazione | Out-Null

$avvio = $null
$icona = $null
if ($modalitaSorgente) {
    Copy-Item -Path (Join-Path $Radice "fotofacile.py") -Destination $Destinazione -Force
    Copy-Item -Path (Join-Path $Radice "fotofacile") -Destination $Destinazione -Recurse -Force
    $avvioAuto = @"
@echo off
cd /d "%~dp0"
$python fotofacile.py
if errorlevel 1 (
  $python fotofacile.py doctor
  pause
)
"@
    $avvio = Join-Path $Destinazione "FotoFacile.bat"
    Set-Content -Path $avvio -Value $avvioAuto -Encoding UTF8
    Set-Content -Path (Join-Path $Destinazione "Versione.txt") -Value "$Nome $Versione (modalità Python)" -Encoding UTF8
} else {
    Copy-Item -Path (Join-Path (Split-Path -Parent $eseguibile) "*") -Destination $Destinazione -Recurse -Force
    $avvio = Join-Path $Destinazione (Split-Path -Leaf $eseguibile)
    $icona = Get-ChildItem -Path $Destinazione -Filter "*.ico" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
}

# disinstallatore accanto al programma
$disinstalla = Join-Path $Destinazione "Disinstalla FotoFacile.bat"
Copy-Item -Path (Join-Path $CartellaScript "DisinstallaFotoFacile.ps1") -Destination $Destinazione -Force
$testoDisinstalla = @"
@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0DisinstallaFotoFacile.ps1"
pause
"@
Set-Content -Path $disinstalla -Value $testoDisinstalla -Encoding UTF8

Scrivi "File installati in: $Destinazione" "Green"

# collegamenti
$desktop = [Environment]::GetFolderPath("Desktop")
$startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
Crea-Collegamento (Join-Path $desktop "$Nome.lnk") $avvio $icona
Crea-Collegamento (Join-Path $startMenu "$Nome.lnk") $avvio $icona
Scrivi "Collegamenti creati sul Desktop e nel menu Start." "Green"

# voce in «App e funzionalità»
New-Item -Path $Chiave -Force | Out-Null
Set-ItemProperty -Path $Chiave -Name "DisplayName" -Value $Nome
Set-ItemProperty -Path $Chiave -Name "DisplayVersion" -Value $Versione
Set-ItemProperty -Path $Chiave -Name "Publisher" -Value "FotoFacile"
Set-ItemProperty -Path $Chiave -Name "InstallLocation" -Value $Destinazione
Set-ItemProperty -Path $Chiave -Name "DisplayIcon" -Value $(if ($icona) { $icona } else { $avvio })
Set-ItemProperty -Path $Chiave -Name "UninstallString" -Value "`"$disinstalla`""
Set-ItemProperty -Path $Chiave -Name "QuietUninstallString" -Value "`"$disinstalla`""
Set-ItemProperty -Path $Chiave -Name "NoModify" -Value 1 -Type DWord
Set-ItemProperty -Path $Chiave -Name "NoRepair" -Value 1 -Type DWord
$peso = (Get-ChildItem -Recurse $Destinazione | Measure-Object -Property Length -Sum).Sum
if ($peso) { Set-ItemProperty -Path $Chiave -Name "EstimatedSize" -Value ([int]($peso / 1KB)) -Type DWord }
Scrivi "Registrato in «App e funzionalità» (disinstallazione da lì o dal collegamento)." "Green"

Scrivi ""
Scrivi "Installazione completata." "Cyan"
Scrivi "Avvia $Nome dal collegamento sul Desktop." "Cyan"
Scrivi "Prima volta: sblocca il telefono, attiva il Debug USB e tocca «Consenti»." "Cyan"
Scrivi ""

if (-not $Silenzioso) {
    $prova = Read-Host "Vuoi aprire $Nome adesso? [S/n]"
    if ($prova -ne "n" -and $prova -ne "N") { Start-Process $avvio }
}
exit 0

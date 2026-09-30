# Prova automatica dell'installatore (SOLO per la pipeline GitHub, mai per l'utente).
# Installa in una cartella temporanea, controlla che il programma parta e lo disinstalla.
param(
    [Parameter(Mandatory = $true)][string]$Installatore,
    [string]$Cartella = "$env:RUNNER_TEMP\prova-fotofacile"
)
$ErrorActionPreference = "Stop"
$log = Join-Path (Get-Location) "log-installazione.txt"

function Fallisci($messaggio) {
    Write-Host "ERRORE: $messaggio" -ForegroundColor Red
    if (Test-Path -LiteralPath $log) { Get-Content -LiteralPath $log -Tail 40 }
    exit 1
}

if (-not (Test-Path -LiteralPath $Installatore)) { Fallisci "non trovo l'installatore $Installatore" }
$installatore = (Resolve-Path -LiteralPath $Installatore).Path

# 1. installazione silenziosa
$argomenti = @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-", "/DIR=`"$Cartella`"", "/LOG=`"$log`"")
$p = Start-Process -FilePath $installatore -ArgumentList $argomenti -Wait -PassThru
if ($p.ExitCode -ne 0) { Fallisci "l'installatore è uscito con codice $($p.ExitCode)" }

$exe = Join-Path $Cartella "FotoFacile.exe"
$disinstallatore = Join-Path $Cartella "unins000.exe"
if (-not (Test-Path -LiteralPath $exe)) { Fallisci "FotoFacile.exe non è stato installato in $Cartella" }
if (-not (Test-Path -LiteralPath $disinstallatore)) { Fallisci "manca il programma di disinstallazione" }

# 2. voce in «App e funzionalità» (installazione senza amministratore: sta in HKCU)
$chiave = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}_is1"
if (-not (Test-Path -LiteralPath $chiave)) { Fallisci "manca la voce di disinstallazione nel registro" }

# 3. il programma installato parte e la diagnosi produce un rapporto (l'exe non ha finestra
#    nera: l'esito si legge dai file, vedi verifica-eseguibile.ps1)
$global:LASTEXITCODE = 0
& (Join-Path $PSScriptRoot "verifica-eseguibile.ps1") -Eseguibile $exe
if ($LASTEXITCODE -ne 0) { Fallisci "la verifica del programma installato è fallita" }

# 4. disinstallazione silenziosa e pulita. Il disinstallatore di Inno Setup si copia in una
#    cartella temporanea e può tornare prima di aver finito: si aspetta che sparisca davvero.
$u = Start-Process -FilePath $disinstallatore -ArgumentList @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART") -Wait -PassThru
if ($u.ExitCode -ne 0) { Fallisci "la disinstallazione è uscita con codice $($u.ExitCode)" }
$limite = (Get-Date).AddSeconds(90)
while ((Test-Path -LiteralPath $exe) -or (Test-Path -LiteralPath $chiave)) {
    if ((Get-Date) -gt $limite) { break }
    Start-Sleep -Seconds 1
}
if (Test-Path -LiteralPath $exe) { Fallisci "dopo la disinstallazione FotoFacile.exe c'è ancora" }
if (Test-Path -LiteralPath $chiave) { Fallisci "dopo la disinstallazione la voce nel registro c'è ancora" }
Write-Host "Installazione, avvio e disinstallazione: tutto ok." -ForegroundColor Green

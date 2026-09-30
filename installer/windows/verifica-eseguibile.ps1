# Verifica un FotoFacile.exe già costruito o già installato (SOLO per la pipeline GitHub).
#
# L'eseguibile è senza finestra nera: non scrive niente sullo schermo e il codice di uscita
# da solo non basta. L'esito vero sta nei file che scrive in %USERPROFILE%\.fotofacile:
#   selftest.txt  ->  {"ok": true, ...} se la parte grafica funziona
#   diagnosi.txt  ->  il rapporto di «doctor»
# Prima di ogni prova i file vecchi vengono cancellati, così non si legge un esito di ieri.
param(
    [Parameter(Mandatory = $true)][string]$Eseguibile
)
$ErrorActionPreference = "Stop"

# «doctor» di norma apre il Blocco note: sul runner non deve, o l'attesa resterebbe appesa.
$env:FOTOFACILE_NO_OPEN = "1"

function Fallisci($messaggio) {
    Write-Host "ERRORE: $messaggio" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $Eseguibile)) { Fallisci "non trovo $Eseguibile" }
$exe = (Resolve-Path -LiteralPath $Eseguibile).Path
$cartellaProgramma = Split-Path -Parent $exe
$cartellaDati = Join-Path $env:USERPROFILE ".fotofacile"
$fileSelftest = Join-Path $cartellaDati "selftest.txt"
$fileDiagnosi = Join-Path $cartellaDati "diagnosi.txt"

function Leggi($percorso) {
    return [System.IO.File]::ReadAllText($percorso, [System.Text.Encoding]::UTF8)
}

# 1. lo script del collegamento diretto (PowerShell/WPD) deve essere dentro il pacchetto
$aiutante = Get-ChildItem -LiteralPath $cartellaProgramma -Recurse -Filter "wpd_win.ps1" -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $aiutante) { Fallisci "nel pacchetto manca wpd_win.ps1 (il collegamento diretto non funzionerebbe)" }

# 2. autocollaudo: apre la finestra (nascosta), costruisce le pagine e si chiude
Remove-Item -LiteralPath $fileSelftest -Force -ErrorAction SilentlyContinue
$s = Start-Process -FilePath $exe -ArgumentList "--selftest" -Wait -PassThru
if (-not (Test-Path -LiteralPath $fileSelftest)) {
    Fallisci "l'autocollaudo non ha scritto $fileSelftest (codice di uscita $($s.ExitCode))"
}
$testoSelftest = Leggi $fileSelftest
Write-Host "selftest.txt: $testoSelftest"
try { $esito = $testoSelftest | ConvertFrom-Json } catch { Fallisci "selftest.txt non è leggibile: $testoSelftest" }
if ($esito.ok -ne $true) { Fallisci "l'autocollaudo è fallito: $($esito.motivo)" }
if ($s.ExitCode -ne 0) { Fallisci "l'autocollaudo dice ok ma il codice di uscita è $($s.ExitCode)" }

# 3. diagnosi: un rapporto leggibile che dice anche se Pillow (conversione WebP) è nel pacchetto
Remove-Item -LiteralPath $fileDiagnosi -Force -ErrorAction SilentlyContinue
$d = Start-Process -FilePath $exe -ArgumentList "doctor" -Wait -PassThru
if (-not (Test-Path -LiteralPath $fileDiagnosi)) {
    Fallisci "la diagnosi non ha scritto $fileDiagnosi (codice di uscita $($d.ExitCode))"
}
$testoDiagnosi = Leggi $fileDiagnosi
Write-Host $testoDiagnosi
if ($testoDiagnosi -notmatch "diagnosi") { Fallisci "il rapporto della diagnosi è vuoto o sbagliato" }
if ($testoDiagnosi -notmatch "Conversione WebP: disponibile") {
    Fallisci "Pillow non è dentro il pacchetto: la conversione WebP non sarebbe disponibile"
}
Write-Host "Verifica di $exe: tutto ok." -ForegroundColor Green
exit 0

# FotoFacile — disinstallazione (PowerShell)
#
# Rimuove collegamenti, voce in «App e funzionalità» e la cartella del programma.
# I file scaricati dall'app (componente di collegamento, cronologia, registro) restano in
# %USERPROFILE%\.fotofacile e vengono elencati alla fine, così l'utente decide se cancellarli.

$ErrorActionPreference = "Continue"
$Nome = "FotoFacile"
$Destinazione = Split-Path -Parent $MyInvocation.MyCommand.Path
$Chiave = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$Nome"

Write-Host ""
Write-Host "Disinstallazione di $Nome" -ForegroundColor Cyan
Write-Host ""

foreach ($collegamento in @(
        (Join-Path ([Environment]::GetFolderPath("Desktop")) "$Nome.lnk"),
        (Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$Nome.lnk")
    )) {
    if (Test-Path $collegamento) {
        Remove-Item $collegamento -Force
        Write-Host "Rimosso il collegamento: $collegamento"
    }
}

if (Test-Path $Chiave) {
    Remove-Item $Chiave -Recurse -Force
    Write-Host "Rimossa la voce da «App e funzionalità»."
}

# non si può cancellare la cartella mentre il file di disinstallazione è in esecuzione da lì:
# si sposta tutto in una cartella temporanea e si cancella quella.
$temporanea = Join-Path $env:TEMP "fotofacile-disinstallazione"
if (Test-Path $temporanea) { Remove-Item $temporanea -Recurse -Force -ErrorAction SilentlyContinue }
Move-Item -Path $Destinazione -Destination $temporanea -Force
Start-Process -FilePath "cmd.exe" -ArgumentList "/c rmdir /s /q `"$temporanea`"" -WindowStyle Hidden
Write-Host "Programma rimosso da: $Destinazione"

$dati = Join-Path $env:USERPROFILE ".fotofacile"
if (Test-Path $dati) {
    Write-Host ""
    Write-Host "Restano i dati del programma (componente di collegamento, cronologia, registro):" -ForegroundColor Yellow
    Write-Host "  $dati" -ForegroundColor Yellow
    $risposta = Read-Host "Vuoi cancellarli anche loro? [s/N]"
    if ($risposta -eq "s" -or $risposta -eq "S") {
        Remove-Item $dati -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Dati cancellati." -ForegroundColor Green
    } else {
        Write-Host "Dati lasciati al loro posto."
    }
}

Write-Host ""
Write-Host "Disinstallazione completata." -ForegroundColor Cyan

# FotoFacile — aiutante Windows: parla con il telefono tramite WPD (Portable Devices).
#
# Perché serve: Windows non legge i telefoni Android come dischi, ma li presenta come
# «dispositivi portatili» dentro «Questo PC». Il modo per parlarci è il componente
# Shell.Application (lo stesso qui usa Esplora file): non è raggiungibile dalla libreria
# standard di Python, ma lo è da PowerShell, che c'è su ogni Windows dal 7 in poi.
#
# Perché uno script separato dal resto: le copie WPD sono asincrone (CopyHere ritorna
# subito) e possono mostrare finestre di avanzamento; tenerle in un processo a parte
# significa che il programma principale può interromperle senza mai bloccare la finestra.
#
# Uso (lo avvia fotofacile/aiutanti/wpd_win.py, non si chiama a mano):
#   powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -File wpd_win.ps1 -Comando dispositivi
#   ... -Comando elenca  -Seriale S [-SoloFoto]
#   ... -Comando copia   -Seriale S -Percorso P -Destinazione CARTELLA
#   ... -Comando cancella -Seriale S -Percorso P
#
# L'uscita standard è sempre leggibile a macchina (JSON UTF-8, scritto direttamente sul
# flusso); i messaggi per la persona vanno sull'uscita degli errori. Codici di uscita:
# 0 tutto bene, 2 errore, 3 nessun telefono.
#
# Nota sulla codifica: questo file è UTF-8 **con** BOM, e deve restare così.
# Windows PowerShell 5.1 legge i file senza BOM con la codifica ANSI del sistema:
# senza BOM gli accenti delle frasi italiane diventano caratteri illeggibili e alcuni
# confronti fra testo (per esempio il tipo di dispositivo) smettono di funzionare.
# Il BOM qui non dà alcun fastidio: i file destinati a cmd.exe sono i `.bat`, che
# vengono scritti a parte senza BOM.

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("dispositivi", "elenca", "copia", "cancella")]
    [string]$Comando,
    [string]$Seriale = "",
    [string]$Percorso = "",
    [string]$Destinazione = "",
    [switch]$SoloFoto,
    [int]$PidSupervisionato = 0,
    [int]$AttesaSecondi = 1500
)

# Ogni guaio va raccontato e tradotto in un codice del contratto: senza questo,
# un'eccezione non gestita uscirebbe con codici diversi da 0/2/3 e il programma
# principale non saprebbe cosa dire all'utente.
$ErrorActionPreference = "Stop"

# ── uscita a prova di codifica ───────────────────────────────────────────
# Si scrive direttamente sul flusso standard in UTF-8, senza passare dalla formattazione
# di PowerShell: così l'uscita non dipende dalla lingua di Windows e non compaiono BOM o
# intestazioni che romperebbero la lettura a righe JSON.

$script:FlussoOut = [System.Console]::OpenStandardOutput()
$script:FlussoErr = [System.Console]::OpenStandardError()

function Scrivi-Riga([string]$Testo) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Testo + "`n")
    $script:FlussoOut.Write($bytes, 0, $bytes.Length)
    $script:FlussoOut.Flush()
}

function Scrivi-Errore([string]$Testo) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Testo + "`n")
    $script:FlussoErr.Write($bytes, 0, $bytes.Length)
    $script:FlussoErr.Flush()
}

function Esci-SenzaTelefono([string]$Testo) {
    Scrivi-Errore $Testo
    exit 3
}

function Test-Supervisione([int]$PidDaControllare) {
    # Quando l'app annulla una copia, uccide questo aiutante: il suo processo sparisce, ma
    # PowerShell (che è un processo figlio) resterebbe vivo a copiare per conto suo,
    # tenendo occupati telefono e disco e lasciando un file «a metà» non cancellabile.
    # Controllando il processo genitore si accorge subito che non c'è più nessuno ad
    # ascoltare e si ferma pulito.
    if (-not $PidDaControllare) { return $true }
    try {
        $null = Get-Process -Id $PidDaControllare -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# ── le stesse estensioni di fotofacile/aiutanti/ptp_mac.py ───────────────
# Se cambiano là, vanno cambiate anche qui: il contratto dell'aiutante è lo stesso su
# tutti i sistemi.

$script:EstensioniFoto = @(
    "jpg", "jpeg", "png", "gif", "webp", "heic", "heif", "bmp", "tif", "tiff", "dng", "avif"
)
$script:EstensioniVideo = @(
    "mp4", "3gp", "3gpp", "mov", "mkv", "avi", "webm", "m4v", "mts"
)
$script:Conteggio = 0
$script:VociVisitate = 0

# Le copie WPD non devono mostrare niente: in un processo senza persona davanti, una
# finestra di avanzamento o una richiesta di conferma resterebbe appesa per sempre.
#   0x4   nessuna finestra di avanzamento
#   0x10  «Sì a tutti» per ogni eventuale richiesta
#   0x200 nessuna conferma di creazione cartelle
#   0x400 nessun messaggio in caso di errore
$script:FlagCopia = 0x4 -bor 0x10 -bor 0x200 -bor 0x400

# ── il telefono visto da Windows ─────────────────────────────────────────

function Apri-Shell {
    return New-Object -ComObject Shell.Application
}

function Nome-Voce($Voce) {
    try { return [string]$Voce.Name } catch { return "" }
}

function Percorso-Voce($Voce) {
    try { return [string]$Voce.Path } catch { return "" }
}

function Tipo-Voce($Voce) {
    try { return [string]$Voce.Type } catch { return "" }
}

function Test-DispositivoPortatile($Voce) {
    # Un disco o una cartella vera non è un telefono: «IsFileSystem» lo dice senza
    # dipendere dalla lingua di Windows.
    try { if ($Voce.IsFileSystem) { return $false } } catch { }
    # «Type» è tradotto nella lingua di Windows: non basta la forma inglese.
    $tipo = Tipo-Voce $Voce
    if ($tipo -eq "Portable Device" -or $tipo -eq "Dispositivo portatile") { return $true }
    # I dispositivi portatili hanno un percorso di tipo shell («\\?\usb#...» oppure
    # «::{...}»), non un'unità con lettera: è il segno che li distingue dai dischi.
    $percorso = Percorso-Voce $Voce
    if ($percorso.StartsWith('\\?\') -or $percorso.StartsWith('::')) { return $true }
    return $false
}

function Seriale-Dispositivo($Voce) {
    # Il percorso shell (una stringa «\\?\usb#...#serial#...») è stabile fra un
    # collegamento e l'altro; il nome mostrato no (cambia con la lingua e col modello).
    $percorso = Percorso-Voce $Voce
    if ($percorso) { return $percorso }
    return Nome-Voce $Voce
}

function Elenco-Dispositivi($Shell) {
    $pc = $Shell.Namespace(17)  # 17 = «Questo PC» (ssfDRIVES)
    if ($null -eq $pc) { return @() }
    $trovati = @()
    foreach ($voce in @($pc.Items())) {
        if (Test-DispositivoPortatile $voce) { $trovati += , $voce }
    }
    return $trovati
}

function Trova-Dispositivo($Shell, [string]$Voluto) {
    $dispositivi = @(Elenco-Dispositivi $Shell)
    if ($dispositivi.Count -eq 0) {
        Esci-SenzaTelefono "Non vedo nessun telefono collegato."
    }
    if (-not $Voluto) { return $dispositivi[0] }
    foreach ($dispositivo in $dispositivi) {
        if ((Seriale-Dispositivo $dispositivo) -eq $Voluto) { return $dispositivo }
        if ((Nome-Voce $dispositivo) -eq $Voluto) { return $dispositivo }
    }
    Esci-SenzaTelefono "Non trovo il telefono indicato: forse è stato scollegato."
}

# ── file: dimensioni, date, elenco ───────────────────────────────────────

function Dimensione-Voce($Voce) {
    # «System.Size» è il nome canonico della colonna, indipendente dalla lingua.
    try {
        $valore = $Voce.ExtendedProperty("System.Size")
        if ($null -ne $valore) { return [long]$valore }
    } catch { }
    try { return [long]$Voce.Size } catch { return [long]0 }
}

function Data-Voce($Voce) {
    foreach ($proprieta in @("System.DateModified", "System.ItemDate", "System.DateCreated")) {
        try {
            $valore = $Voce.ExtendedProperty($proprieta)
            if ($null -eq $valore) { continue }
            $quando = [datetime]$valore
            $momento = [System.DateTimeOffset]$quando
            return [long]$momento.ToUnixTimeSeconds()
        } catch { }
    }
    return [long]0
}

function Genere-File([string]$NomeFile) {
    $punto = $NomeFile.LastIndexOf(".")
    if ($punto -lt 0) { return "" }
    $estensione = $NomeFile.Substring($punto + 1).ToLowerInvariant()
    if ($script:EstensioniFoto -contains $estensione) { return "photo" }
    if ($script:EstensioniVideo -contains $estensione) { return "video" }
    return ""
}

function Elenca-Cartella($Cartella, [string]$Prefisso, [bool]$SoloFoto) {
    $voci = @()
    try { $voci = @($Cartella.Items()) } catch {
        # Una cartella illeggibile non deve far fallire tutta la ricerca: si salta e si
        # annota sull'uscita degli errori.
        Scrivi-Errore "Salto la cartella $Prefisso : $($_.Exception.Message)"
        return
    }
    foreach ($voce in $voci) {
        $script:VociVisitate = $script:VociVisitate + 1
        if (($script:VociVisitate % 200) -eq 0 -and -not (Test-Supervisione $PidSupervisionato)) {
            # Nessuno sta più aspettando l'elenco: si smette di far lavorare il telefono.
            throw "Il collegamento è stato interrotto."
        }
        $nome = Nome-Voce $voce
        if (-not $nome) { continue }
        $cammino = "$Prefisso/$nome"
        $eCartella = $false
        try { $eCartella = [bool]$voce.IsFolder } catch { $eCartella = $false }
        if ($eCartella) {
            try {
                $sotto = $voce.GetFolder
            } catch {
                Scrivi-Errore "Salto la cartella $cammino : $($_.Exception.Message)"
                continue
            }
            if ($null -ne $sotto) { Elenca-Cartella $sotto $cammino $SoloFoto }
            continue
        }
        $genere = Genere-File $nome
        if (-not $genere) { continue }
        if ($SoloFoto -and $genere -eq "video") { continue }
        $riga = @{
            percorso = $cammino
            dimensione = (Dimensione-Voce $voce)
            data = (Data-Voce $voce)
            genere = $genere
        }
        Scrivi-Riga (ConvertTo-Json $riga -Compress -Depth 5)
        $script:Conteggio = $script:Conteggio + 1
    }
}

function Trova-Voce([string]$Cammino, $Dispositivo) {
    # I percorsi sono quelli stampati da «elenca» («/Internal storage/DCIM/...»): si
    # scende dal telefono cercando ogni pezzo per nome, perché i dispositivi portatili
    # non hanno un percorso di file system da aprire direttamente.
    $parti = @($Cammino.Split("/") | Where-Object { $_ -ne "" })
    if ($parti.Count -eq 0) { return $null }
    $cartella = $Dispositivo.GetFolder
    if ($null -eq $cartella) { return $null }
    $voce = $null
    for ($indice = 0; $indice -lt $parti.Count; $indice++) {
        $voce = $null
        foreach ($figlio in @($cartella.Items())) {
            $script:VociVisitate = $script:VociVisitate + 1
            if (($script:VociVisitate % 200) -eq 0 -and -not (Test-Supervisione $PidSupervisionato)) {
                throw "Il collegamento è stato interrotto."
            }
            if ((Nome-Voce $figlio) -eq $parti[$indice]) { $voce = $figlio; break }
        }
        if ($null -eq $voce) { return $null }
        if ($indice -lt ($parti.Count - 1)) {
            $eCartella = $false
            try { $eCartella = [bool]$voce.IsFolder } catch { $eCartella = $false }
            if (-not $eCartella) { return $null }
            $cartella = $voce.GetFolder
            if ($null -eq $cartella) { return $null }
        }
    }
    return $voce
}

# ── attesa della copia asincrona ─────────────────────────────────────────
# CopyHere ritorna subito: la copia continua in sottofondo. Si aspetta che il file
# esista e che la sua dimensione raggiunga quella dichiarata dal telefono; solo allora
# i byte sono affidabili. Se il telefono non dichiara la dimensione, Comando-Copia
# rinuncia: senza un termine di paragone non si può sapere se la copia è finita.

function Attendi-File([string]$Cartella, [string]$NomeAtteso, [long]$DimensioneAttesa) {
    $orologio = [System.Diagnostics.Stopwatch]::StartNew()
    $prossimoControlloDisco = 0.0
    $file = ""
    while ($true) {
        if (-not (Test-Supervisione $PidSupervisionato)) {
            throw "Il collegamento è stato interrotto."
        }
        if ($orologio.Elapsed.TotalSeconds -gt $AttesaSecondi) {
            throw "Il telefono non ha finito di consegnare il file in tempo."
        }
        if ($orologio.Elapsed.TotalSeconds -ge $prossimoControlloDisco) {
            # Servono due copie del file: quella di appoggio (che prepara Windows) e il
            # «.part» del programma principale. Se lo spazio non basta, CopyHere fallirebbe
            # in silenzio (le finestre di errore sono soppresse) e si aspetterebbe a vuoto:
            # meglio dirlo subito.
            $liberi = [long]-1
            try {
                $unita = (Get-Item -LiteralPath $Cartella).PSDrive
                if ($null -ne $unita -and $null -ne $unita.Free) { $liberi = [long]$unita.Free }
            } catch { $liberi = [long]-1 }
            $richiesti = 2 * $DimensioneAttesa + 4MB
            if ($liberi -ge 0 -and $liberi -lt $richiesti) {
                throw "Non c'è più spazio sul disco per completare la copia."
            }
            $prossimoControlloDisco = $orologio.Elapsed.TotalSeconds + 2.0
        }
        if (-not $file) {
            $candidato = Join-Path $Cartella $NomeAtteso
            if (Test-Path -LiteralPath $candidato -PathType Leaf) {
                $file = $candidato
            } else {
                # Alcuni telefoni cambiano leggermente il nome: si prende comunque il
                # primo file comparso nella cartella di appoggio.
                $primo = Get-ChildItem -LiteralPath $Cartella -Force -ErrorAction SilentlyContinue |
                    Where-Object { -not $_.PSIsContainer } |
                    Select-Object -First 1
                if ($null -ne $primo) { $file = $primo.FullName }
            }
            if (-not $file) {
                if ($orologio.Elapsed.TotalSeconds -gt 120) {
                    throw "Il telefono non ha consegnato il file."
                }
                Start-Sleep -Milliseconds 200
                continue
            }
        }
        $dimensione = [long]0
        try { $dimensione = [long](Get-Item -LiteralPath $file).Length } catch { $dimensione = [long]0 }
        if ($dimensione -ge $DimensioneAttesa) { return $file }
        Start-Sleep -Milliseconds 200
    }
}

# ── comandi ──────────────────────────────────────────────────────────────

function Comando-Dispositivi($Shell) {
    $voci = @()
    foreach ($dispositivo in @(Elenco-Dispositivi $Shell)) {
        $voci += @{
            seriale = (Seriale-Dispositivo $dispositivo)
            nome = (Nome-Voce $dispositivo)
            stato = "device"
            prodotto = ""
        }
    }
    Scrivi-Riga (ConvertTo-Json @{ dispositivi = @($voci) } -Compress -Depth 5)
}

function Comando-Elenca($Shell) {
    $dispositivo = Trova-Dispositivo $Shell $Seriale
    $radice = $dispositivo.GetFolder
    if ($null -eq $radice) {
        throw "Non riesco ad aprire il contenuto del telefono."
    }
    $script:Conteggio = 0
    $script:VociVisitate = 0
    Elenca-Cartella $radice "" ([bool]$SoloFoto)
    Scrivi-Riga (ConvertTo-Json @{ fine = $true; conteggio = $script:Conteggio } -Compress)
}

function Comando-Copia($Shell) {
    if (-not $Percorso) { throw "Manca il file da copiare (--percorso)." }
    if (-not $Destinazione) { throw "Manca la cartella di appoggio per la copia (--destinazione)." }
    if (-not (Test-Path -LiteralPath $Destinazione -PathType Container)) {
        throw "La cartella di appoggio della copia non esiste."
    }
    $dispositivo = Trova-Dispositivo $Shell $Seriale
    $voce = Trova-Voce $Percorso $dispositivo
    if ($null -eq $voce) { throw "Sul telefono non trovo più il file $Percorso." }
    $nomeFile = Nome-Voce $voce
    $dimensioneAttesa = Dimensione-Voce $voce
    if ($dimensioneAttesa -le 0) {
        # CopyHere è asincrono e non dice quando ha finito: senza sapere quanto deve
        # essere grande il file non c'è modo di distinguere una copia completa da una
        # fermata a metà. Meglio rinunciare con una spiegazione che consegnare una foto
        # troncata (e, con «elimina dopo la copia», far perdere l'originale).
        throw "Il telefono non mi ha detto quanto è grande $nomeFile, quindi non lo copio per non rischiare di troncarlo."
    }

    # La cartella di appoggio è creata e cancellata dal programma principale (vedi
    # trasporto_win.py): così, se questo processo viene interrotto di netto, non resta
    # una cartella con dentro mezza foto nella cartella scelta dall'utente.
    $destinazioneShell = $Shell.Namespace($Destinazione)
    if ($null -eq $destinazioneShell) { throw "Non riesco a preparare la cartella di appoggio." }
    # CopyHere è asincrono: ritorna subito, mentre la copia continua. Attendi-File aspetta
    # che il file esista e che la sua dimensione sia quella dichiarata dal telefono.
    $destinazioneShell.CopyHere($voce, $script:FlagCopia)
    $file = Attendi-File $Destinazione $nomeFile $dimensioneAttesa
    # I byte vengono consegnati sul flusso di uscita del contratto: il programma
    # principale li sta già scrivendo nel file «.part» della destinazione. Si procede
    # a blocchi (invece di una copia unica) per accorgersi subito se l'app ha annullato
    # o è stata chiusa.
    $lettura = [System.IO.File]::OpenRead($file)
    try {
        $blocco = [byte[]]::new(524288)
        $orologioInvio = [System.Diagnostics.Stopwatch]::StartNew()
        $prossimoControllo = 0.0
        while (($letti = $lettura.Read($blocco, 0, $blocco.Length)) -gt 0) {
            if ($orologioInvio.Elapsed.TotalSeconds -ge $prossimoControllo) {
                if (-not (Test-Supervisione $PidSupervisionato)) {
                    throw "Il collegamento è stato interrotto."
                }
                $prossimoControllo = $orologioInvio.Elapsed.TotalSeconds + 0.5
            }
            $script:FlussoOut.Write($blocco, 0, $letti)
        }
        $script:FlussoOut.Flush()
    } finally {
        $lettura.Dispose()
    }
}

function Comando-Cancella($Shell) {
    # Shell.Application (l'unico accesso ai dispositivi portatili che non chieda permessi
    # di amministratore) sa cancellare solo con InvokeVerb("delete"), che apre una
    # richiesta di conferma. In un processo senza persona davanti quella richiesta
    # resterebbe appesa: meglio dire chiaramente che da qui non è disponibile, invece di
    # rischiare un blocco che l'utente non saprebbe spiegarsi.
    Scrivi-Errore "La cancellazione non è disponibile con il collegamento di Windows."
    Scrivi-Errore "Il file resta sul telefono: puoi cancellarlo dalla Galleria."
    exit 2
}

# ── avvio ────────────────────────────────────────────────────────────────

try {
    $shell = Apri-Shell
    switch ($Comando) {
        "dispositivi" { Comando-Dispositivi $shell }
        "elenca" { Comando-Elenca $shell }
        "copia" { Comando-Copia $shell }
        "cancella" { Comando-Cancella $shell }
    }
} catch {
    Scrivi-Errore $_.Exception.Message
    exit 2
}
exit 0

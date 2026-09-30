# FotoFacile — Specifica di Progetto

**Data:** 2026-09-28
**Stato:** approvata per l'implementazione (l'utente ha richiesto esplicitamente "crea il piano ed eseguilo")

> **Aggiornamento del 28/09/2026 — il comportamento visibile è cambiato.** Questa specifica
> descrive il progetto originale (trasporto ADB obbligatorio, copia con le cartelle del
> telefono). Due scelte sono state poi cambiate: il collegamento al telefono **non richiede
> più il Debug USB** (viene scelto da sé fra collegamento diretto e ADB, vedi
> `fotofacile/core/trasporto.py` e `docs/PIANO-REVISIONE.md`) e la copia è **piatta** per
> impostazione predefinita (`preserve_structure=False`), con le cartelle del telefono
> ricreabili a richiesta. Le sezioni sotto sono state aggiornate dove descrivevano il
> comportamento vecchio; il §10-bis elenca anche i limiti ora risolti.

## 1. Obiettivo

Un programma desktop con interfaccia grafica che permetta a **persone non tecniche** di
copiare le foto (e i video) da un telefono Android al computer in pochi clic, senza dover
capire il file manager, senza scegliere percorsi a mano e senza messaggi tecnici.

**Problema reale:** su macOS il trasferimento MTP non è supportato nativamente; "Android File
Transfer" è instabile, Windows Explorer si blocca a metà copia, e le cartelle del telefono
sono difficili da trovare. Il gestore file fallisce o mostra cartelle vuote.

**Successo =** l'utente collega il cavo, segue 3-4 schermate in italiano semplice, e a fine
procedura trova tutte le sue foto in una cartella sul computer, con un resoconto chiaro di
cosa è stato copiato. Se qualcosa manca (Debug USB spento, componente assente), il programma
lo spiega e propone il rimedio in un pulsante.

## 2. Vincoli e decisioni

| Decisione | Scelta | Motivazione |
|---|---|---|
| Trasporto dati | **Collegamento diretto** scelto da sé (PTP/ImageCaptureCore su macOS, WPD su Windows, MTP/gio su Linux), con **ADB come scorciatoia opzionale** | Non serve attivare il Debug USB; ADB resta il più veloce (e l'unico che cancella i file dal telefono) quando è già attivo. Vedi §3 e `docs/PIANO-REVISIONE.md`. |
| Linguaggio/UI | **Python 3.9+ con Tkinter** (solo libreria standard) | Zero dipendenze da installare per l'utente finale: `python3 fotofacile.py` (o `py fotofacile.py` su Windows). Tkinter è già presente su macOS/Windows/Linux. |
| Piattaforme | **Windows 10/11, macOS 11+, Linux (Ubuntu/Fedora/Debian)** — nessuna funzione esclusiva di un sistema | Richiesta esplicita dell'utente: software multi-piattaforma. Ogni differenza di sistema è isolata in `core/osutil.py`, `core/adb.py`, `core/installer.py`, `ui/theme.py`. |
| Installazione componente mancante | **Auto-download di platform-tools ufficiali Google** in `~/.fotofacile/platform-tools`, fallback `brew` (macOS) / istruzioni manuali (Windows/Linux) | L'utente non deve mai aprire un terminale. Su Windows si estraggono anche `AdbWinApi.dll` e `AdbWinUsbApi.dll` (obbligatorie per far funzionare `adb.exe`). |
| Lingua UI | **Italiano semplice**, niente gergo (mai la parola "ADB" a schermo) | Pubblico non tecnico. |
| Privacy | Nessuna rete in uscita, nessun upload, nessuna telemetria; l'unica connessione di rete è il download di platform-tools da dl.google.com su richiesta | Fiducia: le foto non escono dal computer. |
| Modo demo | Backend finto (`FakeAdbBackend`) attivabile dall'UI e usato nei test | Consente di provare tutta la procedura, e di testare la GUI, senza un telefono collegato. |
| Sistema di test | `pytest` in venv di sviluppo; **nessuna dipendenza obbligatoria** per l'uso (su macOS il collegamento diretto aggiunge PyObjC, vedi §7) | Suite veloce e isolata. |

**Fuori ambito (YAGNI):** trasferimento via Wi-Fi/ADB wireless, sincronizzazione automatica,
upload cloud, Android come destinazione (computer → telefono), gestione contatti/chat,
conversione HEIC, app Android companion, packaging `.app`/installer `.dmg` (§11 lo elenca
come possibile estensione futura).

## 3. Architettura

```
fotofacile.py                  # avvio: python3 fotofacile.py [demo|doctor|--help]
fotofacile/
  cli.py                       # argomenti CLI, avvio GUI o diagnostica
  core/                        # logica pura, testabile, zero Tkinter
    adb.py                     # individuazione eseguibile (adb / adb.exe), esecuzione comandi, errori
    ops.py                     # comandi esterni e download eseguiti A PASSI (senza thread)
    adb_passi.py               # le operazioni adb a passi: dispositivi, ricerca, copia, cancella
    osutil.py                  # differenze di sistema: apri cartella, sensibilità maiuscole, cartelle utente
    devices.py                 # scoperta dispositivi e stati (device/unauthorized/...)
    trasporto.py               # scelta automatica del modo di collegamento (diretto / ADB / demo)
    trasporto_aiutante.py      # dialogo a righe JSON con i programmi aiutanti e copia .part
    trasporto_mac.py           # collegamento diretto macOS (ImageCaptureCore, tramite aiutante)
    trasporto_win.py           # collegamento diretto Windows (WPD, tramite PowerShell)
    trasporto_linux.py         # collegamento diretto Linux (gio/gvfs, ripiego jmtpfs)
    scanner.py                 # elenco file multimediali presenti sul telefono
    planner.py                 # costruzione piano di copia (filtri, dedup, percorsi)
    transfer.py                # esecuzione copia con avanzamento, annulla, retry, verifica
    history.py                 # archivio JSON dei file già copiati (per dispositivo)
    installer.py               # download/estrazione platform-tools
    demo.py                    # backend finto per test e modalità demo
  aiutanti/                    # processi separati per il collegamento diretto (mai importati dal main)
    ptp_mac.py                 # macOS: ImageCaptureCore (PyObjC)
    wpd_win.py, wpd_win.ps1    # Windows: WPD con Shell.Application (PowerShell)
    mtp_linux.py               # Linux: gio/gvfs (ripiego jmtpfs)
  ui/                          # solo presentazione, strato sottile
    app.py                     # finestra principale + controllo procedura guidata
    theme.py                   # font, colori, stile ttk
    widgets.py                 # componenti riusabili (indicatore passi, log, scelta cartella)
    page_connect.py            # Passo 1: collega il telefono
    page_select.py             # Passo 2: scegli cosa copiare
    page_options.py            # Passo 3: destinazione e opzioni
    page_transfer.py           # Passo 4: copia in corso / resoconto finale
tests/                         # test unitari della logica + smoke test GUI
```

**Principi:**
- `core/` non importa mai `tkinter`: tutta la logica è testabile in isolamento.
- I generatori a passi sono la sola forma di "asincronia" ammessa nel progetto.
- `ui/` non contiene logica di business: legge lo stato e chiama `core/`.
- **Multi-piattaforma:** nessun percorso "cablato" per un solo sistema operativo; le differenze
  sono confinate in `core/osutil.py` (cartelle utente, apertura del file manager, sensibilità
  maiuscole del file system), `core/adb.py` (nome dell'eseguibile, percorsi noti),
  `core/installer.py` (URL per piattaforma, estrazione delle librerie Windows) e
  `ui/theme.py` (tema ttk e font disponibili). Il codice di logica e UI resta identico.
- **Niente thread.** Le operazioni lunghe (ricerca sul telefono, copia, download del
  componente) sono **generatori a piccoli passi** portati avanti da `after()` dentro il ciclo
  della grafica: l'interfaccia resta reattiva senza dipendere dalla sicurezza dei thread di Tk.
  Motivo concreto: su macOS con Tk 9 creare un thread mentre la finestra è aperta **blocca
  l'intero programma** (verificato: anche un thread che non tocca Tk). Il costo è un motore
  cooperativo (`core/ops.py`, `core/adb_passi.py`) al posto di `threading`; il beneficio è un
  programma che non può bloccarsi e test deterministici. L'output lungo dei comandi esterni
  viene scritto su file temporanei, così i processi non si bloccano mai sul tubo di
  comunicazione.
- Interfaccia unica verso il telefono: la grafica parla solo tramite il protocollo `Trasporto`
  (`core/trasporto.py`), implementato da `TrasportoAdb` (Debug USB), `TrasportoAiutante` +
  aiutanti di sistema (collegamento diretto) e `TrasportoDemo` (telefono finto): nessun test
  tocca un dispositivo reale.

## 4. Flusso utente (procedura guidata)

**Passo 1 — Collega il telefono.** Istruzioni grandi e chiare ("Collega il telefono al
computer con il cavo e tieni lo schermo sbloccato. Non devi attivare nessuna impostazione").
Il programma sceglie da sé il collegamento migliore disponibile (diretto; ADB solo se già
attivo) e rileva **live** ogni 2 secondi con messaggi umani per ogni stato:
- nessun telefono → "Non vedo ancora nessun telefono…"
- `unauthorized` (solo con ADB) → "Telefono trovato! Sbloccalo e tocca **Consenti** sullo schermo"
- `device` → "Perfetto! Telefono collegato: <modello>"
- `offline`/errore → pulsante "Riprova il collegamento".
Pulsanti: **Il telefono non viene riconosciuto?** (prima i rimedi semplici — cavo, porta USB,
schermo sbloccato — e solo alla fine le istruzioni per il «Debug USB» per marca, come ultima
possibilità), **Installa componente mancante** (solo se sul computer non esiste nessun
collegamento diretto, con download ed esito), **Riprova il collegamento**, e link discreto
**Prova senza telefono (demo)**.

**Passo 2 — Scegli cosa copiare.** Scansione automatica delle cartelle multimediali note
(DCIM/Camera, DCIM/Screenshots, Pictures e sottocartelle, Download, WhatsApp/Telegram media
se presenti). Albero con caselle di spunta, conteggio file e peso per cartella; riepilogo
totale in basso; filtro "solo foto a partire dal …" (opzionale); casella **Includi video**.
Scansione in background con barra di avanzamento e pulsante Annulla.

**Passo 3 — Dove e come.** Cartella di destinazione con scelta guidata (predefinita:
`~/Pictures/FotoFacile/<Modello>/<AAAA-MM-GG>`), casella **Ricrea anche le cartelle del
telefono (di solito non serve)** (predefinita: no: i file finiscono direttamente nella
cartella scelta), **Salta i file già copiati** (predefinita: sì), **Cancella le
foto dal telefono dopo la copia** (predefinita: no, con avviso rosso esplicito), controllo
dello spazio libero su disco ("Servono 3,4 GB, disponibili 120 GB" oppure avviso bloccante).

**Passo 4 — Copia.** Barra di avanzamento generale + file corrente + barra file, velocità
(MB/s), tempo rimanente, contatori (copiati / saltati / errori), pulsante **Interrompi**.
Log dettagliato richiudibile. Al termine: resoconto chiaro, **Apri la cartella delle foto**,
**Salva resoconto** (file di testo), **Chiudi**. Non si perde nulla: nessun file parziale
resta nella cartella (scrittura su `.part` e rinomina solo a copia verificata).

## 5. Modello dati

```python
@dataclass(frozen=True)
class DeviceInfo:      serial: str; state: str; model: str; product: str
@dataclass(frozen=True)
class MediaFile:       remote_path: str; size: int; mtime: int; kind: str  # "photo"|"video"
@dataclass(frozen=True)
class MediaFolder:     remote_path: str; label: str; file_count: int; total_size: int
@dataclass(frozen=True)
class TransferOptions: destination: Path; preserve_structure: bool = False; skip_existing: bool
                       delete_after: bool; include_videos: bool = True
                       date_from: int | None = None      # epoch: copia solo file più recenti
                       overwrite_renames: bool = True    # collisione → "nome (1).jpg"
@dataclass
class TransferResults: copied: list[Path]; skipped: int; failed: list[tuple[MediaFile, str]]
                       bytes_copied: int; elapsed: float; cancelled: bool
```

**Archivio deduplica** `~/.fotofacile/history.json`:
`{"version": 1, "devices": {"<serial>": {"<percorso relativo>": {"size": int, "mtime": int, "dest": str}}}}`
Scrittura atomica (file temporaneo + `os.replace`); file corrotto → copiato in
`history.json.corrupt-<timestamp>` e ricreato vuoto (mai perdere l'originale).

## 6. Comportamenti critici (contratto)

1. **Errori tradotti:** ogni errore di `core` è un'eccezione `FotoFacileError` con
   `message` (frase umana in italiano) e `hint` (cosa fare). La UI mostra sempre messaggio +
   suggerimento, mai uno stack trace.
2. **File parziali:** si scrive su `<nome>.part`; rinomina atomica a fine copia verificata;
   su annullamento o errore il `.part` viene rimosso. Mai un file troncato con nome definitivo.
3. **Verifica:** i byte scritti devono corrispondere alla dimensione nota del file remoto;
   se la dimensione non è nota, si verifica la corretta chiusura dello stream.
4. **Collisioni:** se il file esiste già nella destinazione: dimensione uguale → considerato
   già presente e saltato; dimensione diversa → si crea `nome (1).jpg`, `nome (2).jpg`.
5. **Deduplica:** se `skip_existing` è attivo, un file il cui percorso relativo e la cui
   coppia (dimensione, mtime) coincidono con la cronologia viene saltato senza toccare la rete.
6. **Cancellazione:** `rm` sul telefono solo per i file copiati e verificati con successo, e
   solo se l'utente ha attivato l'opzione. Un fallimento di `rm` non compromette la copia:
   viene annotato nel resoconto.
7. **Annullamento:** interrompe entro un file (al massimo un blocco da 64 KB), ripulisce il
   `.part`, restituisce `cancelled=True` e un resoconto parziale valido.
8. **Spazio disco:** se lo spazio libero è inferiore al totale da copiare, il Passo 3 blocca
   l'avanzamento e spiega l'errore.
9. **Nomi difficili:** percorsi con apostrofi, spazi, parentesi, `#`, `&`, caratteri non
   latini vengono quotati correttamente; righe di output non interpretabili vengono saltate e
   registrate nel log, mai fatte esplodere.
10. **Nomi validi su ogni sistema (Windows incluso):** i caratteri proibiti da Windows
    (`\ / : * ? " < > |`, caratteri di controllo) diventano `_`; i nomi riservati
    (`CON`, `PRN`, `AUX`, `NUL`, `COM1`…`COM9`, `LPT1`…`LPT9`) vengono prefissati con `_`;
     i punti e gli spazi finali vengono rimossi; i nomi troppo lunghi (> 150 caratteri) e i
     percorsi oltre 240 caratteri vengono accorciati mantenendo l'estensione. Così la stessa
      cartella creata su macOS funziona anche su Windows.
11. **Collisioni con maiuscole diverse:** su Windows e macOS (file system non sensibile alle
     maiuscole) `Foto.jpg` e `foto.jpg` sono considerati lo stesso file per i controlli di
     presenza e di collisione; su Linux resta il confronto esatto.
12. **Nessun blocco dell'interfaccia:** ogni comando ADB ha timeout (scansione 120 s, copia
    per singolo file 15 min) e può essere annullato.
13. **Retry:** un errore transitorio di lettura durante la copia viene ritentato fino a 2 volte
    prima di marcare il file come errore.
14. **Autodiagnosi:** `python3 fotofacile.py doctor` (su Windows `py fotofacile.py doctor`)
    stampa stato di: sistema operativo, versione Python/Tkinter, adb trovato (con percorso e
    versione), dispositivi collegati, cartella di lavoro, accesso in scrittura alla
    destinazione — utile al supporto su tutti i sistemi.
15. **Apertura cartella:** al termine, il pulsante «Apri la cartella delle foto» usa il file
    manager del sistema (Finder su macOS, Esplora file su Windows, xdg-open su Linux) e, se
    fallisce, mostra il percorso da copiare a mano invece di dare un errore tecnico.

## 7. Dipendenze e compatibilità

- Runtime: **Python 3.9+** con Tkinter. Tutta la logica e la grafica usano la sola libreria
  standard (`subprocess`, `zipfile`, `urllib`, `json`, `shutil`, `pathlib`, `dataclasses`…).
  L'unica eccezione è il collegamento diretto su macOS, che usa
  `pyobjc-framework-ImageCaptureCore` (`requirements.txt`): è **opzionale** e se manca il
  programma ripiega su ADB.
- Esterno (opzionale): eseguibile `adb` (`adb.exe` su Windows), scaricato automaticamente
dall'app solo se non esiste nessun collegamento diretto (oppure già presente nel sistema).
Serve al collegamento rapido con Debug USB e alla cancellazione dei file dal telefono.
- Sviluppo: `pytest` in `.venv`.

| Aspetto | Windows | macOS | Linux |
|---|---|---|---|
| Avvio | `py fotofacile.py` | `python3 fotofacile.py` | `python3 fotofacile.py` |
| Collegamento diretto (senza Debug USB) | WPD via PowerShell (di sistema) | PTP via ImageCaptureCore (PyObjC, `requirements.txt`) | MTP via `gio`/gvfs (ripiego `jmtpfs`) |
| Eseguibile componente (scorciatoia opzionale, Debug USB) | `adb.exe` (+ `AdbWinApi.dll`, `AdbWinUsbApi.dll`) | `adb` | `adb` |
| URL platform-tools | `…-windows.zip` | `…-darwin.zip` | `…-linux.zip` |
| Percorsi cercati | `%LOCALAPPDATA%\Android\Sdk\platform-tools`, `%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools`, PATH | `~/.fotofacile/platform-tools`, `/opt/homebrew/bin`, `/usr/local/bin`, `~/Library/Android/sdk/platform-tools`, PATH | `~/.fotofacile/platform-tools`, `/usr/bin`, `/usr/local/bin`, PATH |
| Cartella dati app | `%USERPROFILE%\.fotofacile` | `~/.fotofacile` | `~/.fotofacile` |
| Apri cartella | `explorer` / `os.startfile` | `open` | `xdg-open` |
| Tema GUI | `vista` | `aqua` | `clam` |
| Font | Segoe UI | Helvetica Neue | DejaVu Sans / Liberation Sans |
| Esecuzione file | rimozione dei bit eseguibili non necessaria, `chmod` saltato | `chmod 755` | `chmod 755` |

## 8. Test

TDD su tutto `core/` (test scritto prima, visto fallire, poi implementazione):

| Area | Casi coperti |
|---|---|
| `adb.py` | quotazione comandi difficili, ordine di ricerca dell'eseguibile, errori con messaggi umani, timeout |
| `devices.py` | `adb devices -l` vuoto/uno/molti/unauthorized/offline, modello assente, righe spurie |
| `trasporto*.py` / `aiutanti/` | scelta automatica del collegamento, contratto degli aiutanti (righe JSON, `dispositivi`/`elenca`/`copia`/`cancella`), copie `.part` e annullamento, cartella di appoggio di Windows, parsing degli elenchi, montaggi Linux isolati |
| `scanner.py` | parsing flusso size/mtime/nome, filtro estensioni, file con `|` nel nome, righe corrotte, cartelle inesistenti |
| `osutil.py` | comando di apertura cartella per sistema, sensibilità maiuscole simulata, percorsi utente, fallback quando il file manager non è disponibile |
| `ops.py` | comando esterno a passi (avvio, attesa, termine, output su file, errori umani), download a blocchi, annullamento |
| `adb_passi.py` | dispositivi, ricerca file, copia con `.part`, cancellazione e riavvio del collegamento, tutto a passi; versione demo equivalente |
| `planner.py` | totali e conteggi, filtro per data, dedup da cronologia, mappatura percorsi con/senza struttura, collisioni e rinomina, nomi non validi su Windows, nomi riservati, nomi lunghi, confronto maiuscole su Windows/macOS |
| `history.py` | caricamento mancante, salvataggio atomico, round-trip, file corrotto → backup, isolamento per seriale |
| `transfer.py` | copia corretta, progressi monotoni, annulla a metà senza residui, retry, dimensione errata → errore, cancella-dopo-solo-se-verificato, `.part` pulito |
| `installer.py` | download finto → estrazione → adb eseguibile, zip corrotto → errore umano, annulla download |
| `ops.py` / `adb_passi.py` | avvio/attesa/termine di processi reali (script finti), output grande su file, scadenza del tempo, annullamento a metà copia, nessun file temporaneo residuo |
| `ui` | navigazione fra i passi, avanzamento dei task a passi, messaggi di errore umani, pagine 1-4 con telefono demo |
| `test_app_completa.py` | la vera applicazione in un processo separato: avvio, quattro passi, copia reale su disco, resoconto (salta da sé se il computer non ha sessione grafica) |

## 9. Criteri di accettazione

1. `python3 fotofacile.py` apre la finestra al Passo 1 senza errori e senza dipendenze esterne.
2. Con dispositivo collegato e autorizzato, in ≤ 4 clic l'utente avvia la copia e vede
   avanzamento, velocità e tempo rimanente.
3. Ad ogni stato anomalo (nessun telefono, non autorizzato, componente assente, spazio
   insufficiente, errore di copia) corrisponde un messaggio in italiano con una azione
   proposta; nessuno stack trace visibile.
4. Al termine esistono sul computer tanti file quanti indicati nel resoconto, tutti integri
   (dimensione verificata), e un secondo avvio non ricopia ciò che è già stato copiato.
5. La modalità demo permette di provare l'intera procedura su una macchina senza telefono.
6. **Niente thread e niente blocchi:** durante la copia la finestra continua a rispondere
   (i test verificano che non venga creato nessun thread e che la navigazione resti possibile).
7. **Multi-piattaforma:** a parità di versione Python, il programma funziona su Windows,
   macOS e Linux; nessun modulo fuori da `core/osutil.py`, `core/adb.py`, `core/installer.py`
   e `ui/theme.py` contiene riferimenti a un sistema operativo specifico.
8. `python3 -m pytest tests -q` passa completamente (i test che richiedono una finestra si
   saltano da soli sui computer senza sessione grafica, senza bloccare la suite).
9. `tests/pilota_app.py` guida la vera applicazione in modalità demo fino al resoconto finale:
   è il collaudo che l'utente può eseguire sul proprio computer.

## 10. Rischi e mitigazioni

| Rischio | Mitigazione |
|---|---|
| L'utente non trova il "Debug USB" | Non è più necessario: il collegamento è scelto da sé e le istruzioni per il Debug USB compaiono solo come ultima possibilità nel dialogo «Il telefono non viene riconosciuto?» |
| Cavo solo-ricarica | Messaggio dedicato: "Prova un altro cavo USB (alcuni cavi ricaricano soltanto)" |
| Autorizzazione non data | Stato `unauthorized` spiegato con le parole dello schermo del telefono |
| Dispositivo in stato `offline` | Pulsante "Riavvia collegamento" (`adb kill-server`/`start-server`) |
| Download platform-tools bloccato | Fallback: istruzioni manuali + `brew install android-platform-tools` |
| Telefono con migliaia di file | Scansione in un solo comando shell sul dispositivo, streaming, annullabile |
| Nomi file insoliti | Quotazione sistematica e righe non valide ignorate e registrate |

## 10-bis. Correzioni nate dalla revisione indipendente (tutte con test)

| Difetto trovato | Correzione |
|---|---|
| Un errore di disco durante la copia reale (`OSError`) non veniva tradotto: `.part` residuo e intero lotto interrotto | `AdbAPassi.copia` traduce gli errori (`cores/errors.traduci_errore_file`), ha un `finally` che termina il processo e rimuove il `.part` anche quando il lavoro viene abbandonato |
| Chiusura della finestra a metà copia: processo `adb` vivo e `.part` sul disco | `App._chiusura` chiede conferma, chiama `annulla_task()` (chiude il generatore, che ripulisce) e rimuove la cartella di lavoro |
| Errore di salvataggio della cronologia dopo una copia riuscita: nessun resoconto, pagina bloccata | il salvataggio della cronologia non è più fatale: viene aggiunto un avviso in `TransferResults.warnings`, mostrato nel resoconto |
| `OSError` dentro callback della grafica (cartella non leggibile, file sparito): nessun messaggio e pagina in stallo | `build_plan` e l'aggiornamento dello spazio sono protetti e mostrano un errore umano; `run_task` protegge anche i callback finali |
| La ricerca non ripiegava su tutta la memoria (`/sdcard`): foto non trovate senza spiegazione | `AdbAPassi.cerca_media` esegue il secondo tentativo con `maxdepth`, come `scanner.list_media` |
| Stato `no permissions` (Linux/udev) non riconosciuto | `parse_devices` interpreta la riga reale di adb |
| `FOTO.JPG` e `foto.jpg` scambiati per lo stesso file (perdita silenziosa su dischi sensibili alle maiuscole) | «già presente» vale solo a parità esatta di nome; i nomi con maiuscole diverse diventano una copia con `(1)` |
| Ritentativi inutili su errori non temporanei (disco pieno, permessi) | solo gli errori `ritentabile=True` (comunicazione col telefono) vengono ritentati |
| File temporanei degli errori non cancellati quando il comando non parte | `ProcessoEsterno` ripulisce sempre, anche in caso di avvio fallito |
| `xdg-open` bloccava la finestra; `explorer` dava un falso errore su Windows | apertura con processo leggero su macOS/Linux, `os.startfile` e nessun controllo del codice di uscita su Windows |
| «Salva resoconto» falliva in silenzio | protetto con messaggio e suggerimento |
| Chiusura senza conferma durante la copia e testo di «Interrompi» non veritiero | conferma esplicita e testo corretto ("mi fermo subito") |
| Destinazione relativa scritta a mano, metodo morto `salva_note`, cartella di lavoro mai rimossa | destinazione assoluta obbligatoria, codice morto rimosso, cartella di lavoro rimossa alla chiusura |
| Componente presente ma guasto: pulsante di installazione disabilitato per sempre | se il controllo fallisce per colpa del componente, il pulsante di installazione torna attivo |
| Estrazione del componente non atomica (interruzione a metà → reinstallazione) | si scarica su file provvisorio, si verifica l'impronta ufficiale e si estrae in una cartella di appoggio; si controlla che `adb` parta e solo allora si sostituisce l'installazione (quella vecchia resta fino all'ultimo istante) |
| «Disco pieno» non riconosciuto nel percorso reale | `errors.traduci_errore_file` riconosce lo spazio esaurito e mostra il messaggio dedicato, senza ritentativi inutili |
| Barra di avanzamento del singolo file non distinta da quella generale | due barre distinte: il totale e il file in corso |
| Download del componente non verificato | impronta ufficiale di Google dal catalogo `repository2-3.xml` (SHA-256/SHA-1) + controllo della struttura dello zip; il pacchetto scaricato viene sempre rimosso alla fine |

**Limiti noti e dichiarati (dopo la revisione):** i collegamenti diretti di Windows e Linux
non sono mai stati provati su hardware reale (non c'era una macchina Windows né un desktop
Linux con `gio`/gvfs); su macOS il collegamento diretto è stato verificato solo fino a «nessun
telefono collegato» (`dispositivi` restituisce `{"dispositivi": []}` e `elenca` risponde
«Non vedo nessun telefono collegato.») e un telefono Android vero non è mai stato collegato. Con il collegamento
diretto di Windows la cancellazione dal telefono non è disponibile (si fa dalla Galleria,
oppure con il Debug USB). Gli altri limiti della prima versione sono stati corretti (vedi
tabella qui sopra); il dettaglio onesto è in `HANDOFF.md` → «Not Yet Done».

## 11. Estensioni future (non in questa versione)

Collegamento Wi‑Fi (`adb connect`), profilatura automatica "solo elementi nuovi dall'ultima
volta", impacchettamento `.app`/`.exe`/`.AppImage` con PyInstaller, supporto iPhone, anteprima
miniature, integrazione con il file manager di sistema.

## 12. Punti di attenzione per la revisione (imbocco "Review Focus")

1. Nomi file con `|`, apostrofi, spazi, caratteri non ASCII o emoji → devono copiarsi
   correttamente (quotazione shell), mai essere saltati silenziosamente.
2. Annullamento a metà di un video grande → nessun `.part` residuo, nessun file troncato.
3. Destinazione su disco pieno a metà copia → errore chiaro, nessun file corrotto.
4. Perdita di connessione USB a metà copia → retry, poi errore nel resoconto senza bloccare il ciclo.
5. Due telefoni collegati contemporaneamente → l'utente sceglie il dispositivo, il seriale
   corretto viene usato in ogni comando.
6. Cronologia corrotta o cancellata a mano → nessun crash, ricostruzione pulita.
7. Stessa foto con nomi non validi su Windows (`IMG:01?.jpg`) o nomi riservati (`CON.jpg`)
   → copiata con nome reso sicuro, e la cartella risultante è utilizzabile sia su macOS sia
   su Windows.
8. Su Windows con «Debug USB» attivo ma driver USB del produttore mancante → messaggio che
   indica di installare il driver, invece di restare in attesa indefinita.

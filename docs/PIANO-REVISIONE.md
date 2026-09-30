# Piano di revisione e sviluppo — FotoFacile

**Stato: implementato.** Le tre fasi sono state completate e la suite passa con **373 test**
(erano 293 prima della revisione). Avvertenza onesta: i collegamenti diretti di **Windows e
Linux non sono mai stati provati su hardware reale**; su macOS il collegamento diretto è stato
verificato solo fino a «nessun telefono collegato» (l'aiutante parte, `dispositivi` restituisce
un elenco vuoto, `elenca` risponde «Non vedo nessun telefono collegato.») e **nessun telefono
Android vero è mai stato collegato**. Vedi `HANDOFF.md` → «Not Yet Done».

Obiettivi richiesti:

1. **Revisione completa del codice** e correzione di tutti gli errori/bug.
2. **Copia solo foto e video**, senza ricreare l'albero delle cartelle del telefono.
3. **Nessun Debug USB obbligatorio**: qualsiasi telefono deve funzionare anche senza debug.

---

## Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**

| # | Gravità | Difetto | File |
|---|---|---|---|
| B1 | critica | `esito()` rilegge in memoria l'intero file appena copiato (OOM su video grandi) | `core/ops.py`, `core/adb_passi.py` |
| B2 | critica | `_limita_percorso` riscrive la radice di destinazione (`/Users/x/Pictures/...` → `/x/Pictures/...`) | `core/planner.py` |
| B3 | alta | `tk.Text` senza `foreground`: testo nero su pannello scuro (illeggibile in modalità scura) | `ui/widgets.py`, `ui/page_connect.py` |
| B4 | alta | `AdbDemoAPassi.pulisci()` → `AttributeError` (`self.cartella_lavoro` inesistente) | `core/adb_passi.py` |
| B5 | alta | catena di `after()` duplicata: il sondaggio del passo 1 si moltiplica | `ui/page_connect.py` |
| B6 | media | `stdout=PIPE` mai letto: possibile blocco del processo esterno | `core/ops.py` |
| B7 | media | `GeneratorExit` salta la pulizia dei file temporanei (`.part`, `.scarico`) | `core/ops.py`, `core/adb_passi.py` |
| B8 | media | la ricerca di ripiego ignora la scelta «includi video» | `core/adb_passi.py` |
| B9 | media | `History.contains` solleva `AttributeError` su cronologia malformata | `core/history.py` |
| B10 | media | i `.bat` generati su Windows hanno il BOM UTF-8 → `'ï»¿@echo' non riconosciuto` | `installer/windows/InstallaFotoFacile.ps1` |
| B11 | media | `Trova-Python`: `$candidato[1..0]` inietta un argomento di troppo | `installer/windows/InstallaFotoFacile.ps1` |
| B12 | media | `crea_pacchetto_windows.py` cancella la destinazione senza controlli | `scripts/crea_pacchetto_windows.py` |
| B13 | bassa | `ricostruisci_pagine()` lascia `current_page = ""` → `ValueError` su «Indietro» | `ui/app.py` |
| B14 | bassa | icone con dimensioni sbagliate (`@2x` identiche a `@1x`, 256 px chiamata 128) | `scripts/make_icon.py` |
| B15 | bassa | `platform-tools.zip` (~10 MB) mai cancellato + estrazione non atomica | `core/installer.py` |
| B16 | bassa | `prova_finestra` non funziona nel pacchetto (PyInstaller ignora `-c`) | `cli.py` |
| B17 | bassa | `.part` condiviso fra due istanze; nessun controllo di nome già esistente | `core/adb_passi.py` |
| B18 | bassa | barra di avanzamento del singolo file identica a quella generale | `ui/page_transfer.py` |
| B19 | bassa | nessun blocco rientrante su «Cerca di nuovo» / casella video | `ui/page_select.py` |
| B20 | bassa | la copia parte anche senza telefono (`serial = ""`) | `ui/page_select.py`, `ui/page_transfer.py` |
| B21 | bassa | `report.save_report` crea `~/Desktop` anche dove non esiste | `core/report.py` |
| B22 | bassa | la finestra di aiuto si ricrea a ogni clic e non è temata | `ui/page_connect.py` |
| B23 | bassa | `after(700, ...)` su finestra già distrutta → `TclError` | `ui/app.py` |
| B24 | bassa | «disco pieno» non segnalato nel percorso reale; nessuna verifica hash del download | `core/errors.py`, `core/installer.py` |

## Fase 2 — Copia «piatta» (solo foto e video) — **completata**

- `preserve_structure` predefinito a `False`: i file finiscono direttamente nella cartella scelta.
- Nomi uguali da cartelle diverse risolti con `nome (1).jpg`, `nome (2).jpg`.
- Interfaccia: testo e casella aggiornati, senza gergo.

## Fase 3 — Trasporti senza Debug USB — **completata**

Nuovo livello `fotofacile/core/trasporto*.py` che sceglie da solo il modo migliore di parlare
con il telefono, **senza** richiedere il Debug USB:

| Sistema | Trasporto | Dipendenze |
|---|---|---|
| macOS | PTP/MTP nativo via ImageCaptureCore (processo aiutante PyObjC) | `pyobjc-framework-ImageCaptureCore` |
| Windows | WPD via `Shell.Application` (script PowerShell) | nessuna (PowerShell è di sistema) |
| Linux | MTP via `gio`/gvfs, ripiego `jmtpfs`, poi `libmtp` | gvfs (presente sui desktop) |
| tutti | ADB (solo se il Debug USB è attivo) come scorciatoia veloce | platform-tools |

Ogni trasporto parla con l'interfaccia comune `Trasporto` e viene pilotato **a passi**,
senza thread, come il resto del programma.

---

## Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi)

Una revisione indipendente del lavoro delle fasi 1–3 ha trovato altri difetti, tutti corretti.

| # | Gravità | Difetto | File |
|---|---|---|---|
| C1 | **critica** | `comando_aiutante()` calcolava il percorso di avvio con una cartella di troppo (`fotofacile/fotofacile.py`, inesistente): **tutto** il collegamento diretto era morto quando si usa il programma dal sorgente. Ora il percorso si ricava da un unico punto (`osutil.comando_se_stesso`) e c'è `fotofacile/__main__.py` come ripiego. | `core/osutil.py`, `core/trasporto_aiutante.py`, `cli.py` |
| C2 | **critica** | `_controllo_fallito` confrontava oggetti ricostruiti a ogni tentativo, quindi il confronto era sempre vero: un errore faceva ripartire lo stesso collegamento all'infinito e l'utente non vedeva mai il messaggio. Ora si tiene traccia dei collegamenti già provati. | `ui/page_connect.py`, `ui/app.py` |
| C3 | alta | `_scansione_in_corso` non veniva azzerato quando il lavoro era abbandonato altrove: la schermata restava bloccata su «Sto cercando…» per sempre. | `ui/page_select.py` |
| C4 | alta | `prova_finestra()` falliva sempre dal sorgente (passava `--prova-finestra` all'interprete nudo). | `cli.py` |
| C5 | media | Un file la cui dimensione non era leggibile veniva copiato come file **vuoto** e contato come riuscito: con «cancella dopo la copia» l'originale sarebbe stato cancellato. Ora l'aiutante si ferma e lo dice. | `aiutanti/ptp_mac.py` |
| C6 | media | `ProcessoEsterno.avvia()` lasciava aperti il file degli errori e il descrittore se il file di destinazione non si poteva aprire. | `core/ops.py` |
| C7 | media | Generatore chiuso ⇒ processo esterno **non** interrotto in `aspetta()`, `dispositivi()`, `riavvia()`. | `core/ops.py`, `core/adb_passi.py` |
| C8 | media | L'elenco dei processi dell'aiutante cresceva di un elemento per ogni file copiato. | `core/trasporto_aiutante.py` |
| C9 | media | La lettura del catalogo Google poteva bloccare la finestra per 30 secondi senza avviso. | `core/installer.py` |
| C10 | media | Il testo d'errore dell'aiutante (spesso la spiegazione più precisa) veniva scartato in favore del consiglio generico. | `core/ops.py` |
| C11 | media | Estrazione atomica: un'interruzione lasciava il componente assente e il ripiego veniva cancellato al tentativo successivo. | `core/installer.py` |
| C12 | media | Con meno di 16 MB liberi il programma rifiutava **qualsiasi** copia, anche una foto da 200 KB. | `core/adb_passi.py` |
| C13 | bassa | Off-by-one nell'accorciamento dei percorsi quando restano cartelle. | `core/planner.py` |
| C14 | bassa | Gli script `.ps1` erano senza BOM: PowerShell 5.1 li legge in ANSI e gli accenti diventano illeggibili. | `fotofacile/aiutanti/wpd_win.ps1`, `installer/windows/*.ps1` |
| C15 | bassa | L'impronta con lunghezza diversa da 40 caratteri veniva verificata con l'algoritmo sbagliato. | `core/installer.py` |
| C16 | bassa | Un errore di pianificazione poteva uscire da un pulsante come traccia invece che come messaggio. | `ui/page_options.py` |
| C17 | bassa | Avvisi mostrati e poi cancellati subito dal cambio di schermata. | `ui/page_select.py`, `ui/page_transfer.py` |
| C18 | bassa | `os.replace` non tradotto in messaggio umano nel collegamento diretto. | `core/trasporto_aiutante.py` |
| C19 | bassa | Codice morto introdotto dalle fasi precedenti. | vari |

### Verifica

- **383 test verdi** (erano 293 all'inizio di questa revisione).
- `doctor` mostra ora i modi di collegamento disponibili.
- Collaudo end-to-end dell'app vera: 54 file copiati, 0 errori, nessun `.part`, **nessuna
  sottocartella** creata (copia piatta confermata).
- Verifica a schermo della modalità scura: area «Dettagli» e finestra di aiuto ora leggibili.
- L'aiutante macOS è stato avviato davvero, dal percorso reale usato dall'app, da una cartella
  diversa da quella del progetto: risponde `{"dispositivi": []}` con codice 0.

### Non verificato (dichiarato)

- Nessun telefono Android è mai stato collegato: il collegamento diretto è verificato solo
  fino a «nessun telefono presente».
- Windows e Linux non sono stati provati su hardware vero.

---

## Terza revisione (D1–D31)

Piano `docs/superpowers/plans/2026-09-30-fotofacile-v0.2.md` (Parte A): D1–D10 trovati leggendo
il codice prima del piano, D11–D31 dall'audit per gruppi G1–G8 (Task A7), con le risposte scritte
a ogni domanda in `docs/REVISIONE-v0.2.md`. Ogni difetto corretto ha un test in
`tests/test_regressioni.py` (rosso prima della correzione) e un commit `fix(Dn): …`. **D7 e D10
non sono ancora corretti**: sono pianificati nei Task D2 e nella Parte C.

| # | Gravità | Dove | Cosa succedeva | Stato |
|---|---|---|---|---|
| D1 | **alta** | `core/transfer.py` | Le foto copiate prendevano la data di oggi, non quella di scatto. | corretto |
| D2 | media | `core/transfer.py` | Chiudendo la finestra durante la copia la cronologia dei file già copiati non si salvava. | corretto |
| D3 | media | `core/transfer.py` | Una cancellazione dal telefono fallita veniva taciuta. | corretto |
| D4 | bassa | `core/transfer.py` | Con un file fallito la barra non arrivava al 100 % e il tempo restante era sbagliato. | corretto |
| D5 | media | `ui/page_select.py` | La ricerca fallita diceva solo «Ricerca non riuscita.», senza motivo. | corretto |
| D6 | bassa | `core/history.py` | Due copie del programma aperte si cancellavano a vicenda la cronologia. | corretto |
| D7 | media | `cli.py` (Windows) | Dal `.exe` `--windowed` `doctor` e `--selftest` non mostrano niente. | pianificato (Task D2) |
| D8 | media | grafica su Windows | Senza dichiarazione DPI il testo era sfocato sugli schermi ingranditi. | corretto |
| D9 | **alta** | `ui/page_connect.py` | Non si diceva di scegliere «Trasferimento file»: il collegamento diretto non vedeva il telefono. | corretto |
| D10 | UX | `ui/*` | Testi piccoli, date da scrivere a mano, percorsi tecnici, dettagli sempre visibili. | pianificato (Parte C) |
| D11 | media | `core/trasporto_aiutante.py`, `core/adb_passi.py` | Una cartella di destinazione impossibile da creare fermava tutta la copia con un errore grezzo. | corretto |
| D12 | bassa | `core/adb_passi.py` | Un file con «spazio» nel nome faceva credere a un disco pieno. | corretto |
| D13 | bassa | `core/ops.py` | Con il disco di sistema pieno l'avvio di un comando dava un `OSError` grezzo e lasciava file in `/tmp`. | corretto |
| D14 | **alta** | `core/trasporto_linux.py` | Su Linux la copia diretta falliva sempre (`TypeError`): nessuna foto copiata. | corretto |
| D15 | media | `aiutanti/ptp_mac.py` | Su macOS, con due telefoni, copia e cancellazione potevano agire su quello sbagliato. | corretto |
| D16 | media | `core/trasporto_aiutante.py`, `core/ops.py` (Windows) | Le foto con accenti o emoji nel nome non venivano copiate. | corretto |
| D17 | **alta** | `aiutanti/wpd_win.ps1` (Windows) | Con le estensioni nascoste nessuna foto veniva elencata (correzione non verificata su Windows vero). | corretto |
| D18 | **alta** | `aiutanti/ptp_mac.py` | Su macOS sparivano in silenzio le foto delle cartelle visitate dopo la prima. | corretto |
| D19 | bassa | `aiutanti/__init__.py` | L'aiutante interrotto lasciava foto in `/tmp` (macOS) o comandi orfani (Linux). | corretto |
| D20 | bassa | `aiutanti/ptp_mac.py` | Gli errori dell'aiutante macOS comparivano con «OSError:» davanti. | corretto |
| D21 | bassa | `core/transfer.py` | La copia interna non traduceva la cartella impossibile da creare. | corretto |
| D22 | media | `core/ops.py`, `core/installer.py` | Una risposta di rete troncata o non HTTP bloccava il download del componente («Qualcosa non ha funzionato»). | corretto |
| D23 | media | `core/ops.py`, `core/installer.py` | Disco pieno o cartella dati impossibile durante l'installazione del componente: errore grezzo o «controlla la connessione». | corretto |
| D24 | bassa | `core/ops.py` | Con la rete lenta ogni passo del download bloccava la finestra per secondi. | corretto |
| D25 | bassa | `core/format.py` | «1 minuto e 1 secondi», «1 ora e 1 minuti». | corretto |
| D26 | bassa | `core/scanner.py` | Un nome con U+2028/U+0085 faceva cercare un file diverso. | corretto |
| D27 | bassa | `cli.py` | Il registro `avvio.log` cresceva per sempre. | corretto |
| D28 | media | `cli.py` | Se `avvio.log` non si poteva scrivere il programma non si apriva affatto. | corretto |
| D29 | media | `ui/app.py` | `go_to` cancellava gli avvisi scritti entrando in una pagina e, dopo un rimando, si credeva nella pagina sbagliata. | corretto |
| D30 | bassa | `ui/app.py` | Chiudendo al passo 1 chiedeva di interrompere una copia inesistente. | corretto |
| D31 | media | `cli.py` (Windows) | Con l'uscita in un file (cp1252) `doctor`, `--selftest` e l'avviso di avvio si fermavano su `UnicodeEncodeError`. | corretto |

Rimandati (dettagli in `docs/REVISIONE-v0.2.md`): alla **Parte C** i difetti trovati dentro le
pagine che verranno riscritte (conferma della cancellazione aggirata da un doppio clic, C8; avvisi
della ricerca mostrati nel passo sbagliato, C6/C7; vicolo cieco dopo un errore di pianificazione e
«in 1 secondi», C9; `cancel_event` non azzerato da `start_scan`, C5/C7/C9); alla **Parte D**
l'archivio vuoto di `build_app.py` fuori da macOS, il LEGGIMI del `.dmg` che manda al Debug USB, la
verifica dell'eseguibile nella pipeline e i punti di `emetti` elencati nel G6.

Verifica a fine audit: **441 test verdi** (erano 385 prima della Parte A), `pyflakes` vuoto,
collaudo `tests/pilota_app.py` con `"ok": true` (54 file, nessun `.part`, nessuna sottocartella).

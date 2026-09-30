# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 82 files · ~79,426 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1478 nodes · 3500 edges · 67 communities (59 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 145 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04b9463a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- pathlib
- test_adb.py
- test_widgets.py
- Critical Behaviors Contract
- installer.py
- App
- test_osutil.py
- FotoFacileError
- DemoAdbBackend
- TransferOptions
- test_ui_app.py
- cli.py
- ConnectPage
- History
- esegui_fino_alla_fine
- build_app.py
- mtp_linux.py
- attendi
- font
- ptp_mac.py
- planner.py
- flag_nascosta
- test_trasporto.py
- OptionsPage
- Annullato
- wpd_win.ps1
- pytest
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- AdbDemoAPassi
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- MediaFile
- .copia
- format.py
- test_installer_pacchetti.py
- ensure_space
- format_size
- sys
- test_robustezza.py
- test_pacchetto_windows.py
- crea_installer_mac.py
- transfer_steps
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_scanner.py
- crea_pacchetto
- TransferPage
- theme.py
- TrasportoAdb
- trasporto.py
- parse_stat_stream
- TrasportoComposto
- osutil.py
- aiutanti/__init__.py
- TrasportoMtpLinux
- tema_testo
- Piano di revisione e sviluppo — FotoFacile

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 91 edges
2. `esegui_fino_alla_fine()` - 54 edges
3. `DeviceInfo` - 53 edges
4. `MediaFile` - 50 edges
5. `TransferOptions` - 45 edges
6. `AdbAPassi` - 43 edges
7. `DemoAdbBackend` - 41 edges
8. `App` - 39 edges
9. `History` - 36 edges
10. `ProcessoEsterno` - 35 edges

## Surprising Connections (you probably didn't know these)
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_shell_quote_gestisce_apostrofi_e_spazi()` --calls--> `shell_quote()`  [EXTRACTED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_shell_quote_gestisce_dollaro_backtick_e_virgolette()` --calls--> `shell_quote()`  [EXTRACTED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_shell_quote_lascia_intatti_i_percorsi_normali()` --calls--> `shell_quote()`  [EXTRACTED]
  tests/test_adb.py → fotofacile/core/adb.py
- `finestra_condivisa()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/conftest.py → fotofacile/core/demo.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (67 total, 3 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.08
Nodes (29): DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, leggi_dispositivi() (+21 more)

### Community 1 - "pathlib"
Cohesion: 0.17
Nodes (19): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.… (+11 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (32): find_adb(), CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend, AdbError (+24 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.10
Nodes (15): Banner, LogPane, PathChooser, Misc, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Barra dei passi della procedura guidata, con quello attuale evidenziato., Area di testo scorrevole con il dettaglio di quello che succede. (+7 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "installer.py"
Cohesion: 0.08
Nodes (51): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), extract_component(), impronta_file(), install_component() (+43 more)

### Community 6 - "App"
Cohesion: 0.08
Nodes (18): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma. (+10 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.18
Nodes (18): app_dir(), default_photos_dir(), file_manager_command(), open_in_file_manager(), Path, Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale., Cartella proposta per salvare le foto (Immagini/FotoFacile)., Comando che apre una cartella nel file manager del sistema. (+10 more)

### Community 8 - "FotoFacileError"
Cohesion: 0.09
Nodes (27): FotoFacileError, Errore con messaggio per l'utente e un suggerimento su come procedere., ProcessoEsterno, Path, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. (+19 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.14
Nodes (15): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_backend_demo_si_presenta_come_dispositivo_pronto(), test_cancellazione_di_percorso_inesistente_da_errore(), test_cancellazione_rimuove_il_file() (+7 more)

### Community 10 - "TransferOptions"
Cohesion: 0.09
Nodes (66): build_plan(), destination_for(), _nome_sicuro(), PlannedFile, Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.… (+58 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.10
Nodes (10): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Un'area vuota sempre presente confonde: compare al primo messaggio., test_i_dettagli_si_mostrano_solo_quando_servono(), test_modalita_demo_attivabile_e_disattivabile(), test_task_con_callback_di_errore_personalizzato(), test_task_con_errore_imprevisto_non_chiude_il_programma(), test_task_con_errore_mostra_il_messaggio_umano(), test_task_eseguito_a_passi_senza_thread() (+2 more)

### Community 12 - "cli.py"
Cohesion: 0.07
Nodes (43): ArgumentParser, avviso_visibile(), build_doctor_report(), build_parser(), contesto_grafico_dubbio(), doctor(), main(), _processo_finestra() (+35 more)

### Community 13 - "ConnectPage"
Cohesion: 0.17
Nodes (7): ConnectPage, Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.07
Nodes (33): default_path(), History, Path, Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in… (+25 more)

### Community 15 - "esegui_fino_alla_fine"
Cohesion: 0.14
Nodes (24): AdbAPassi, Rimuove la cartella di appoggio usata per gli elenchi temporanei., Elenca i telefoni collegati e il loro stato., Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su… (+16 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.05
Nodes (77): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+69 more)

### Community 18 - "attendi"
Cohesion: 0.15
Nodes (20): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Funzioni di appoggio per i test della grafica., Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto() (+12 more)

### Community 19 - "font"
Cohesion: 0.13
Nodes (21): apply_theme(), contrasto(), font(), pick_font_family(), Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono). (+13 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.06
Nodes (52): AiutanteNonDisponibile, apri_sessione(), _apri_telefono(), _Attesa, cammina(), chiudi_sessione(), comando_cancella(), comando_copia() (+44 more)

### Community 21 - "planner.py"
Cohesion: 0.18
Nodes (20): datetime, Costruzione del piano di copia: cosa copiare, dove, e cosa saltare. I nomi dei…, TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato., Testo del resoconto, leggibile da chiunque. (+12 more)

### Community 22 - "flag_nascosta"
Cohesion: 0.19
Nodes (14): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+6 more)

### Community 23 - "test_trasporto.py"
Cohesion: 0.08
Nodes (30): genere_per_estensione(), «photo», «video» o ``None`` in base all'estensione del file., Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, Telefono collegato via cavo su Windows, senza Debug USB., TrasportoWpdWindows, Path, Verifica del livello «collegamento diretto»: lettura dell'uscita degli…, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py. (+22 more)

### Community 24 - "OptionsPage"
Cohesion: 0.35
Nodes (3): OptionsPage, Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 25 - "Annullato"
Cohesion: 0.12
Nodes (15): Annullato, Exception, Segnale interno: l'utente ha interrotto l'operazione in corso., comando_aiutante(), _dimensione(), Path, _rallenta_scrittura(), Manda avanti un comando dell'aiutante a piccoli passi, annullabile. (+7 more)

### Community 26 - "wpd_win.ps1"
Cohesion: 0.22
Nodes (21): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+13 more)

### Community 27 - "pytest"
Cohesion: 0.17
Nodes (14): _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), pytest, Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…, Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice., test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema() (+6 more)

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "AdbDemoAPassi"
Cohesion: 0.18
Nodes (12): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., Path, _risposta(), test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia(), test_demo_a_passi_elenca_e_copia() (+4 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.08
Nodes (18): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+10 more)

### Community 39 - "MediaFile"
Cohesion: 0.12
Nodes (9): MediaFile, leggi_elenco(), Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file(), test_mediafile_ha_nome_e_cartella(), test_leggi_elenco_coercizza_i_numeri_e_azzera_quelli_rotti() (+1 more)

### Community 40 - ".copia"
Cohesion: 0.12
Nodes (19): _controlla_spazio(), _esito_di_copia(), percorso_temporaneo(), Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Nome del file «a metà», unico per processo. Il numero del processo evita che…, Avvisa in modo comprensibile se il disco è pieno, **prima** di iniziare a… (+11 more)

### Community 41 - "format.py"
Cohesion: 0.21
Nodes (14): format_date(), format_duration(), format_eta(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile., parametrize (+6 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.09
Nodes (17): re, skipif, _bat(), pacchetto(), fixture, Path, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per… (+9 more)

### Community 43 - "ensure_space"
Cohesion: 0.12
Nodes (19): Errore durante la copia di un file., TransferError, _accorcia_cartella(), _accorcia_nome(), _dimensione(), ensure_space(), _Esistenza, _limita_percorso() (+11 more)

### Community 44 - "format_size"
Cohesion: 0.17
Nodes (7): format_size(), Dimensione leggibile all'italiana: «3,4 GB»., Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa…, SelectPage

### Community 45 - "sys"
Cohesion: 0.12
Nodes (16): chiave_sistema(), Nome del sistema normalizzato a «win32» / «darwin» / «linux»., _eseguibile(), Collegamento diretto su Linux: MTP tramite ``gio``/gvfs, con ``jmtpfs`` di…, True se questo file è il collegamento giusto per il sistema in uso., Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, True solo su Linux e solo se c'è un modo per montare l'MTP., sistema_supportato() (+8 more)

### Community 46 - "test_robustezza.py"
Cohesion: 0.23
Nodes (13): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Su Linux il comando non deve bloccare la finestra., Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_apertura_cartella_su_linux_usa_processo_leggero(), test_apertura_cartella_su_windows_non_boccia_explorer(), test_copia_reale_abbandonata_non_lascia_nulla() (+5 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.10
Nodes (11): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, «python3 scripts/crea_pacchetto_windows.py .» non deve svuotare la cartella…, Una cartella padre del repository non va mai cancellata (qui il repository è…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, test_il_codice_copiato_funziona() (+3 more)

### Community 48 - "crea_installer_mac.py"
Cohesion: 0.27
Nodes (9): argparse, crea_dmg(), _esegui(), main(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, versione() (+1 more)

### Community 49 - "transfer_steps"
Cohesion: 0.50
Nodes (5): Progress, _pubblica(), Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo., transfer_steps()

### Community 50 - "Trasporto"
Cohesion: 0.12
Nodes (10): nomi_trasporti(), Protocol, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata)., Prova a far ripartire il collegamento (usato dal pulsante «Riavvia… (+2 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.14
Nodes (13): Code Context, Completed, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know, Goal, Handoff: FotoFacile — app desktop per copiare foto da Android (+5 more)

### Community 52 - "test_scanner.py"
Cohesion: 0.20
Nodes (12): build_scan_command(), list_media(), Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_comando_scansione_con_video_e_profondita(), test_comando_scansione_quota_percorsi_e_filtra_estensioni() (+4 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.29
Nodes (11): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+3 more)

### Community 54 - "TransferPage"
Cohesion: 0.18
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita., La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 55 - "theme.py"
Cohesion: 0.15
Nodes (13): Canvas, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., _canale(), luminanza(), modalita_scura(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, True se la tavolozza attiva è quella scura. (+5 more)

### Community 56 - "TrasportoAdb"
Cohesion: 0.16
Nodes (4): Path, Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 57 - "trasporto.py"
Cohesion: 0.19
Nodes (11): Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, Come FotoFacile parla con il telefono. Il programma non usa **un solo** metodo…, Elenco dei collegamenti utilizzabili su questo computer, dal più comodo al…, Costruisce il collegamento diretto adatto al sistema, se esiste., Il modo migliore disponibile, oppure ``None`` se non ce n'è nessuno., scegli_trasporto() (+3 more)

### Community 58 - "parse_stat_stream"
Cohesion: 0.20
Nodes (12): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le…, test_elenco_file_produce_righe_stat_compatibili() (+4 more)

### Community 59 - "TrasportoComposto"
Cohesion: 0.18
Nodes (4): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto

### Community 61 - "osutil.py"
Cohesion: 0.24
Nodes (10): is_case_insensitive_fs(), is_windows(), python_command(), Unico punto in cui il programma si adatta al sistema operativo., Come si avvia Python da terminale su questo sistema., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., True sui sistemi dove «Foto.jpg» e «foto.jpg» sono lo stesso file., _system() (+2 more)

### Community 62 - "aiutanti/__init__.py"
Cohesion: 0.22
Nodes (9): aiutante_per_sistema(), carica(), esegui(), modulo_disponibile(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita. (+1 more)

### Community 63 - "TrasportoMtpLinux"
Cohesion: 0.20
Nodes (5): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 65 - "tema_testo"
Cohesion: 0.25
Nodes (7): Istruzioni per marca, con menù a tendina. La finestra viene riusata, non…, Misc, Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, Colora una finestra secondaria come quella principale. Serve a evitare il bordo…, tema_finestra(), tema_testo(), Text

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.40
Nodes (4): Fase 1 — Errori e bug (verificabili con i test), Fase 2 — Copia «piatta» (solo foto e video), Fase 3 — Trasporti senza Debug USB, Piano di revisione e sviluppo — FotoFacile

## Knowledge Gaps
- **37 isolated node(s):** `run_tests.sh script`, `Goal`, `Completed`, `Not Yet Done`, `Failed Approaches (Don't Repeat These)` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 529 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `pathlib`, `test_adb.py`, `installer.py`, `App`, `test_osutil.py`, `TransferOptions`, `test_ui_app.py`, `esegui_fino_alla_fine`, `planner.py`, `test_trasporto.py`, `Annullato`, `AdbDemoAPassi`, `AdbBackend`, `.copia`, `ensure_space`, `test_robustezza.py`, `transfer_steps`, `Trasporto`, `theme.py`, `trasporto.py`, `TrasportoComposto`, `osutil.py`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `MediaFile` connect `MediaFile` to `pathlib`, `TransferOptions`, `format_size`, `sys`, `test_robustezza.py`, `esegui_fino_alla_fine`, `Trasporto`, `test_scanner.py`, `planner.py`, `theme.py`, `Annullato`, `TrasportoAdb`, `trasporto.py`, `parse_stat_stream`, `TrasportoComposto`, `test_trasporto.py`, `AdbDemoAPassi`, `TrasportoMtpLinux`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `pathlib`, `test_widgets.py`, `FotoFacileError`, `cli.py`, `ConnectPage`, `format_size`, `History`, `TransferPage`, `OptionsPage`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 3 INFERRED edges - model-reasoned connections that need verification._
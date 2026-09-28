# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 69 files · ~57,992 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 1, .command 1, .icns 1)

## Summary
- 1091 nodes · 2617 edges · 65 communities (51 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 178 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d2374f6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- planner.py
- test_adb.py
- widgets.py
- Critical Behaviors Contract
- test_installer.py
- App
- test_osutil.py
- ProcessoEsterno
- DemoAdbBackend
- TransferOptions
- test_ui_app.py
- test_cli.py
- ConnectPage
- History
- AdbAPassi
- build_app.py
- FotoFacileError
- attendi
- test_theme.py
- ScaricatoreAPassi
- page_transfer.py
- flag_nascosta
- test_autocollaudo_riporta_esito_positivo
- OptionsPage
- fotofacile/__init__.py
- test_avvio_salta_la_prova_quando_il_contesto_e_grafico
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- AdbDemoAPassi
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- cli.py
- .copia
- format_size
- test_installer_pacchetti.py
- Path
- doctor
- conftest.py
- test_robustezza.py
- test_pacchetto_windows.py
- crea_installer_mac.py
- transfer_steps
- Files to Know
- Handoff: FotoFacile — app desktop per copiare foto da Android
- font
- sys
- TransferPage
- theme.py
- sistema_scuro
- .run_task
- test_page_transfer.py
- pytest
- ._costruisci_pagine
- main
- test_errore_nella_callback_non_ferma_il_programma

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 70 edges
2. `TransferOptions` - 46 edges
3. `App` - 44 edges
4. `AdbAPassi` - 43 edges
5. `esegui_fino_alla_fine()` - 42 edges
6. `DemoAdbBackend` - 39 edges
7. `History` - 36 edges
8. `DeviceInfo` - 35 edges
9. `MediaFile` - 33 edges
10. `transfer()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Failed Approaches (Don't Repeat These)` --references--> `update()`  [INFERRED]
  HANDOFF.md → tests/test_cli.py
- `Current State` --references--> `doctor()`  [INFERRED]
  HANDOFF.md → fotofacile/cli.py
- `Edge Cases & Error Handling` --references--> `doctor()`  [INFERRED]
  HANDOFF.md → fotofacile/cli.py
- `Warnings` --references--> `find_adb()`  [INFERRED]
  HANDOFF.md → fotofacile/core/adb.py
- `Code Context` --references--> `AdbAPassi`  [INFERRED]
  HANDOFF.md → fotofacile/core/adb_passi.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (65 total, 14 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.15
Nodes (20): DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_dispositivo_non_autorizzato_non_pronto() (+12 more)

### Community 1 - "planner.py"
Cohesion: 0.14
Nodes (22): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Unico punto in cui il programma si adatta al sistema operativo. (+14 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (35): find_adb(), CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+27 more)

### Community 3 - "widgets.py"
Cohesion: 0.13
Nodes (12): Banner, LogPane, PathChooser, Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Area di testo scorrevole con il dettaglio di quello che succede., test_banner_accetta_tutti_i_toni() (+4 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_installer.py"
Cohesion: 0.09
Nodes (38): _chiave_sistema(), component_dir(), download_file(), extract_component(), install_component(), installa_a_passi(), is_installed(), _nome_eseguibile() (+30 more)

### Community 6 - "App"
Cohesion: 0.19
Nodes (6): App, Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare., Contenitore della procedura guidata: crea le pagine e coordina il lavoro.

### Community 7 - "test_osutil.py"
Cohesion: 0.07
Nodes (31): app_dir(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command(), Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale. (+23 more)

### Community 8 - "ProcessoEsterno"
Cohesion: 0.13
Nodes (17): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica., RisultatoComando (+9 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.06
Nodes (41): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., build_scan_command(), group_folders(), _kind_for(), _label() (+33 more)

### Community 10 - "TransferOptions"
Cohesion: 0.08
Nodes (70): Errore durante la copia di un file., TransferError, build_plan(), destination_for(), ensure_space(), _nome_sicuro(), PlannedFile, Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare. (+62 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.08
Nodes (11): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Senza questo, avviata dal Terminale, la finestra può restare nascosta dietro., Un'area vuota sempre presente confonde: compare al primo messaggio., test_i_dettagli_si_mostrano_solo_quando_servono(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_la_finestra_si_mette_davanti(), test_modalita_demo_attivabile_e_disattivabile(), test_task_con_errore_imprevisto_non_chiude_il_programma() (+3 more)

### Community 12 - "test_cli.py"
Cohesion: 0.22
Nodes (11): main(), Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_avvio_avvisa_in_chiaro_se_la_grafica_non_parte(), test_avvio_normale_senza_demo(), test_diagnostica_riporta_tutte_le_voci() (+3 more)

### Community 13 - "ConnectPage"
Cohesion: 0.14
Nodes (8): ConnectPage, aggiorna(), Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Istruzioni per marca, con menù a tendina., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.12
Nodes (16): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., Cronologia dei file già copiati, caricata una volta sola., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo() (+8 more)

### Community 15 - "AdbAPassi"
Cohesion: 0.24
Nodes (19): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+11 more)

### Community 16 - "build_app.py"
Cohesion: 0.22
Nodes (18): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+10 more)

### Community 17 - "FotoFacileError"
Cohesion: 0.16
Nodes (13): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), Edge Cases & Error Handling, test_errore_di_permesso_non_viene_ritentato() (+5 more)

### Community 18 - "attendi"
Cohesion: 0.18
Nodes (14): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto(), test_modalita_demo_attivabile_dal_passo_1() (+6 more)

### Community 19 - "test_theme.py"
Cohesion: 0.18
Nodes (14): apply_theme(), pick_font_family(), Misc, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., _prova_finestra(), True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available() (+6 more)

### Community 20 - "ScaricatoreAPassi"
Cohesion: 0.14
Nodes (6): Path, Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, test_scaricatore_annullabile(), test_scaricatore_scrive_i_byte_e_riporta_avanzamento(), test_scaricatore_senza_rete_spiega_cosa_controllare()

### Community 21 - "page_transfer.py"
Cohesion: 0.18
Nodes (20): datetime, TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato., Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. (+12 more)

### Community 22 - "flag_nascosta"
Cohesion: 0.16
Nodes (13): avviso_visibile(), prova_finestra(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio., Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Apre la finestra principale; se la grafica non è disponibile lo spiega con…, scrivi_log_avvio() (+5 more)

### Community 23 - "test_autocollaudo_riporta_esito_positivo"
Cohesion: 0.29
Nodes (3): L'autocollaudo serve a verificare una build impacchettata: deve dire…, test_autocollaudo_riporta_esito_positivo(), update()

### Community 27 - "test_page_select.py"
Cohesion: 0.52
Nodes (6): _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "AdbDemoAPassi"
Cohesion: 0.12
Nodes (16): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio usata per gli elenchi temporanei., Annullato, Exception, Segnale interno: l'utente ha interrotto l'operazione in corso., Code Context, Path (+8 more)

### Community 37 - "make_icon.py"
Cohesion: 0.16
Nodes (17): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), main(), Path, Crea un .ico contenente il PNG 256×256 (formato accettato da Windows). (+9 more)

### Community 38 - "AdbBackend"
Cohesion: 0.10
Nodes (13): AdbBackend, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono., Avvia il collegamento. (+5 more)

### Community 39 - "cli.py"
Cohesion: 0.18
Nodes (9): ArgumentParser, build_parser(), contesto_grafico_dubbio(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, True se non ci sono segnali di una sessione grafica (automazione, servizi,…, selftest(), Avvio rapido di FotoFacile. Windows: py fotofacile.py macOS/Linux: python3… (+1 more)

### Community 40 - ".copia"
Cohesion: 0.13
Nodes (7): Path, Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., Elenca i telefoni collegati e il loro stato.

### Community 41 - "format_size"
Cohesion: 0.12
Nodes (19): format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Dimensione leggibile all'italiana: «3,4 GB». (+11 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.12
Nodes (10): re, _bat(), pacchetto(), fixture, Path, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Ogni frammento Python scritto nei .bat deve essere compilabile davvero., Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire. (+2 more)

### Community 43 - "Path"
Cohesion: 0.26
Nodes (8): _accorcia_cartelle(), _dimensione(), _Esistenza, _limita_percorso(), Path, Riduce il percorso entro il limite sicuro multipiattaforma. Ordine degli…, Dimensione di un file esistente; -1 se nel frattempo è sparito., Verifica rapidamente se un nome è già occupato, con o senza distinzione di…

### Community 44 - "doctor"
Cohesion: 0.25
Nodes (8): build_doctor_report(), doctor(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., Stampa una diagnosi completa dello stato del computer e del collegamento., Completed, Current State, test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_senza_componente()

### Community 45 - "conftest.py"
Cohesion: 0.27
Nodes (9): app(), casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una…, Cartella utente finta: i test non devono mai toccare i file reali dell'utente. (+1 more)

### Community 46 - "test_robustezza.py"
Cohesion: 0.17
Nodes (11): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_copia_reale_abbandonata_non_lascia_nulla(), test_copia_reale_con_errore_di_disco_non_lascia_part(), test_copia_reale_con_permesso_negato_spiega_come_rimediare(), test_cronologia_non_scrivibile_non_perde_le_foto_copiate() (+3 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.14
Nodes (7): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, test_il_codice_copiato_funziona(), test_il_pacchetto_non_contiene_file_di_sviluppo()

### Community 48 - "crea_installer_mac.py"
Cohesion: 0.19
Nodes (12): argparse, crea_dmg(), _esegui(), main(), CompletedProcess, Path, Crea l'installatore macOS (.dmg) di FotoFacile: si apre, si trascina l'app in…, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il… (+4 more)

### Community 49 - "transfer_steps"
Cohesion: 0.22
Nodes (12): _chiudi(), conta(), download_file_stream(), Progress, _pubblica(), Path, Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo. (+4 more)

### Community 50 - "Files to Know"
Cohesion: 0.21
Nodes (6): Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Ferma il lavoro in corso (l'utente ha cambiato idea o è tornato indietro). Il…, Chiude il programma; se sta copiando chiede conferma e non lascia file a metà., Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio)., Files to Know

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.17
Nodes (11): Goal, Handoff: FotoFacile — app desktop per copiare foto da Android, Key Decisions, Not Yet Done, Resume Instructions, Setup Required, Warnings, azzera() (+3 more)

### Community 52 - "font"
Cohesion: 0.31
Nodes (6): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_indicatore_passi()

### Community 53 - "sys"
Cohesion: 0.27
Nodes (10): _copia_albero(), crea_pacchetto(), main(), Path, Crea la cartella «FotoFacile per Windows» pronta da copiare su un PC Windows.…, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Crea la cartella pronta per Windows e restituisce il percorso., _scrivi_testo() (+2 more)

### Community 55 - "theme.py"
Cohesion: 0.24
Nodes (9): _canale(), contrasto(), luminanza(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Luminanza relativa di un colore «#rrggbb» (formula WCAG)., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono)., Il testo deve essere chiaro su sfondo scuro: era il difetto che rendeva l'app…, test_modalita_scura_ha_contrasto_leggibile() (+1 more)

### Community 56 - "sistema_scuro"
Cohesion: 0.28
Nodes (6): True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), test_modalita_scura_non_impedisce_l_avvio_se_il_comando_manca(), test_modalita_scura_su_linux(), test_riconosce_la_modalita_scura_di_macos(), runner()

### Community 57 - ".run_task"
Cohesion: 0.32
Nodes (5): Any, tick(), Porta avanti un generatore a passi dentro il ciclo della grafica., Esegue il seguito di un task senza che un errore di grafica fermi il programma., Failed Approaches (Don't Repeat These)

### Community 58 - "test_page_transfer.py"
Cohesion: 0.39
Nodes (6): Funzioni di appoggio per i test della grafica., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla()

### Community 59 - "pytest"
Cohesion: 0.33
Nodes (4): pytest, Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…, Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice., test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema()

### Community 62 - "main"
Cohesion: 1.00
Nodes (4): main(), fallisci(), passo(), scrivi_esito()

## Knowledge Gaps
- **27 isolated node(s):** `run_tests.sh script`, `Goal`, `Not Yet Done`, `Key Decisions`, `Resume Instructions` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 381 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `planner.py`, `test_adb.py`, `test_installer.py`, `App`, `test_osutil.py`, `.copia`, `ProcessoEsterno`, `TransferOptions`, `test_ui_app.py`, `test_robustezza.py`, `AdbAPassi`, `transfer_steps`, `ScaricatoreAPassi`, `page_transfer.py`, `.run_task`, `AdbDemoAPassi`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `planner.py`, `test_adb.py`, `widgets.py`, `DemoAdbBackend`, `ConnectPage`, `History`, `AdbAPassi`, `FotoFacileError`, `flag_nascosta`, `OptionsPage`, `AdbDemoAPassi`, `cli.py`, `format_size`, `conftest.py`, `Files to Know`, `font`, `TransferPage`, `.run_task`, `._costruisci_pagine`, `main`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `ProcessoEsterno` connect `ProcessoEsterno` to `planner.py`, `test_osutil.py`, `.copia`, `test_robustezza.py`, `AdbAPassi`, `FotoFacileError`, `Files to Know`, `ScaricatoreAPassi`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 8 INFERRED edges - model-reasoned connections that need verification._
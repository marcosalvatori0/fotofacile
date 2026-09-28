# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 65 files · ~53,822 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 1, .command 1, .icns 1)

## Summary
- 1057 nodes · 2569 edges · 58 communities (43 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 181 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `20d1ea5b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- AdbBackend
- test_adb.py
- widgets.py
- Critical Behaviors Contract
- FotoFacileError
- App
- pathlib
- ProcessoEsterno
- DemoAdbBackend
- TransferOptions
- test_ui_app.py
- theme.py
- ConnectPage
- History
- Annullato
- test_pacchetto_windows.py
- transfer.py
- attendi
- test_theme.py
- test_scaricatore_scrive_i_byte_e_riporta_avanzamento
- planner.py
- AdbAPassi
- TransferPlan
- OptionsPage
- font
- scanner.py
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- test_page_transfer.py
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- build_app.py
- cli.py
- ._costruisci_pagine
- SelectPage
- Files to Know
- Path
- .run_task
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_scanner.py
- test_robustezza.py
- AdbDemoAPassi
- TransferPage
- main
- sistema_scuro
- MediaFile
- test_i_comandi_esterni_usano_il_flag_nascosta
- .show_help
- test_errore_nella_callback_non_ferma_il_programma
- .pulisci
- test_scaricatore_senza_rete_spiega_cosa_controllare

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 70 edges
2. `TransferOptions` - 46 edges
3. `App` - 45 edges
4. `AdbAPassi` - 43 edges
5. `esegui_fino_alla_fine()` - 42 edges
6. `DemoAdbBackend` - 39 edges
7. `History` - 36 edges
8. `DeviceInfo` - 35 edges
9. `MediaFile` - 33 edges
10. `transfer()` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Current State` --references--> `doctor()`  [INFERRED]
  HANDOFF.md → fotofacile/cli.py
- `Failed Approaches (Don't Repeat These)` --references--> `update()`  [INFERRED]
  HANDOFF.md → tests/test_cli.py
- `Completed` --references--> `doctor()`  [INFERRED]
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

## Communities (58 total, 15 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.11
Nodes (23): dataclasses, DeviceInfo, parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_backend_demo_si_presenta_come_dispositivo_pronto() (+15 more)

### Community 1 - "AdbBackend"
Cohesion: 0.10
Nodes (13): AdbBackend, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono., Avvia il collegamento. (+5 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (35): CompletedProcess, find_adb(), Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+27 more)

### Community 3 - "widgets.py"
Cohesion: 0.12
Nodes (13): Banner, LogPane, PathChooser, _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Area di testo scorrevole con il dettaglio di quello che succede. (+5 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "FotoFacileError"
Cohesion: 0.05
Nodes (60): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), _chiave_sistema(), component_dir() (+52 more)

### Community 6 - "App"
Cohesion: 0.17
Nodes (7): App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare., Contenitore della procedura guidata: crea le pagine e coordina il lavoro.

### Community 7 - "pathlib"
Cohesion: 0.05
Nodes (62): Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, app_dir(), default_photos_dir() (+54 more)

### Community 8 - "ProcessoEsterno"
Cohesion: 0.13
Nodes (17): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica., RisultatoComando (+9 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.15
Nodes (13): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_cancellazione_di_percorso_inesistente_da_errore(), test_cancellazione_rimuove_il_file(), test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla() (+5 more)

### Community 10 - "TransferOptions"
Cohesion: 0.08
Nodes (69): Errore durante la copia di un file., TransferError, build_plan(), destination_for(), ensure_space(), _nome_sicuro(), PlannedFile, Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare. (+61 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.07
Nodes (13): app(), fixture, Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Senza questo, avviata dal Terminale, la finestra può restare nascosta dietro., Un'area vuota sempre presente confonde: compare al primo messaggio., test_i_dettagli_si_mostrano_solo_quando_servono(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_la_finestra_si_mette_davanti() (+5 more)

### Community 12 - "theme.py"
Cohesion: 0.24
Nodes (9): _canale(), contrasto(), luminanza(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Luminanza relativa di un colore «#rrggbb» (formula WCAG)., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono)., Il testo deve essere chiaro su sfondo scuro: era il difetto che rendeva l'app…, test_modalita_scura_ha_contrasto_leggibile() (+1 more)

### Community 13 - "ConnectPage"
Cohesion: 0.17
Nodes (6): ConnectPage, Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.13
Nodes (15): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo(), test_file_assente_viene_trattato_come_vuoto() (+7 more)

### Community 15 - "Annullato"
Cohesion: 0.13
Nodes (9): Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., Elenca i telefoni collegati e il loro stato., Annullato, Exception (+1 more)

### Community 16 - "test_pacchetto_windows.py"
Cohesion: 0.11
Nodes (16): _copia_albero(), crea_pacchetto(), main(), Path, Crea la cartella «FotoFacile per Windows» pronta da copiare su un PC Windows.…, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Crea la cartella pronta per Windows e restituisce il percorso., _scrivi_testo() (+8 more)

### Community 17 - "transfer.py"
Cohesion: 0.23
Nodes (13): _chiudi(), conta(), download_file_stream(), Progress, _pubblica(), Path, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.…, Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``… (+5 more)

### Community 18 - "attendi"
Cohesion: 0.18
Nodes (14): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto(), test_modalita_demo_attivabile_dal_passo_1() (+6 more)

### Community 19 - "test_theme.py"
Cohesion: 0.22
Nodes (12): apply_theme(), pick_font_family(), Misc, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), test_ricade_su_un_font_generico_se_nessuno_disponibile() (+4 more)

### Community 21 - "planner.py"
Cohesion: 0.14
Nodes (23): datetime, format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date. (+15 more)

### Community 22 - "AdbAPassi"
Cohesion: 0.30
Nodes (17): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato(), test_cerca_media_legge_l_output_anche_se_e_lungo() (+9 more)

### Community 23 - "TransferPlan"
Cohesion: 0.22
Nodes (16): TransferPlan, build_report(), _cartelle_di_riserva(), Path, Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile., Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,…, save_report() (+8 more)

### Community 25 - "font"
Cohesion: 0.24
Nodes (7): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_font_restituisce_tupla_usabile_da_tkinter(), test_indicatore_passi()

### Community 26 - "scanner.py"
Cohesion: 0.17
Nodes (14): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le… (+6 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.36
Nodes (7): Funzioni di appoggio per i test della grafica., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "test_page_transfer.py"
Cohesion: 0.60
Nodes (5): _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla()

### Community 37 - "make_icon.py"
Cohesion: 0.16
Nodes (17): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), main(), Path, Crea un .ico contenente il PNG 256×256 (formato accettato da Windows). (+9 more)

### Community 38 - "build_app.py"
Cohesion: 0.20
Nodes (19): argparse, comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main() (+11 more)

### Community 39 - "cli.py"
Cohesion: 0.05
Nodes (44): ArgumentParser, avviso_visibile(), build_doctor_report(), build_parser(), contesto_grafico_dubbio(), doctor(), main(), prova_finestra() (+36 more)

### Community 41 - "SelectPage"
Cohesion: 0.24
Nodes (3): Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., SelectPage

### Community 42 - "Files to Know"
Cohesion: 0.24
Nodes (6): Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Ferma il lavoro in corso (l'utente ha cambiato idea o è tornato indietro). Il…, Chiude il programma; se sta copiando chiede conferma e non lascia file a metà., Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio)., Files to Know, Key Decisions

### Community 43 - "Path"
Cohesion: 0.26
Nodes (8): _accorcia_cartelle(), _dimensione(), _Esistenza, _limita_percorso(), Path, Riduce il percorso entro il limite sicuro multipiattaforma. Ordine degli…, Dimensione di un file esistente; -1 se nel frattempo è sparito., Verifica rapidamente se un nome è già occupato, con o senza distinzione di…

### Community 44 - ".run_task"
Cohesion: 0.32
Nodes (5): Any, tick(), Porta avanti un generatore a passi dentro il ciclo della grafica., Esegue il seguito di un task senza che un errore di grafica fermi il programma., Completed

### Community 45 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.14
Nodes (13): Cronologia dei file già copiati, caricata una volta sola., Code Context, Current State, Failed Approaches (Don't Repeat These), Goal, Handoff: FotoFacile — app desktop per copiare foto da Android, Not Yet Done, Resume Instructions (+5 more)

### Community 46 - "test_scanner.py"
Cohesion: 0.24
Nodes (11): build_scan_command(), list_media(), Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_comando_scansione_con_video_e_profondita(), test_comando_scansione_quota_percorsi_e_filtra_estensioni() (+3 more)

### Community 47 - "test_robustezza.py"
Cohesion: 0.22
Nodes (10): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_copia_reale_abbandonata_non_lascia_nulla(), test_copia_reale_con_errore_di_disco_non_lascia_part(), test_copia_reale_con_permesso_negato_spiega_come_rimediare(), test_processo_non_avviabile_non_lascia_file_temporanei() (+2 more)

### Community 48 - "AdbDemoAPassi"
Cohesion: 0.17
Nodes (7): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio usata per gli elenchi temporanei., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi()

### Community 50 - "main"
Cohesion: 1.00
Nodes (4): main(), fallisci(), passo(), scrivi_esito()

### Community 51 - "sistema_scuro"
Cohesion: 0.28
Nodes (6): True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), test_modalita_scura_non_impedisce_l_avvio_se_il_comando_manca(), test_modalita_scura_su_linux(), test_riconosce_la_modalita_scura_di_macos(), runner()

### Community 52 - "MediaFile"
Cohesion: 0.25
Nodes (4): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, MediaFile, test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file(), test_mediafile_ha_nome_e_cartella()

## Knowledge Gaps
- **27 isolated node(s):** `run_tests.sh script`, `Goal`, `Not Yet Done`, `Verificare la grafica di nascosto (trucco utile)`, `Resume Instructions` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 359 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `test_adb.py`, `App`, `pathlib`, `ProcessoEsterno`, `TransferOptions`, `test_ui_app.py`, `.run_task`, `Annullato`, `AdbDemoAPassi`, `transfer.py`, `test_robustezza.py`, `planner.py`, `AdbAPassi`, `TransferPlan`, `test_scaricatore_senza_rete_spiega_cosa_controllare`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `test_adb.py`, `widgets.py`, `FotoFacileError`, `pathlib`, `DemoAdbBackend`, `ConnectPage`, `History`, `AdbAPassi`, `OptionsPage`, `font`, `cli.py`, `._costruisci_pagine`, `SelectPage`, `Files to Know`, `.run_task`, `Handoff: FotoFacile — app desktop per copiare foto da Android`, `AdbDemoAPassi`, `TransferPage`, `main`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `ProcessoEsterno` connect `ProcessoEsterno` to `FotoFacileError`, `pathlib`, `Files to Know`, `Annullato`, `test_robustezza.py`, `test_i_comandi_esterni_usano_il_flag_nascosta`, `AdbAPassi`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 8 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 63 files · ~51,362 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 1, .command 1, .icns 1)

## Summary
- 1021 nodes · 2500 edges · 46 communities (37 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 177 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d520cd69`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_robustezza.py
- AdbBackend
- test_adb.py
- app.py
- Critical Behaviors Contract
- test_installer.py
- App
- test_osutil.py
- ProcessoEsterno
- DemoAdbBackend
- test_planner.py
- test_ui_app.py
- theme.py
- ConnectPage
- History
- AdbAPassi
- finestra_condivisa
- TransferOptions
- attendi
- test_theme.py
- test_ops.py
- format_size
- download_file
- FotoFacileError
- OptionsPage
- font
- PathChooser
- pytest
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
- test_la_finestra_si_mette_davanti
- Files to Know
- .run_task
- Handoff: FotoFacile — app desktop per copiare foto da Android
- main

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

## Communities (46 total, 9 thin omitted)

### Community 0 - "test_robustezza.py"
Cohesion: 0.05
Nodes (76): dataclasses, datetime, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, DeviceInfo, get_devices(), parse_devices(), pick_device() (+68 more)

### Community 1 - "AdbBackend"
Cohesion: 0.10
Nodes (13): AdbBackend, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono., Avvia il collegamento. (+5 more)

### Community 2 - "test_adb.py"
Cohesion: 0.09
Nodes (35): CompletedProcess, find_adb(), Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+27 more)

### Community 3 - "app.py"
Cohesion: 0.14
Nodes (13): Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, Banner, LogPane, _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, True se questa macchina riesce davvero ad aprire una finestra. La verifica…, Area di testo scorrevole con il dettaglio di quello che succede. (+5 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_installer.py"
Cohesion: 0.14
Nodes (29): _chiave_sistema(), component_dir(), extract_component(), install_component(), installa_a_passi(), is_installed(), _nome_eseguibile(), platform_tools_url() (+21 more)

### Community 6 - "App"
Cohesion: 0.15
Nodes (9): App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare., Contenitore della procedura guidata: crea le pagine e coordina il lavoro., Barra dei passi della procedura guidata, con quello attuale evidenziato. (+1 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.09
Nodes (27): app_dir(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command(), Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale. (+19 more)

### Community 8 - "ProcessoEsterno"
Cohesion: 0.17
Nodes (9): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica., RisultatoComando (+1 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.06
Nodes (42): demo_files(), DemoAdbBackend, Telefono finto: serve per i test automatici e per la modalità demo senza…, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., build_scan_command(), group_folders(), _kind_for() (+34 more)

### Community 10 - "test_planner.py"
Cohesion: 0.08
Nodes (46): Errore durante la copia di un file., TransferError, _accorcia_cartelle(), build_plan(), destination_for(), _dimensione(), ensure_space(), _Esistenza (+38 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.07
Nodes (12): app(), fixture, Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Un'area vuota sempre presente confonde: compare al primo messaggio., test_errore_nella_callback_non_ferma_il_programma(), test_i_dettagli_si_mostrano_solo_quando_servono(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_modalita_demo_attivabile_e_disattivabile() (+4 more)

### Community 12 - "theme.py"
Cohesion: 0.15
Nodes (13): Passo 1: guidare la persona a collegare il telefono e autorizzare il computer.…, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., _canale(), contrasto(), luminanza(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Luminanza relativa di un colore «#rrggbb» (formula WCAG). (+5 more)

### Community 13 - "ConnectPage"
Cohesion: 0.14
Nodes (8): ConnectPage, aggiorna(), Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Istruzioni per marca, con menù a tendina., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.13
Nodes (15): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo(), test_file_assente_viene_trattato_come_vuoto() (+7 more)

### Community 15 - "AdbAPassi"
Cohesion: 0.05
Nodes (49): AdbAPassi, AdbDemoAPassi, Path, Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde». (+41 more)

### Community 16 - "finestra_condivisa"
Cohesion: 0.25
Nodes (8): app(), casa_temporanea(), finestra_condivisa(), fixture, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una…, Cartella utente finta: i test non devono mai toccare i file reali dell'utente., root()

### Community 17 - "TransferOptions"
Cohesion: 0.16
Nodes (35): TransferOptions, _chiudi(), conta(), download_file_stream(), Path, Copia il piano e restituisce il resoconto (modo diretto, senza passi)., Scrive un file dal telefono su disco passando da un temporaneo ``.part`` (modo…, transfer() (+27 more)

### Community 18 - "attendi"
Cohesion: 0.18
Nodes (14): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto(), test_modalita_demo_attivabile_dal_passo_1() (+6 more)

### Community 19 - "test_theme.py"
Cohesion: 0.13
Nodes (17): apply_theme(), pick_font_family(), Misc, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), test_font_restituisce_tupla_usabile_da_tkinter() (+9 more)

### Community 20 - "test_ops.py"
Cohesion: 0.11
Nodes (15): Path, Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, Path, script(), test_comando_inesistente_produce_errore_umano(), test_output_grande_va_su_file_per_non_intasare_il_collegamento(), test_processo_breve_riporta_output_e_codice() (+7 more)

### Community 21 - "format_size"
Cohesion: 0.09
Nodes (21): format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Dimensione leggibile all'italiana: «3,4 GB». (+13 more)

### Community 22 - "download_file"
Cohesion: 0.24
Nodes (7): download_file(), Scarica un file riportando l'avanzamento., risposta_finta(), test_download_annullato_non_lascia_file(), test_download_file_scrive_i_byte_giusti(), test_download_riporta_avanzamento(), test_download_senza_rete_spiega_cosa_fare()

### Community 23 - "FotoFacileError"
Cohesion: 0.19
Nodes (11): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), copia(), test_task_con_callback_di_errore_personalizzato() (+3 more)

### Community 25 - "font"
Cohesion: 0.46
Nodes (3): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc

### Community 26 - "PathChooser"
Cohesion: 0.33
Nodes (4): PathChooser, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., test_scelta_cartella_aggiorna_il_valore(), test_scelta_cartella_senza_callback()

### Community 27 - "pytest"
Cohesion: 0.43
Nodes (7): pytest, _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.31
Nodes (9): shutil, _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema() (+1 more)

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "test_page_transfer.py"
Cohesion: 0.39
Nodes (6): Funzioni di appoggio per i test della grafica., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla()

### Community 37 - "make_icon.py"
Cohesion: 0.16
Nodes (17): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), main(), Path, Crea un .ico contenente il PNG 256×256 (formato accettato da Windows). (+9 more)

### Community 38 - "build_app.py"
Cohesion: 0.20
Nodes (19): argparse, comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main() (+11 more)

### Community 39 - "cli.py"
Cohesion: 0.05
Nodes (43): ArgumentParser, avviso_visibile(), build_doctor_report(), build_parser(), contesto_grafico_dubbio(), doctor(), main(), prova_finestra() (+35 more)

### Community 42 - "Files to Know"
Cohesion: 0.24
Nodes (6): Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Ferma il lavoro in corso (l'utente ha cambiato idea o è tornato indietro). Il…, Chiude il programma; se sta copiando chiede conferma e non lascia file a metà., Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio)., Files to Know, Key Decisions

### Community 44 - ".run_task"
Cohesion: 0.32
Nodes (5): Any, tick(), Porta avanti un generatore a passi dentro il ciclo della grafica., Esegue il seguito di un task senza che un errore di grafica fermi il programma., Completed

### Community 45 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.15
Nodes (12): Cronologia dei file già copiati, caricata una volta sola., Code Context, Current State, Failed Approaches (Don't Repeat These), Goal, Handoff: FotoFacile — app desktop per copiare foto da Android, Not Yet Done, Resume Instructions (+4 more)

### Community 50 - "main"
Cohesion: 1.00
Nodes (4): main(), fallisci(), passo(), scrivi_esito()

## Knowledge Gaps
- **26 isolated node(s):** `run_tests.sh script`, `Goal`, `Not Yet Done`, `Resume Instructions`, `Setup Required` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 336 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `test_robustezza.py`, `test_adb.py`, `app.py`, `test_installer.py`, `App`, `test_osutil.py`, `ProcessoEsterno`, `test_planner.py`, `test_ui_app.py`, `.run_task`, `AdbAPassi`, `TransferOptions`, `test_ops.py`, `download_file`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `test_robustezza.py`, `test_adb.py`, `app.py`, `cli.py`, `._costruisci_pagine`, `DemoAdbBackend`, `Files to Know`, `.run_task`, `Handoff: FotoFacile — app desktop per copiare foto da Android`, `History`, `AdbAPassi`, `ConnectPage`, `finestra_condivisa`, `main`, `format_size`, `FotoFacileError`, `OptionsPage`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `AdbAPassi` connect `AdbAPassi` to `test_robustezza.py`, `app.py`, `App`, `ProcessoEsterno`, `Files to Know`, `Handoff: FotoFacile — app desktop per copiare foto da Android`, `FotoFacileError`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 8 INFERRED edges - model-reasoned connections that need verification._
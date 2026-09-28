# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 62 files · ~49,247 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 1, .icns 1, .ico 1)

## Summary
- 966 nodes · 2412 edges · 51 communities (44 shown, 7 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 170 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1590a1ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- planner.py
- transfer.py
- test_adb.py
- font
- Critical Behaviors Contract
- test_installer.py
- App
- osutil.py
- ProcessoEsterno
- DemoAdbBackend
- TransferOptions
- test_ui_app.py
- scanner.py
- ConnectPage
- History
- AdbAPassi
- conftest.py
- .copia
- attendi
- adb_passi.py
- ScaricatoreAPassi
- SelectPage
- AdbDemoAPassi
- FotoFacileError
- Path
- MediaFile
- test_scanner.py
- test_page_select.py
- test_page_options.py
- test_robustezza.py
- test_page_transfer.py
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- build_app.py
- main
- cli.py
- open_in_file_manager
- .ricostruisci_pagine
- widgets.py
- .run_task
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_autocollaudo_riporta_esito_positivo
- test_installer_passi.py
- pytest
- fotofacile/__init__.py
- main

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
- `Completed` --references--> `doctor()`  [INFERRED]
  HANDOFF.md → fotofacile/cli.py
- `Current State` --references--> `doctor()`  [INFERRED]
  HANDOFF.md → fotofacile/cli.py
- `Warnings` --references--> `find_adb()`  [INFERRED]
  HANDOFF.md → fotofacile/core/adb.py
- `Code Context` --references--> `AdbAPassi`  [INFERRED]
  HANDOFF.md → fotofacile/core/adb_passi.py
- `Files to Know` --references--> `AdbAPassi`  [INFERRED]
  HANDOFF.md → fotofacile/core/adb_passi.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (51 total, 7 thin omitted)

### Community 0 - "planner.py"
Cohesion: 0.05
Nodes (61): dataclasses, datetime, Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano. (+53 more)

### Community 1 - "transfer.py"
Cohesion: 0.07
Nodes (30): AdbBackend, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono., Avvia il collegamento. (+22 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (35): CompletedProcess, find_adb(), Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+27 more)

### Community 3 - "font"
Cohesion: 0.06
Nodes (32): OptionsPage, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono., apply_theme(), font(), pick_font_family(), Misc, Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma., Scegliе il primo font preferito presente sul sistema (Windows, macOS o Linux). (+24 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_installer.py"
Cohesion: 0.10
Nodes (37): _chiave_sistema(), component_dir(), download_file(), extract_component(), install_component(), installa_a_passi(), is_installed(), _nome_eseguibile() (+29 more)

### Community 6 - "App"
Cohesion: 0.16
Nodes (7): App, Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare., Contenitore della procedura guidata: crea le pagine e coordina il lavoro., Usa un backend in memoria (test) o il telefono demo., Frame

### Community 7 - "osutil.py"
Cohesion: 0.17
Nodes (19): app_dir(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), Path, python_command(), Unico punto in cui il programma si adatta al sistema operativo., Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale. (+11 more)

### Community 8 - "ProcessoEsterno"
Cohesion: 0.13
Nodes (17): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica., RisultatoComando (+9 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.15
Nodes (13): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_backend_demo_si_presenta_come_dispositivo_pronto(), test_cancellazione_di_percorso_inesistente_da_errore(), test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla() (+5 more)

### Community 10 - "TransferOptions"
Cohesion: 0.08
Nodes (69): Errore durante la copia di un file., TransferError, build_plan(), destination_for(), ensure_space(), _nome_sicuro(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Solleva un errore comprensibile se lo spazio libero non basta. (+61 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.09
Nodes (8): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., test_errore_nella_callback_non_ferma_il_programma(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_modalita_demo_attivabile_e_disattivabile(), test_task_con_errore_imprevisto_non_chiude_il_programma(), test_task_eseguito_a_passi_senza_thread(), test_un_task_abbandonato_chiude_il_generatore(), test_un_task_abbandonato_si_ferma_subito()

### Community 12 - "scanner.py"
Cohesion: 0.15
Nodes (17): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le… (+9 more)

### Community 13 - "ConnectPage"
Cohesion: 0.14
Nodes (8): ConnectPage, aggiorna(), Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Istruzioni per marca, con menù a tendina., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.13
Nodes (15): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo(), test_file_assente_viene_trattato_come_vuoto() (+7 more)

### Community 15 - "AdbAPassi"
Cohesion: 0.25
Nodes (18): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+10 more)

### Community 16 - "conftest.py"
Cohesion: 0.21
Nodes (11): sys, app(), casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una… (+3 more)

### Community 17 - ".copia"
Cohesion: 0.17
Nodes (5): Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde».

### Community 18 - "attendi"
Cohesion: 0.18
Nodes (14): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto(), test_modalita_demo_attivabile_dal_passo_1() (+6 more)

### Community 19 - "adb_passi.py"
Cohesion: 0.18
Nodes (15): Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, hashlib (+7 more)

### Community 20 - "ScaricatoreAPassi"
Cohesion: 0.14
Nodes (6): Path, Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, test_scaricatore_annullabile(), test_scaricatore_scrive_i_byte_e_riporta_avanzamento(), test_scaricatore_senza_rete_spiega_cosa_controllare()

### Community 21 - "SelectPage"
Cohesion: 0.24
Nodes (3): Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., SelectPage

### Community 22 - "AdbDemoAPassi"
Cohesion: 0.17
Nodes (7): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio usata per gli elenchi temporanei., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi()

### Community 23 - "FotoFacileError"
Cohesion: 0.21
Nodes (10): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), test_task_con_callback_di_errore_personalizzato(), lavoro() (+2 more)

### Community 24 - "Path"
Cohesion: 0.26
Nodes (8): _accorcia_cartelle(), _dimensione(), _Esistenza, _limita_percorso(), Path, Riduce il percorso entro il limite sicuro multipiattaforma. Ordine degli…, Dimensione di un file esistente; -1 se nel frattempo è sparito., Verifica rapidamente se un nome è già occupato, con o senza distinzione di…

### Community 25 - "MediaFile"
Cohesion: 0.18
Nodes (7): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, PlannedFile, MediaFile, test_errore_di_permesso_non_viene_ritentato(), copia(), test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file(), test_mediafile_ha_nome_e_cartella()

### Community 26 - "test_scanner.py"
Cohesion: 0.24
Nodes (11): build_scan_command(), list_media(), Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_comando_scansione_con_video_e_profondita(), test_comando_scansione_quota_percorsi_e_filtra_estensioni() (+3 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.52
Nodes (6): _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "test_robustezza.py"
Cohesion: 0.22
Nodes (10): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_copia_reale_abbandonata_non_lascia_nulla(), test_copia_reale_con_errore_di_disco_non_lascia_part(), test_copia_reale_con_permesso_negato_spiega_come_rimediare(), test_processo_non_avviabile_non_lascia_file_temporanei() (+2 more)

### Community 30 - "test_page_transfer.py"
Cohesion: 0.39
Nodes (6): Funzioni di appoggio per i test della grafica., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla()

### Community 37 - "make_icon.py"
Cohesion: 0.16
Nodes (17): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), main(), Path, Crea un .ico contenente il PNG 256×256 (formato accettato da Windows). (+9 more)

### Community 38 - "build_app.py"
Cohesion: 0.21
Nodes (17): argparse, comando_pyinstaller(), crea_archivio(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 39 - "main"
Cohesion: 0.21
Nodes (13): build_doctor_report(), main(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_avvio_normale_senza_demo(), test_costruzione_diagnostica_con_telefono_e_problemi() (+5 more)

### Community 40 - "cli.py"
Cohesion: 0.15
Nodes (12): ArgumentParser, build_parser(), doctor(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Apre la finestra principale; se la grafica non è disponibile lo spiega con…, Stampa una diagnosi completa dello stato del computer e del collegamento., selftest() (+4 more)

### Community 41 - "open_in_file_manager"
Cohesion: 0.16
Nodes (9): open_in_file_manager(), Apre la cartella nel file manager, senza bloccare la finestra e senza falsi…, test_apertura_cartella_senza_file_manager_mostra_il_percorso(), test_apertura_cartella_usa_il_comando_giusto(), runner(), test_codice_di_uscita_diverso_da_zero_e_un_errore_su_linux(), Su Linux il comando non deve bloccare la finestra., test_apertura_cartella_su_linux_usa_processo_leggero() (+1 more)

### Community 42 - ".ricostruisci_pagine"
Cohesion: 0.22
Nodes (5): Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Ferma il lavoro in corso (l'utente ha cambiato idea o è tornato indietro). Il…, Chiude il programma; se sta copiando chiede conferma e non lascia file a metà., Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio)., Key Decisions

### Community 43 - "widgets.py"
Cohesion: 0.22
Nodes (9): _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), Warnings, azzera(), Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)., app() (+1 more)

### Community 44 - ".run_task"
Cohesion: 0.31
Nodes (5): Any, tick(), Porta avanti un generatore a passi dentro il ciclo della grafica., Esegue il seguito di un task senza che un errore di grafica fermi il programma., Completed

### Community 45 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.22
Nodes (7): Cronologia dei file già copiati, caricata una volta sola., Code Context, Goal, Handoff: FotoFacile — app desktop per copiare foto da Android, Not Yet Done, Resume Instructions, Setup Required

### Community 46 - "test_autocollaudo_riporta_esito_positivo"
Cohesion: 0.25
Nodes (4): Failed Approaches (Don't Repeat These), L'autocollaudo serve a verificare una build impacchettata: deve dire…, test_autocollaudo_riporta_esito_positivo(), update()

### Community 47 - "test_installer_passi.py"
Cohesion: 0.39
Nodes (5): Path, _risposta(), test_installazione_a_passi_annullabile(), test_installazione_a_passi_scarica_ed_estrae(), _zip()

### Community 48 - "pytest"
Cohesion: 0.29
Nodes (5): pytest, subprocess, Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…, Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice., test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema()

### Community 50 - "main"
Cohesion: 1.00
Nodes (4): main(), fallisci(), passo(), scrivi_esito()

## Knowledge Gaps
- **23 isolated node(s):** `run_tests.sh script`, `Goal`, `Not Yet Done`, `Resume Instructions`, `Setup Required` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 305 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `planner.py`, `transfer.py`, `test_adb.py`, `test_installer.py`, `App`, `osutil.py`, `ProcessoEsterno`, `TransferOptions`, `test_ui_app.py`, `AdbAPassi`, `.copia`, `adb_passi.py`, `ScaricatoreAPassi`, `AdbDemoAPassi`, `MediaFile`, `test_robustezza.py`, `open_in_file_manager`, `.run_task`, `test_installer_passi.py`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `planner.py`, `test_adb.py`, `font`, `cli.py`, `DemoAdbBackend`, `.ricostruisci_pagine`, `.run_task`, `Handoff: FotoFacile — app desktop per copiare foto da Android`, `History`, `AdbAPassi`, `ConnectPage`, `test_autocollaudo_riporta_esito_positivo`, `conftest.py`, `adb_passi.py`, `main`, `SelectPage`, `AdbDemoAPassi`, `FotoFacileError`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `AdbAPassi` connect `AdbAPassi` to `planner.py`, `transfer.py`, `App`, `ProcessoEsterno`, `Handoff: FotoFacile — app desktop per copiare foto da Android`, `.copia`, `adb_passi.py`, `FotoFacileError`, `MediaFile`, `test_robustezza.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 8 INFERRED edges - model-reasoned connections that need verification._
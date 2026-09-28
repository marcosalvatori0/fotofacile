# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 65 files · ~54,169 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 1, .command 1, .icns 1)

## Summary
- 1056 nodes · 2565 edges · 43 communities (33 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 178 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83d68fd9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- adb_passi.py
- test_adb.py
- test_widgets.py
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
- test_robustezza.py
- build_app.py
- FotoFacileError
- attendi
- theme.py
- ScaricatoreAPassi
- planner.py
- scrivi_log_avvio
- test_autocollaudo_riporta_esito_positivo
- OptionsPage
- fotofacile/__init__.py
- test_avvio_salta_la_prova_quando_il_contesto_e_grafico
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- cli.py
- SelectPage
- Path
- doctor
- widgets.py
- test_i_comandi_esterni_usano_il_flag_nascosta

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

## Communities (43 total, 10 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.06
Nodes (34): AdbBackend, Elenca i telefoni collegati e il loro stato., Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+26 more)

### Community 1 - "adb_passi.py"
Cohesion: 0.17
Nodes (14): Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, hashlib, json (+6 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (35): CompletedProcess, find_adb(), Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+27 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.11
Nodes (14): Banner, LogPane, PathChooser, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Barra dei passi della procedura guidata, con quello attuale evidenziato., Area di testo scorrevole con il dettaglio di quello che succede., StepIndicator (+6 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_installer.py"
Cohesion: 0.08
Nodes (43): _chiave_sistema(), component_dir(), download_file(), extract_component(), install_component(), installa_a_passi(), is_installed(), _nome_eseguibile() (+35 more)

### Community 6 - "App"
Cohesion: 0.06
Nodes (31): Any, App, tick(), Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma. (+23 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.11
Nodes (29): app_dir(), default_photos_dir(), file_manager_command(), flag_nascosta(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command() (+21 more)

### Community 8 - "ProcessoEsterno"
Cohesion: 0.13
Nodes (18): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica., RisultatoComando (+10 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.05
Nodes (48): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio usata per gli elenchi temporanei., demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., build_scan_command() (+40 more)

### Community 10 - "TransferOptions"
Cohesion: 0.08
Nodes (69): build_plan(), destination_for(), _nome_sicuro(), PlannedFile, Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo. (+61 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.07
Nodes (12): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Senza questo, avviata dal Terminale, la finestra può restare nascosta dietro., Un'area vuota sempre presente confonde: compare al primo messaggio., test_errore_nella_callback_non_ferma_il_programma(), test_i_dettagli_si_mostrano_solo_quando_servono(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_la_finestra_si_mette_davanti(), test_modalita_demo_attivabile_e_disattivabile() (+4 more)

### Community 12 - "test_cli.py"
Cohesion: 0.22
Nodes (11): main(), Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_avvio_avvisa_in_chiaro_se_la_grafica_non_parte(), test_avvio_normale_senza_demo(), test_diagnostica_riporta_tutte_le_voci() (+3 more)

### Community 13 - "ConnectPage"
Cohesion: 0.14
Nodes (8): ConnectPage, aggiorna(), Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Istruzioni per marca, con menù a tendina., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "History"
Cohesion: 0.13
Nodes (15): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo(), test_file_assente_viene_trattato_come_vuoto() (+7 more)

### Community 15 - "test_robustezza.py"
Cohesion: 0.07
Nodes (40): AdbAPassi, Path, Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione. (+32 more)

### Community 16 - "build_app.py"
Cohesion: 0.08
Nodes (34): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+26 more)

### Community 17 - "FotoFacileError"
Cohesion: 0.21
Nodes (10): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), test_task_con_callback_di_errore_personalizzato(), lavoro() (+2 more)

### Community 18 - "attendi"
Cohesion: 0.15
Nodes (20): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Funzioni di appoggio per i test della grafica., Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto() (+12 more)

### Community 19 - "theme.py"
Cohesion: 0.08
Nodes (29): apply_theme(), _canale(), contrasto(), font(), luminanza(), pick_font_family(), Misc, Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.… (+21 more)

### Community 20 - "ScaricatoreAPassi"
Cohesion: 0.14
Nodes (6): Path, Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, test_scaricatore_annullabile(), test_scaricatore_scrive_i_byte_e_riporta_avanzamento(), test_scaricatore_senza_rete_spiega_cosa_controllare()

### Community 21 - "planner.py"
Cohesion: 0.05
Nodes (63): dataclasses, datetime, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Errore durante la copia di un file., TransferError, format_date(), format_duration(), format_eta() (+55 more)

### Community 22 - "scrivi_log_avvio"
Cohesion: 0.25
Nodes (7): avviso_visibile(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., scrivi_log_avvio(), test_avviso_visibile_usa_osascript_su_macos(), test_log_di_avvio_viene_scritto()

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

### Community 37 - "make_icon.py"
Cohesion: 0.16
Nodes (17): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), main(), Path, Crea un .ico contenente il PNG 256×256 (formato accettato da Windows). (+9 more)

### Community 39 - "cli.py"
Cohesion: 0.14
Nodes (14): argparse, ArgumentParser, build_parser(), contesto_grafico_dubbio(), prova_finestra(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, True se non ci sono segnali di una sessione grafica (automazione, servizi,… (+6 more)

### Community 41 - "SelectPage"
Cohesion: 0.24
Nodes (3): Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., SelectPage

### Community 43 - "Path"
Cohesion: 0.26
Nodes (8): _accorcia_cartelle(), _dimensione(), _Esistenza, _limita_percorso(), Path, Riduce il percorso entro il limite sicuro multipiattaforma. Ordine degli…, Dimensione di un file esistente; -1 se nel frattempo è sparito., Verifica rapidamente se un nome è già occupato, con o senza distinzione di…

### Community 44 - "doctor"
Cohesion: 0.25
Nodes (8): build_doctor_report(), doctor(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., Stampa una diagnosi completa dello stato del computer e del collegamento., Completed, Current State, test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_senza_componente()

### Community 45 - "widgets.py"
Cohesion: 0.11
Nodes (23): _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), Warnings, pytest, sys, app() (+15 more)

## Knowledge Gaps
- **27 isolated node(s):** `run_tests.sh script`, `Goal`, `Not Yet Done`, `Key Decisions`, `Resume Instructions` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 359 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `adb_passi.py`, `test_adb.py`, `test_installer.py`, `App`, `test_osutil.py`, `ProcessoEsterno`, `DemoAdbBackend`, `TransferOptions`, `test_ui_app.py`, `test_robustezza.py`, `ScaricatoreAPassi`, `planner.py`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `adb_passi.py`, `test_adb.py`, `test_widgets.py`, `cli.py`, `DemoAdbBackend`, `SelectPage`, `ConnectPage`, `History`, `test_robustezza.py`, `widgets.py`, `FotoFacileError`, `planner.py`, `OptionsPage`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `ProcessoEsterno` connect `ProcessoEsterno` to `adb_passi.py`, `App`, `test_robustezza.py`, `FotoFacileError`, `ScaricatoreAPassi`, `test_i_comandi_esterni_usano_il_flag_nascosta`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 8 INFERRED edges - model-reasoned connections that need verification._
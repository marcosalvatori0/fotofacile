# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- Corpus is ~44,458 words - fits in a single context window. You may not need a graph.

## Summary
- 885 nodes · 2138 edges · 37 communities (31 shown, 6 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 136 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- adb a passi: operazioni
- Interfaccia AdbBackend
- Avvio, CLI e diagnosi
- Finestra e schermata opzioni
- Concetti di design e specifica
- Installazione del componente
- Metodi della finestra App
- Differenze di sistema (osutil)
- Processi esterni a passi
- Telefono demo
- Piano di copia e percorsi
- Test della finestra
- Ricerca dei file sul telefono
- Passo 1: collegamento
- Cronologia dei file copiati
- Telefono vero a passi (AdbAPassi)
- Componenti grafici riusabili
- Copia a blocchi dal telefono
- Aiuto Debug USB e appoggi test
- Errori di copia e nomi sicuri
- Download a blocchi del componente
- Passo 2: scelta delle foto
- Telefono finto a passi
- Errori con messaggio umano
- Collisioni di nomi
- Modelli dati e casi difficili
- Test della ricerca file
- Appoggi per i test grafici
- Test della schermata opzioni
- Test copia reale
- Test del trasferimento (Passo 4)
- Ambito futuro ed esclusioni
- Interfaccia semplice in italiano
- Script di esecuzione test

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 70 edges
2. `TransferOptions` - 46 edges
3. `App` - 42 edges
4. `AdbAPassi` - 41 edges
5. `esegui_fino_alla_fine()` - 41 edges
6. `DemoAdbBackend` - 39 edges
7. `History` - 36 edges
8. `DeviceInfo` - 35 edges
9. `MediaFile` - 33 edges
10. `transfer()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `finestra_condivisa()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/conftest.py → fotofacile/core/demo.py
- `test_avanti_funziona_solo_con_telefono_pronto()` --calls--> `DeviceInfo`  [EXTRACTED]
  tests/test_page_connect.py → fotofacile/core/devices.py
- `test_copia_fallita_rimuove_il_file_parziale()` --uses--> `FotoFacileError`  [INFERRED]
  tests/test_adb_passi.py → fotofacile/core/errors.py
- `test_errore_sui_dispositivi_produce_messaggio_umano()` --uses--> `FotoFacileError`  [INFERRED]
  tests/test_adb_passi.py → fotofacile/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (37 total, 6 thin omitted)

### Community 0 - "adb a passi: operazioni"
Cohesion: 0.06
Nodes (58): Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``. (+50 more)

### Community 1 - "Interfaccia AdbBackend"
Cohesion: 0.07
Nodes (58): AdbBackend, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono., Avvia il collegamento. (+50 more)

### Community 2 - "Avvio, CLI e diagnosi"
Cohesion: 0.05
Nodes (53): ArgumentParser, CompletedProcess, build_doctor_report(), build_parser(), doctor(), main(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Apre la finestra principale; se la grafica non è disponibile lo spiega con… (+45 more)

### Community 3 - "Finestra e schermata opzioni"
Cohesion: 0.06
Nodes (31): Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, OptionsPage, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono., apply_theme(), font(), pick_font_family(), Misc, Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma. (+23 more)

### Community 4 - "Concetti di design e specifica"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "Installazione del componente"
Cohesion: 0.08
Nodes (40): _chiave_sistema(), component_dir(), download_file(), extract_component(), install_component(), installa_a_passi(), is_installed(), _nome_eseguibile() (+32 more)

### Community 6 - "Metodi della finestra App"
Cohesion: 0.08
Nodes (21): Any, App, tick(), Passa al telefono finto: permette di provare tutto senza dispositivo collegato., Torna al telefono vero, se il componente di collegamento è disponibile., Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Cronologia dei file già copiati, caricata una volta sola., Porta avanti un generatore a passi dentro il ciclo della grafica. (+13 more)

### Community 7 - "Differenze di sistema (osutil)"
Cohesion: 0.10
Nodes (28): app_dir(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command(), Unico punto in cui il programma si adatta al sistema operativo. (+20 more)

### Community 8 - "Processi esterni a passi"
Cohesion: 0.12
Nodes (18): ProcessoEsterno, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito., Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica. (+10 more)

### Community 9 - "Telefono demo"
Cohesion: 0.11
Nodes (18): demo_files(), DemoAdbBackend, Telefono finto: serve per i test automatici e per la modalità demo senza…, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., AdbError, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Errore di comunicazione con il telefono: spesso basta riprovare. (+10 more)

### Community 10 - "Piano di copia e percorsi"
Cohesion: 0.16
Nodes (28): build_plan(), destination_for(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo., relative_path(), foto(), FOTO.JPG e foto.jpg sono due foto diverse: non vanno confuse, né sovrascritte. (+20 more)

### Community 11 - "Test della finestra"
Cohesion: 0.08
Nodes (12): azzera(), Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)., app(), fixture, Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., test_errore_nella_callback_non_ferma_il_programma(), test_la_finestra_resta_reattiva_durante_un_task_lungo(), test_modalita_demo_attivabile_e_disattivabile() (+4 more)

### Community 12 - "Ricerca dei file sul telefono"
Cohesion: 0.14
Nodes (22): build_scan_command(), group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Costruisce l'unico comando che elenca i file sul telefono. (+14 more)

### Community 13 - "Passo 1: collegamento"
Cohesion: 0.14
Nodes (8): ConnectPage, aggiorna(), Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Se il componente è guasto o assente, il pulsante di installazione torna attivo., Istruzioni per marca, con menù a tendina., Scarica il componente mancante mostrando l'avanzamento nel registro., Telefono finto: permette di provare tutta la procedura senza dispositivo., Prima schermata: collega il telefono, con aiuto, installazione e prova demo.

### Community 14 - "Cronologia dei file copiati"
Cohesion: 0.13
Nodes (15): default_path(), History, Path, Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., True se quel file, con la stessa dimensione e data, è già stato copiato., test_contenuto_diverso_non_risulta_gia_copiato(), test_cronologie_separate_per_dispositivo() (+7 more)

### Community 15 - "Telefono vero a passi (AdbAPassi)"
Cohesion: 0.23
Nodes (20): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+12 more)

### Community 16 - "Componenti grafici riusabili"
Cohesion: 0.14
Nodes (16): _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), app(), casa_temporanea(), finestra_condivisa(), fixture (+8 more)

### Community 17 - "Copia a blocchi dal telefono"
Cohesion: 0.15
Nodes (6): Path, Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde».

### Community 18 - "Aiuto Debug USB e appoggi test"
Cohesion: 0.18
Nodes (14): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti(), test_avanti_funziona_solo_con_telefono_pronto(), test_modalita_demo_attivabile_dal_passo_1() (+6 more)

### Community 19 - "Errori di copia e nomi sicuri"
Cohesion: 0.16
Nodes (14): Errore durante la copia di un file., TransferError, _dimensione(), ensure_space(), _nome_sicuro(), Costruzione del piano di copia: cosa copiare, dove, e cosa saltare. I nomi dei…, Dimensione di un file esistente; -1 se nel frattempo è sparito., Solleva un errore comprensibile se lo spazio libero non basta. (+6 more)

### Community 20 - "Download a blocchi del componente"
Cohesion: 0.14
Nodes (6): Path, Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, test_scaricatore_annullabile(), test_scaricatore_scrive_i_byte_e_riporta_avanzamento(), test_scaricatore_senza_rete_spiega_cosa_controllare()

### Community 21 - "Passo 2: scelta delle foto"
Cohesion: 0.24
Nodes (3): Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., SelectPage

### Community 22 - "Telefono finto a passi"
Cohesion: 0.19
Nodes (7): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio usata per gli elenchi temporanei., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi()

### Community 23 - "Errori con messaggio umano"
Cohesion: 0.18
Nodes (12): FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file(), copia(), test_processo_non_avviabile_non_lascia_file_temporanei() (+4 more)

### Community 24 - "Collisioni di nomi"
Cohesion: 0.33
Nodes (6): _accorcia_cartelle(), _Esistenza, _limita_percorso(), Path, Riduce il percorso entro il limite sicuro multipiattaforma. Ordine degli…, Verifica rapidamente se un nome è già occupato, con o senza distinzione di…

### Community 25 - "Modelli dati e casi difficili"
Cohesion: 0.23
Nodes (7): PlannedFile, MediaFile, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, test_cronologia_non_leggibile_non_impedisce_l_avvio(), test_cronologia_non_scrivibile_non_perde_le_foto_copiate(), test_errore_di_permesso_non_viene_ritentato(), test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file()

### Community 26 - "Test della ricerca file"
Cohesion: 0.28
Nodes (7): list_media(), Event, Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_list_media_annullata_ritorna_vuoto(), test_list_media_ripiega_su_tutta_la_memoria_se_non_trova_nulla(), test_list_media_usa_il_seriale_richiesto()

### Community 27 - "Appoggi per i test grafici"
Cohesion: 0.36
Nodes (7): Funzioni di appoggio per i test della grafica., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "Test della schermata opzioni"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Test copia reale"
Cohesion: 0.25
Nodes (6): Path, Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_copia_reale_abbandonata_non_lascia_nulla(), test_copia_reale_con_errore_di_disco_non_lascia_part(), test_copia_reale_con_permesso_negato_spiega_come_rimediare()

### Community 30 - "Test del trasferimento (Passo 4)"
Cohesion: 0.60
Nodes (5): _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla()

## Knowledge Gaps
- **19 isolated node(s):** `run_tests.sh script`, `USB Debugging Authorization Setup`, `Demo Mode Without a Phone`, `Doctor Self-Diagnosis Command`, `Safe Copy via .part and Atomic Rename` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 278 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `Errori con messaggio umano` to `adb a passi: operazioni`, `Interfaccia AdbBackend`, `Avvio, CLI e diagnosi`, `Finestra e schermata opzioni`, `Installazione del componente`, `Metodi della finestra App`, `Differenze di sistema (osutil)`, `Processi esterni a passi`, `Telefono demo`, `Test della finestra`, `Telefono vero a passi (AdbAPassi)`, `Copia a blocchi dal telefono`, `Errori di copia e nomi sicuri`, `Download a blocchi del componente`, `Telefono finto a passi`, `Modelli dati e casi difficili`, `Test copia reale`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `App` connect `Metodi della finestra App` to `adb a passi: operazioni`, `Avvio, CLI e diagnosi`, `Finestra e schermata opzioni`, `Telefono demo`, `Passo 1: collegamento`, `Cronologia dei file copiati`, `Telefono vero a passi (AdbAPassi)`, `Componenti grafici riusabili`, `Passo 2: scelta delle foto`, `Telefono finto a passi`, `Errori con messaggio umano`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `AdbAPassi` connect `Telefono vero a passi (AdbAPassi)` to `adb a passi: operazioni`, `Interfaccia AdbBackend`, `Finestra e schermata opzioni`, `Metodi della finestra App`, `Processi esterni a passi`, `Copia a blocchi dal telefono`, `Errori con messaggio umano`, `Modelli dati e casi difficili`, `Test copia reale`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `transfer()` and `transfer_steps()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `App` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`App` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `AdbAPassi` (e.g. with `DeviceInfo` and `FotoFacileError`) actually correct?**
  _`AdbAPassi` has 6 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - FotoFacile  (2026-09-29)

## Corpus Check
- 84 files · ~87,556 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1588 nodes · 3756 edges · 86 communities (72 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04b9463a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- test_robustezza.py
- RealAdbBackend
- test_widgets.py
- Critical Behaviors Contract
- test_installer.py
- App
- test_osutil.py
- FotoFacileError
- DemoAdbBackend
- test_transfer.py
- test_ui_app.py
- test_cli.py
- ConnectPage
- History
- esegui_fino_alla_fine
- build_app.py
- mtp_linux.py
- attendi
- theme.py
- ptp_mac.py
- page_transfer.py
- osutil.py
- planner.py
- TransferOptions
- TrasportoAiutante
- wpd_win.ps1
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- test_installer_passi.py
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- TrasportoDemo
- trasporto_aiutante.py
- pytest
- test_installer_pacchetti.py
- test_regressioni.py
- format_size
- TrasportoWpdWindows
- test_trasporto.py
- test_pacchetto_windows.py
- parse_stat_stream
- transfer_steps
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- MediaFile
- crea_pacchetto
- TransferPage
- destination_for
- cli.py
- TrasportoAdb
- test_adb.py
- TrasportoComposto
- installer.py
- esegui
- TrasportoMtpLinux
- page_connect.py
- Piano di revisione e sviluppo — FotoFacile
- install_component
- extract_component
- start_gui
- shell_quote
- doctor
- test_il_dmg_si_crea_e_contiene_l_app
- download_file_stream
- AdbError
- leggi_elenco
- suggested_destination
- demo_files
- test_errore_di_permesso_non_viene_ritentato
- pacchetto
- contesto_grafico_dubbio
- test_rifiuta_di_cancellare_la_cartella_corrente
- test_rifiuta_di_cancellare_una_cartella_che_contiene_il_progetto
- .__init__
- widgets.py

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 99 edges
2. `esegui_fino_alla_fine()` - 62 edges
3. `MediaFile` - 55 edges
4. `DemoAdbBackend` - 53 edges
5. `DeviceInfo` - 53 edges
6. `TransferOptions` - 49 edges
7. `App` - 47 edges
8. `ProcessoEsterno` - 42 edges
9. `AdbAPassi` - 41 edges
10. `History` - 39 edges

## Surprising Connections (you probably didn't know these)
- `test_montaggio_gvfs_trovato_dal_seriale()` --calls--> `montaggio_da_seriale()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_lettura_dei_montaggi_di_gio()` --calls--> `leggi_dispositivi_gio()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_dispositivi_non_elenca_due_volte_lo_stesso_telefono()` --calls--> `dispositivi()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_il_percorso_del_telefono_non_puo_uscire_dal_montaggio()` --calls--> `percorso_di_filesystem()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (86 total, 8 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.11
Nodes (26): Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, leggi_dispositivi() (+18 more)

### Community 1 - "test_robustezza.py"
Cohesion: 0.14
Nodes (21): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.…, Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.… (+13 more)

### Community 2 - "RealAdbBackend"
Cohesion: 0.16
Nodes (13): CompletedProcess, Implementazione reale dell'interfaccia verso adb., RealAdbBackend, Path, _script_adb(), test_cancellazione_usa_rm_con_seriale_e_percorso_quotato(), test_check_riporta_la_prima_riga_della_versione(), test_devices_raw_riporta_l_output_di_adb() (+5 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.10
Nodes (15): Banner, LogPane, PathChooser, Misc, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Barra dei passi della procedura guidata, con quello attuale evidenziato., Area di testo scorrevole con il dettaglio di quello che succede. (+7 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_installer.py"
Cohesion: 0.30
Nodes (11): download_file(), platform_tools_url(), Scarica un file riportando l'avanzamento. ``validatore`` (facoltativo) riceve…, Indirizzo ufficiale del pacchetto per questo sistema operativo., risposta_finta(), test_download_annullato_non_lascia_file(), test_download_file_scrive_i_byte_giusti(), test_download_riporta_avanzamento() (+3 more)

### Community 6 - "App"
Cohesion: 0.05
Nodes (28): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Passa a un modo di collegamento **non ancora provato**. Tener traccia di quelli… (+20 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.11
Nodes (26): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command() (+18 more)

### Community 8 - "FotoFacileError"
Cohesion: 0.14
Nodes (9): FotoFacileError, Errore con messaggio per l'utente e un suggerimento su come procedere., Prova davvero il componente appena estratto: un file presente non è un file…, _verifica_eseguibile(), Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., Non c'è niente da riavviare: il collegamento diretto non ha un servizio. Si…, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., shutil (+1 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.09
Nodes (19): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., DemoAdbBackend, Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi() (+11 more)

### Community 10 - "test_transfer.py"
Cohesion: 0.28
Nodes (25): Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Path, Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni., test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream() (+17 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.09
Nodes (14): azzera(), Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)., app(), fixture, Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Un'area vuota sempre presente confonde: compare al primo messaggio., test_i_dettagli_si_mostrano_solo_quando_servono(), test_modalita_demo_attivabile_e_disattivabile() (+6 more)

### Community 12 - "test_cli.py"
Cohesion: 0.22
Nodes (15): main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_autocollaudo_riporta_esito_positivo() (+7 more)

### Community 13 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 14 - "History"
Cohesion: 0.10
Nodes (20): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+12 more)

### Community 15 - "esegui_fino_alla_fine"
Cohesion: 0.05
Nodes (58): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., esegui_fino_alla_fine(), ProcessoEsterno, Path, True se il comando è ancora in corso. (+50 more)

### Community 16 - "build_app.py"
Cohesion: 0.14
Nodes (25): argparse, comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main() (+17 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.06
Nodes (67): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+59 more)

### Community 18 - "attendi"
Cohesion: 0.13
Nodes (22): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Funzioni di appoggio per i test della grafica., Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., test_aiuto_contiene_le_marche_e_i_passi() (+14 more)

### Community 19 - "theme.py"
Cohesion: 0.11
Nodes (26): apply_theme(), _canale(), contrasto(), font(), luminanza(), pick_font_family(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux). (+18 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.06
Nodes (52): AiutanteNonDisponibile, apri_sessione(), _apri_telefono(), _Attesa, cammina(), chiudi_sessione(), comando_cancella(), comando_copia() (+44 more)

### Community 21 - "page_transfer.py"
Cohesion: 0.18
Nodes (20): TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato., Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,… (+12 more)

### Community 22 - "osutil.py"
Cohesion: 0.11
Nodes (26): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+18 more)

### Community 23 - "planner.py"
Cohesion: 0.13
Nodes (20): Errore durante la copia di un file., TransferError, _accorcia_cartella(), _accorcia_nome(), _dimensione(), ensure_space(), _Esistenza, _limita_percorso() (+12 more)

### Community 24 - "TransferOptions"
Cohesion: 0.22
Nodes (24): build_plan(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., TransferOptions, foto(), FOTO.JPG e foto.jpg sono due foto diverse: non vanno confuse, né sovrascritte., test_collisione_dimensione_diversa_rinomina(), test_collisione_stessa_dimensione_viene_saltata(), test_dedup_non_attiva_quando_disattivata() (+16 more)

### Community 25 - "TrasportoAiutante"
Cohesion: 0.11
Nodes (13): comando_se_stesso(), Come rilanciare **questo stesso programma** con un'opzione interna. Serve alle…, ambiente_aiutante(), comando_aiutante(), Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile. (+5 more)

### Community 26 - "wpd_win.ps1"
Cohesion: 0.22
Nodes (21): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+13 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.52
Nodes (6): _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "test_installer_passi.py"
Cohesion: 0.39
Nodes (8): installa_a_passi(), Scarica, verifica ed estrae il componente **a piccoli passi**, senza bloccare…, io, Path, _risposta(), test_installazione_a_passi_annullabile(), test_installazione_a_passi_scarica_ed_estrae(), _zip()

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.09
Nodes (14): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+6 more)

### Community 39 - "TrasportoDemo"
Cohesion: 0.12
Nodes (6): setter, Pausa fra un controllo e l'altro (nei test si azzera per non aspettare)., Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 40 - "trasporto_aiutante.py"
Cohesion: 0.10
Nodes (30): _controlla_spazio(), _dimensione_prevista(), _esito_di_copia(), percorso_temporaneo(), Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Nome del file «a metà», unico per processo. Il numero del processo evita che… (+22 more)

### Community 41 - "pytest"
Cohesion: 0.18
Nodes (16): datetime, format_date(), format_duration(), format_eta(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile. (+8 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.12
Nodes (8): re, pacchetto(), fixture, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Anche i frammenti Python incorporati nei .ps1 devono essere compilabili davvero., PowerShell conta all'indietro: per un array di un solo elemento $a[1..0]…, test_gli_snippet_python_dentro_gli_script_powershell_sono_validi(), test_il_controllo_di_python_negli_script_powershell_non_aggiunge_argomenti_fantasma()

### Community 43 - "test_regressioni.py"
Cohesion: 0.08
Nodes (35): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., controlla_archivio(), impronta_file(), Impronta (hash) di un file, calcolata a blocchi: non lo carica mai in memoria., Controlla che il file scaricato sia davvero il pacchetto ufficiale. Due…, Path, Un test per ogni errore realmente trovato e corretto. Ogni test qui descrive un… (+27 more)

### Community 44 - "format_size"
Cohesion: 0.13
Nodes (11): Canvas, format_size(), Dimensione leggibile all'italiana: «3,4 GB»., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa… (+3 more)

### Community 45 - "TrasportoWpdWindows"
Cohesion: 0.14
Nodes (11): Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, Costruisce il collegamento diretto adatto al sistema, se esiste., _trasporto_diretto(), Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, Telefono collegato via cavo su Windows, senza Debug USB., True solo su Windows: l'aiutante è uno script PowerShell di Windows. (+3 more)

### Community 46 - "test_trasporto.py"
Cohesion: 0.08
Nodes (31): main(), parametrize, Path, Verifica del livello «collegamento diretto»: lettura dell'uscita degli…, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs… (+23 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.10
Nodes (11): Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, Il Debug USB non deve mai sembrare un passaggio obbligato: è la richiesta…, test_il_codice_copiato_funziona(), test_il_pacchetto_non_contiene_file_di_sviluppo(), test_il_pacchetto_porta_l_aiutante_per_windows() (+3 more)

### Community 48 - "parse_stat_stream"
Cohesion: 0.13
Nodes (21): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le…, test_cancellazione_di_percorso_inesistente_da_errore() (+13 more)

### Community 49 - "transfer_steps"
Cohesion: 0.50
Nodes (5): Progress, _pubblica(), Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo., transfer_steps()

### Community 50 - "Trasporto"
Cohesion: 0.08
Nodes (14): Protocol, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Il modo migliore disponibile, oppure ``None`` se non ce n'è nessuno., Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata). (+6 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.11
Nodes (18): Code Context, Collegamento senza Debug USB (novità principale), Completed, Copia piatta, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know (+10 more)

### Community 52 - "MediaFile"
Cohesion: 0.14
Nodes (15): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, build_scan_command(), list_media(), MediaFile, Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file() (+7 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.38
Nodes (9): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+1 more)

### Community 54 - "TransferPage"
Cohesion: 0.17
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 55 - "destination_for"
Cohesion: 0.14
Nodes (14): destination_for(), Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.…, relative_path(), test_destinazione_con_e_senza_struttura(), test_nome_lunghissimo_accorciato_mantenendo_estensione(), test_nome_vuoto_o_solo_caratteri_strani(), test_nomi_non_validi_su_windows_vengono_resi_sicuri() (+6 more)

### Community 56 - "cli.py"
Cohesion: 0.12
Nodes (16): ArgumentParser, build_parser(), elenco_modi(), _processo_finestra(), prova_finestra(), prova_finestra_diretta(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Quali modi di collegamento al telefono sono utilizzabili su questo computer. È… (+8 more)

### Community 57 - "TrasportoAdb"
Cohesion: 0.16
Nodes (4): Path, Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 58 - "test_adb.py"
Cohesion: 0.31
Nodes (10): find_adb(), Path, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, test_find_adb_ignora_variabile_inesistente_e_cerca_nel_percorso(), test_find_adb_preferisce_la_variabile_di_ambiente(), test_find_adb_ritorna_none_se_assente(), test_find_adb_su_windows_cerca_adb_exe_nel_profilo(), test_find_adb_su_windows_cerca_nell_sdk_android() (+2 more)

### Community 59 - "TrasportoComposto"
Cohesion: 0.09
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 61 - "installer.py"
Cohesion: 0.24
Nodes (10): catalogo_platform_tools(), _chiave_sistema(), _nome_eseguibile(), Scaricamento e installazione del componente di collegamento (Android platform-…, Indirizzo e impronta del pacchetto: dal catalogo ufficiale, con ripiego su…, Indirizzo *preciso* (con versione) e impronta SHA-1 letti dal catalogo Google.…, risolvi_sorgente(), hashlib (+2 more)

### Community 62 - "esegui"
Cohesion: 0.29
Nodes (7): carica(), esegui(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., esegui_aiutante(), Modalità interna: il programma richiama sé stesso per parlare con il telefono.…

### Community 63 - "TrasportoMtpLinux"
Cohesion: 0.14
Nodes (8): _eseguibile(), Path, Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, Telefono collegato via cavo su Linux, senza Debug USB., True solo su Linux e solo se c'è un modo per montare l'MTP., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 65 - "page_connect.py"
Cohesion: 0.15
Nodes (12): build_help_text_generico(), Passo 1: guidare la persona a collegare il telefono. Questa schermata è la più…, Cosa provare **prima** di pensare al Debug USB., Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Misc, Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, Colora una finestra secondaria come quella principale. Serve a evitare il bordo…, tema_finestra() (+4 more)

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.25
Nodes (7): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Verifica

### Community 67 - "install_component"
Cohesion: 0.25
Nodes (11): component_dir(), install_component(), is_installed(), Path, Dove viene installato il componente: <cartella utente>/.fotofacile/platform-…, Scarica, verifica ed estrae il componente, restituendo il percorso…, _rimuovi(), test_cartella_componente_predefinita_sotto_la_cartella_utente() (+3 more)

### Community 68 - "extract_component"
Cohesion: 0.24
Nodes (10): extract_component(), Estrae il componente (eseguibile e librerie) e lo installa **in modo atomico**.…, Scompatta il pacchetto appiattendo i percorsi (dentro c'è una sola cartella)., _scompatta(), crea_zip(), Path, test_estrazione_da_file_corrotto_produce_errore_umano(), test_estrazione_senza_eseguibile_produce_errore_umano() (+2 more)

### Community 69 - "start_gui"
Cohesion: 0.22
Nodes (10): avviso_visibile(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Apre la finestra principale; se la grafica non è disponibile lo spiega con…, scrivi_log_avvio(), start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico() (+2 more)

### Community 70 - "shell_quote"
Cohesion: 0.25
Nodes (6): Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, shell_quote(), test_shell_quote_gestisce_apostrofi_e_spazi(), test_shell_quote_gestisce_dollaro_backtick_e_virgolette(), test_shell_quote_lascia_intatti_i_percorsi_normali()

### Community 71 - "doctor"
Cohesion: 0.29
Nodes (7): build_doctor_report(), doctor(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., Stampa una diagnosi completa dello stato del computer e del collegamento., test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi(), test_costruzione_diagnostica_senza_componente()

### Community 72 - "test_il_dmg_si_crea_e_contiene_l_app"
Cohesion: 0.22
Nodes (9): skipif, _bat(), Path, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per…, Ogni frammento Python scritto nei .bat deve essere compilabile davvero., Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire., test_gli_snippet_python_dentro_i_bat_sono_validi(), test_il_dmg_si_crea_e_contiene_l_app() (+1 more)

### Community 73 - "download_file_stream"
Cohesion: 0.32
Nodes (7): _chiudi(), download_file_stream(), Path, Scrive un file dal telefono su disco passando da un temporaneo ``.part`` (modo…, _rimuovi(), test_copia_in_sottocartella_inesistente_la_crea(), test_copia_multipla_in_blocchi_da_dimensioni_diverse()

### Community 74 - "AdbError"
Cohesion: 0.29
Nodes (5): Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., AdbError, Errore di comunicazione con il telefono: spesso basta riprovare., test_comando_fallito_produce_errore_umano(), test_errore_espone_messaggio_e_suggerimento()

### Community 75 - "leggi_elenco"
Cohesion: 0.29
Nodes (7): genere_per_estensione(), leggi_elenco(), Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., test_genere_per_estensione_copre_tutte_le_estensioni_anche_maiuscole(), test_leggi_elenco_coercizza_i_numeri_e_azzera_quelli_rotti(), test_leggi_elenco_legge_le_righe_buone_e_ignora_le_rotte()

### Community 76 - "suggested_destination"
Cohesion: 0.33
Nodes (6): _nome_sicuro(), Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Rende un nome di file accettabile su Windows, macOS e Linux., suggested_destination(), test_destinazione_suggerita_ripulisce_il_modello(), test_destinazione_suggerita_usa_modello_e_data()

### Community 77 - "demo_files"
Cohesion: 0.50
Nodes (3): demo_files(), Albero di esempio deterministico con foto e video realistici., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili()

### Community 81 - "contesto_grafico_dubbio"
Cohesion: 0.67
Nodes (3): contesto_grafico_dubbio(), True se non ci sono segnali di una sessione grafica (automazione, servizi,…, test_contesto_grafico_dubbio_quando_mancano_i_segnali()

### Community 85 - "widgets.py"
Cohesion: 0.13
Nodes (17): _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available(), sys, app(), casa_temporanea(), finestra_condivisa() (+9 more)

## Knowledge Gaps
- **43 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 579 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `test_robustezza.py`, `test_installer.py`, `App`, `test_osutil.py`, `DemoAdbBackend`, `test_transfer.py`, `test_ui_app.py`, `esegui_fino_alla_fine`, `page_transfer.py`, `osutil.py`, `planner.py`, `TrasportoAiutante`, `test_installer_passi.py`, `trasporto_aiutante.py`, `test_regressioni.py`, `TrasportoWpdWindows`, `test_trasporto.py`, `transfer_steps`, `Trasporto`, `test_adb.py`, `TrasportoComposto`, `installer.py`, `extract_component`, `download_file_stream`, `AdbError`, `test_errore_di_permesso_non_viene_ritentato`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `test_robustezza.py`, `test_widgets.py`, `start_gui`, `TrasportoDemo`, `test_regressioni.py`, `format_size`, `ConnectPage`, `History`, `esegui_fino_alla_fine`, `Trasporto`, `widgets.py`, `TransferPage`, `cli.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `MediaFile` connect `MediaFile` to `test_robustezza.py`, `DemoAdbBackend`, `test_transfer.py`, `esegui_fino_alla_fine`, `page_transfer.py`, `osutil.py`, `planner.py`, `TransferOptions`, `TrasportoAiutante`, `TrasportoDemo`, `trasporto_aiutante.py`, `test_regressioni.py`, `format_size`, `test_trasporto.py`, `parse_stat_stream`, `Trasporto`, `TrasportoAdb`, `TrasportoComposto`, `TrasportoMtpLinux`, `leggi_elenco`, `test_errore_di_permesso_non_viene_ritentato`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `DemoAdbBackend` (e.g. with `AdbDemoAPassi` and `AdbError`) actually correct?**
  _`DemoAdbBackend` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
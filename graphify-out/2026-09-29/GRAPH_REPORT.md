# Graph Report - FotoFacile  (2026-09-28)

## Corpus Check
- 84 files · ~87,137 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1579 nodes · 3747 edges · 86 communities (72 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04b9463a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- test_robustezza.py
- test_adb.py
- widgets.py
- Critical Behaviors Contract
- installer.py
- App
- test_osutil.py
- FotoFacileError
- DemoAdbBackend
- MediaFile
- test_ui_app.py
- test_cli.py
- ConnectPage
- History
- esegui_fino_alla_fine
- build_app.py
- mtp_linux.py
- test_page_connect.py
- tk_available
- ptp_mac.py
- TransferPlan
- wpd_win.py
- script
- OptionsPage
- TrasportoAiutante
- wpd_win.ps1
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- test_installazione_a_passi_annullabile
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- TrasportoDemo
- .copia
- format.py
- test_installer_pacchetti.py
- test_regressioni.py
- format_size
- TrasportoWpdWindows
- test_trasporto.py
- test_pacchetto_windows.py
- crea_installer_mac.py
- page_transfer.py
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_scanner.py
- crea_pacchetto
- TransferPage
- theme.py
- cli.py
- trasporto.py
- ProcessoEsterno
- TrasportoComposto
- .aspetta
- esegui
- TrasportoMtpLinux
- tema_testo
- Piano di revisione e sviluppo — FotoFacile
- font
- attendi
- start_gui
- page_options.py
- doctor
- test_il_dmg_si_crea_e_contiene_l_app
- .__init__
- ._costruisci_pagine
- ._esegui_callback
- ._usa_adb
- test_wpd_passa_la_destinazione_all_aiutante
- TrasportoPtpMac
- .annulla_task
- contesto_grafico_dubbio
- .remote
- .pulisci
- .riavvia
- test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema

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
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_montaggio_gvfs_trovato_dal_seriale()` --calls--> `montaggio_da_seriale()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_lettura_dei_montaggi_di_gio()` --calls--> `leggi_dispositivi_gio()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_dispositivi_non_elenca_due_volte_lo_stesso_telefono()` --calls--> `dispositivi()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_il_percorso_del_telefono_non_puo_uscire_dal_montaggio()` --calls--> `percorso_di_filesystem()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (86 total, 8 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.14
Nodes (20): Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_dispositivo_non_autorizzato_non_pronto() (+12 more)

### Community 1 - "test_robustezza.py"
Cohesion: 0.12
Nodes (30): dataclasses, _esito_di_copia(), Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Controlla che il comando di copia sia finito bene, spiegando il motivo se no., Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato… (+22 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (35): find_adb(), Cancella un file dal telefono (solo dopo che la copia è stata verificata)., CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb. (+27 more)

### Community 3 - "widgets.py"
Cohesion: 0.17
Nodes (9): Banner, LogPane, _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Area di testo scorrevole con il dettaglio di quello che succede., test_banner_accetta_tutti_i_toni(), test_banner_mostra_messaggio_e_suggerimento() (+1 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "installer.py"
Cohesion: 0.07
Nodes (57): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), extract_component(), impronta_file(), install_component() (+49 more)

### Community 6 - "App"
Cohesion: 0.16
Nodes (7): App, Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, True quando **nessun** modo di collegarsi è disponibile. Con il collegamento…, Contenitore della procedura guidata: crea le pagine e coordina il lavoro., Compatibilità: con il lavoro a passi non c'è nessuna coda da svuotare., Chiude il programma; se sta copiando chiede conferma e non lascia file a metà., Rimuove i file temporanei di lavoro (elenchi di ricerca, file di appoggio).

### Community 7 - "test_osutil.py"
Cohesion: 0.09
Nodes (32): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command() (+24 more)

### Community 8 - "FotoFacileError"
Cohesion: 0.13
Nodes (14): FotoFacileError, Exception, Errore con messaggio per l'utente e un suggerimento su come procedere., Path, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, test_scaricatore_annullabile() (+6 more)

### Community 9 - "DemoAdbBackend"
Cohesion: 0.06
Nodes (43): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., demo_files(), DemoAdbBackend, Telefono finto: serve per i test automatici e per la modalità demo senza…, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno. (+35 more)

### Community 10 - "MediaFile"
Cohesion: 0.05
Nodes (96): Errore durante la copia di un file., TransferError, _accorcia_cartella(), _accorcia_nome(), build_plan(), destination_for(), _dimensione(), ensure_space() (+88 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.11
Nodes (9): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., Senza questo, avviata dal Terminale, la finestra può restare nascosta dietro., Un'area vuota sempre presente confonde: compare al primo messaggio., test_i_dettagli_si_mostrano_solo_quando_servono(), test_la_finestra_si_mette_davanti(), test_task_con_errore_imprevisto_non_chiude_il_programma(), test_task_con_errore_mostra_il_messaggio_umano(), test_un_task_abbandonato_chiude_il_generatore() (+1 more)

### Community 12 - "test_cli.py"
Cohesion: 0.22
Nodes (15): main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_autocollaudo_riporta_esito_positivo() (+7 more)

### Community 13 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 14 - "History"
Cohesion: 0.06
Nodes (32): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+24 more)

### Community 15 - "esegui_fino_alla_fine"
Cohesion: 0.19
Nodes (24): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato(), test_cerca_media_legge_l_output_anche_se_e_lungo() (+16 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.06
Nodes (71): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+63 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.12
Nodes (16): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_aiuto_contiene_le_marche_e_i_passi(), test_aiuto_per_marca_sconosciuta_non_lascia_vuoti() (+8 more)

### Community 19 - "tk_available"
Cohesion: 0.16
Nodes (18): apply_theme(), pick_font_family(), Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available() (+10 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.06
Nodes (52): AiutanteNonDisponibile, apri_sessione(), _apri_telefono(), _Attesa, cammina(), chiudi_sessione(), comando_cancella(), comando_copia() (+44 more)

### Community 21 - "TransferPlan"
Cohesion: 0.19
Nodes (19): TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato., Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,… (+11 more)

### Community 22 - "wpd_win.py"
Cohesion: 0.27
Nodes (10): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+2 more)

### Community 23 - "script"
Cohesion: 0.19
Nodes (10): Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., script(), test_copia_annullata_rimuove_il_file_a_meta(), test_copia_fallita_rimuove_il_file_a_meta(), test_copia_riporta_l_avanzamento_intermedio(), test_copia_scrive_i_byte_e_rinomina_solo_alla_fine(), test_wpd_cancella_traduce_il_rifiuto_in_un_suggerimento() (+2 more)

### Community 24 - "OptionsPage"
Cohesion: 0.35
Nodes (3): OptionsPage, Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 25 - "TrasportoAiutante"
Cohesion: 0.11
Nodes (14): ambiente_aiutante(), _dimensione(), Path, _rallenta_scrittura(), Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile. (+6 more)

### Community 26 - "wpd_win.ps1"
Cohesion: 0.22
Nodes (21): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+13 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.36
Nodes (7): Funzioni di appoggio per i test della grafica., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "test_installazione_a_passi_annullabile"
Cohesion: 0.50
Nodes (5): Path, _risposta(), test_installazione_a_passi_annullabile(), test_installazione_a_passi_scarica_ed_estrae(), _zip()

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.08
Nodes (18): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+10 more)

### Community 39 - "TrasportoDemo"
Cohesion: 0.20
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., test_riavvio_ricontrolla_i_collegamenti_disponibili()

### Community 40 - ".copia"
Cohesion: 0.12
Nodes (18): _controlla_spazio(), _dimensione_prevista(), percorso_temporaneo(), Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Nome del file «a metà», unico per processo. Il numero del processo evita che…, Quanti byte serviranno, se si sa: serve a non chiedere spazio a caso. (+10 more)

### Community 41 - "format.py"
Cohesion: 0.16
Nodes (17): datetime, format_date(), format_duration(), format_eta(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile. (+9 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.12
Nodes (8): re, pacchetto(), fixture, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Anche i frammenti Python incorporati nei .ps1 devono essere compilabili davvero., PowerShell conta all'indietro: per un array di un solo elemento $a[1..0]…, test_gli_snippet_python_dentro_gli_script_powershell_sono_validi(), test_il_controllo_di_python_negli_script_powershell_non_aggiunge_argomenti_fantasma()

### Community 43 - "test_regressioni.py"
Cohesion: 0.09
Nodes (27): comando_se_stesso(), Come rilanciare **questo stesso programma** con un'opzione interna. Serve alle…, comando_aiutante(), Come rilanciare **questo stesso programma** in modalità aiutante. Funziona sia…, Path, Un test per ogni errore realmente trovato e corretto. Ogni test qui descrive un…, Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: due copie avviate insieme nella stessa cartella scrivevano nello stesso… (+19 more)

### Community 44 - "format_size"
Cohesion: 0.17
Nodes (7): format_size(), Dimensione leggibile all'italiana: «3,4 GB»., Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa…, SelectPage

### Community 45 - "TrasportoWpdWindows"
Cohesion: 0.29
Nodes (5): Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, Telefono collegato via cavo su Windows, senza Debug USB., True solo su Windows: l'aiutante è uno script PowerShell di Windows., TrasportoWpdWindows, test_il_collegamento_windows_non_e_disponibile_fuori_da_windows()

### Community 46 - "test_trasporto.py"
Cohesion: 0.11
Nodes (21): genere_per_estensione(), leggi_dispositivi(), leggi_elenco(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., parametrize, Verifica del livello «collegamento diretto»: lettura dell'uscita degli… (+13 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.10
Nodes (11): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, «python3 scripts/crea_pacchetto_windows.py .» non deve svuotare la cartella…, Una cartella padre del repository non va mai cancellata (qui il repository è…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, test_il_codice_copiato_funziona() (+3 more)

### Community 48 - "crea_installer_mac.py"
Cohesion: 0.31
Nodes (8): argparse, crea_dmg(), _esegui(), main(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, versione()

### Community 49 - "page_transfer.py"
Cohesion: 0.38
Nodes (6): Progress, _pubblica(), Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo., transfer_steps(), Passo 4: copia con avanzamento, interruzione e resoconto finale.

### Community 50 - "Trasporto"
Cohesion: 0.11
Nodes (10): Protocol, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata)., Prova a far ripartire il collegamento (usato dal pulsante «Riavvia… (+2 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.14
Nodes (13): Code Context, Completed, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know, Goal, Handoff: FotoFacile — app desktop per copiare foto da Android (+5 more)

### Community 52 - "test_scanner.py"
Cohesion: 0.06
Nodes (28): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, build_scan_command(), group_folders(), _label(), list_media(), MediaFolder, Event, Costruisce l'unico comando che elenca i file sul telefono. (+20 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.29
Nodes (11): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+3 more)

### Community 54 - "TransferPage"
Cohesion: 0.17
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 55 - "theme.py"
Cohesion: 0.18
Nodes (12): Canvas, _canale(), contrasto(), luminanza(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Colora una superficie di disegno, allineandola al pannello., Luminanza relativa di un colore «#rrggbb» (formula WCAG)., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono). (+4 more)

### Community 56 - "cli.py"
Cohesion: 0.13
Nodes (14): ArgumentParser, build_parser(), _processo_finestra(), prova_finestra(), prova_finestra_diretta(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.… (+6 more)

### Community 57 - "trasporto.py"
Cohesion: 0.18
Nodes (13): chiave_sistema(), is_windows(), True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., Nome del sistema normalizzato a «win32» / «darwin» / «linux»., _system(), Collegamento diretto su macOS: PTP/MTP tramite ImageCaptureCore. macOS non ha…, Come FotoFacile parla con il telefono. Il programma non usa **un solo** metodo…, Elenco dei collegamenti utilizzabili su questo computer, dal più comodo al… (+5 more)

### Community 58 - "ProcessoEsterno"
Cohesion: 0.22
Nodes (14): ProcessoEsterno, Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Un comando esterno (per esempio adb) seguito senza bloccare la grafica., Path, script(), test_comando_inesistente_produce_errore_umano(), test_output_grande_va_su_file_per_non_intasare_il_collegamento(), test_processo_breve_riporta_output_e_codice() (+6 more)

### Community 59 - "TrasportoComposto"
Cohesion: 0.10
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 61 - ".aspetta"
Cohesion: 0.14
Nodes (7): True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., RisultatoComando, main()

### Community 62 - "esegui"
Cohesion: 0.20
Nodes (10): carica(), esegui(), modulo_disponibile(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., esegui_aiutante() (+2 more)

### Community 63 - "TrasportoMtpLinux"
Cohesion: 0.14
Nodes (8): _eseguibile(), Path, Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, Telefono collegato via cavo su Linux, senza Debug USB., True solo su Linux e solo se c'è un modo per montare l'MTP., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 65 - "tema_testo"
Cohesion: 0.25
Nodes (7): Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Misc, Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, Colora una finestra secondaria come quella principale. Serve a evitare il bordo…, tema_finestra(), tema_testo(), Text

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.25
Nodes (7): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Verifica

### Community 67 - "font"
Cohesion: 0.27
Nodes (7): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_font_restituisce_tupla_usabile_da_tkinter(), test_indicatore_passi()

### Community 68 - "attendi"
Cohesion: 0.35
Nodes (10): attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla(), test_modalita_demo_attivabile_e_disattivabile() (+2 more)

### Community 69 - "start_gui"
Cohesion: 0.22
Nodes (10): avviso_visibile(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Apre la finestra principale; se la grafica non è disponibile lo spiega con…, scrivi_log_avvio(), start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico() (+2 more)

### Community 70 - "page_options.py"
Cohesion: 0.22
Nodes (6): Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., PathChooser, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., shutil, test_scelta_cartella_aggiorna_il_valore(), test_scelta_cartella_senza_callback()

### Community 71 - "doctor"
Cohesion: 0.22
Nodes (9): build_doctor_report(), doctor(), elenco_modi(), Quali modi di collegamento al telefono sono utilizzabili su questo computer. È…, Testo della diagnosi: serve al supporto per capire cosa non va su un computer., Stampa una diagnosi completa dello stato del computer e del collegamento., test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi() (+1 more)

### Community 72 - "test_il_dmg_si_crea_e_contiene_l_app"
Cohesion: 0.22
Nodes (9): skipif, _bat(), Path, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per…, Ogni frammento Python scritto nei .bat deve essere compilabile davvero., Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire., test_gli_snippet_python_dentro_i_bat_sono_validi(), test_il_dmg_si_crea_e_contiene_l_app() (+1 more)

### Community 73 - ".__init__"
Cohesion: 0.33
Nodes (3): Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Usa un backend in memoria (test) o il telefono demo., Passa al telefono finto: permette di provare tutto senza dispositivo collegato.

### Community 74 - "._costruisci_pagine"
Cohesion: 0.29
Nodes (3): Ricrea le schermate da zero: si riparte puliti, senza riaprire il programma., Registra una pagina dentro il contenitore centrale (non sulla finestra)., Frame

### Community 75 - "._esegui_callback"
Cohesion: 0.33
Nodes (3): Any, Porta avanti un generatore a passi dentro il ciclo della grafica., Esegue il seguito di un task senza che un errore di grafica fermi il programma.

### Community 76 - "._usa_adb"
Cohesion: 0.33
Nodes (3): Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Torna al telefono vero, se su questo computer è possibile.

### Community 77 - "test_wpd_passa_la_destinazione_all_aiutante"
Cohesion: 0.33
Nodes (6): Path, CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, test_le_cartelle_di_appoggio_jmtpfs_sono_riconosciute_nostre(), test_wpd_passa_la_destinazione_all_aiutante(), test_wpd_win_aggiunge_solo_foto_solo_quando_serve(), test_wpd_win_costruisce_il_comando_per_powershell()

### Community 78 - "TrasportoPtpMac"
Cohesion: 0.40
Nodes (4): Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, test_il_collegamento_macos_non_e_disponibile_fuori_da_macos()

### Community 81 - "contesto_grafico_dubbio"
Cohesion: 0.67
Nodes (3): contesto_grafico_dubbio(), True se non ci sono segnali di una sessione grafica (automazione, servizi,…, test_contesto_grafico_dubbio_quando_mancano_i_segnali()

## Knowledge Gaps
- **39 isolated node(s):** `run_tests.sh script`, `Goal`, `Completed`, `Not Yet Done`, `Failed Approaches (Don't Repeat These)` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 573 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `test_robustezza.py`, `test_adb.py`, `installer.py`, `test_osutil.py`, `DemoAdbBackend`, `MediaFile`, `test_ui_app.py`, `esegui_fino_alla_fine`, `TransferPlan`, `script`, `TrasportoAiutante`, `test_installazione_a_passi_annullabile`, `AdbBackend`, `.copia`, `test_regressioni.py`, `TrasportoWpdWindows`, `test_trasporto.py`, `page_transfer.py`, `Trasporto`, `trasporto.py`, `ProcessoEsterno`, `TrasportoComposto`, `.aspetta`, `attendi`, `page_options.py`, `._esegui_callback`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `test_robustezza.py`, `widgets.py`, `ConnectPage`, `History`, `tk_available`, `OptionsPage`, `test_regressioni.py`, `format_size`, `Trasporto`, `TransferPage`, `cli.py`, `.aspetta`, `font`, `start_gui`, `.__init__`, `._costruisci_pagine`, `._esegui_callback`, `._usa_adb`, `.annulla_task`, `.remote`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `MediaFile` connect `MediaFile` to `test_robustezza.py`, `TrasportoDemo`, `.copia`, `DemoAdbBackend`, `format.py`, `test_regressioni.py`, `format_size`, `test_trasporto.py`, `esegui_fino_alla_fine`, `Trasporto`, `test_scanner.py`, `TransferPlan`, `trasporto.py`, `TrasportoComposto`, `TrasportoAiutante`, `TrasportoMtpLinux`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `DemoAdbBackend` (e.g. with `AdbDemoAPassi` and `AdbError`) actually correct?**
  _`DemoAdbBackend` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
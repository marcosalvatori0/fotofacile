# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 90 files · ~127,877 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1905 nodes · 4447 edges · 105 communities (89 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f0a6e56`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parse_devices
- TransferOptions
- test_trasporto.py
- test_widgets.py
- Critical Behaviors Contract
- transfer.py
- App
- test_osutil.py
- ConnectPage
- test_cli.py
- MediaFile
- test_ui_app.py
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- test_scanner.py
- History
- ProcessoEsterno
- build_app.py
- mtp_linux.py
- attendi
- tk_available
- ptp_mac.py
- TransferPlan
- DemoAdbBackend
- _Esistenza
- transfer
- TrasportoMtpLinux
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
- app.py
- esegui_fino_alla_fine
- format_size
- test_installer_pacchetti.py
- flag_nascosta
- _VocePtpFinta
- test_installer.py
- installer.py
- test_pacchetto_windows.py
- TrasportoDemo
- test_conversione.py
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- leggi_elenco
- crea_pacchetto
- TrasportoAiutante
- TransferPage
- comando_se_stesso
- Path
- pathlib
- scanner.py
- FotoFacileError
- TrasportoAdb
- conftest.py
- SelectPage
- Piano di revisione e sviluppo — FotoFacile
- _copia_con_opzioni
- RealAdbBackend
- trasporto_aiutante.py
- _bat
- esegui
- scrivi_log_avvio
- _RispostaLenta
- OptionsPage
- TrasportoComposto
- destination_for
- test_regressioni.py
- AdbDemoAPassi
- planner.py
- DeviceInfo
- main
- _TelefonoFinto
- test_adb.py
- avviso_visibile
- doctor
- Revisione v0.2 — audit per gruppi (Task A7)
- crea_dmg
- setter
- build_doctor_report
- shell_quote
- font
- script
- osutil.py
- codifica_di_windows
- AdbError
- ._run
- build_help_text_generico
- __main__.py
- .disponibile
- _TelefonoCheControllaLeCancellazioni
- build_parser
- test_percorso_lunghissimo_non_esce_mai_dalla_cartella_scelta
- .__init__

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 115 edges
2. `esegui_fino_alla_fine()` - 73 edges
3. `TransferOptions` - 66 edges
4. `MediaFile` - 65 edges
5. `DeviceInfo` - 57 edges
6. `DemoAdbBackend` - 55 edges
7. `build_plan()` - 51 edges
8. `App` - 47 edges
9. `ProcessoEsterno` - 45 edges
10. `AdbAPassi` - 43 edges

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

## Communities (105 total, 10 thin omitted)

### Community 0 - "parse_devices"
Cohesion: 0.18
Nodes (16): get_devices(), parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_dispositivo_non_autorizzato_non_pronto(), test_get_devices_usa_il_backend(), test_lista_con_righe_spurie_e_due_dispositivi() (+8 more)

### Community 1 - "TransferOptions"
Cohesion: 0.16
Nodes (35): Errore durante la copia di un file., TransferError, build_plan(), ensure_space(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Solleva un errore comprensibile se lo spazio libero non basta. ``free_bytes`` a…, TransferOptions, foto() (+27 more)

### Community 2 - "test_trasporto.py"
Cohesion: 0.08
Nodes (29): Path, Verifica del livello «collegamento diretto»: lettura dell'uscita degli…, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs…, jmtpfs monta sempre il primo telefono: con due collegati, proseguire vorrebbe…, L'aiutante deve poter uccidere PowerShell e spiegare l'errore prima che il… (+21 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.13
Nodes (11): Banner, LogPane, PathChooser, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Area di testo scorrevole con il dettaglio di quello che succede., test_banner_accetta_tutti_i_toni(), test_banner_mostra_messaggio_e_suggerimento() (+3 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "transfer.py"
Cohesion: 0.15
Nodes (20): _applica_data(), _chiudi(), download_file_stream(), _passi_di_copia(), Progress, _pubblica(), Path, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.… (+12 more)

### Community 6 - "App"
Cohesion: 0.07
Nodes (21): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Passa a un modo di collegamento **non ancora provato**. Tener traccia di quelli… (+13 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.12
Nodes (24): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), open_in_file_manager(), Path, Cartella che contiene il pacchetto: serve a far ritrovare i moduli al processo…, Su Windows dichiara che il programma gestisce da sé la scala dello schermo.… (+16 more)

### Community 8 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 9 - "test_cli.py"
Cohesion: 0.16
Nodes (20): main(), prova_finestra_diretta(), Apre e chiude una finestra vuota: è il corpo di ``--prova-finestra``., L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo() (+12 more)

### Community 10 - "MediaFile"
Cohesion: 0.18
Nodes (6): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, MediaFile, Prima: sotto i 16 MB liberi il programma si rifiutava di copiare **qualsiasi**…, test_una_foto_piccola_si_copia_anche_con_poco_spazio(), test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file(), test_mediafile_ha_nome_e_cartella()

### Community 11 - "test_ui_app.py"
Cohesion: 0.10
Nodes (13): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., La pagina «Scegli le foto» accoglie solo con un telefono collegato (altrimenti…, Un'area vuota sempre presente confonde: compare al primo messaggio., _telefono_demo(), test_i_dettagli_si_mostrano_solo_quando_servono(), test_modalita_demo_attivabile_e_disattivabile(), test_navigazione_avanti_indietro(), test_task_con_callback_di_errore_personalizzato() (+5 more)

### Community 12 - "PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)"
Cohesion: 0.05
Nodes (41): Auto-revisione del piano, Cosa abbiamo trovato leggendo il codice (base del piano), FotoFacile v0.2 — Piano di implementazione, Global Constraints, PARTE 0 — Punto di partenza, PARTE A — Revisione completa e correzione dei difetti, PARTE B — Il problema del WebP, PARTE C — Interfaccia semplice e leggibile (anche per gli anziani) (+33 more)

### Community 13 - "test_scanner.py"
Cohesion: 0.22
Nodes (11): build_scan_command(), list_media(), Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_comando_scansione_con_video_e_profondita(), test_comando_scansione_quota_percorsi_e_filtra_estensioni() (+3 more)

### Community 14 - "History"
Cohesion: 0.10
Nodes (21): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+13 more)

### Community 15 - "ProcessoEsterno"
Cohesion: 0.09
Nodes (25): ProcessoEsterno, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta. (+17 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.06
Nodes (67): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+59 more)

### Community 18 - "attendi"
Cohesion: 0.13
Nodes (21): build_help_text(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., attendi(), Funzioni di appoggio per i test della grafica., Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_aiuto_contiene_le_marche_e_i_passi() (+13 more)

### Community 19 - "tk_available"
Cohesion: 0.13
Nodes (21): apply_theme(), pick_font_family(), Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), True se questa macchina riesce davvero ad aprire una finestra. La verifica…, tk_available() (+13 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.06
Nodes (56): AiutanteNonDisponibile, apri_sessione(), _apri_telefono(), _Attesa, cammina(), chiudi_sessione(), comando_cancella(), comando_copia() (+48 more)

### Community 21 - "TransferPlan"
Cohesion: 0.22
Nodes (16): TransferPlan, build_report(), _cartelle_di_riserva(), Path, Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,…, save_report() (+8 more)

### Community 22 - "DemoAdbBackend"
Cohesion: 0.14
Nodes (16): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_backend_demo_si_presenta_come_dispositivo_pronto(), test_cancellazione_di_percorso_inesistente_da_errore(), test_cancellazione_rimuove_il_file() (+8 more)

### Community 23 - "_Esistenza"
Cohesion: 0.23
Nodes (8): _Esistenza, Path, Verifica rapidamente se un nome è già occupato, con o senza distinzione di…, Trova un nome non ancora occupato aggiungendo « (1)», « (2)»…, Come ``nome_libero``, ma il nome vale solo se **tutte** le varianti sono…, Il primo nome, dal contatore ``partenza``, per cui ogni variante è libera. Il…, Senza questo, avviata dal Terminale, la finestra può restare nascosta dietro., test_la_finestra_si_mette_davanti()

### Community 24 - "transfer"
Cohesion: 0.25
Nodes (27): Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Path, Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni., test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream() (+19 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.20
Nodes (5): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.52
Nodes (6): _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.27
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "test_installer_passi.py"
Cohesion: 0.12
Nodes (21): Telefono finto: serve per i test automatici e per la modalità demo senza…, installa_a_passi(), Scarica, verifica ed estrae il componente **a piccoli passi**, senza bloccare…, Passo 1: guidare la persona a collegare il telefono. Questa schermata è la più…, hashlib, io, Path, _risposta() (+13 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.09
Nodes (14): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+6 more)

### Community 39 - "app.py"
Cohesion: 0.10
Nodes (21): Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., _canale(), contrasto(), luminanza(), Misc, Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.… (+13 more)

### Community 40 - "esegui_fino_alla_fine"
Cohesion: 0.12
Nodes (34): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., pytest, Path (+26 more)

### Community 41 - "format_size"
Cohesion: 0.17
Nodes (19): datetime, format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date. (+11 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.12
Nodes (8): re, pacchetto(), fixture, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Anche i frammenti Python incorporati nei .ps1 devono essere compilabili davvero., PowerShell conta all'indietro: per un array di un solo elemento $a[1..0]…, test_gli_snippet_python_dentro_gli_script_powershell_sono_validi(), test_il_controllo_di_python_negli_script_powershell_non_aggiunge_argomenti_fantasma()

### Community 43 - "flag_nascosta"
Cohesion: 0.19
Nodes (14): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+6 more)

### Community 44 - "_VocePtpFinta"
Cohesion: 0.17
Nodes (8): _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive(), test_d18_una_voce_ripetuta_si_elenca_una_volta_sola(), _VocePtpFinta

### Community 45 - "test_installer.py"
Cohesion: 0.14
Nodes (26): component_dir(), download_file(), extract_component(), is_installed(), platform_tools_url(), Dove viene installato il componente: <cartella utente>/.fotofacile/platform-…, Estrae il componente (eseguibile e librerie) e lo installa **in modo atomico**.…, Scarica un file riportando l'avanzamento. ``validatore`` (facoltativo) riceve… (+18 more)

### Community 46 - "installer.py"
Cohesion: 0.15
Nodes (23): catalogo_platform_tools(), _chiave_sistema(), controlla_archivio(), _estrai_e_sostituisci(), impronta_file(), install_component(), _nome_eseguibile(), Path (+15 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.09
Nodes (13): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, Una cartella padre del repository non va mai cancellata (qui il repository è…, Il Debug USB non deve mai sembrare un passaggio obbligato: è la richiesta… (+5 more)

### Community 48 - "TrasportoDemo"
Cohesion: 0.18
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 49 - "test_conversione.py"
Cohesion: 0.09
Nodes (43): converti_webp(), e_webp(), _libero(), pillow_disponibile(), Path, Conversione delle immagini WebP in JPG (o PNG se hanno trasparenza). Il WebP…, True se Pillow c'è e sa leggere il WebP., True se il **contenuto** del file è WebP, qualunque sia il nome. (+35 more)

### Community 50 - "Trasporto"
Cohesion: 0.09
Nodes (12): Protocol, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata)., Prova a far ripartire il collegamento (usato dal pulsante «Riavvia… (+4 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.11
Nodes (18): Code Context, Collegamento senza Debug USB (novità principale), Completed, Copia piatta, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know (+10 more)

### Community 52 - "leggi_elenco"
Cohesion: 0.15
Nodes (13): main(), genere_per_estensione(), leggi_elenco(), Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., Gli aiutanti Python scrivono JSON solo ASCII: la lettura in UTF-8 non dipende…, test_d16_gli_aiutanti_scrivono_righe_leggibili_con_ogni_codifica(), Audit G3: un a-capo (o un separatore Unicode che `splitlines` taglierebbe) nel… (+5 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.23
Nodes (13): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+5 more)

### Community 54 - "TrasportoAiutante"
Cohesion: 0.14
Nodes (10): ambiente_aiutante(), Path, True se su questo computer l'aiutante può funzionare., Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile., Variabili d'ambiente per il processo figlio. Dal sorgente serve ``PYTHONPATH``:… (+2 more)

### Community 55 - "TransferPage"
Cohesion: 0.19
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 56 - "comando_se_stesso"
Cohesion: 0.29
Nodes (7): _processo_finestra(), prova_finestra(), Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.…, comando_se_stesso(), Come rilanciare **questo stesso programma** con un'opzione interna. Serve alle…, comando_aiutante(), Come rilanciare **questo stesso programma** in modalità aiutante. Funziona sia…

### Community 57 - "Path"
Cohesion: 0.16
Nodes (15): _aspetta_file(), _processo_vivo(), Path, skipif, Prima: il percorso per rilanciare sé stesso era sbagliato di una cartella…, Windows PowerShell 5.1 legge i file `.ps1` senza BOM con la codifica ANSI: gli…, Al contrario i `.bat` non devono averlo: cmd.exe non lo salta e la prima riga…, Prima: se il file di destinazione non si poteva aprire, il file degli errori e… (+7 more)

### Community 58 - "pathlib"
Cohesion: 0.10
Nodes (26): argparse, Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non… (+18 more)

### Community 59 - "scanner.py"
Cohesion: 0.14
Nodes (17): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le… (+9 more)

### Community 61 - "FotoFacileError"
Cohesion: 0.10
Nodes (18): errore_disco_componente(), FotoFacileError, Exception, Path, Guaio del disco mentre si scarica o si installa il componente di collegamento…, Errore con messaggio per l'utente e un suggerimento su come procedere., Path, Gli OSError di questo blocco sono guai del disco, non della rete (D23). (+10 more)

### Community 62 - "TrasportoAdb"
Cohesion: 0.16
Nodes (4): Path, Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 63 - "conftest.py"
Cohesion: 0.19
Nodes (13): app(), azzera(), casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una… (+5 more)

### Community 65 - "SelectPage"
Cohesion: 0.15
Nodes (8): Canvas, Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa…, SelectPage, Colora una superficie di disegno, allineandola al pannello., tema_tela()

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.22
Nodes (8): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Terza revisione (D1–D31), Verifica

### Community 67 - "_copia_con_opzioni"
Cohesion: 0.13
Nodes (24): _controlla_nessuna_perdita(), _copia_con_opzioni(), _copia_piatta(), _immagine_bytes(), Copia piatta con conversione WebP; ``voci`` è una lista di (percorso,…, Ordine PNG, WebP trasparente, PNG: il nome del convertito lo decide il piano,…, ``a.png`` (o ``a.webp``) è già nella cartella di destinazione e ``a (1).png``…, Come ``_copia_piatta`` ma con le opzioni scelte; ``voci`` = (percorso,… (+16 more)

### Community 68 - "RealAdbBackend"
Cohesion: 0.22
Nodes (13): Implementazione reale dell'interfaccia verso adb., RealAdbBackend, Path, _script_adb(), test_cancellazione_usa_rm_con_seriale_e_percorso_quotato(), test_check_riporta_la_prima_riga_della_versione(), test_comando_fallito_produce_errore_umano(), test_devices_raw_riporta_l_output_di_adb() (+5 more)

### Community 69 - "trasporto_aiutante.py"
Cohesion: 0.12
Nodes (29): _controlla_spazio(), _dimensione_prevista(), _esito_di_copia(), percorso_temporaneo(), Path, Controlla che il comando di copia sia finito bene, spiegando il motivo se no., Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file. (+21 more)

### Community 70 - "_bat"
Cohesion: 0.33
Nodes (6): _bat(), Path, Ogni frammento Python scritto nei .bat deve essere compilabile davvero., Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire., test_gli_snippet_python_dentro_i_bat_sono_validi(), test_nei_bat_non_ci_sono_caret_dentro_il_codice_python()

### Community 71 - "esegui"
Cohesion: 0.24
Nodes (9): carica(), esegui(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., Trasforma la richiesta di terminare (SIGTERM) in un'uscita ordinata. Il…, _termina_con_ordine(), esegui_aiutante() (+1 more)

### Community 72 - "scrivi_log_avvio"
Cohesion: 0.25
Nodes (8): comando_formati(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, Mostra, per ogni estensione, quali formati veri contiene (serve a capire il…, scrivi_log_avvio(), test_log_di_avvio_viene_scritto(), test_d27_il_registro_di_avvio_non_cresce_per_sempre(), test_d27_un_registro_piccolo_continua_a_crescere()

### Community 73 - "_RispostaLenta"
Cohesion: 0.22
Nodes (4): Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n…, _risposta_http(), _RispostaLenta, test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato()

### Community 74 - "OptionsPage"
Cohesion: 0.35
Nodes (3): OptionsPage, Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 75 - "TrasportoComposto"
Cohesion: 0.10
Nodes (10): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore(), test_composto_sceglie_il_primo_collegamento_che_vede_il_telefono() (+2 more)

### Community 76 - "destination_for"
Cohesion: 0.10
Nodes (21): destination_for(), _nome_sicuro(), Rende un nome di file accettabile su Windows, macOS e Linux., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.…, relative_path(), suggested_destination() (+13 more)

### Community 77 - "test_regressioni.py"
Cohesion: 0.08
Nodes (28): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., _funzione_powershell(), _lavoro_infinito(), Un test per ogni errore realmente trovato e corretto. Ogni test qui descrive un…, Prima: chiudere la finestra durante il download lasciava `platform-…, Prima: due copie avviate insieme nella stessa cartella scrivevano nello stesso…, Prima: la verifica dell'impronta esisteva ma non era mai stata eseguita, e… (+20 more)

### Community 78 - "AdbDemoAPassi"
Cohesion: 0.10
Nodes (16): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi(), Prima: `AdbDemoAPassi.pulisci()` cercava un attributo che non esisteva e…, Prima: abbandonare una copia in modalità demo lasciava il `.part` nella… (+8 more)

### Community 79 - "planner.py"
Cohesion: 0.18
Nodes (13): dataclasses, _accorcia_cartella(), _accorcia_nome(), _dimensione(), _limita_percorso(), PlannedFile, _radice_e_coda(), Costruzione del piano di copia: cosa copiare, dove, e cosa saltare. I nomi dei… (+5 more)

### Community 80 - "DeviceInfo"
Cohesion: 0.13
Nodes (12): Elenca i telefoni collegati e il loro stato., DeviceInfo, leggi_dispositivi(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., test_modello_con_underscore_diventa_leggibile(), test_modello_vuoto_ricade_sul_seriale(), test_avanti_funziona_solo_con_telefono_pronto(), test_d5_ricerca_fallita_spiega_il_motivo() (+4 more)

### Community 81 - "main"
Cohesion: 0.50
Nodes (4): main(), Guardia: un errore di programmazione continua a dire di che tipo è (serve a…, test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici(), test_d20_un_guaio_imprevisto_resta_riconoscibile()

### Community 82 - "_TelefonoFinto"
Cohesion: 0.14
Nodes (11): _piano_con_destinazione_occupata(), _piano_singolo(), Il WebP trasparente diventa a.png: il vero a.png di un'altra cartella non lo…, Piano costruito a cartella vuota; poi, prima della copia, qualcuno crea il file…, Il minimo che serve a `transfer`: due metodi., _TelefonoFinto, test_d1_la_copia_conserva_la_data_di_scatto(), test_d21_la_copia_interna_traduce_la_cartella_impossibile_da_creare() (+3 more)

### Community 83 - "test_adb.py"
Cohesion: 0.31
Nodes (10): find_adb(), Path, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, test_find_adb_ignora_variabile_inesistente_e_cerca_nel_percorso(), test_find_adb_preferisce_la_variabile_di_ambiente(), test_find_adb_ritorna_none_se_assente(), test_find_adb_su_windows_cerca_adb_exe_nel_profilo(), test_find_adb_su_windows_cerca_nell_sdk_android() (+2 more)

### Community 84 - "avviso_visibile"
Cohesion: 0.18
Nodes (11): avviso_visibile(), contesto_grafico_dubbio(), True se non ci sono segnali di una sessione grafica (automazione, servizi,…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Apre la finestra principale; se la grafica non è disponibile lo spiega con…, start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico(), test_avviso_visibile_usa_osascript_su_macos() (+3 more)

### Community 85 - "doctor"
Cohesion: 0.25
Nodes (8): doctor(), elenco_modi(), Quali modi di collegamento al telefono sono utilizzabili su questo computer. È…, Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Stampa senza fermarsi sui caratteri che l'uscita non sa scrivere. Su Windows,…, Stampa una diagnosi completa dello stato del computer e del collegamento., selftest(), _stampa()

### Community 86 - "Revisione v0.2 — audit per gruppi (Task A7)"
Cohesion: 0.05
Nodes (42): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Cosa sostituirà la Parte D, Difetti che la Parte D **non** copre (da aggiungere alla Parte D) (+34 more)

### Community 87 - "crea_dmg"
Cohesion: 0.25
Nodes (8): crea_dmg(), _esegui(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, skipif, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per…, test_il_dmg_si_crea_e_contiene_l_app()

### Community 89 - "build_doctor_report"
Cohesion: 0.19
Nodes (9): build_doctor_report(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., _casa_isolata(), fixture, Qui si avvia la grafica (finta): il registro di avvio deve finire in una…, test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi(), test_costruzione_diagnostica_senza_componente() (+1 more)

### Community 90 - "shell_quote"
Cohesion: 0.25
Nodes (6): Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, shell_quote(), test_shell_quote_gestisce_apostrofi_e_spazi(), test_shell_quote_gestisce_dollaro_backtick_e_virgolette(), test_shell_quote_lascia_intatti_i_percorsi_normali()

### Community 91 - "font"
Cohesion: 0.31
Nodes (6): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_indicatore_passi()

### Community 92 - "script"
Cohesion: 0.15
Nodes (13): Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: la ricerca estesa a tutta la memoria passava sempre…, Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il…, Prima: dopo ogni copia l'intero file veniva riletto in memoria come stringa. Un…, script(), test_copia_non_rilegge_il_file_appena_scritto(), test_d14_la_copia_diretta_su_linux_accetta_la_dimensione(), test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji() (+5 more)

### Community 93 - "osutil.py"
Cohesion: 0.10
Nodes (24): chiave_sistema(), is_case_insensitive_fs(), is_windows(), python_command(), Unico punto in cui il programma si adatta al sistema operativo., Come si avvia Python da terminale su questo sistema., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., Nome del sistema normalizzato a «win32» / «darwin» / «linux». (+16 more)

### Community 94 - "codifica_di_windows"
Cohesion: 0.50
Nodes (4): codifica_di_windows(), fixture, Rilegge i file di testo come farebbe Windows quando la codifica non è indicata., registro_non_scrivibile()

### Community 95 - "AdbError"
Cohesion: 0.25
Nodes (4): Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., AdbError, Errore di comunicazione con il telefono: spesso basta riprovare., test_errore_espone_messaggio_e_suggerimento()

### Community 97 - "build_help_text_generico"
Cohesion: 0.40
Nodes (5): build_help_text_generico(), Cosa provare **prima** di pensare al Debug USB., I primi consigli non devono nominare il Debug USB: non è obbligatorio., test_l_aiuto_cita_trasferimento_file(), test_l_aiuto_generico_non_parla_di_debug()

### Community 99 - ".disponibile"
Cohesion: 0.50
Nodes (3): _eseguibile(), Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, True solo su Linux e solo se c'è un modo per montare l'MTP.

## Knowledge Gaps
- **111 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 717 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `TransferOptions`, `test_trasporto.py`, `transfer.py`, `App`, `test_osutil.py`, `MediaFile`, `test_ui_app.py`, `ProcessoEsterno`, `TransferPlan`, `transfer`, `test_installer_passi.py`, `app.py`, `esegui_fino_alla_fine`, `format_size`, `test_installer.py`, `installer.py`, `Trasporto`, `TrasportoAiutante`, `Path`, `pathlib`, `trasporto_aiutante.py`, `TrasportoComposto`, `test_regressioni.py`, `AdbDemoAPassi`, `planner.py`, `DeviceInfo`, `test_adb.py`, `script`, `osutil.py`, `AdbError`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `SelectPage`, `test_widgets.py`, `app.py`, `ConnectPage`, `OptionsPage`, `test_regressioni.py`, `History`, `ProcessoEsterno`, `TrasportoDemo`, `Trasporto`, `tk_available`, `avviso_visibile`, `doctor`, `TransferPage`, `pathlib`, `font`, `conftest.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `MediaFile` connect `MediaFile` to `TransferOptions`, `test_trasporto.py`, `transfer.py`, `test_scanner.py`, `TransferPlan`, `transfer`, `TrasportoMtpLinux`, `esegui_fino_alla_fine`, `TrasportoDemo`, `Trasporto`, `leggi_elenco`, `TrasportoAiutante`, `pathlib`, `scanner.py`, `TrasportoAdb`, `SelectPage`, `_copia_con_opzioni`, `trasporto_aiutante.py`, `TrasportoComposto`, `test_regressioni.py`, `AdbDemoAPassi`, `planner.py`, `_TelefonoFinto`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `_passi_di_copia()` and `transfer()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
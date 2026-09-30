# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 90 files · ~127,697 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1902 nodes · 4437 edges · 103 communities (91 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f0a6e56`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- TransferOptions
- script
- widgets.py
- Critical Behaviors Contract
- transfer.py
- App
- test_osutil.py
- ConnectPage
- test_cli.py
- MediaFile
- test_ui_app.py
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- parse_stat_stream
- History
- ProcessoEsterno
- build_app.py
- mtp_linux.py
- test_page_connect.py
- test_theme.py
- ptp_mac.py
- planner.py
- DemoAdbBackend
- _Esistenza
- transfer
- TrasportoMtpLinux
- wpd_win.ps1
- pytest
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- FotoFacileError
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- theme.py
- AdbAPassi
- page_transfer.py
- test_installer_pacchetti.py
- wpd_win.py
- _VocePtpFinta
- installer.py
- errore_disco_componente
- test_pacchetto_windows.py
- TrasportoDemo
- test_conversione.py
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_trasporto.py
- crea_pacchetto
- TrasportoAiutante
- TransferPage
- cli.py
- Path
- history.py
- attendi
- test_ops.py
- TrasportoAdb
- conftest.py
- SelectPage
- Piano di revisione e sviluppo — FotoFacile
- test_regressioni.py
- test_adb.py
- adb_passi.py
- _bat
- esegui
- scrivi_log_avvio
- _RispostaLenta
- OptionsPage
- TrasportoComposto
- destination_for
- avviso_visibile
- AdbDemoAPassi
- crea_installer_mac.py
- leggi_dispositivi
- main
- TrasportoWpdWindows
- _apri_telefono
- start_gui
- _Attesa
- Revisione v0.2 — audit per gruppi (Task A7)
- crea_dmg
- setter
- build_doctor_report
- test_robustezza.py
- font
- esegui_fino_alla_fine
- pathlib
- codifica_di_windows
- prova_finestra_diretta
- comando_copia
- leggi_file
- __main__.py
- AiutanteNonDisponibile
- voce_json
- _casa_isolata

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

## Communities (103 total, 6 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.14
Nodes (21): Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo… (+13 more)

### Community 1 - "TransferOptions"
Cohesion: 0.16
Nodes (33): Errore durante la copia di un file., TransferError, build_plan(), ensure_space(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Solleva un errore comprensibile se lo spazio libero non basta. ``free_bytes`` a…, Trasforma un percorso del telefono in percorso relativo pulito., relative_path() (+25 more)

### Community 2 - "script"
Cohesion: 0.15
Nodes (13): Path, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, script(), test_copia_annullata_rimuove_il_file_a_meta(), test_copia_riporta_l_avanzamento_intermedio(), test_copia_scrive_i_byte_e_rinomina_solo_alla_fine() (+5 more)

### Community 3 - "widgets.py"
Cohesion: 0.09
Nodes (22): Banner, LogPane, PathChooser, _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., True se questa macchina riesce davvero ad aprire una finestra. La verifica… (+14 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "transfer.py"
Cohesion: 0.16
Nodes (20): _applica_data(), _chiudi(), download_file_stream(), _passi_di_copia(), Progress, _pubblica(), Path, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.… (+12 more)

### Community 6 - "App"
Cohesion: 0.07
Nodes (21): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Passa a un modo di collegamento **non ancora provato**. Tener traccia di quelli… (+13 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.10
Nodes (29): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, python_command() (+21 more)

### Community 8 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 9 - "test_cli.py"
Cohesion: 0.16
Nodes (20): ArgumentParser, build_parser(), main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo() (+12 more)

### Community 10 - "MediaFile"
Cohesion: 0.13
Nodes (13): MediaFile, _piano_con_destinazione_occupata(), Piano costruito a cartella vuota; poi, prima della copia, qualcuno crea il file…, Prima: un file JSON valido ma con la struttura sbagliata faceva sollevare…, Prima: sotto i 16 MB liberi il programma si rifiutava di copiare **qualsiasi**…, Prima: accorciando due nomi lunghi lo stesso modo si poteva ottenere lo stesso…, Prima: se il contatore « (1)» veniva tagliato dall'accorciamento, il ciclo che…, test_cronologia_con_voci_malformate_non_fa_crash() (+5 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.10
Nodes (13): app(), fixture, Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., La pagina «Scegli le foto» accoglie solo con un telefono collegato (altrimenti…, Un'area vuota sempre presente confonde: compare al primo messaggio., _telefono_demo(), test_i_dettagli_si_mostrano_solo_quando_servono(), test_modalita_demo_attivabile_e_disattivabile() (+5 more)

### Community 12 - "PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)"
Cohesion: 0.05
Nodes (41): Auto-revisione del piano, Cosa abbiamo trovato leggendo il codice (base del piano), FotoFacile v0.2 — Piano di implementazione, Global Constraints, PARTE 0 — Punto di partenza, PARTE A — Revisione completa e correzione dei difetti, PARTE B — Il problema del WebP, PARTE C — Interfaccia semplice e leggibile (anche per gli anziani) (+33 more)

### Community 13 - "parse_stat_stream"
Cohesion: 0.10
Nodes (26): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, build_scan_command(), group_folders(), _kind_for(), _label(), list_media(), MediaFolder, parse_stat_stream() (+18 more)

### Community 14 - "History"
Cohesion: 0.10
Nodes (20): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+12 more)

### Community 15 - "ProcessoEsterno"
Cohesion: 0.10
Nodes (17): ProcessoEsterno, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta. (+9 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.06
Nodes (67): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+59 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.10
Nodes (19): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_aiuto_contiene_le_marche_e_i_passi() (+11 more)

### Community 19 - "test_theme.py"
Cohesion: 0.18
Nodes (15): apply_theme(), pick_font_family(), Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., True se il sistema è in modalità scura (Windows, macOS o Linux)., sistema_scuro(), test_font_restituisce_tupla_usabile_da_tkinter(), test_modalita_scura_non_impedisce_l_avvio_se_il_comando_manca() (+7 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.20
Nodes (12): comando_dispositivi(), _componenti(), nome(), _pompa(), Aiutante macOS: parla con il telefono tramite il componente di sistema…, Elenca i telefoni che macOS riconosce come fotocamera., Importa PyObjC e ImageCaptureCore, spiegando con calma se mancano., True se questo aiutante può funzionare su questo computer. (+4 more)

### Community 21 - "planner.py"
Cohesion: 0.15
Nodes (22): dataclasses, datetime, Costruzione del piano di copia: cosa copiare, dove, e cosa saltare. I nomi dei…, TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato. (+14 more)

### Community 22 - "DemoAdbBackend"
Cohesion: 0.12
Nodes (18): demo_files(), DemoAdbBackend, Telefono finto: serve per i test automatici e per la modalità demo senza…, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., hashlib, test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_backend_demo_si_presenta_come_dispositivo_pronto() (+10 more)

### Community 23 - "_Esistenza"
Cohesion: 0.13
Nodes (17): _accorcia_cartella(), _accorcia_nome(), _dimensione(), _Esistenza, _limita_percorso(), Path, _radice_e_coda(), Riduce il percorso entro il limite sicuro multipiattaforma **senza toccare la… (+9 more)

### Community 24 - "transfer"
Cohesion: 0.21
Nodes (29): PlannedFile, Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Event, Path (+21 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.14
Nodes (8): _eseguibile(), Path, Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, Telefono collegato via cavo su Linux, senza Debug USB., True solo su Linux e solo se c'è un modo per montare l'MTP., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "pytest"
Cohesion: 0.31
Nodes (8): pytest, Funzioni di appoggio per i test della grafica., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "FotoFacileError"
Cohesion: 0.12
Nodes (17): FotoFacileError, Errore con messaggio per l'utente e un suggerimento su come procedere., Non c'è niente da riavviare: il collegamento diretto non ha un servizio. Si…, Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, _opener_con(), parametrize, `open(..., "wb")` dà un `BufferedWriter`: i byte restano in coda e l'errore…, Prima: un disco pieno arrivava come un generico «adb non è riuscito», senza… (+9 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.10
Nodes (13): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+5 more)

### Community 39 - "theme.py"
Cohesion: 0.13
Nodes (17): Canvas, Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., _canale(), contrasto(), luminanza(), Misc, Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Colora una superficie di disegno, allineandola al pannello. (+9 more)

### Community 40 - "AdbAPassi"
Cohesion: 0.19
Nodes (17): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., Riavvia il collegamento: risolve molti casi di «telefono non risponde»., Path, script(), test_cancellazione_usa_il_percorso_quotato(), test_cerca_media_legge_l_output_anche_se_e_lungo() (+9 more)

### Community 41 - "page_transfer.py"
Cohesion: 0.18
Nodes (18): format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Dimensione leggibile all'italiana: «3,4 GB». (+10 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.12
Nodes (8): re, pacchetto(), fixture, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Anche i frammenti Python incorporati nei .ps1 devono essere compilabili davvero., PowerShell conta all'indietro: per un array di un solo elemento $a[1..0]…, test_gli_snippet_python_dentro_gli_script_powershell_sono_validi(), test_il_controllo_di_python_negli_script_powershell_non_aggiunge_argomenti_fantasma()

### Community 43 - "wpd_win.py"
Cohesion: 0.27
Nodes (10): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+2 more)

### Community 44 - "_VocePtpFinta"
Cohesion: 0.15
Nodes (10): cammina(), Percorre tutto il contenuto del telefono restituendo coppie ``(file,…, _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive() (+2 more)

### Community 45 - "installer.py"
Cohesion: 0.07
Nodes (57): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), _estrai_e_sostituisci(), extract_component(), impronta_file() (+49 more)

### Community 46 - "errore_disco_componente"
Cohesion: 0.50
Nodes (4): errore_disco_componente(), Exception, Path, Guaio del disco mentre si scarica o si installa il componente di collegamento…

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

### Community 52 - "test_trasporto.py"
Cohesion: 0.08
Nodes (26): main(), genere_per_estensione(), leggi_elenco(), Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., Gli aiutanti Python scrivono JSON solo ASCII: la lettura in UTF-8 non dipende…, test_d16_gli_aiutanti_scrivono_righe_leggibili_con_ogni_codifica(), Verifica del livello «collegamento diretto»: lettura dell'uscita degli… (+18 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.23
Nodes (13): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+5 more)

### Community 54 - "TrasportoAiutante"
Cohesion: 0.14
Nodes (10): ambiente_aiutante(), Path, True se su questo computer l'aiutante può funzionare., Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile., Variabili d'ambiente per il processo figlio. Dal sorgente serve ``PYTHONPATH``:… (+2 more)

### Community 55 - "TransferPage"
Cohesion: 0.21
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 56 - "cli.py"
Cohesion: 0.11
Nodes (21): doctor(), elenco_modi(), _processo_finestra(), prova_finestra(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Quali modi di collegamento al telefono sono utilizzabili su questo computer. È…, Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.… (+13 more)

### Community 57 - "Path"
Cohesion: 0.16
Nodes (15): _aspetta_file(), _processo_vivo(), Path, skipif, Prima: il percorso per rilanciare sé stesso era sbagliato di una cartella…, Windows PowerShell 5.1 legge i file `.ps1` senza BOM con la codifica ANSI: gli…, Al contrario i `.bat` non devono averlo: cmd.exe non lo salta e la prima riga…, Prima: se il file di destinazione non si poteva aprire, il file degli errori e… (+7 more)

### Community 58 - "history.py"
Cohesion: 0.21
Nodes (9): Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, json, os, sys, Pilota l'applicazione vera, dall'avvio al resoconto, senza intervento umano.…, Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…, Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice., test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema() (+1 more)

### Community 59 - "attendi"
Cohesion: 0.35
Nodes (10): attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla(), test_d5_ricerca_fallita_spiega_il_motivo() (+2 more)

### Community 61 - "test_ops.py"
Cohesion: 0.14
Nodes (18): Path, Gli OSError di questo blocco sono guai del disco, non della rete (D23)., Scarica un file da internet a piccoli blocchi, senza bloccare la grafica., ScaricatoreAPassi, _sul_disco(), Path, script(), test_output_grande_va_su_file_per_non_intasare_il_collegamento() (+10 more)

### Community 62 - "TrasportoAdb"
Cohesion: 0.16
Nodes (4): Path, Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 63 - "conftest.py"
Cohesion: 0.21
Nodes (12): app(), azzera(), casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una… (+4 more)

### Community 65 - "SelectPage"
Cohesion: 0.18
Nodes (5): Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa…, SelectPage

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.22
Nodes (8): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Terza revisione (D1–D31), Verifica

### Community 67 - "test_regressioni.py"
Cohesion: 0.06
Nodes (50): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., _controlla_nessuna_perdita(), _copia_con_opzioni(), _copia_piatta(), _funzione_powershell(), _immagine_bytes(), _lavoro_infinito() (+42 more)

### Community 68 - "test_adb.py"
Cohesion: 0.08
Nodes (35): find_adb(), Cancella un file dal telefono (solo dopo che la copia è stata verificata)., CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb. (+27 more)

### Community 69 - "adb_passi.py"
Cohesion: 0.11
Nodes (31): _controlla_spazio(), _dimensione_prevista(), _esito_di_copia(), percorso_temporaneo(), Path, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Controlla che il comando di copia sia finito bene, spiegando il motivo se no., Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla… (+23 more)

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
Cohesion: 0.09
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 76 - "destination_for"
Cohesion: 0.10
Nodes (20): destination_for(), _nome_sicuro(), Rende un nome di file accettabile su Windows, macOS e Linux., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.…, suggested_destination(), test_destinazione_con_e_senza_struttura(), test_destinazione_suggerita_ripulisce_il_modello() (+12 more)

### Community 77 - "avviso_visibile"
Cohesion: 0.25
Nodes (8): avviso_visibile(), Fa vedere un avviso anche quando la finestra del programma non può aprirsi., test_avviso_visibile_usa_osascript_su_macos(), test_d28_l_avviso_compare_anche_se_il_registro_non_si_scrive(), test_d31_l_autocollaudo_esce_anche_con_la_codifica_di_windows(), test_d31_l_avviso_di_avvio_non_si_ferma_sulla_codifica(), test_d31_la_diagnosi_esce_anche_in_un_file_con_la_codifica_di_windows(), _uscita_cp1252()

### Community 78 - "AdbDemoAPassi"
Cohesion: 0.09
Nodes (21): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., io, Path, _risposta(), test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia() (+13 more)

### Community 79 - "crea_installer_mac.py"
Cohesion: 0.50
Nodes (4): argparse, main(), versione(), shutil

### Community 80 - "leggi_dispositivi"
Cohesion: 0.40
Nodes (5): leggi_dispositivi(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., parametrize, test_leggi_dispositivi_ignora_testi_non_validi(), test_leggi_dispositivi_riconosce_i_campi()

### Community 81 - "main"
Cohesion: 0.50
Nodes (4): main(), Guardia: un errore di programmazione continua a dire di che tipo è (serve a…, test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici(), test_d20_un_guaio_imprevisto_resta_riconoscibile()

### Community 82 - "TrasportoWpdWindows"
Cohesion: 0.50
Nodes (3): Telefono collegato via cavo su Windows, senza Debug USB., True solo su Windows: l'aiutante è uno script PowerShell di Windows., TrasportoWpdWindows

### Community 83 - "_apri_telefono"
Cohesion: 0.23
Nodes (9): _apri_telefono(), comando_elenca(), Identificativo stabile del telefono: non cambia fra un collegamento e l'altro., Trova il telefono (quello indicato o il primo) e apre la sessione., seriale(), Guardia: con un telefono solo si continua a usarlo anche se l'identificativo è…, _TelefonoMacFinto, test_d15_con_due_telefoni_non_si_usa_quello_sbagliato() (+1 more)

### Community 84 - "start_gui"
Cohesion: 0.29
Nodes (7): contesto_grafico_dubbio(), True se non ci sono segnali di una sessione grafica (automazione, servizi,…, Apre la finestra principale; se la grafica non è disponibile lo spiega con…, start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico(), test_contesto_grafico_dubbio_quando_mancano_i_segnali(), test_d28_il_programma_si_apre_anche_se_il_registro_non_si_scrive()

### Community 85 - "_Attesa"
Cohesion: 0.18
Nodes (8): apri_sessione(), _Attesa, enumera(), Raccoglitore del risultato di una chiamata asincrona. ImageCaptureCore non…, Risposta del tipo ``(errore)``., Risposta del tipo ``(dati, errore)``., Apre la «conversazione» con il telefono, necessaria prima di qualunque lettura., Chiede al telefono l'elenco completo del contenuto.

### Community 86 - "Revisione v0.2 — audit per gruppi (Task A7)"
Cohesion: 0.05
Nodes (42): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Cosa sostituirà la Parte D, Difetti che la Parte D **non** copre (da aggiungere alla Parte D) (+34 more)

### Community 87 - "crea_dmg"
Cohesion: 0.25
Nodes (8): crea_dmg(), _esegui(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, skipif, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per…, test_il_dmg_si_crea_e_contiene_l_app()

### Community 89 - "build_doctor_report"
Cohesion: 0.40
Nodes (5): build_doctor_report(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi(), test_costruzione_diagnostica_senza_componente()

### Community 90 - "test_robustezza.py"
Cohesion: 0.21
Nodes (14): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Su Linux il comando non deve bloccare la finestra., Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_apertura_cartella_su_linux_usa_processo_leggero(), test_apertura_cartella_su_windows_non_boccia_explorer(), test_copia_reale_abbandonata_non_lascia_nulla() (+6 more)

### Community 91 - "font"
Cohesion: 0.22
Nodes (7): Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, tema_testo(), Misc, Text

### Community 92 - "esegui_fino_alla_fine"
Cohesion: 0.13
Nodes (19): esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., test_installazione_a_passi_annullabile(), Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il…, Prima: dopo ogni copia l'intero file veniva riletto in memoria come stringa. Un…, script(), test_copia_non_rilegge_il_file_appena_scritto() (+11 more)

### Community 93 - "pathlib"
Cohesion: 0.11
Nodes (26): Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, chiave_sistema(), is_windows(), Unico punto in cui il programma si adatta al sistema operativo., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., Nome del sistema normalizzato a «win32» / «darwin» / «linux». (+18 more)

### Community 94 - "codifica_di_windows"
Cohesion: 0.50
Nodes (4): codifica_di_windows(), fixture, Rilegge i file di testo come farebbe Windows quando la codifica non è indicata., registro_non_scrivibile()

### Community 96 - "comando_copia"
Cohesion: 0.32
Nodes (8): chiudi_sessione(), comando_cancella(), comando_copia(), _dimensione_di(), Chiude la conversazione: è gentile e libera il telefono per altre applicazioni., Il file del telefono che corrisponde al percorso indicato., trova_file(), _valore()

### Community 97 - "leggi_file"
Cohesion: 0.29
Nodes (7): _leggi_a_blocchi(), leggi_file(), _leggi_scaricando(), _LetturaNonDisponibile, Consegna a ``scrivi`` i byte di un file del telefono, a blocchi. Si prova prima…, Il telefono non sa consegnare i byte a blocchi: si usa l'altro metodo., Ripiego: si fa consegnare il file in una cartella temporanea e poi lo si…

### Community 99 - "AiutanteNonDisponibile"
Cohesion: 0.40
Nodes (5): AiutanteNonDisponibile, NessunTelefono, Exception, PyObjC o ImageCaptureCore non ci sono: il collegamento diretto non è…, Nessun telefono collegato riconosciuto come fotocamera.

### Community 100 - "voce_json"
Cohesion: 0.40
Nodes (5): _data_di(), genere_per_nome(), «photo», «video» o ``None`` in base all'estensione del file., Descrizione di un file, nella forma che il programma principale si aspetta., voce_json()

### Community 104 - "_casa_isolata"
Cohesion: 0.67
Nodes (3): _casa_isolata(), fixture, Qui si avvia la grafica (finta): il registro di avvio deve finire in una…

## Knowledge Gaps
- **111 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 715 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `TransferOptions`, `transfer.py`, `App`, `test_osutil.py`, `MediaFile`, `test_ui_app.py`, `ProcessoEsterno`, `planner.py`, `transfer`, `AdbAPassi`, `installer.py`, `errore_disco_componente`, `Trasporto`, `test_trasporto.py`, `TrasportoAiutante`, `Path`, `attendi`, `test_ops.py`, `test_regressioni.py`, `test_adb.py`, `adb_passi.py`, `TrasportoComposto`, `AdbDemoAPassi`, `TrasportoWpdWindows`, `test_robustezza.py`, `esegui_fino_alla_fine`, `pathlib`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `SelectPage`, `widgets.py`, `test_regressioni.py`, `ConnectPage`, `OptionsPage`, `History`, `ProcessoEsterno`, `TrasportoDemo`, `Trasporto`, `start_gui`, `TransferPage`, `cli.py`, `history.py`, `pathlib`, `conftest.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `MediaFile` connect `MediaFile` to `TransferOptions`, `transfer.py`, `parse_stat_stream`, `planner.py`, `transfer`, `TrasportoMtpLinux`, `theme.py`, `AdbAPassi`, `TrasportoDemo`, `Trasporto`, `test_trasporto.py`, `TrasportoAiutante`, `TrasportoAdb`, `SelectPage`, `test_regressioni.py`, `adb_passi.py`, `TrasportoComposto`, `AdbDemoAPassi`, `test_robustezza.py`, `pathlib`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `_passi_di_copia()` and `transfer()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
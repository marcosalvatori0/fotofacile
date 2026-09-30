# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 98 files · ~133,781 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2118 nodes · 4908 edges · 99 communities (87 shown, 7 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 186 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9a4b900a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parse_devices
- TransferOptions
- ProcessoEsterno
- test_widgets.py
- Critical Behaviors Contract
- TrasportoComposto
- App
- test_osutil.py
- ConnectPage
- test_cli.py
- DeviceInfo
- test_ui_app.py
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- Impostazioni
- History
- TrasportoDemo
- sys
- mtp_linux.py
- test_page_connect.py
- test_theme.py
- ptp_mac.py
- _VocePtpFinta
- test_installer.py
- SelectPage
- transfer
- TrasportoMtpLinux
- wpd_win.ps1
- test_page_select.py
- trasporto_aiutante.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- pytest
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- Trasporto
- cli.py
- esegui_fino_alla_fine
- format_size
- Path
- flag_nascosta
- _Esistenza
- installer.py
- _monta_jmtpfs
- AdbBackend
- osutil.py
- test_conversione.py
- test_workflow.py
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_page_options.py
- _apri_telefono
- TrasportoAiutante
- TransferPage
- _passi_di_copia
- test_page_transfer.py
- parse_stat_stream
- dispositivi
- pathlib
- _Attesa
- download_file_stream
- attendi
- FotoFacileError
- test_scanner.py
- Piano di revisione e sviluppo — FotoFacile
- MediaFile
- comando_copia
- finestra_condivisa
- emetti
- esegui
- azzera
- script
- leggi_file
- ._esegui_ricerca
- LogPane
- test_regressioni.py
- DemoAdbBackend
- suggested_destination
- AiutanteNonDisponibile
- app.py
- test_trasporto.py
- voce_json
- test_adb.py
- Revisione v0.2 — audit per gruppi (Task A7)
- cammina
- OptionsPage
- _RispostaLenta
- scrivi_log_avvio
- build_doctor_report
- build_parser
- prova_finestra_diretta
- __main__.py
- avviso_visibile
- _casa_isolata
- aiuto.py

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 123 edges
2. `esegui_fino_alla_fine()` - 73 edges
3. `TransferOptions` - 69 edges
4. `MediaFile` - 69 edges
5. `DeviceInfo` - 65 edges
6. `DemoAdbBackend` - 55 edges
7. `App` - 53 edges
8. `build_plan()` - 51 edges
9. `ProcessoEsterno` - 45 edges
10. `AdbAPassi` - 43 edges

## Surprising Connections (you probably didn't know these)
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_il_percorso_del_telefono_non_puo_uscire_dal_montaggio()` --calls--> `percorso_di_filesystem()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile()` --uses--> `AdbDemoAPassi`  [INFERRED]
  tests/test_regressioni.py → fotofacile/core/adb_passi.py
- `finestra_condivisa()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/conftest.py → fotofacile/core/demo.py
- `test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla()` --calls--> `DemoAdbBackend`  [EXTRACTED]
  tests/test_demo.py → fotofacile/core/demo.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (99 total, 7 thin omitted)

### Community 0 - "parse_devices"
Cohesion: 0.13
Nodes (20): parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_backend_demo_si_presenta_come_dispositivo_pronto(), test_stato_modificabile_per_provare_gli_altri_casi(), test_stato_nessuno_telefono(), test_dispositivo_non_autorizzato_non_pronto() (+12 more)

### Community 1 - "TransferOptions"
Cohesion: 0.12
Nodes (44): Errore durante la copia di un file., TransferError, build_plan(), destination_for(), ensure_space(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Solleva un errore comprensibile se lo spazio libero non basta. ``free_bytes`` a…, Trasforma un percorso del telefono in percorso relativo pulito. (+36 more)

### Community 2 - "ProcessoEsterno"
Cohesion: 0.08
Nodes (30): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Scarica un file da internet a piccoli blocchi, senza bloccare la grafica. (+22 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.11
Nodes (16): Banner, PathChooser, Misc, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riapplica i caratteri: da chiamare quando cambia la dimensione del testo., Riquadro con il percorso scelto e il pulsante per cambiarlo., Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator (+8 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "TrasportoComposto"
Cohesion: 0.09
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 6 - "App"
Cohesion: 0.06
Nodes (26): Any, App, Dimensione iniziale proporzionata al testo, ma mai più grande dello schermo., Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.… (+18 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.10
Nodes (31): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), open_in_file_manager(), Path, Cartella che contiene il pacchetto: serve a far ritrovare i moduli al processo… (+23 more)

### Community 8 - "ConnectPage"
Cohesion: 0.14
Nodes (10): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Un altro controllo a vuoto: dopo qualche tentativo compare l'aiuto grande., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Tasto Invio: come «Avanti»., Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile. (+2 more)

### Community 9 - "test_cli.py"
Cohesion: 0.15
Nodes (22): main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, «FotoFacile.exe doctor» (collegamento del menu Start) deve arrivare a doctor(),…, La CI legge selftest.txt: l'esito va scritto anche quando l'autocollaudo riesce., La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo() (+14 more)

### Community 10 - "DeviceInfo"
Cohesion: 0.17
Nodes (21): DeviceInfo, TransferPlan, build_report(), _cartelle_di_riserva(), Path, Resoconto testuale dell'operazione: cosa è stato copiato, saltato o non copiato., Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il… (+13 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.07
Nodes (22): _con_focus_su(), _pulsante_e_dentro_la_pagina(), _punti(), Dimensione in punti del carattere di un widget, comunque Tk la restituisca., Registro, banner e barra dei passi vivono nella finestra e non vengono…, ttk.Button non risponde a Invio (solo a Spazio): «Indietro» non deve far…, Sulle caselle si spunta con Spazio: Invio non deve far partire l'azione della…, Prova con un evento vero: Tab su «← Indietro» del passo 3 e poi Invio. (+14 more)

### Community 12 - "PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)"
Cohesion: 0.05
Nodes (41): Auto-revisione del piano, Cosa abbiamo trovato leggendo il codice (base del piano), FotoFacile v0.2 — Piano di implementazione, Global Constraints, PARTE 0 — Punto di partenza, PARTE A — Revisione completa e correzione dei difetti, PARTE B — Il problema del WebP, PARTE C — Interfaccia semplice e leggibile (anche per gli anziani) (+33 more)

### Community 13 - "Impostazioni"
Cohesion: 0.22
Nodes (15): Impostazioni, percorso_impostazioni(), Path, Impostazioni personali (per ora: la dimensione del testo), salvate fra un avvio…, Riporta un valore qualunque alla scala ammessa più vicina (o al predefinito)., Legge le impostazioni; qualunque problema porta ai valori predefiniti., Scrive le impostazioni; se non si può, pazienza (non è mai un errore per…, scala_vicina() (+7 more)

### Community 14 - "History"
Cohesion: 0.10
Nodes (21): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+13 more)

### Community 15 - "TrasportoDemo"
Cohesion: 0.17
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 16 - "sys"
Cohesion: 0.08
Nodes (14): re, sys, L'aiutante per Windows (`wpd_win.ps1`) deve restare completo e avviabile. Prima…, Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non…, `python fotofacile.py doctor` (e quindi `FotoFacile.exe doctor`) arriva alla…, test_il_progetto_porta_l_aiutante_per_windows(), test_il_punto_di_avvio_esegue_la_diagnosi(), Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il… (+6 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.15
Nodes (24): comando_cancella(), comando_copia(), comando_dispositivi(), comando_elenca(), ComponenteMancante, _eseguibile(), genere_per_estensione(), GuaioMtp (+16 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.08
Nodes (23): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., parametrize, Il tasto Invio non deve scavalcare il pulsante «Avanti» spento., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Tornando al passo 1 non deve restare l'avviso di prima. (+15 more)

### Community 19 - "test_theme.py"
Cohesion: 0.10
Nodes (30): apply_theme(), contrasto(), pick_font_family(), Misc, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono)., True se il sistema è in modalità scura (Windows, macOS o Linux). (+22 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.20
Nodes (12): comando_dispositivi(), _componenti(), nome(), _pompa(), Aiutante macOS: parla con il telefono tramite il componente di sistema…, Elenca i telefoni che macOS riconosce come fotocamera., Importa PyObjC e ImageCaptureCore, spiegando con calma se mancano., True se questo aiutante può funzionare su questo computer. (+4 more)

### Community 21 - "_VocePtpFinta"
Cohesion: 0.15
Nodes (10): cammina(), Percorre tutto il contenuto del telefono restituendo coppie ``(file,…, _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive() (+2 more)

### Community 22 - "test_installer.py"
Cohesion: 0.14
Nodes (26): component_dir(), download_file(), extract_component(), is_installed(), platform_tools_url(), Dove viene installato il componente: <cartella utente>/.fotofacile/platform-…, Estrae il componente (eseguibile e librerie) e lo installa **in modo atomico**.…, Scarica un file riportando l'avanzamento. ``validatore`` (facoltativo) riceve… (+18 more)

### Community 23 - "SelectPage"
Cohesion: 0.06
Nodes (28): e_rumore(), _minuscolo(), nome_amichevole(), nomi_distinti(), Nomi comprensibili per le cartelle del telefono e riconoscimento di sticker e…, I segmenti del percorso senza la radice della memoria (``/sdcard``,…, Il nome da mostrare a una persona: «Foto ricevute su WhatsApp», non un percorso., Nome da mostrare per ogni percorso; se due cartelle avrebbero lo stesso nome,… (+20 more)

### Community 24 - "transfer"
Cohesion: 0.21
Nodes (29): PlannedFile, Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Event, Path (+21 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.20
Nodes (5): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.16
Nodes (22): _con_file(), _f(), Un «Interrompi» precedente lasciava `cancel_event` acceso e la ricerca nasceva…, Il conteggio non deve promettere foto che l'elenco poi non mostra., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_cartelle_con_lo_stesso_nome_si_distinguono() (+14 more)

### Community 28 - "trasporto_aiutante.py"
Cohesion: 0.11
Nodes (31): _controlla_spazio(), _dimensione_prevista(), _esito_di_copia(), percorso_temporaneo(), Path, Controlla che il comando di copia sia finito bene, spiegando il motivo se no., Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file. (+23 more)

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "pytest"
Cohesion: 0.05
Nodes (41): argparse, pytest, comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema() (+33 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "Trasporto"
Cohesion: 0.05
Nodes (18): Path, Protocol, setter, Pausa fra un controllo e l'altro (nei test si azzera per non aspettare)., Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato. (+10 more)

### Community 39 - "cli.py"
Cohesion: 0.16
Nodes (14): doctor(), elenco_modi(), _processo_finestra(), prova_finestra(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Stampa una diagnosi completa dello stato del computer e del collegamento., Quali modi di collegamento al telefono sono utilizzabili su questo computer. È…, Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.… (+6 more)

### Community 40 - "esegui_fino_alla_fine"
Cohesion: 0.15
Nodes (28): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+20 more)

### Community 41 - "format_size"
Cohesion: 0.15
Nodes (21): datetime, format_date(), format_duration(), format_eta(), format_size(), format_speed(), parole_tempo_residuo(), parse_date() (+13 more)

### Community 42 - "Path"
Cohesion: 0.16
Nodes (13): _aspetta_file(), _processo_vivo(), Path, skipif, Ogni cancellazione dal telefono deve avere il suo file sul disco (niente foto…, Prima: il percorso per rilanciare sé stesso era sbagliato di una cartella…, Windows PowerShell 5.1 legge i file `.ps1` senza BOM con la codifica ANSI: gli…, _TelefonoCheControllaLeCancellazioni (+5 more)

### Community 43 - "flag_nascosta"
Cohesion: 0.19
Nodes (14): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+6 more)

### Community 44 - "_Esistenza"
Cohesion: 0.13
Nodes (17): _accorcia_cartella(), _accorcia_nome(), _dimensione(), _Esistenza, _limita_percorso(), Path, _radice_e_coda(), Riduce il percorso entro il limite sicuro multipiattaforma **senza toccare la… (+9 more)

### Community 45 - "installer.py"
Cohesion: 0.12
Nodes (30): catalogo_platform_tools(), _chiave_sistema(), controlla_archivio(), _estrai_e_sostituisci(), impronta_file(), install_component(), installa_a_passi(), _nome_eseguibile() (+22 more)

### Community 46 - "_monta_jmtpfs"
Cohesion: 0.13
Nodes (24): _cartella_nostra(), comando_smonta(), _file_stato(), _monta_jmtpfs(), _nota_se_vuoto(), _punto_jmtpfs(), Path, Il file dove si ricordano i montaggi jmtpfs fra un comando e l'altro. (+16 more)

### Community 47 - "AdbBackend"
Cohesion: 0.12
Nodes (10): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+2 more)

### Community 48 - "osutil.py"
Cohesion: 0.09
Nodes (25): chiave_sistema(), is_windows(), python_command(), Unico punto in cui il programma si adatta al sistema operativo., Come si avvia Python da terminale su questo sistema., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., Nome del sistema normalizzato a «win32» / «darwin» / «linux»., _system() (+17 more)

### Community 49 - "test_conversione.py"
Cohesion: 0.09
Nodes (43): converti_webp(), e_webp(), _libero(), pillow_disponibile(), Path, Conversione delle immagini WebP in JPG (o PNG se hanno trasparenza). Il WebP…, True se Pillow c'è e sa leggere il WebP., True se il **contenuto** del file è WebP, qualunque sia il nome. (+35 more)

### Community 50 - "test_workflow.py"
Cohesion: 0.13
Nodes (10): flusso(), _passi(), fixture, parametrize, L'exe senza finestra nera non scrive su stdout: l'esito sta in selftest.txt., test_gli_script_powershell_hanno_il_bom(), test_il_lavoro_windows_costruisce_installa_e_carica_i_file_giusti(), test_il_testo_della_release_non_parla_piu_di_debug_usb() (+2 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.10
Nodes (19): Code Context, Completed, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know, Goal, Handoff: FotoFacile — app desktop per copiare foto da Android (+11 more)

### Community 52 - "test_page_options.py"
Cohesion: 0.14
Nodes (20): _prepara(), Path, «Copia le foto» non deve spostarsi né sparire quando si aprono le altre opzioni., test_cancellare_dal_telefono_chiede_conferma_con_una_finestra(), test_esc_torna_al_passo_precedente(), test_il_promemoria_resta_visibile_con_le_altre_opzioni_chiuse(), test_il_riassunto_dice_che_le_foto_saranno_tolte_dal_telefono(), test_il_riassunto_dice_cosa_succedera() (+12 more)

### Community 53 - "_apri_telefono"
Cohesion: 0.23
Nodes (9): _apri_telefono(), comando_elenca(), Identificativo stabile del telefono: non cambia fra un collegamento e l'altro., Trova il telefono (quello indicato o il primo) e apre la sessione., seriale(), Guardia: con un telefono solo si continua a usarlo anche se l'identificativo è…, _TelefonoMacFinto, test_d15_con_due_telefoni_non_si_usa_quello_sbagliato() (+1 more)

### Community 54 - "TrasportoAiutante"
Cohesion: 0.13
Nodes (11): ambiente_aiutante(), Path, True se su questo computer l'aiutante può funzionare., Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile., Non c'è niente da riavviare: il collegamento diretto non ha un servizio. Si… (+3 more)

### Community 55 - "TransferPage"
Cohesion: 0.12
Nodes (8): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, Porta la pagina allo stato «copia appena iniziata» (serve dopo un errore)., La copia si è fermata per un errore: si spiega e si offre una via d'uscita., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., Tasto Invio: a copia finita apre la cartella; durante la copia non fa niente., Tasto Esc: durante e dopo una copia riuscita non si torna indietro; dopo un…, Durante la copia c'è solo «Interrompi»; a fine copia compaiono gli altri…, TransferPage

### Community 56 - "_passi_di_copia"
Cohesion: 0.18
Nodes (13): _applica_data(), _passi_di_copia(), Progress, _pubblica(), Il corpo della copia; il salvataggio della cronologia sta nell'involucro., Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo., Rimette sul file copiato la data originale della foto (se il telefono la… (+5 more)

### Community 57 - "test_page_transfer.py"
Cohesion: 0.15
Nodes (19): _fino_al_trasferimento(), _media(), _pronta_a_copiare(), Con «Interrompi» non si resta più con il solo «Chiudi»., test_a_fine_copia_c_e_un_fatto_chiaro_e_gli_avvisi_si_vedono(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_copia_interrotta_o_con_errori_comincia_con_l_avviso() (+11 more)

### Community 58 - "parse_stat_stream"
Cohesion: 0.12
Nodes (20): demo_files(), Albero di esempio deterministico con foto e video realistici., group_folders(), _kind_for(), _label(), parse_stat_stream(), Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le… (+12 more)

### Community 59 - "dispositivi"
Cohesion: 0.10
Nodes (23): _aggiungi_uri(), cartella_gvfs(), _chiave_seriale(), dispositivi(), dispositivi_jmtpfs(), _esegui(), leggi_dispositivi_gio(), montaggio_da_seriale() (+15 more)

### Community 60 - "pathlib"
Cohesion: 0.15
Nodes (22): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non… (+14 more)

### Community 61 - "_Attesa"
Cohesion: 0.18
Nodes (8): apri_sessione(), _Attesa, enumera(), Raccoglitore del risultato di una chiamata asincrona. ImageCaptureCore non…, Risposta del tipo ``(errore)``., Risposta del tipo ``(dati, errore)``., Apre la «conversazione» con il telefono, necessaria prima di qualunque lettura., Chiede al telefono l'elenco completo del contenuto.

### Community 62 - "download_file_stream"
Cohesion: 0.14
Nodes (13): _chiudi(), CopiatoreInterno, download_file_stream(), Path, Scrive un file dal telefono su disco passando da un temporaneo ``.part`` (modo…, Copia usando un backend in memoria (modalità demo e test) o il telefono demo.…, Cancella un file dal telefono (usato solo dopo una copia verificata)., Dà al file l'estensione ``.webp`` (il contenuto è WebP): meglio onesto che… (+5 more)

### Community 63 - "attendi"
Cohesion: 0.10
Nodes (21): attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_modalita_demo_attivabile_dal_passo_1(), test_nessun_telefono_invita_a_collegarlo(), test_riavvio_ricontrolla_i_collegamenti_disponibili(), test_riconosce_il_telefono_pronto() (+13 more)

### Community 64 - "FotoFacileError"
Cohesion: 0.13
Nodes (17): errore_disco_componente(), FotoFacileError, Exception, Path, Guaio del disco mentre si scarica o si installa il componente di collegamento…, Errore con messaggio per l'utente e un suggerimento su come procedere., Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, _opener_con() (+9 more)

### Community 65 - "test_scanner.py"
Cohesion: 0.14
Nodes (17): build_scan_command(), list_media(), MediaFolder, Event, Costruisce l'unico comando che elenca i file sul telefono., Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_comando_scansione_con_video_e_profondita() (+9 more)

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.22
Nodes (8): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Terza revisione (D1–D31), Verifica

### Community 67 - "MediaFile"
Cohesion: 0.09
Nodes (22): MediaFile, _piano_con_destinazione_occupata(), _piano_singolo(), Il WebP trasparente diventa a.png: il vero a.png di un'altra cartella non lo…, Piano costruito a cartella vuota; poi, prima della copia, qualcuno crea il file…, Prima: un file JSON valido ma con la struttura sbagliata faceva sollevare…, Prima: sotto i 16 MB liberi il programma si rifiutava di copiare **qualsiasi**…, Il minimo che serve a `transfer`: due metodi. (+14 more)

### Community 68 - "comando_copia"
Cohesion: 0.32
Nodes (8): chiudi_sessione(), comando_cancella(), comando_copia(), _dimensione_di(), Chiude la conversazione: è gentile e libera il telefono per altre applicazioni., Il file del telefono che corrisponde al percorso indicato., trova_file(), _valore()

### Community 69 - "finestra_condivisa"
Cohesion: 0.25
Nodes (8): casa_temporanea(), finestra_condivisa(), fixture, Contenitore usa e getta per i test dei singoli componenti grafici. È una…, La scala del testo è globale: ogni test riparte dalla dimensione normale (1.0)., Cartella utente finta: i test non devono mai toccare i file reali dell'utente., root(), scala_testo_normale()

### Community 70 - "emetti"
Cohesion: 0.15
Nodes (14): comando_formati(), emetti(), Path, Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Mostra, per ogni estensione, quali formati veri contiene (serve a capire il…, Stampa senza fermarsi sui caratteri che l'uscita non sa scrivere. Su Windows,…, Mostra un rapporto: sul terminale se c'è, altrimenti in un file che si apre da…, selftest() (+6 more)

### Community 71 - "esegui"
Cohesion: 0.24
Nodes (9): carica(), esegui(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., Trasforma la richiesta di terminare (SIGTERM) in un'uscita ordinata. Il…, _termina_con_ordine(), esegui_aiutante() (+1 more)

### Community 72 - "azzera"
Cohesion: 0.25
Nodes (8): app(), azzera(), La finestra condivisa, azzerata prima e dopo ogni test., Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)., app(), focus(), fixture, I tasti generati arrivano solo alla finestra col focus: quella dei test è…

### Community 73 - "script"
Cohesion: 0.20
Nodes (10): Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il…, Prima: dopo ogni copia l'intero file veniva riletto in memoria come stringa. Un…, script(), test_copia_non_rilegge_il_file_appena_scritto(), test_d14_la_copia_diretta_su_linux_accetta_la_dimensione(), test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji(), test_la_copia_diretta_con_aiutante_rifiuta_di_sovrascrivere() (+2 more)

### Community 74 - "leggi_file"
Cohesion: 0.29
Nodes (7): _leggi_a_blocchi(), leggi_file(), _leggi_scaricando(), _LetturaNonDisponibile, Consegna a ``scrivi`` i byte di un file del telefono, a blocchi. Si prova prima…, Il telefono non sa consegnare i byte a blocchi: si usa l'altro metodo., Ripiego: si fa consegnare il file in una cartella temporanea e poi lo si…

### Community 75 - "._esegui_ricerca"
Cohesion: 0.18
Nodes (4): Elenca i telefoni collegati e il loro stato., Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde».

### Community 76 - "LogPane"
Cohesion: 0.25
Nodes (4): LogPane, Riapplica il carattere: da chiamare quando cambia la dimensione del testo., Area di testo scorrevole con il dettaglio di quello che succede., test_pannello_registro()

### Community 77 - "test_regressioni.py"
Cohesion: 0.06
Nodes (52): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., main(), codifica_di_windows(), _controlla_nessuna_perdita(), _copia_con_opzioni(), _copia_piatta(), _funzione_powershell() (+44 more)

### Community 78 - "DemoAdbBackend"
Cohesion: 0.09
Nodes (27): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., DemoAdbBackend, Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., io, Path, _risposta() (+19 more)

### Community 79 - "suggested_destination"
Cohesion: 0.33
Nodes (6): _nome_sicuro(), Rende un nome di file accettabile su Windows, macOS e Linux., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., suggested_destination(), test_destinazione_suggerita_ripulisce_il_modello(), test_destinazione_suggerita_usa_modello_e_data()

### Community 80 - "AiutanteNonDisponibile"
Cohesion: 0.40
Nodes (5): AiutanteNonDisponibile, NessunTelefono, Exception, PyObjC o ImageCaptureCore non ci sono: il collegamento diretto non è…, Nessun telefono collegato riconosciuto come fotocamera.

### Community 81 - "app.py"
Cohesion: 0.09
Nodes (32): Canvas, Finestra principale: navigazione fra i passi, lavoro a piccoli passi, registro.…, Passo 1: guidare la persona a collegare il telefono. Questa schermata è la più…, Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., _canale(), font() (+24 more)

### Community 82 - "test_trasporto.py"
Cohesion: 0.07
Nodes (37): main(), genere_per_estensione(), leggi_dispositivi(), leggi_elenco(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., parametrize (+29 more)

### Community 83 - "voce_json"
Cohesion: 0.40
Nodes (5): _data_di(), genere_per_nome(), «photo», «video» o ``None`` in base all'estensione del file., Descrizione di un file, nella forma che il programma principale si aspetta., voce_json()

### Community 85 - "test_adb.py"
Cohesion: 0.08
Nodes (34): find_adb(), CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+26 more)

### Community 86 - "Revisione v0.2 — audit per gruppi (Task A7)"
Cohesion: 0.04
Nodes (45): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Cosa sostituirà la Parte D, Difetti che la Parte D **non** copre (da aggiungere alla Parte D) (+37 more)

### Community 87 - "cammina"
Cohesion: 0.50
Nodes (4): cammina(), Percorre il telefono montato restituendo ``(percorso, informazioni)`` per ogni…, stat_result, test_una_radice_illeggibile_non_diventa_un_elenco_vuoto()

### Community 88 - "OptionsPage"
Cohesion: 0.22
Nodes (5): OptionsPage, Tasto Invio: come «Copia le foto»., Tasto Esc: torna al passo precedente., Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 89 - "_RispostaLenta"
Cohesion: 0.12
Nodes (8): Path, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., Gli OSError di questo blocco sono guai del disco, non della rete (D23)., _sul_disco(), Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n…, _risposta_http(), _RispostaLenta, test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato()

### Community 90 - "scrivi_log_avvio"
Cohesion: 0.17
Nodes (12): contesto_grafico_dubbio(), Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, True se non ci sono segnali di una sessione grafica (automazione, servizi,…, Apre la finestra principale; se la grafica non è disponibile lo spiega con…, scrivi_log_avvio(), start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico(), test_contesto_grafico_dubbio_quando_mancano_i_segnali() (+4 more)

### Community 93 - "build_doctor_report"
Cohesion: 0.33
Nodes (6): build_doctor_report(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi(), test_costruzione_diagnostica_senza_componente(), test_la_diagnosi_riferisce_la_conversione_webp()

### Community 98 - "avviso_visibile"
Cohesion: 0.25
Nodes (8): avviso_visibile(), Fa vedere un avviso anche quando la finestra del programma non può aprirsi., test_avviso_visibile_usa_osascript_su_macos(), test_d28_l_avviso_compare_anche_se_il_registro_non_si_scrive(), test_d31_l_autocollaudo_esce_anche_con_la_codifica_di_windows(), test_d31_l_avviso_di_avvio_non_si_ferma_sulla_codifica(), test_d31_la_diagnosi_esce_anche_in_un_file_con_la_codifica_di_windows(), _uscita_cp1252()

### Community 99 - "_casa_isolata"
Cohesion: 0.67
Nodes (3): _casa_isolata(), fixture, Qui si avvia la grafica (finta): il registro di avvio deve finire in una…

## Knowledge Gaps
- **114 isolated node(s):** `run_tests.sh script`, `Goal`, `Parte A — correzioni dell'audit (D1–D31)`, `Parte B — WebP`, `Parte C — nuova interfaccia (4 passi, pensata per chi non è pratico)` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 782 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `TransferOptions`, `ProcessoEsterno`, `TrasportoComposto`, `App`, `test_osutil.py`, `DeviceInfo`, `test_ui_app.py`, `test_page_connect.py`, `test_installer.py`, `transfer`, `trasporto_aiutante.py`, `Trasporto`, `esegui_fino_alla_fine`, `Path`, `installer.py`, `osutil.py`, `TrasportoAiutante`, `TransferPage`, `_passi_di_copia`, `test_page_transfer.py`, `pathlib`, `download_file_stream`, `attendi`, `MediaFile`, `script`, `._esegui_ricerca`, `test_regressioni.py`, `DemoAdbBackend`, `app.py`, `test_trasporto.py`, `test_adb.py`, `_RispostaLenta`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `test_widgets.py`, `finestra_condivisa`, `emetti`, `cli.py`, `Trasporto`, `ConnectPage`, `LogPane`, `test_regressioni.py`, `History`, `TrasportoDemo`, `app.py`, `test_theme.py`, `TransferPage`, `SelectPage`, `OptionsPage`, `scrivi_log_avvio`, `pathlib`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `DeviceInfo` connect `DeviceInfo` to `parse_devices`, `TrasportoComposto`, `test_ui_app.py`, `TrasportoDemo`, `test_page_connect.py`, `test_page_select.py`, `trasporto_aiutante.py`, `Trasporto`, `cli.py`, `esegui_fino_alla_fine`, `test_page_options.py`, `TrasportoAiutante`, `TransferPage`, `test_page_transfer.py`, `pathlib`, `attendi`, `._esegui_ricerca`, `test_regressioni.py`, `DemoAdbBackend`, `test_trasporto.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `_passi_di_copia()` and `transfer()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
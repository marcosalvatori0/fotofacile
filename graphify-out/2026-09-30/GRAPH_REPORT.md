# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 98 files · ~131,581 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2114 nodes · 4904 edges · 102 communities (87 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 186 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eceeaae1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- TransferOptions
- ProcessoEsterno
- test_widgets.py
- Critical Behaviors Contract
- TrasportoComposto
- App
- osutil.py
- ConnectPage
- test_cli.py
- TransferPlan
- test_ui_app.py
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- Impostazioni
- History
- TrasportoDemo
- build_app.py
- mtp_linux.py
- test_page_connect.py
- test_theme.py
- ptp_mac.py
- _VocePtpFinta
- test_installer_iss.py
- SelectPage
- transfer
- TrasportoMtpLinux
- wpd_win.ps1
- test_page_select.py
- adb_passi.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- pathlib
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- Trasporto
- scanner.py
- esegui_fino_alla_fine
- planner.py
- test_regressioni.py
- cli.py
- _Esistenza
- installer.py
- _monta_jmtpfs
- AdbBackend
- app.py
- test_conversione.py
- test_workflow.py
- Handoff: FotoFacile — app desktop per copiare foto da Android
- test_page_options.py
- _apri_telefono
- trasporto_aiutante.py
- TransferPage
- transfer.py
- test_page_transfer.py
- test_demo.py
- montaggio_da_seriale
- errors.py
- _Attesa
- TrasportoAdb
- attendi
- FotoFacileError
- list_media
- Piano di revisione e sviluppo — FotoFacile
- MediaFile
- comando_copia
- conftest.py
- emetti
- esegui
- azzera
- script
- leggi_file
- build_scan_command
- _copia_con_opzioni
- DemoAdbBackend
- suggested_destination
- AiutanteNonDisponibile
- theme.py
- test_trasporto.py
- voce_json
- TrasportoPtpMac
- test_adb.py
- Revisione v0.2 — audit per gruppi (Task A7)
- cammina
- OptionsPage
- _RispostaLenta
- scrivi_log_avvio
- .remote
- build_doctor_report
- build_parser
- prova_finestra_diretta
- .cancella
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
- `test_dispositivi_non_elenca_due_volte_lo_stesso_telefono()` --calls--> `dispositivi()`  [EXTRACTED]
  tests/test_trasporto.py → fotofacile/aiutanti/mtp_linux.py
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
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

## Communities (102 total, 9 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.11
Nodes (25): dataclasses, Elenca i telefoni collegati e il loro stato., DeviceInfo, get_devices(), parse_devices(), pick_device(), Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Estrae i dispositivi dall'output di ``adb devices -l``. (+17 more)

### Community 1 - "TransferOptions"
Cohesion: 0.12
Nodes (44): Errore durante la copia di un file., TransferError, build_plan(), destination_for(), ensure_space(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Solleva un errore comprensibile se lo spazio libero non basta. ``free_bytes`` a…, Trasforma un percorso del telefono in percorso relativo pulito. (+36 more)

### Community 2 - "ProcessoEsterno"
Cohesion: 0.07
Nodes (31): ProcessoEsterno, Path, Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo., True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il… (+23 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.08
Nodes (20): Banner, LogPane, PathChooser, Misc, Riapplica il carattere: da chiamare quando cambia la dimensione del testo., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riapplica i caratteri: da chiamare quando cambia la dimensione del testo., Riquadro con il percorso scelto e il pulsante per cambiarlo. (+12 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "TrasportoComposto"
Cohesion: 0.09
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 6 - "App"
Cohesion: 0.06
Nodes (25): Any, App, Dimensione iniziale proporzionata al testo, ma mai più grande dello schermo., Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.… (+17 more)

### Community 7 - "osutil.py"
Cohesion: 0.07
Nodes (43): Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, app_dir(), chiave_sistema(), comando_se_stesso(), default_photos_dir(), file_manager_command(), is_case_insensitive_fs(), is_windows() (+35 more)

### Community 8 - "ConnectPage"
Cohesion: 0.14
Nodes (10): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Un altro controllo a vuoto: dopo qualche tentativo compare l'aiuto grande., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Tasto Invio: come «Avanti»., Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile. (+2 more)

### Community 9 - "test_cli.py"
Cohesion: 0.14
Nodes (22): main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, «FotoFacile.exe doctor» (collegamento del menu Start) deve arrivare a doctor(),…, La CI legge selftest.txt: l'esito va scritto anche quando l'autocollaudo riesce., La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo() (+14 more)

### Community 10 - "TransferPlan"
Cohesion: 0.19
Nodes (18): TransferPlan, build_report(), _cartelle_di_riserva(), Path, Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,…, save_report() (+10 more)

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
Nodes (20): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+12 more)

### Community 15 - "TrasportoDemo"
Cohesion: 0.17
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 16 - "build_app.py"
Cohesion: 0.16
Nodes (22): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+14 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.11
Nodes (32): cartella_gvfs(), comando_cancella(), comando_copia(), comando_dispositivi(), comando_elenca(), ComponenteMancante, dispositivi(), _eseguibile() (+24 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.08
Nodes (23): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., parametrize, Il tasto Invio non deve scavalcare il pulsante «Avanti» spento., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Tornando al passo 1 non deve restare l'avviso di prima. (+15 more)

### Community 19 - "test_theme.py"
Cohesion: 0.10
Nodes (29): apply_theme(), contrasto(), pick_font_family(), Misc, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra., Rapporto di contrasto fra due colori (WCAG: 4,5 minimo, 7 buono)., True se il sistema è in modalità scura (Windows, macOS o Linux). (+21 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.20
Nodes (12): comando_dispositivi(), _componenti(), nome(), _pompa(), Aiutante macOS: parla con il telefono tramite il componente di sistema…, Elenca i telefoni che macOS riconosce come fotocamera., Importa PyObjC e ImageCaptureCore, spiegando con calma se mancano., True se questo aiutante può funzionare su questo computer. (+4 more)

### Community 21 - "_VocePtpFinta"
Cohesion: 0.15
Nodes (10): cammina(), Percorre tutto il contenuto del telefono restituendo coppie ``(file,…, _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive() (+2 more)

### Community 22 - "test_installer_iss.py"
Cohesion: 0.18
Nodes (6): _direttiva(), iss(), fixture, test_finestra_ingrandita_e_stile_moderno(), test_installa_senza_amministratore_e_senza_finestra_di_scelta(), test_solo_windows_10_o_successivo_a_64_bit()

### Community 23 - "SelectPage"
Cohesion: 0.06
Nodes (28): e_rumore(), _minuscolo(), nome_amichevole(), nomi_distinti(), Nomi comprensibili per le cartelle del telefono e riconoscimento di sticker e…, I segmenti del percorso senza la radice della memoria (``/sdcard``,…, Il nome da mostrare a una persona: «Foto ricevute su WhatsApp», non un percorso., Nome da mostrare per ogni percorso; se due cartelle avrebbero lo stesso nome,… (+20 more)

### Community 24 - "transfer"
Cohesion: 0.22
Nodes (28): Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Event, Path, Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni. (+20 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.20
Nodes (5): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.16
Nodes (22): _con_file(), _f(), Un «Interrompi» precedente lasciava `cancel_event` acceso e la ricerca nasceva…, Il conteggio non deve promettere foto che l'elenco poi non mostra., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_cartelle_con_lo_stesso_nome_si_distinguono() (+14 more)

### Community 28 - "adb_passi.py"
Cohesion: 0.11
Nodes (19): _controlla_spazio(), _dimensione_prevista(), percorso_temporaneo(), Path, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Riavvia il collegamento: risolve molti casi di «telefono non risponde». (+11 more)

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "pathlib"
Cohesion: 0.06
Nodes (31): argparse, json, pathlib, pytest, re, crea_dmg(), _esegui(), main() (+23 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "Trasporto"
Cohesion: 0.11
Nodes (10): Protocol, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata)., Prova a far ripartire il collegamento (usato dal pulsante «Riavvia… (+2 more)

### Community 39 - "scanner.py"
Cohesion: 0.16
Nodes (19): group_folders(), _kind_for(), _label(), MediaFolder, parse_stat_stream(), Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…, Raggruppa i file per cartella, ordinando per dimensione decrescente., Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le… (+11 more)

### Community 40 - "esegui_fino_alla_fine"
Cohesion: 0.14
Nodes (33): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+25 more)

### Community 41 - "planner.py"
Cohesion: 0.13
Nodes (24): datetime, format_date(), format_duration(), format_eta(), format_size(), format_speed(), parole_tempo_residuo(), parse_date() (+16 more)

### Community 42 - "test_regressioni.py"
Cohesion: 0.05
Nodes (52): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., main(), _aspetta_file(), codifica_di_windows(), _funzione_powershell(), _lavoro_infinito(), _opener_con() (+44 more)

### Community 43 - "cli.py"
Cohesion: 0.10
Nodes (23): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+15 more)

### Community 44 - "_Esistenza"
Cohesion: 0.13
Nodes (17): _accorcia_cartella(), _accorcia_nome(), _dimensione(), _Esistenza, _limita_percorso(), Path, _radice_e_coda(), Riduce il percorso entro il limite sicuro multipiattaforma **senza toccare la… (+9 more)

### Community 45 - "installer.py"
Cohesion: 0.07
Nodes (54): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), _estrai_e_sostituisci(), extract_component(), impronta_file() (+46 more)

### Community 46 - "_monta_jmtpfs"
Cohesion: 0.11
Nodes (28): _cartella_nostra(), comando_smonta(), dispositivi_jmtpfs(), _esegui(), _file_stato(), _monta_jmtpfs(), _nota_se_vuoto(), _punto_jmtpfs() (+20 more)

### Community 47 - "AdbBackend"
Cohesion: 0.09
Nodes (14): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+6 more)

### Community 48 - "app.py"
Cohesion: 0.13
Nodes (18): find_adb(), Path, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Come FotoFacile parla con il telefono. Il programma non usa **un solo** metodo…, Elenco dei collegamenti utilizzabili su questo computer, dal più comodo al…, Costruisce il collegamento diretto adatto al sistema, se esiste., Il modo migliore disponibile, oppure ``None`` se non ce n'è nessuno., scegli_trasporto() (+10 more)

### Community 49 - "test_conversione.py"
Cohesion: 0.09
Nodes (43): converti_webp(), e_webp(), _libero(), pillow_disponibile(), Path, Conversione delle immagini WebP in JPG (o PNG se hanno trasparenza). Il WebP…, True se Pillow c'è e sa leggere il WebP., True se il **contenuto** del file è WebP, qualunque sia il nome. (+35 more)

### Community 50 - "test_workflow.py"
Cohesion: 0.13
Nodes (10): flusso(), _passi(), fixture, parametrize, L'exe senza finestra nera non scrive su stdout: l'esito sta in selftest.txt., test_gli_script_powershell_hanno_il_bom(), test_il_lavoro_windows_costruisce_installa_e_carica_i_file_giusti(), test_il_testo_della_release_non_parla_piu_di_debug_usb() (+2 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.11
Nodes (18): Code Context, Collegamento senza Debug USB (novità principale), Completed, Copia piatta, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know (+10 more)

### Community 52 - "test_page_options.py"
Cohesion: 0.14
Nodes (20): _prepara(), Path, «Copia le foto» non deve spostarsi né sparire quando si aprono le altre opzioni., test_cancellare_dal_telefono_chiede_conferma_con_una_finestra(), test_esc_torna_al_passo_precedente(), test_il_promemoria_resta_visibile_con_le_altre_opzioni_chiuse(), test_il_riassunto_dice_che_le_foto_saranno_tolte_dal_telefono(), test_il_riassunto_dice_cosa_succedera() (+12 more)

### Community 53 - "_apri_telefono"
Cohesion: 0.23
Nodes (9): _apri_telefono(), comando_elenca(), Identificativo stabile del telefono: non cambia fra un collegamento e l'altro., Trova il telefono (quello indicato o il primo) e apre la sessione., seriale(), Guardia: con un telefono solo si continua a usarlo anche se l'identificativo è…, _TelefonoMacFinto, test_d15_con_due_telefoni_non_si_usa_quello_sbagliato() (+1 more)

### Community 54 - "trasporto_aiutante.py"
Cohesion: 0.10
Nodes (22): Annullato, Exception, Segnale interno: l'utente ha interrotto l'operazione in corso., cartella_progetto(), Cartella che contiene il pacchetto: serve a far ritrovare i moduli al processo…, ambiente_aiutante(), comando_aiutante(), _dimensione() (+14 more)

### Community 55 - "TransferPage"
Cohesion: 0.13
Nodes (8): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, Porta la pagina allo stato «copia appena iniziata» (serve dopo un errore)., La copia si è fermata per un errore: si spiega e si offre una via d'uscita., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., Tasto Invio: a copia finita apre la cartella; durante la copia non fa niente., Tasto Esc: durante e dopo una copia riuscita non si torna indietro; dopo un…, Durante la copia c'è solo «Interrompi»; a fine copia compaiono gli altri…, TransferPage

### Community 56 - "transfer.py"
Cohesion: 0.17
Nodes (19): _applica_data(), _chiudi(), download_file_stream(), _passi_di_copia(), Progress, _pubblica(), Path, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.… (+11 more)

### Community 57 - "test_page_transfer.py"
Cohesion: 0.13
Nodes (21): _fino_al_trasferimento(), _media(), _pronta_a_copiare(), Con «Interrompi» non si resta più con il solo «Chiudi»., test_a_fine_copia_c_e_un_fatto_chiaro_e_gli_avvisi_si_vedono(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_copia_interrotta_o_con_errori_comincia_con_l_avviso() (+13 more)

### Community 58 - "test_demo.py"
Cohesion: 0.18
Nodes (10): demo_files(), Albero di esempio deterministico con foto e video realistici., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_cancellazione_di_percorso_inesistente_da_errore(), test_cancellazione_rimuove_il_file(), test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla(), test_demo_ha_sia_foto_sia_video(), test_stream_di_percorso_inesistente_da_errore() (+2 more)

### Community 59 - "montaggio_da_seriale"
Cohesion: 0.18
Nodes (11): _aggiungi_uri(), _chiave_seriale(), leggi_dispositivi_gio(), montaggio_da_seriale(), Forma canonica di un seriale gvfs, per confronti e per non contare doppioni.…, La cartella dove gvfs ha montato il telefono indicato, se è montato. Il nome…, Coppie ``(seriale, nome)`` ricavate dall'elenco di ``gio mount -li``. Non si…, I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs… (+3 more)

### Community 60 - "errors.py"
Cohesion: 0.14
Nodes (18): Telefono finto: serve per i test automatici e per la modalità demo senza…, errore_disco_componente(), Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Guaio del disco mentre si scarica o si installa il componente di collegamento…, installa_a_passi(), Scarica, verifica ed estrae il componente **a piccoli passi**, senza bloccare…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Gli OSError di questo blocco sono guai del disco, non della rete (D23). (+10 more)

### Community 61 - "_Attesa"
Cohesion: 0.18
Nodes (8): apri_sessione(), _Attesa, enumera(), Raccoglitore del risultato di una chiamata asincrona. ImageCaptureCore non…, Risposta del tipo ``(errore)``., Risposta del tipo ``(dati, errore)``., Apre la «conversazione» con il telefono, necessaria prima di qualunque lettura., Chiede al telefono l'elenco completo del contenuto.

### Community 62 - "TrasportoAdb"
Cohesion: 0.12
Nodes (6): Path, setter, Pausa fra un controllo e l'altro (nei test si azzera per non aspettare)., Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 63 - "attendi"
Cohesion: 0.10
Nodes (21): attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_modalita_demo_attivabile_dal_passo_1(), test_nessun_telefono_invita_a_collegarlo(), test_riavvio_ricontrolla_i_collegamenti_disponibili(), test_riconosce_il_telefono_pronto() (+13 more)

### Community 64 - "FotoFacileError"
Cohesion: 0.09
Nodes (23): _esito_di_copia(), Controlla che il comando di copia sia finito bene, spiegando il motivo se no., FotoFacileError, Errore con messaggio per l'utente e un suggerimento su come procedere., Non c'è niente da riavviare: il collegamento diretto non ha un servizio. Si…, Path, Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, Toglie il file «a metà» anche se l'aiutante di Windows lo tiene ancora aperto.… (+15 more)

### Community 65 - "list_media"
Cohesion: 0.28
Nodes (7): list_media(), Event, Cerca i file multimediali; se non ne trova, esplora tutta la memoria del…, BackendFinto, test_list_media_annullata_ritorna_vuoto(), test_list_media_ripiega_su_tutta_la_memoria_se_non_trova_nulla(), test_list_media_usa_il_seriale_richiesto()

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.22
Nodes (8): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Terza revisione (D1–D31), Verifica

### Community 67 - "MediaFile"
Cohesion: 0.13
Nodes (14): PlannedFile, MediaFile, Il WebP trasparente diventa a.png: il vero a.png di un'altra cartella non lo…, Prima: un file JSON valido ma con la struttura sbagliata faceva sollevare…, Prima: sotto i 16 MB liberi il programma si rifiutava di copiare **qualsiasi**…, Prima: accorciando due nomi lunghi lo stesso modo si poteva ottenere lo stesso…, Prima: se il contatore « (1)» veniva tagliato dall'accorciamento, il ciclo che…, test_cronologia_con_voci_malformate_non_fa_crash() (+6 more)

### Community 68 - "comando_copia"
Cohesion: 0.32
Nodes (8): chiudi_sessione(), comando_cancella(), comando_copia(), _dimensione_di(), Chiude la conversazione: è gentile e libera il telefono per altre applicazioni., Il file del telefono che corrisponde al percorso indicato., trova_file(), _valore()

### Community 69 - "conftest.py"
Cohesion: 0.21
Nodes (11): Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, os, casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, Contenitore usa e getta per i test dei singoli componenti grafici. È una…, La scala del testo è globale: ogni test riparte dalla dimensione normale (1.0). (+3 more)

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
Cohesion: 0.25
Nodes (8): Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il…, script(), test_d14_la_copia_diretta_su_linux_accetta_la_dimensione(), test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji(), test_la_copia_diretta_con_aiutante_rifiuta_di_sovrascrivere(), test_processo_senza_file_di_output_non_usa_un_tubo(), test_un_comando_abbandonato_viene_interrotto()

### Community 74 - "leggi_file"
Cohesion: 0.29
Nodes (7): _leggi_a_blocchi(), leggi_file(), _leggi_scaricando(), _LetturaNonDisponibile, Consegna a ``scrivi`` i byte di un file del telefono, a blocchi. Si prova prima…, Il telefono non sa consegnare i byte a blocchi: si usa l'altro metodo., Ripiego: si fa consegnare il file in una cartella temporanea e poi lo si…

### Community 75 - "build_scan_command"
Cohesion: 0.29
Nodes (5): Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, build_scan_command(), Costruisce l'unico comando che elenca i file sul telefono., test_comando_scansione_con_video_e_profondita(), test_comando_scansione_quota_percorsi_e_filtra_estensioni()

### Community 77 - "_copia_con_opzioni"
Cohesion: 0.11
Nodes (29): _controlla_nessuna_perdita(), _copia_con_opzioni(), _copia_piatta(), _immagine_bytes(), parametrize, Copia piatta con conversione WebP; ``voci`` è una lista di (percorso,…, Ordine PNG, WebP trasparente, PNG: il nome del convertito lo decide il piano,…, ``a.png`` (o ``a.webp``) è già nella cartella di destinazione e ``a (1).png``… (+21 more)

### Community 78 - "DemoAdbBackend"
Cohesion: 0.08
Nodes (24): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., DemoAdbBackend, Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi() (+16 more)

### Community 79 - "suggested_destination"
Cohesion: 0.33
Nodes (6): _nome_sicuro(), Rende un nome di file accettabile su Windows, macOS e Linux., Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., suggested_destination(), test_destinazione_suggerita_ripulisce_il_modello(), test_destinazione_suggerita_usa_modello_e_data()

### Community 80 - "AiutanteNonDisponibile"
Cohesion: 0.40
Nodes (5): AiutanteNonDisponibile, NessunTelefono, Exception, PyObjC o ImageCaptureCore non ci sono: il collegamento diretto non è…, Nessun telefono collegato riconosciuto come fotocamera.

### Community 81 - "theme.py"
Cohesion: 0.10
Nodes (30): Canvas, Passo 1: guidare la persona a collegare il telefono. Questa schermata è la più…, Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., _canale(), font(), imposta_scala() (+22 more)

### Community 82 - "test_trasporto.py"
Cohesion: 0.08
Nodes (34): main(), genere_per_estensione(), leggi_dispositivi(), leggi_elenco(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., parametrize (+26 more)

### Community 83 - "voce_json"
Cohesion: 0.40
Nodes (5): _data_di(), genere_per_nome(), «photo», «video» o ``None`` in base all'estensione del file., Descrizione di un file, nella forma che il programma principale si aspetta., voce_json()

### Community 84 - "TrasportoPtpMac"
Cohesion: 0.40
Nodes (4): Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, test_il_collegamento_macos_non_e_disponibile_fuori_da_macos()

### Community 85 - "test_adb.py"
Cohesion: 0.12
Nodes (23): CompletedProcess, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend, shell_quote(), AdbError, Errore di comunicazione con il telefono: spesso basta riprovare. (+15 more)

### Community 86 - "Revisione v0.2 — audit per gruppi (Task A7)"
Cohesion: 0.05
Nodes (42): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Cosa sostituirà la Parte D, Difetti che la Parte D **non** copre (da aggiungere alla Parte D) (+34 more)

### Community 87 - "cammina"
Cohesion: 0.50
Nodes (4): cammina(), Percorre il telefono montato restituendo ``(percorso, informazioni)`` per ogni…, stat_result, test_una_radice_illeggibile_non_diventa_un_elenco_vuoto()

### Community 88 - "OptionsPage"
Cohesion: 0.22
Nodes (5): OptionsPage, Tasto Invio: come «Copia le foto»., Tasto Esc: torna al passo precedente., Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 89 - "_RispostaLenta"
Cohesion: 0.25
Nodes (4): Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n…, _risposta_http(), _RispostaLenta, test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato()

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
- **111 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 779 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `TransferOptions`, `ProcessoEsterno`, `TrasportoComposto`, `App`, `osutil.py`, `TransferPlan`, `test_ui_app.py`, `test_page_connect.py`, `transfer`, `adb_passi.py`, `Trasporto`, `esegui_fino_alla_fine`, `planner.py`, `test_regressioni.py`, `installer.py`, `app.py`, `trasporto_aiutante.py`, `TransferPage`, `transfer.py`, `test_page_transfer.py`, `errors.py`, `attendi`, `MediaFile`, `script`, `_copia_con_opzioni`, `DemoAdbBackend`, `theme.py`, `test_trasporto.py`, `test_adb.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `ProcessoEsterno`, `test_widgets.py`, `ConnectPage`, `History`, `TrasportoDemo`, `test_theme.py`, `SelectPage`, `pathlib`, `Trasporto`, `test_regressioni.py`, `cli.py`, `app.py`, `TransferPage`, `conftest.py`, `emetti`, `DemoAdbBackend`, `OptionsPage`, `scrivi_log_avvio`, `.remote`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `DeviceInfo` connect `DeviceInfo` to `TrasportoComposto`, `TransferPlan`, `test_ui_app.py`, `TrasportoDemo`, `test_page_connect.py`, `test_page_select.py`, `adb_passi.py`, `Trasporto`, `esegui_fino_alla_fine`, `planner.py`, `test_regressioni.py`, `app.py`, `test_page_options.py`, `trasporto_aiutante.py`, `test_page_transfer.py`, `TrasportoAdb`, `attendi`, `DemoAdbBackend`, `test_trasporto.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `TransferOptions` (e.g. with `_passi_di_copia()` and `transfer()`) actually correct?**
  _`TransferOptions` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
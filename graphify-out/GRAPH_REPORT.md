# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 86 files · ~123,352 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1798 nodes · 4150 edges · 113 communities (95 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 171 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `63af238d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parse_devices
- planner.py
- test_adb.py
- test_widgets.py
- Critical Behaviors Contract
- Path
- App
- test_osutil.py
- ConnectPage
- test_cli.py
- installer.py
- test_ui_app.py
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- parse_stat_stream
- History
- ProcessoEsterno
- build_app.py
- _monta_jmtpfs
- test_page_connect.py
- theme.py
- ptp_mac.py
- DeviceInfo
- flag_nascosta
- ensure_space
- test_transfer.py
- TrasportoMtpLinux
- wpd_win.ps1
- test_page_select.py
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- test_percorso_lunghissimo_non_esce_mai_dalla_cartella_scelta
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- tema_testo
- esegui_fino_alla_fine
- page_transfer.py
- test_installer_pacchetti.py
- TransferPage
- _VocePtpFinta
- test_robustezza.py
- finestra_condivisa
- test_pacchetto_windows.py
- TrasportoDemo
- ._esegui_ricerca
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- leggi_elenco
- crea_pacchetto
- TrasportoAiutante
- test_trasporto.py
- cli.py
- TrasportoComposto
- mtp_linux.py
- _monta
- test_regressioni.py
- TrasportoAdb
- osutil.py
- format_size
- Piano di revisione e sviluppo — FotoFacile
- font
- test_installer_passi.py
- trasporto_aiutante.py
- TransferOptions
- esegui
- .__init__
- _RispostaLenta
- OptionsPage
- TrasportoFinto
- test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile
- DemoAdbBackend
- AdbDemoAPassi
- GuaioMtp
- attendi
- MediaFile
- leggi_dispositivi_gio
- main
- start_gui
- avviso_visibile
- Revisione v0.2 — audit per gruppi (Task A7)
- crea_dmg
- FotoFacileError
- comando_elenca
- montaggio_da_seriale
- NessunTelefono
- leggi_dispositivi
- doctor
- TrasportoWpdWindows
- script
- scrivi_log_avvio
- suggested_destination
- azzera
- _bat
- _cartella_nostra
- TrasportoPtpMac
- setter
- codifica_di_windows
- _casa_isolata
- _piano_singolo
- build_parser
- prova_finestra_diretta
- __main__.py
- test_rifiuta_di_cancellare_la_cartella_corrente
- test_scaricatore_abbandonato_non_lascia_file_a_meta
- test_d11_errore_del_sistema_durante_la_copia_diretta_da_un_errore_comprensibile

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 111 edges
2. `esegui_fino_alla_fine()` - 71 edges
3. `MediaFile` - 59 edges
4. `DeviceInfo` - 57 edges
5. `DemoAdbBackend` - 54 edges
6. `TransferOptions` - 54 edges
7. `App` - 47 edges
8. `ProcessoEsterno` - 45 edges
9. `AdbAPassi` - 43 edges
10. `History` - 43 edges

## Surprising Connections (you probably didn't know these)
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile()` --uses--> `AdbDemoAPassi`  [INFERRED]
  tests/test_regressioni.py → fotofacile/core/adb_passi.py
- `finestra_condivisa()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/conftest.py → fotofacile/core/demo.py
- `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/test_regressioni.py → fotofacile/core/demo.py
- `test_modello_con_underscore_diventa_leggibile()` --calls--> `DeviceInfo`  [EXTRACTED]
  tests/test_devices.py → fotofacile/core/devices.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (113 total, 12 thin omitted)

### Community 0 - "parse_devices"
Cohesion: 0.17
Nodes (18): get_devices(), parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_dispositivo_non_autorizzato_non_pronto(), test_get_devices_usa_il_backend(), test_lista_con_righe_spurie_e_due_dispositivi() (+10 more)

### Community 1 - "planner.py"
Cohesion: 0.14
Nodes (23): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Telefono finto: serve per i test automatici e per la modalità demo senza…, Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non… (+15 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (34): find_adb(), CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+26 more)

### Community 3 - "test_widgets.py"
Cohesion: 0.13
Nodes (11): Banner, LogPane, PathChooser, Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., Area di testo scorrevole con il dettaglio di quello che succede., test_banner_accetta_tutti_i_toni(), test_banner_mostra_messaggio_e_suggerimento() (+3 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "Path"
Cohesion: 0.21
Nodes (12): _aspetta_file(), _processo_vivo(), Path, skipif, Prima: il percorso per rilanciare sé stesso era sbagliato di una cartella…, Windows PowerShell 5.1 legge i file `.ps1` senza BOM con la codifica ANSI: gli…, Al contrario i `.bat` non devono averlo: cmd.exe non lo salta e la prima riga…, test_d19_linux_interrotto_non_lascia_comandi_orfani() (+4 more)

### Community 6 - "App"
Cohesion: 0.06
Nodes (25): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Passa a un modo di collegamento **non ancora provato**. Tener traccia di quelli… (+17 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.12
Nodes (25): app_dir(), cartella_progetto(), default_photos_dir(), file_manager_command(), open_in_file_manager(), Path, Cartella che contiene il pacchetto: serve a far ritrovare i moduli al processo…, Su Windows dichiara che il programma gestisce da sé la scala dello schermo.… (+17 more)

### Community 8 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 9 - "test_cli.py"
Cohesion: 0.21
Nodes (15): main(), L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo(), test_autocollaudo_riporta_esito_negativo(), test_autocollaudo_riporta_esito_positivo() (+7 more)

### Community 10 - "installer.py"
Cohesion: 0.07
Nodes (57): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), _estrai_e_sostituisci(), extract_component(), impronta_file() (+49 more)

### Community 11 - "test_ui_app.py"
Cohesion: 0.10
Nodes (13): Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero., La pagina «Scegli le foto» accoglie solo con un telefono collegato (altrimenti…, Un'area vuota sempre presente confonde: compare al primo messaggio., _telefono_demo(), test_i_dettagli_si_mostrano_solo_quando_servono(), test_modalita_demo_attivabile_e_disattivabile(), test_navigazione_avanti_indietro(), test_task_con_callback_di_errore_personalizzato() (+5 more)

### Community 12 - "PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)"
Cohesion: 0.05
Nodes (41): Auto-revisione del piano, Cosa abbiamo trovato leggendo il codice (base del piano), FotoFacile v0.2 — Piano di implementazione, Global Constraints, PARTE 0 — Punto di partenza, PARTE A — Revisione completa e correzione dei difetti, PARTE B — Il problema del WebP, PARTE C — Interfaccia semplice e leggibile (anche per gli anziani) (+33 more)

### Community 13 - "parse_stat_stream"
Cohesion: 0.11
Nodes (25): build_scan_command(), group_folders(), _kind_for(), _label(), list_media(), MediaFolder, parse_stat_stream(), Event (+17 more)

### Community 14 - "History"
Cohesion: 0.10
Nodes (21): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+13 more)

### Community 15 - "ProcessoEsterno"
Cohesion: 0.10
Nodes (22): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Un comando esterno (per esempio adb) seguito senza bloccare la grafica. (+14 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "_monta_jmtpfs"
Cohesion: 0.16
Nodes (19): comando_smonta(), _file_stato(), _monta_jmtpfs(), _nota_se_vuoto(), _punto_jmtpfs(), Path, Il file dove si ricordano i montaggi jmtpfs fra un comando e l'altro., Smonta una cartella jmtpfs e la rimuove, **senza mai toccare i file del… (+11 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.10
Nodes (19): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_aiuto_contiene_le_marche_e_i_passi() (+11 more)

### Community 19 - "theme.py"
Cohesion: 0.11
Nodes (26): apply_theme(), _canale(), contrasto(), luminanza(), pick_font_family(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux)., Applica la tavolozza (chiara o scura) e lo stile a tutta la finestra. (+18 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.06
Nodes (56): AiutanteNonDisponibile, apri_sessione(), _apri_telefono(), _Attesa, cammina(), chiudi_sessione(), comando_cancella(), comando_copia() (+48 more)

### Community 21 - "DeviceInfo"
Cohesion: 0.20
Nodes (17): DeviceInfo, TransferPlan, build_report(), _cartelle_di_riserva(), Path, Testo del resoconto, leggibile da chiunque., Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,… (+9 more)

### Community 22 - "flag_nascosta"
Cohesion: 0.19
Nodes (14): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+6 more)

### Community 23 - "ensure_space"
Cohesion: 0.12
Nodes (19): Errore durante la copia di un file., TransferError, _accorcia_cartella(), _accorcia_nome(), _dimensione(), ensure_space(), _Esistenza, _limita_percorso() (+11 more)

### Community 24 - "test_transfer.py"
Cohesion: 0.24
Nodes (28): PlannedFile, Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Path, Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni. (+20 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.20
Nodes (5): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs()

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "test_page_select.py"
Cohesion: 0.36
Nodes (7): Funzioni di appoggio per i test della grafica., _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione(), test_scansione_riempie_l_elenco_delle_cartelle(), test_totali_con_e_senza_video()

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.08
Nodes (20): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+12 more)

### Community 39 - "tema_testo"
Cohesion: 0.25
Nodes (7): Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Misc, Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, Colora una finestra secondaria come quella principale. Serve a evitare il bordo…, tema_finestra(), tema_testo(), Text

### Community 40 - "esegui_fino_alla_fine"
Cohesion: 0.22
Nodes (19): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, script(), test_cancellazione_usa_il_percorso_quotato() (+11 more)

### Community 41 - "page_transfer.py"
Cohesion: 0.17
Nodes (17): datetime, format_date(), format_duration(), format_eta(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date., Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile. (+9 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.13
Nodes (7): pacchetto(), fixture, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Anche i frammenti Python incorporati nei .ps1 devono essere compilabili davvero., PowerShell conta all'indietro: per un array di un solo elemento $a[1..0]…, test_gli_snippet_python_dentro_gli_script_powershell_sono_validi(), test_il_controllo_di_python_negli_script_powershell_non_aggiunge_argomenti_fantasma()

### Community 43 - "TransferPage"
Cohesion: 0.21
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 44 - "_VocePtpFinta"
Cohesion: 0.17
Nodes (8): _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive(), test_d18_una_voce_ripetuta_si_elenca_una_volta_sola(), _VocePtpFinta

### Community 45 - "test_robustezza.py"
Cohesion: 0.21
Nodes (14): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Su Linux il comando non deve bloccare la finestra., Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_apertura_cartella_su_linux_usa_processo_leggero(), test_apertura_cartella_su_windows_non_boccia_explorer(), test_copia_reale_abbandonata_non_lascia_nulla() (+6 more)

### Community 46 - "finestra_condivisa"
Cohesion: 0.33
Nodes (6): casa_temporanea(), finestra_condivisa(), fixture, Contenitore usa e getta per i test dei singoli componenti grafici. È una…, Cartella utente finta: i test non devono mai toccare i file reali dell'utente., root()

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.09
Nodes (13): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, Una cartella padre del repository non va mai cancellata (qui il repository è…, Il Debug USB non deve mai sembrare un passaggio obbligato: è la richiesta… (+5 more)

### Community 48 - "TrasportoDemo"
Cohesion: 0.17
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 49 - "._esegui_ricerca"
Cohesion: 0.18
Nodes (4): Elenca i telefoni collegati e il loro stato., Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde».

### Community 50 - "Trasporto"
Cohesion: 0.10
Nodes (11): Protocol, Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata)., Prova a far ripartire il collegamento (usato dal pulsante «Riavvia…, Rimuove i file temporanei di lavoro. (+3 more)

### Community 51 - "Handoff: FotoFacile — app desktop per copiare foto da Android"
Cohesion: 0.11
Nodes (18): Code Context, Collegamento senza Debug USB (novità principale), Completed, Copia piatta, Current State, Edge Cases & Error Handling, Failed Approaches (Don't Repeat These), Files to Know (+10 more)

### Community 52 - "leggi_elenco"
Cohesion: 0.18
Nodes (11): main(), genere_per_estensione(), leggi_elenco(), Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali. Le…, «photo», «video» o ``None`` in base all'estensione del file., Audit G3: un a-capo (o un separatore Unicode che `splitlines` taglierebbe) nel…, test_aiutante_linux_nomi_con_a_capo_restano_una_riga(), test_aiutante_linux_senza_telefono_esce_con_3() (+3 more)

### Community 53 - "crea_pacchetto"
Cohesion: 0.29
Nodes (11): _controlla_destinazione(), _copia_albero(), crea_pacchetto(), main(), Path, Scrive un file di testo con fine riga Windows (CRLF), come si aspetta cmd.exe., Ferma le cancellazioni pericolose prima che il pacchetto sovrascriva la…, Crea la cartella pronta per Windows e restituisce il percorso. `forza` permette… (+3 more)

### Community 54 - "TrasportoAiutante"
Cohesion: 0.13
Nodes (12): _dimensione(), Path, _rallenta_scrittura(), Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile., Non c'è niente da riavviare: il collegamento diretto non ha un servizio. Si… (+4 more)

### Community 55 - "test_trasporto.py"
Cohesion: 0.13
Nodes (18): Path, Verifica del livello «collegamento diretto»: lettura dell'uscita degli…, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, L'aiutante deve poter uccidere PowerShell e spiegare l'errore prima che il…, script(), test_copia_annullata_rimuove_il_file_a_meta() (+10 more)

### Community 56 - "cli.py"
Cohesion: 0.18
Nodes (11): elenco_modi(), _processo_finestra(), prova_finestra(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi., Quali modi di collegamento al telefono sono utilizzabili su questo computer. È…, Prova ad aprire una finestra in un processo separato, senza bloccare l'avvio.…, comando_se_stesso(), Come rilanciare **questo stesso programma** con un'opzione interna. Serve alle… (+3 more)

### Community 57 - "TrasportoComposto"
Cohesion: 0.15
Nodes (6): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, test_composto_pulisci_non_solleva_mai(), test_composto_sceglie_il_primo_collegamento_che_vede_il_telefono()

### Community 58 - "mtp_linux.py"
Cohesion: 0.11
Nodes (17): argparse, Aiutante Linux: parla con il telefono tramite MTP usando ``gio``/gvfs. Sul…, _eseguibile(), Collegamento diretto su Linux: MTP tramite ``gio``/gvfs, con ``jmtpfs`` di…, Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei…, True solo su Linux e solo se c'è un modo per montare l'MTP., json, re (+9 more)

### Community 59 - "_monta"
Cohesion: 0.19
Nodes (13): ComponenteMancante, dispositivi(), dispositivi_jmtpfs(), _esegui(), _eseguibile(), _monta(), Coppie ``(seriale, nome)`` ricavate da ``jmtpfs -l`` (ripiego senza gvfs)., Telefoni MTP visibili a questo computer, senza montarli. Si guardano tre fonti,… (+5 more)

### Community 61 - "test_regressioni.py"
Cohesion: 0.10
Nodes (21): modulo_disponibile(), True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., hashlib, _funzione_powershell(), _lavoro_infinito(), Un test per ogni errore realmente trovato e corretto. Ogni test qui descrive un…, Prima: due copie avviate insieme nella stessa cartella scrivevano nello stesso…, Prima: salvare il resoconto creava una cartella «Desktop» anche su computer che… (+13 more)

### Community 62 - "TrasportoAdb"
Cohesion: 0.18
Nodes (4): Path, Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 63 - "osutil.py"
Cohesion: 0.12
Nodes (19): chiave_sistema(), is_case_insensitive_fs(), is_windows(), python_command(), Unico punto in cui il programma si adatta al sistema operativo., Come si avvia Python da terminale su questo sistema., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»)., Nome del sistema normalizzato a «win32» / «darwin» / «linux». (+11 more)

### Community 65 - "format_size"
Cohesion: 0.12
Nodes (13): Canvas, format_size(), Dimensione leggibile all'italiana: «3,4 GB»., Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Disegna l'elenco delle cartelle con una casella di spunta per ciascuna., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa… (+5 more)

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.22
Nodes (8): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Terza revisione (D1–D31), Verifica

### Community 67 - "font"
Cohesion: 0.24
Nodes (7): font(), Tupla (famiglia, dimensione[, stile]) usabile da Tkinter., Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_font_restituisce_tupla_usabile_da_tkinter(), test_indicatore_passi()

### Community 68 - "test_installer_passi.py"
Cohesion: 0.23
Nodes (11): io, Path, _risposta(), test_demo_a_passi_annullabile_senza_residui(), test_demo_a_passi_cancella_e_riavvia(), test_demo_a_passi_elenca_e_copia(), test_demo_a_passi_riporta_avanzamento_a_pezzi(), test_installazione_a_passi_annullabile() (+3 more)

### Community 69 - "trasporto_aiutante.py"
Cohesion: 0.13
Nodes (22): _controlla_spazio(), _dimensione_prevista(), percorso_temporaneo(), Path, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Nome del file «a metà», unico per processo. Il numero del processo evita che…, Quanti byte serviranno, se si sa: serve a non chiedere spazio a caso. (+14 more)

### Community 70 - "TransferOptions"
Cohesion: 0.12
Nodes (39): build_plan(), destination_for(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.…, relative_path(), TransferOptions, foto() (+31 more)

### Community 71 - "esegui"
Cohesion: 0.24
Nodes (9): carica(), esegui(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., Trasforma la richiesta di terminare (SIGTERM) in un'uscita ordinata. Il…, _termina_con_ordine(), esegui_aiutante() (+1 more)

### Community 73 - "_RispostaLenta"
Cohesion: 0.22
Nodes (4): Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n…, _risposta_http(), _RispostaLenta, test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato()

### Community 74 - "OptionsPage"
Cohesion: 0.35
Nodes (3): OptionsPage, Spazio libero in byte nella cartella scelta; ``None`` se non è possibile…, Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono.

### Community 75 - "TrasportoFinto"
Cohesion: 0.14
Nodes (6): Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore(), test_composto_senza_telefoni_non_solleva(), TrasportoFinto

### Community 76 - "test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile"
Cohesion: 0.22
Nodes (11): _opener_con(), parametrize, `open(..., "wb")` dà un `BufferedWriter`: i byte restano in coda e l'errore…, Gli aiutanti Python scrivono JSON solo ASCII: la lettura in UTF-8 non dipende…, test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile(), test_d16_gli_aiutanti_scrivono_righe_leggibili_con_ogni_codifica(), test_d22_una_risposta_di_rete_anomala_da_un_errore_comprensibile(), test_d23_cartella_dei_dati_impossibile_da_creare() (+3 more)

### Community 77 - "DemoAdbBackend"
Cohesion: 0.14
Nodes (16): demo_files(), DemoAdbBackend, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_backend_demo_si_presenta_come_dispositivo_pronto(), test_cancellazione_di_percorso_inesistente_da_errore(), test_cancellazione_rimuove_il_file() (+8 more)

### Community 78 - "AdbDemoAPassi"
Cohesion: 0.09
Nodes (18): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., Prima: `AdbDemoAPassi.pulisci()` cercava un attributo che non esisteva e…, Prima: abbandonare una copia in modalità demo lasciava il `.part` nella…, Prima: un disco pieno arrivava come un generico «adb non è riuscito», senza…, Prima: la ricerca estesa a tutta la memoria passava sempre…, Le foto già copiate restano, il file a metà no. (+10 more)

### Community 79 - "GuaioMtp"
Cohesion: 0.27
Nodes (9): comando_cancella(), comando_copia(), GuaioMtp, percorso_di_filesystem(), Exception, Il file vero dentro il montaggio, dal percorso opaco del contratto. Il percorso…, Un guaio raccontabile all'utente, con un suggerimento su come procedere.…, _valore() (+1 more)

### Community 80 - "attendi"
Cohesion: 0.47
Nodes (8): attendi(), Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla(), test_d5_ricerca_fallita_spiega_il_motivo()

### Community 81 - "MediaFile"
Cohesion: 0.13
Nodes (14): MediaFile, _passi_di_copia(), Progress, _pubblica(), Il corpo della copia; il salvataggio della cronologia sta nell'involucro., Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``…, Chiama la funzione di avanzamento, ma non più di 12 volte al secondo., _salva_cronologia() (+6 more)

### Community 82 - "leggi_dispositivi_gio"
Cohesion: 0.25
Nodes (8): _aggiungi_uri(), _chiave_seriale(), leggi_dispositivi_gio(), _nome_leggibile(), Forma canonica di un seriale gvfs, per confronti e per non contare doppioni.…, Il seriale gvfs è una stringa codificata: per mostrarlo si decodifica., Coppie ``(seriale, nome)`` ricavate dall'elenco di ``gio mount -li``. Non si…, test_lettura_dei_montaggi_di_gio()

### Community 83 - "main"
Cohesion: 0.50
Nodes (4): main(), Guardia: un errore di programmazione continua a dire di che tipo è (serve a…, test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici(), test_d20_un_guaio_imprevisto_resta_riconoscibile()

### Community 84 - "start_gui"
Cohesion: 0.29
Nodes (7): contesto_grafico_dubbio(), True se non ci sono segnali di una sessione grafica (automazione, servizi,…, Apre la finestra principale; se la grafica non è disponibile lo spiega con…, start_gui(), test_avvio_salta_la_prova_quando_il_contesto_e_grafico(), test_contesto_grafico_dubbio_quando_mancano_i_segnali(), test_d28_il_programma_si_apre_anche_se_il_registro_non_si_scrive()

### Community 85 - "avviso_visibile"
Cohesion: 0.25
Nodes (8): avviso_visibile(), Autocollaudo: apre la finestra, costruisce i quattro passi e si chiude. Serve…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Stampa senza fermarsi sui caratteri che l'uscita non sa scrivere. Su Windows,…, selftest(), _stampa(), test_avviso_visibile_usa_osascript_su_macos(), test_d28_l_avviso_compare_anche_se_il_registro_non_si_scrive()

### Community 86 - "Revisione v0.2 — audit per gruppi (Task A7)"
Cohesion: 0.05
Nodes (42): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Cosa sostituirà la Parte D, Difetti che la Parte D **non** copre (da aggiungere alla Parte D) (+34 more)

### Community 87 - "crea_dmg"
Cohesion: 0.25
Nodes (8): crea_dmg(), _esegui(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, skipif, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per…, test_il_dmg_si_crea_e_contiene_l_app()

### Community 88 - "FotoFacileError"
Cohesion: 0.10
Nodes (22): _esito_di_copia(), Controlla che il comando di copia sia finito bene, spiegando il motivo se no., errore_disco_componente(), FotoFacileError, Exception, Path, Guaio del disco mentre si scarica o si installa il componente di collegamento…, Errore con messaggio per l'utente e un suggerimento su come procedere. (+14 more)

### Community 89 - "comando_elenca"
Cohesion: 0.29
Nodes (7): cammina(), comando_elenca(), genere_per_estensione(), Percorre il telefono montato restituendo ``(percorso, informazioni)`` per ogni…, «photo», «video» o ``None`` in base all'estensione del file., stat_result, test_una_radice_illeggibile_non_diventa_un_elenco_vuoto()

### Community 90 - "montaggio_da_seriale"
Cohesion: 0.29
Nodes (7): cartella_gvfs(), montaggio_da_seriale(), La cartella dove gvfs crea i montaggi (``$XDG_RUNTIME_DIR/gvfs``)., La cartella dove gvfs ha montato il telefono indicato, se è montato. Il nome…, I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs…, test_montaggio_gvfs_trovato_anche_con_il_seriale_leggibile(), test_montaggio_gvfs_trovato_dal_seriale()

### Community 91 - "NessunTelefono"
Cohesion: 0.29
Nodes (7): comando_dispositivi(), NessunTelefono, CompletedProcess, Traduce l'errore di ``gio mount`` in una frase utile, riconoscendo i casi…, Nessun telefono collegato, o quello indicato non c'è più., _spiega_montaggio(), _stampa_riga()

### Community 92 - "leggi_dispositivi"
Cohesion: 0.33
Nodes (5): leggi_dispositivi(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., parametrize, test_leggi_dispositivi_ignora_testi_non_validi(), test_leggi_dispositivi_riconosce_i_campi()

### Community 93 - "doctor"
Cohesion: 0.29
Nodes (7): build_doctor_report(), doctor(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., Stampa una diagnosi completa dello stato del computer e del collegamento., test_costruzione_diagnostica_con_telefono_e_problemi(), test_costruzione_diagnostica_elenca_i_modi(), test_costruzione_diagnostica_senza_componente()

### Community 94 - "TrasportoWpdWindows"
Cohesion: 0.29
Nodes (5): Spiega con calma che con WPD la cancellazione non è disponibile. L'aiutante…, Telefono collegato via cavo su Windows, senza Debug USB., True solo su Windows: l'aiutante è uno script PowerShell di Windows., TrasportoWpdWindows, test_il_collegamento_windows_non_e_disponibile_fuori_da_windows()

### Community 95 - "script"
Cohesion: 0.29
Nodes (7): Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava. Un…, Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il…, script(), test_d14_la_copia_diretta_su_linux_accetta_la_dimensione(), test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji(), test_processo_senza_file_di_output_non_usa_un_tubo(), test_un_comando_abbandonato_viene_interrotto()

### Community 96 - "scrivi_log_avvio"
Cohesion: 0.33
Nodes (6): Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, scrivi_log_avvio(), test_log_di_avvio_viene_scritto(), test_d27_il_registro_di_avvio_non_cresce_per_sempre(), test_d27_un_registro_piccolo_continua_a_crescere()

### Community 97 - "suggested_destination"
Cohesion: 0.33
Nodes (6): _nome_sicuro(), Proposta di cartella: Immagini/FotoFacile/<modello>/<data>., Rende un nome di file accettabile su Windows, macOS e Linux., suggested_destination(), test_destinazione_suggerita_ripulisce_il_modello(), test_destinazione_suggerita_usa_modello_e_data()

### Community 98 - "azzera"
Cohesion: 0.33
Nodes (6): app(), azzera(), La finestra condivisa, azzerata prima e dopo ogni test., Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto)., app(), fixture

### Community 99 - "_bat"
Cohesion: 0.33
Nodes (6): _bat(), Path, Ogni frammento Python scritto nei .bat deve essere compilabile davvero., Il caret serve a cmd, ma dentro il codice Python lo rompe: non deve comparire., test_gli_snippet_python_dentro_i_bat_sono_validi(), test_nei_bat_non_ci_sono_caret_dentro_il_codice_python()

### Community 100 - "_cartella_nostra"
Cohesion: 0.40
Nodes (5): _cartella_nostra(), True solo per le cartelle temporanee che crea questo aiutante. Il file di stato…, Il file di stato di jmtpfs è un semplice file di testo: se fosse rovinato, non…, test_le_cartelle_di_appoggio_jmtpfs_sono_riconosciute_nostre(), test_lo_smontaggio_non_cancella_cartelle_che_non_sono_nostre()

### Community 101 - "TrasportoPtpMac"
Cohesion: 0.40
Nodes (4): Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, test_il_collegamento_macos_non_e_disponibile_fuori_da_macos()

### Community 103 - "codifica_di_windows"
Cohesion: 0.50
Nodes (4): codifica_di_windows(), fixture, Rilegge i file di testo come farebbe Windows quando la codifica non è indicata., registro_non_scrivibile()

### Community 104 - "_casa_isolata"
Cohesion: 0.67
Nodes (3): _casa_isolata(), fixture, Qui si avvia la grafica (finta): il registro di avvio deve finire in una…

### Community 106 - "_piano_singolo"
Cohesion: 0.67
Nodes (3): _piano_singolo(), test_d1_la_copia_conserva_la_data_di_scatto(), test_d21_la_copia_interna_traduce_la_cartella_impossibile_da_creare()

## Knowledge Gaps
- **111 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 686 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `App` connect `App` to `planner.py`, `format_size`, `test_widgets.py`, `font`, `ConnectPage`, `OptionsPage`, `TransferPage`, `History`, `finestra_condivisa`, `ProcessoEsterno`, `TrasportoDemo`, `Trasporto`, `start_gui`, `avviso_visibile`, `cli.py`, `mtp_linux.py`, `test_regressioni.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `FotoFacileError` connect `FotoFacileError` to `planner.py`, `test_adb.py`, `App`, `test_osutil.py`, `installer.py`, `test_ui_app.py`, `ProcessoEsterno`, `DeviceInfo`, `ensure_space`, `test_transfer.py`, `AdbBackend`, `esegui_fino_alla_fine`, `page_transfer.py`, `test_robustezza.py`, `._esegui_ricerca`, `Trasporto`, `TrasportoAiutante`, `test_trasporto.py`, `TrasportoComposto`, `test_regressioni.py`, `osutil.py`, `test_installer_passi.py`, `trasporto_aiutante.py`, `TransferOptions`, `TrasportoFinto`, `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile`, `AdbDemoAPassi`, `attendi`, `MediaFile`, `TrasportoWpdWindows`, `test_d11_errore_del_sistema_durante_la_copia_diretta_da_un_errore_comprensibile`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `DeviceInfo` connect `DeviceInfo` to `parse_devices`, `planner.py`, `test_ui_app.py`, `test_page_connect.py`, `test_page_select.py`, `test_page_options.py`, `esegui_fino_alla_fine`, `page_transfer.py`, `TrasportoDemo`, `._esegui_ricerca`, `Trasporto`, `TrasportoAiutante`, `test_trasporto.py`, `TrasportoComposto`, `test_regressioni.py`, `TrasportoAdb`, `trasporto_aiutante.py`, `TrasportoFinto`, `AdbDemoAPassi`, `attendi`, `leggi_dispositivi`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `DemoAdbBackend` (e.g. with `AdbDemoAPassi` and `AdbError`) actually correct?**
  _`DemoAdbBackend` has 5 INFERRED edges - model-reasoned connections that need verification._
# Graph Report - FotoFacile  (2026-09-30)

## Corpus Check
- 86 files · ~118,162 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1764 nodes · 4094 edges · 86 communities (76 shown, 5 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 171 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9263b56d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DeviceInfo
- pathlib
- test_adb.py
- widgets.py
- Critical Behaviors Contract
- test_regressioni.py
- App
- test_osutil.py
- ConnectPage
- test_cli.py
- installer.py
- attendi
- PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)
- MediaFile
- History
- ProcessoEsterno
- build_app.py
- mtp_linux.py
- test_page_connect.py
- theme.py
- ptp_mac.py
- page_transfer.py
- wpd_win.py
- planner.py
- test_transfer.py
- TrasportoMtpLinux
- wpd_win.ps1
- pytest
- test_page_options.py
- Q: perché FotoFacileError è il nodo ponte dell'intera architettura?
- destination_for
- Future Extensions Wi-Fi Packaging iPhone
- Simple Italian UI Without Technical Jargon
- run_tests.sh
- make_icon.py
- AdbBackend
- tema_testo
- AdbAPassi
- format_size
- test_installer_pacchetti.py
- TransferPage
- _VocePtpFinta
- test_robustezza.py
- conftest.py
- test_pacchetto_windows.py
- TrasportoDemo
- .copia
- Trasporto
- Handoff: FotoFacile — app desktop per copiare foto da Android
- leggi_elenco
- crea_pacchetto
- TrasportoAiutante
- test_trasporto.py
- cli.py
- _apri_telefono
- sys
- _Attesa
- save_report
- TrasportoAdb
- osutil.py
- SelectPage
- Piano di revisione e sviluppo — FotoFacile
- StepIndicator
- test_errore_di_permesso_non_viene_ritentato
- trasporto_aiutante.py
- TransferOptions
- esegui
- .__init__
- _RispostaLenta
- TrasportoComposto
- DemoAdbBackend
- esegui_fino_alla_fine
- comando_copia
- _TelefonoFinto
- leggi_file
- main
- start_gui
- G3 — Aiutanti
- FotoFacileError
- comando_elenca
- leggi_dispositivi

## God Nodes (most connected - your core abstractions)
1. `FotoFacileError` - 111 edges
2. `esegui_fino_alla_fine()` - 71 edges
3. `MediaFile` - 59 edges
4. `DeviceInfo` - 55 edges
5. `DemoAdbBackend` - 54 edges
6. `TransferOptions` - 54 edges
7. `App` - 47 edges
8. `ProcessoEsterno` - 45 edges
9. `AdbAPassi` - 43 edges
10. `History` - 43 edges

## Surprising Connections (you probably didn't know these)
- `test_protocollo_backend_richiesto()` --uses--> `AdbBackend`  [INFERRED]
  tests/test_adb.py → fotofacile/core/adb.py
- `finestra_condivisa()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/conftest.py → fotofacile/core/demo.py
- `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile()` --uses--> `DemoAdbBackend`  [INFERRED]
  tests/test_regressioni.py → fotofacile/core/demo.py
- `test_avanti_funziona_solo_con_telefono_pronto()` --calls--> `DeviceInfo`  [EXTRACTED]
  tests/test_page_connect.py → fotofacile/core/devices.py
- `TrasportoFinto` --uses--> `DeviceInfo`  [INFERRED]
  tests/test_trasporto.py → fotofacile/core/devices.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-Threads Cooperative Step Engine** — readme_no_threads, docs_superpowers_plans_2026_09_28_fotofacile_ops_passi, docs_superpowers_plans_2026_09_28_fotofacile_adb_passi, docs_superpowers_plans_2026_09_28_fotofacile_app_run_task, docs_superpowers_plans_2026_09_28_fotofacile_tk9_macos_thread_bug [EXTRACTED 1.00]
- **Four-Step Guided Wizard Flow** — readme_four_step_wizard, docs_superpowers_plans_2026_09_28_fotofacile_page_connect, docs_superpowers_plans_2026_09_28_fotofacile_page_select, docs_superpowers_plans_2026_09_28_fotofacile_page_options, docs_superpowers_plans_2026_09_28_fotofacile_page_transfer [EXTRACTED 1.00]
- **Safe Copy Integrity Contract** — docs_superpowers_specs_2026_09_28_fotofacile_design_critical_behaviors, readme_part_rename, docs_superpowers_specs_2026_09_28_fotofacile_design_verify_size, docs_superpowers_specs_2026_09_28_fotofacile_design_cancel_midfile, docs_superpowers_specs_2026_09_28_fotofacile_design_delete_after_verified [EXTRACTED 1.00]

## Communities (86 total, 5 thin omitted)

### Community 0 - "DeviceInfo"
Cohesion: 0.13
Nodes (22): DeviceInfo, get_devices(), parse_devices(), pick_device(), Estrae i dispositivi dall'output di ``adb devices -l``., Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo…, test_backend_demo_si_presenta_come_dispositivo_pronto(), test_stato_modificabile_per_provare_gli_altri_casi() (+14 more)

### Community 1 - "pathlib"
Cohesion: 0.18
Nodes (17): dataclasses, Le operazioni sul telefono eseguite **a piccoli passi**, per l'interfaccia…, Comunicazione con il telefono tramite l'eseguibile adb (Android platform-…, Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano., Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento., Archivio dei file già copiati, per non ricopiarli una seconda volta. Separato…, Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…, Copia dei file dal telefono al computer: avanzamento, annullamento, verifica.… (+9 more)

### Community 2 - "test_adb.py"
Cohesion: 0.08
Nodes (34): find_adb(), CompletedProcess, Path, Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)., Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su…, Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato,…, Implementazione reale dell'interfaccia verso adb., RealAdbBackend (+26 more)

### Community 3 - "widgets.py"
Cohesion: 0.12
Nodes (15): Banner, LogPane, PathChooser, _prova_finestra(), Componenti grafici riusabili: nessuna logica di business, solo presentazione., Messaggio grande con suggerimento: è il modo principale con cui l'app parla…, Riquadro con il percorso scelto e il pulsante «Sfoglia…»., True se questa macchina riesce davvero ad aprire una finestra. La verifica… (+7 more)

### Community 4 - "Critical Behaviors Contract"
Cohesion: 0.05
Nodes (55): AdbBackend Protocol Interface, core adb_passi.py Stepped adb Operations, App.run_task Generator Advancing with after(), Case-Insensitive Filesystem Collision Handling, cli.main and fotofacile.py Entry Point, DemoAdbBackend Fake Phone Backend, build_doctor_report Diagnosis Output, History Atomic Per-Device JSON Archive (+47 more)

### Community 5 - "test_regressioni.py"
Cohesion: 0.07
Nodes (47): _aspetta_file(), codifica_di_windows(), _funzione_powershell(), _opener_con(), _processo_vivo(), fixture, parametrize, Path (+39 more)

### Community 6 - "App"
Cohesion: 0.06
Nodes (24): Any, App, Mette la finestra davanti alle altre: avviata dal Terminale resterebbe dietro., Rimette la finestra a livello normale, ma solo se esiste ancora. Se l'utente…, Usa un backend in memoria (test) o il telefono demo., Usa il collegamento rapido tramite adb (serve il Debug USB già attivo)., Sceglie da sé come parlare con il telefono, senza chiedere niente all'utente.…, Passa a un modo di collegamento **non ancora provato**. Tener traccia di quelli… (+16 more)

### Community 7 - "test_osutil.py"
Cohesion: 0.12
Nodes (24): app_dir(), default_photos_dir(), file_manager_command(), open_in_file_manager(), Path, Su Windows dichiara che il programma gestisce da sé la scala dello schermo.…, Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale., Cartella proposta per salvare le foto (Immagini/FotoFacile). (+16 more)

### Community 8 - "ConnectPage"
Cohesion: 0.17
Nodes (8): ConnectPage, Prima schermata: collega il telefono, con aiuto, installazione e prova demo., Chiede al telefono come sta e aggiorna il messaggio in base allo stato reale., Il controllo non è riuscito: si ripiega su un altro modo di collegamento, se…, Scarica il componente mancante mostrando l'avanzamento nel registro., Il download non è riuscito: il pulsante torna subito utilizzabile., Riprova il collegamento: prima si ricontrolla quali modi sono disponibili. È il…, Telefono finto: permette di provare tutta la procedura senza dispositivo.

### Community 9 - "test_cli.py"
Cohesion: 0.13
Nodes (20): build_doctor_report(), main(), Testo della diagnosi: serve al supporto per capire cosa non va su un computer., L'autocollaudo serve a verificare una build impacchettata: deve dire…, Se la finestra non si può aprire, l'utente deve leggere cosa fare — non restare…, La diagnosi deve dire subito se il collegamento **senza Debug USB** è…, test_aiuto_elenca_le_modalita(), test_aiuto_menziona_autocollaudo() (+12 more)

### Community 10 - "installer.py"
Cohesion: 0.07
Nodes (58): catalogo_platform_tools(), _chiave_sistema(), component_dir(), controlla_archivio(), download_file(), _estrai_e_sostituisci(), extract_component(), impronta_file() (+50 more)

### Community 11 - "attendi"
Cohesion: 0.09
Nodes (23): attendi(), Funzioni di appoggio per i test della grafica., Fa girare il ciclo della grafica finché la condizione non è vera (o scade)., _fino_al_trasferimento(), test_annullamento_lascia_il_disco_pulito(), test_copia_completa_e_resoconto(), test_resoconto_salvabile(), test_seconda_copia_non_ricopia_nulla() (+15 more)

### Community 12 - "PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)"
Cohesion: 0.05
Nodes (41): Auto-revisione del piano, Cosa abbiamo trovato leggendo il codice (base del piano), FotoFacile v0.2 — Piano di implementazione, Global Constraints, PARTE 0 — Punto di partenza, PARTE A — Revisione completa e correzione dei difetti, PARTE B — Il problema del WebP, PARTE C — Interfaccia semplice e leggibile (anche per gli anziani) (+33 more)

### Community 13 - "MediaFile"
Cohesion: 0.10
Nodes (28): build_scan_command(), group_folders(), _kind_for(), _label(), list_media(), MediaFile, MediaFolder, parse_stat_stream() (+20 more)

### Community 14 - "History"
Cohesion: 0.10
Nodes (21): default_path(), History, Path, Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione., Carica la cronologia; un file corrotto o malformato viene messo da parte, mai…, True se quel file, con la stessa dimensione e data, è già stato copiato., Tiene solo le voci con la forma giusta: tutto il resto viene ignorato in…, _solo_voci_valide() (+13 more)

### Community 15 - "ProcessoEsterno"
Cohesion: 0.09
Nodes (27): ProcessoEsterno, True se il comando è ancora in corso., Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)., Generatore: cede il controllo alla grafica finché il comando non è finito. Se…, Output e codice di uscita; solleva un errore comprensibile se è andata male., Unisce il consiglio previsto con quello che ha detto davvero il comando. Il…, Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta., Scarica un file da internet a piccoli blocchi, senza bloccare la grafica. (+19 more)

### Community 16 - "build_app.py"
Cohesion: 0.24
Nodes (17): comando_pyinstaller(), crea_archivio(), crea_scorciatoia(), dimensione_mb(), eseguibile_dentro(), icona_per_sistema(), main(), pacchetto_creato() (+9 more)

### Community 17 - "mtp_linux.py"
Cohesion: 0.06
Nodes (72): _aggiungi_uri(), cammina(), cartella_gvfs(), _cartella_nostra(), _chiave_seriale(), comando_cancella(), comando_copia(), comando_dispositivi() (+64 more)

### Community 18 - "test_page_connect.py"
Cohesion: 0.10
Nodes (19): build_help_text(), build_help_text_generico(), Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca., Cosa provare **prima** di pensare al Debug USB., «Riprova il collegamento» non presuppone nessuna impostazione sul telefono., I primi consigli non devono nominare il Debug USB: non è obbligatorio., Se su questo computer non esiste **nessun** modo di collegarsi, l'app lo dice., test_aiuto_contiene_le_marche_e_i_passi() (+11 more)

### Community 19 - "theme.py"
Cohesion: 0.11
Nodes (26): apply_theme(), _canale(), contrasto(), font(), luminanza(), pick_font_family(), Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma.…, Sceglie il primo font preferito presente sul sistema (Windows, macOS o Linux). (+18 more)

### Community 20 - "ptp_mac.py"
Cohesion: 0.20
Nodes (12): comando_dispositivi(), _componenti(), nome(), _pompa(), Aiutante macOS: parla con il telefono tramite il componente di sistema…, Elenca i telefoni che macOS riconosce come fotocamera., Importa PyObjC e ImageCaptureCore, spiegando con calma se mancano., True se questo aiutante può funzionare su questo computer. (+4 more)

### Community 21 - "page_transfer.py"
Cohesion: 0.21
Nodes (17): TransferPlan, build_report(), Testo del resoconto, leggibile da chiunque., _passi_di_copia(), Progress, _pubblica(), Il corpo della copia; il salvataggio della cronologia sta nell'involucro., Copia il piano sul disco a piccoli passi, verificando ogni file. ``copiatore``… (+9 more)

### Community 22 - "wpd_win.py"
Cohesion: 0.27
Nodes (10): _codice_di_uscita(), comando_powershell(), main(), percorso_script(), Path, Aiutante Windows: avvia lo script PowerShell che parla con il telefono (WPD).…, Riporta i codici di PowerShell ai tre del contratto (0, 2, 3)., Il file PowerShell che fa il lavoro vero, accanto a questo modulo. (+2 more)

### Community 23 - "planner.py"
Cohesion: 0.11
Nodes (25): Errore durante la copia di un file., TransferError, _accorcia_cartella(), _accorcia_nome(), _dimensione(), ensure_space(), _Esistenza, _limita_percorso() (+17 more)

### Community 24 - "test_transfer.py"
Cohesion: 0.25
Nodes (27): Copia il piano e restituisce il resoconto (modo diretto, senza passi)., transfer(), BackendFinto, media(), piano(), Path, Backend in memoria: fornisce contenuti, simula errori e registra cancellazioni., test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream() (+19 more)

### Community 25 - "TrasportoMtpLinux"
Cohesion: 0.12
Nodes (11): Path, Telefono collegato via cavo su Linux, senza Debug USB., Chiude i processi rimasti e smonta i telefoni usati. Smontare alla chiusura…, TrasportoMtpLinux, Telefono collegato via cavo su macOS, senza Debug USB., True se siamo su macOS e il componente di sistema è raggiungibile. Il controllo…, TrasportoPtpMac, Costruisce il collegamento diretto adatto al sistema, se esiste. (+3 more)

### Community 26 - "wpd_win.ps1"
Cohesion: 0.21
Nodes (23): Attendi-File(), Comando-Cancella(), Comando-Copia(), Comando-Dispositivi(), Comando-Elenca(), Data-Voce(), Dimensione-Voce(), Elenca-Cartella() (+15 more)

### Community 27 - "pytest"
Cohesion: 0.22
Nodes (10): pytest, Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…, Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice., test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema(), _scansiona(), test_avanti_con_selezione_passa_alle_opzioni(), test_avanti_senza_selezione_spiega_e_non_avanza(), test_filtro_per_data_riduce_la_selezione() (+2 more)

### Community 28 - "test_page_options.py"
Cohesion: 0.36
Nodes (8): _prepara(), Path, test_cancellazione_dal_telefono_richiede_conferma(), test_cartella_proposta_quando_vuota(), test_proposta_cartella_e_opzioni(), test_secondo_giro_non_ricopia_nulla(), test_spazio_insufficiente_blocca_spiegando_il_problema(), test_spazio_sufficiente_porta_al_trasferimento()

### Community 29 - "Q: perché FotoFacileError è il nodo ponte dell'intera architettura?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: perché FotoFacileError è il nodo ponte dell'intera architettura?, Source Nodes

### Community 30 - "destination_for"
Cohesion: 0.12
Nodes (16): destination_for(), Trasforma un percorso del telefono in percorso relativo pulito., Percorso di destinazione del file, con nomi validi su ogni sistema operativo.…, relative_path(), test_destinazione_con_e_senza_struttura(), test_nome_lunghissimo_accorciato_mantenendo_estensione(), test_nome_vuoto_o_solo_caratteri_strani(), test_nomi_non_validi_su_windows_vengono_resi_sicuri() (+8 more)

### Community 37 - "make_icon.py"
Cohesion: 0.09
Nodes (28): _arrotondato(), _cerchio(), _colore_pixel(), crea_iconset(), disegna(), immagine_png(), livelli(), main() (+20 more)

### Community 38 - "AdbBackend"
Cohesion: 0.07
Nodes (21): AdbBackend, Protocol, Tutto ciò che il programma sa fare con un telefono. Implementata da…, Restituisce la versione del componente, o solleva AdbError., Output di ``adb devices -l``., Esegue sul telefono il comando di ricerca e restituisce l'output., Legge un file dal telefono a blocchi., Cancella un file dal telefono. (+13 more)

### Community 39 - "tema_testo"
Cohesion: 0.25
Nodes (7): Cosa provare quando il telefono non viene riconosciuto. Prima le cose semplici…, Misc, Colora un'area di testo classica: sfondo **e** testo, cursore e selezione…, Colora una finestra secondaria come quella principale. Serve a evitare il bordo…, tema_finestra(), tema_testo(), Text

### Community 40 - "AdbAPassi"
Cohesion: 0.21
Nodes (19): AdbAPassi, Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione., Rimuove la cartella di appoggio usata per gli elenchi temporanei., Annullato, Exception, Segnale interno: l'utente ha interrotto l'operazione in corso., Path, script() (+11 more)

### Community 41 - "format_size"
Cohesion: 0.14
Nodes (20): datetime, format_date(), format_duration(), format_eta(), format_size(), format_speed(), parse_date(), Formattazione in italiano di dimensioni, velocità, tempi e date. (+12 more)

### Community 42 - "test_installer_pacchetti.py"
Cohesion: 0.09
Nodes (17): re, _bat(), pacchetto(), fixture, Path, skipif, Verifica degli installer (macOS .dmg e Windows) e dei file `.bat` per Windows.…, Collaudo vero: si costruisce un .dmg da un finto .app e lo si monta per… (+9 more)

### Community 43 - "TransferPage"
Cohesion: 0.19
Nodes (4): Riporta al passo precedente evitando un vicolo cieco senza uscita. L'avviso va…, La copia si è fermata per un errore: si spiega e si sbloccano i pulsanti., Barra di avanzamento, velocità, tempo rimanente e resoconto finale., TransferPage

### Community 44 - "_VocePtpFinta"
Cohesion: 0.15
Nodes (10): cammina(), Percorre tutto il contenuto del telefono restituendo coppie ``(file,…, _CartellaPtpFinta, _ProxyPtpFinto, Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta., Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella., Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come…, test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive() (+2 more)

### Community 45 - "test_robustezza.py"
Cohesion: 0.23
Nodes (13): Path, Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…, Su Linux il comando non deve bloccare la finestra., Se l'utente chiude la finestra a metà copia, il file parziale deve sparire., script(), test_apertura_cartella_su_linux_usa_processo_leggero(), test_apertura_cartella_su_windows_non_boccia_explorer(), test_copia_reale_abbandonata_non_lascia_nulla() (+5 more)

### Community 46 - "conftest.py"
Cohesion: 0.21
Nodes (12): app(), azzera(), casa_temporanea(), finestra_condivisa(), fixture, Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…, La finestra condivisa, azzerata prima e dopo ogni test., Contenitore usa e getta per i test dei singoli componenti grafici. È una… (+4 more)

### Community 47 - "test_pacchetto_windows.py"
Cohesion: 0.08
Nodes (15): pacchetto(), fixture, Verifica che la cartella pronta per Windows sia completa e avviabile. Il…, Senza `wpd_win.ps1` il collegamento diretto di Windows — cioè quello che non…, La copia deve essere completa: qui la si esegue davvero (diagnosi, senza…, Niente cartelle di lavoro, test o ambienti virtuali: solo quello che serve…, «python3 scripts/crea_pacchetto_windows.py .» non deve svuotare la cartella…, Il Debug USB non deve mai sembrare un passaggio obbligato: è la richiesta… (+7 more)

### Community 48 - "TrasportoDemo"
Cohesion: 0.18
Nodes (4): Telefono finto, senza dispositivo: serve alla modalità demo e ai test., TrasportoDemo, Prima: il confronto per capire se il collegamento era cambiato era sempre vero…, test_cambiare_collegamento_non_riprova_sempre_lo_stesso()

### Community 49 - ".copia"
Cohesion: 0.12
Nodes (9): _controlla_spazio(), Path, Elenca i telefoni collegati e il loro stato., Cerca le foto sul telefono; se non trova nulla guarda in tutta la memoria. Il…, Copia un file dal telefono: si scrive un file ``.part`` e lo si rinomina alla…, Assicura che i byte siano davvero sul disco prima di rinominare il file., Cancella un file dal telefono (solo dopo che la copia è stata verificata)., Riavvia il collegamento: risolve molti casi di «telefono non risponde». (+1 more)

### Community 50 - "Trasporto"
Cohesion: 0.08
Nodes (14): Protocol, Il trasporto che ha risposto per ultimo (il primo, se nessuno ha ancora…, Il modo migliore disponibile, oppure ``None`` se non ce n'è nessuno., Un modo di parlare con un telefono. Tutte le operazioni cedono il controllo a…, True se su questo computer il collegamento può funzionare (non serve un…, Elenca i telefoni collegati e il loro stato., Elenca foto e video presenti sul telefono., Cancella un file dal telefono (solo dopo una copia verificata). (+6 more)

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
Cohesion: 0.16
Nodes (8): Path, Comando che avvia l'aiutante., Variabili d'ambiente per il processo aiutante., Toglie dall'elenco i processi già terminati. Senza questa pulizia l'elenco…, Manda avanti un comando dell'aiutante a piccoli passi, annullabile., Collegamento diretto: parla con il telefono tramite un programma aiutante. Le…, True se su questo computer l'aiutante può funzionare., TrasportoAiutante

### Community 55 - "test_trasporto.py"
Cohesion: 0.10
Nodes (23): Path, Verifica del livello «collegamento diretto»: lettura dell'uscita degli…, Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py., Pilota uno script finto come se fosse un aiutante vero., CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una…, I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs…, jmtpfs monta sempre il primo telefono: con due collegati, proseguire vorrebbe…, L'aiutante deve poter uccidere PowerShell e spiegare l'errore prima che il… (+15 more)

### Community 56 - "cli.py"
Cohesion: 0.12
Nodes (16): ArgumentParser, build_parser(), doctor(), elenco_modi(), _processo_finestra(), prova_finestra(), prova_finestra_diretta(), Avvio del programma: interfaccia grafica, modalità demo e diagnosi. (+8 more)

### Community 57 - "_apri_telefono"
Cohesion: 0.24
Nodes (8): _apri_telefono(), Identificativo stabile del telefono: non cambia fra un collegamento e l'altro., Trova il telefono (quello indicato o il primo) e apre la sessione., seriale(), Guardia: con un telefono solo si continua a usarlo anche se l'identificativo è…, _TelefonoMacFinto, test_d15_con_due_telefoni_non_si_usa_quello_sbagliato(), test_d15_con_un_solo_telefono_si_usa_quello()

### Community 58 - "sys"
Cohesion: 0.24
Nodes (10): argparse, crea_dmg(), _esegui(), main(), CompletedProcess, Path, Costruisce il .dmg con dentro l'app, la scorciatoia ad Applicazioni e il…, versione() (+2 more)

### Community 59 - "_Attesa"
Cohesion: 0.18
Nodes (8): apri_sessione(), _Attesa, enumera(), Raccoglitore del risultato di una chiamata asincrona. ImageCaptureCore non…, Risposta del tipo ``(errore)``., Risposta del tipo ``(dati, errore)``., Apre la «conversazione» con il telefono, necessaria prima di qualunque lettura., Chiede al telefono l'elenco completo del contenuto.

### Community 61 - "save_report"
Cohesion: 0.22
Nodes (10): _cartelle_di_riserva(), Path, Dove salvare il resoconto se la cartella delle foto non è scrivibile. Si usa il…, Salva il resoconto: nella cartella delle foto, altrimenti sul Desktop,…, save_report(), Prima: salvare il resoconto creava una cartella «Desktop» anche su computer che…, test_resoconto_non_crea_il_desktop_se_non_esiste(), test_salvataggio_resoconto_crea_la_cartella() (+2 more)

### Community 62 - "TrasportoAdb"
Cohesion: 0.12
Nodes (6): Path, setter, Pausa fra un controllo e l'altro (nei test si azzera per non aspettare)., Copia un file dal telefono, restituendo i byte scritti., Telefono tramite ``adb``: serve il Debug USB attivo, ma è il più veloce., TrasportoAdb

### Community 63 - "osutil.py"
Cohesion: 0.10
Nodes (24): chiave_sistema(), flag_nascosta(), is_case_insensitive_fs(), is_windows(), python_command(), Unico punto in cui il programma si adatta al sistema operativo., Come si avvia Python da terminale su questo sistema., True su Windows (accetta anche «windows», oltre a «win32» e «cygwin»). (+16 more)

### Community 65 - "SelectPage"
Cohesion: 0.14
Nodes (9): Canvas, Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare., Annulla l'attesa programmata (l'app la chiama quando si cambia schermata)., Elenco delle cartelle con caselle di spunta, filtri e totale scelto., Avvia la ricerca appena il telefono è libero. Se all'ingresso in questa…, SelectPage, Colora una superficie di disegno, allineandola al pannello., tema_tela() (+1 more)

### Community 66 - "Piano di revisione e sviluppo — FotoFacile"
Cohesion: 0.25
Nodes (7): Fase 1 — Errori e bug (verificabili con i test) — **completata (B1–B24 corretti)**, Fase 2 — Copia «piatta» (solo foto e video) — **completata**, Fase 3 — Trasporti senza Debug USB — **completata**, Fase 4 — Seconda revisione indipendente (dopo le prime tre fasi), Non verificato (dichiarato), Piano di revisione e sviluppo — FotoFacile, Verifica

### Community 67 - "StepIndicator"
Cohesion: 0.33
Nodes (4): Misc, Barra dei passi della procedura guidata, con quello attuale evidenziato., StepIndicator, test_indicatore_passi()

### Community 69 - "trasporto_aiutante.py"
Cohesion: 0.09
Nodes (31): _dimensione_prevista(), _esito_di_copia(), percorso_temporaneo(), Nome del file «a metà», unico per processo. Il numero del processo evita che…, Quanti byte serviranno, se si sa: serve a non chiedere spazio a caso., Controlla che il comando di copia sia finito bene, spiegando il motivo se no., cartella_progetto(), comando_se_stesso() (+23 more)

### Community 70 - "TransferOptions"
Cohesion: 0.22
Nodes (24): build_plan(), Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare., TransferOptions, foto(), FOTO.JPG e foto.jpg sono due foto diverse: non vanno confuse, né sovrascritte., test_collisione_dimensione_diversa_rinomina(), test_collisione_stessa_dimensione_viene_saltata(), test_dedup_non_attiva_quando_disattivata() (+16 more)

### Community 71 - "esegui"
Cohesion: 0.18
Nodes (12): carica(), esegui(), modulo_disponibile(), Programmi aiutanti: un modo di parlare con il telefono per ogni sistema…, True se il modulo dell'aiutante esiste. Non lo importa: nessun costo all'avvio., Importa il modulo dell'aiutante, o solleva KeyError se non esiste., Esegue un aiutante e restituisce il suo codice di uscita., Trasforma la richiesta di terminare (SIGTERM) in un'uscita ordinata. Il… (+4 more)

### Community 73 - "_RispostaLenta"
Cohesion: 0.25
Nodes (4): Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n…, _risposta_http(), _RispostaLenta, test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato()

### Community 75 - "TrasportoComposto"
Cohesion: 0.09
Nodes (11): Prova i collegamenti disponibili in ordine e usa il primo che trova un…, Riavvia tutti i collegamenti: è quello che l'utente si aspetta dal pulsante., TrasportoComposto, Exception, Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato…, test_composto_pulisci_non_solleva_mai(), test_composto_riavvia_anche_se_un_collegamento_fallisce(), test_composto_salta_il_collegamento_che_solleva_un_errore() (+3 more)

### Community 77 - "DemoAdbBackend"
Cohesion: 0.09
Nodes (21): demo_files(), DemoAdbBackend, Telefono finto: serve per i test automatici e per la modalità demo senza…, Albero di esempio deterministico con foto e video realistici., Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno., hashlib, test_albero_demo_contiene_cartelle_diverse_e_nomi_difficili(), test_cancellazione_di_percorso_inesistente_da_errore() (+13 more)

### Community 78 - "esegui_fino_alla_fine"
Cohesion: 0.12
Nodes (25): AdbDemoAPassi, Telefono finto a passi: identico a :class:`AdbAPassi`, ma senza dispositivo…, Rimuove la cartella di appoggio del telefono finto., esegui_fino_alla_fine(), Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)., Path, _risposta(), test_demo_a_passi_annullabile_senza_residui() (+17 more)

### Community 80 - "comando_copia"
Cohesion: 0.32
Nodes (8): chiudi_sessione(), comando_cancella(), comando_copia(), _dimensione_di(), Chiude la conversazione: è gentile e libera il telefono per altre applicazioni., Il file del telefono che corrisponde al percorso indicato., trova_file(), _valore()

### Community 81 - "_TelefonoFinto"
Cohesion: 0.22
Nodes (6): _piano_singolo(), Il minimo che serve a `transfer`: due metodi., _TelefonoFinto, test_d1_la_copia_conserva_la_data_di_scatto(), test_d21_la_copia_interna_traduce_la_cartella_impossibile_da_creare(), test_d4_il_totale_non_conta_i_file_falliti()

### Community 82 - "leggi_file"
Cohesion: 0.17
Nodes (12): AiutanteNonDisponibile, _leggi_a_blocchi(), leggi_file(), _leggi_scaricando(), _LetturaNonDisponibile, NessunTelefono, Exception, Consegna a ``scrivi`` i byte di un file del telefono, a blocchi. Si prova prima… (+4 more)

### Community 83 - "main"
Cohesion: 0.50
Nodes (4): main(), Guardia: un errore di programmazione continua a dire di che tipo è (serve a…, test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici(), test_d20_un_guaio_imprevisto_resta_riconoscibile()

### Community 84 - "start_gui"
Cohesion: 0.17
Nodes (13): avviso_visibile(), contesto_grafico_dubbio(), Path, Annota un messaggio nel registro di avvio (~/.fotofacile/avvio.log). Se il…, True se non ci sono segnali di una sessione grafica (automazione, servizi,…, Fa vedere un avviso anche quando la finestra del programma non può aprirsi., Apre la finestra principale; se la grafica non è disponibile lo spiega con…, scrivi_log_avvio() (+5 more)

### Community 86 - "G3 — Aiutanti"
Cohesion: 0.06
Nodes (30): `adb.py` e `devices.py`, Altri controlli del gruppo, Altri controlli: `parse_stat_stream` con righe strane, `demo.py`, `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?, Estrazione atomica e guai del disco, Filtrare `.thumbnails`/`cache`/`Stickers` già qui costa meno che poi (vedi Task C4)?, `format_size` / `format_eta` con 0, negativi, `None`, valori enormi?, G1 — Copia e disco (+22 more)

### Community 88 - "FotoFacileError"
Cohesion: 0.10
Nodes (16): errore_disco_componente(), FotoFacileError, Exception, Path, Traduce un errore del sistema (disco, permessi, dispositivo) in una frase utile., Guaio del disco mentre si scarica o si installa il componente di collegamento…, Errore con messaggio per l'utente e un suggerimento su come procedere., traduci_errore_file() (+8 more)

### Community 91 - "comando_elenca"
Cohesion: 0.40
Nodes (6): comando_elenca(), _data_di(), genere_per_nome(), «photo», «video» o ``None`` in base all'estensione del file., Descrizione di un file, nella forma che il programma principale si aspetta., voce_json()

### Community 92 - "leggi_dispositivi"
Cohesion: 0.40
Nodes (5): leggi_dispositivi(), Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati., parametrize, test_leggi_dispositivi_ignora_testi_non_validi(), test_leggi_dispositivi_riconosce_i_campi()

## Knowledge Gaps
- **101 isolated node(s):** `run_tests.sh script`, `Goal`, `Collegamento senza Debug USB (novità principale)`, `Copia piatta`, `Revisione completa` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 672 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FotoFacileError` connect `FotoFacileError` to `pathlib`, `test_adb.py`, `test_regressioni.py`, `App`, `test_osutil.py`, `installer.py`, `attendi`, `ProcessoEsterno`, `page_transfer.py`, `planner.py`, `test_transfer.py`, `AdbBackend`, `AdbAPassi`, `format_size`, `test_robustezza.py`, `.copia`, `Trasporto`, `TrasportoAiutante`, `test_trasporto.py`, `save_report`, `osutil.py`, `test_errore_di_permesso_non_viene_ritentato`, `trasporto_aiutante.py`, `TransferOptions`, `TrasportoComposto`, `esegui_fino_alla_fine`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `App` connect `App` to `pathlib`, `SelectPage`, `widgets.py`, `StepIndicator`, `test_regressioni.py`, `ConnectPage`, `TransferPage`, `DemoAdbBackend`, `History`, `conftest.py`, `ProcessoEsterno`, `TrasportoDemo`, `Trasporto`, `start_gui`, `cli.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `DeviceInfo` connect `DeviceInfo` to `pathlib`, `test_regressioni.py`, `attendi`, `test_page_connect.py`, `page_transfer.py`, `pytest`, `test_page_options.py`, `AdbAPassi`, `format_size`, `TrasportoDemo`, `.copia`, `Trasporto`, `TrasportoAiutante`, `test_trasporto.py`, `TrasportoAdb`, `trasporto_aiutante.py`, `TrasportoComposto`, `esegui_fino_alla_fine`, `leggi_dispositivi`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `FotoFacileError` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`FotoFacileError` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `MediaFile` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`MediaFile` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `DeviceInfo` (e.g. with `AdbAPassi` and `AdbDemoAPassi`) actually correct?**
  _`DeviceInfo` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `DemoAdbBackend` (e.g. with `AdbDemoAPassi` and `AdbError`) actually correct?**
  _`DemoAdbBackend` has 5 INFERRED edges - model-reasoned connections that need verification._
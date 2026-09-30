# Revisione v0.2 — audit per gruppi (Task A7)

Per ogni gruppo di file: le domande del piano, con la risposta scritta. «ok» vuol dire che
il comportamento è stato controllato leggendo il codice (riga indicata); «difetto Dn» vuol
dire che il difetto è stato **riprodotto con un test** in `tests/test_regressioni.py` e
corretto con un commit `fix(Dn): …`. Quello che non si è riusciti a riprodurre è segnato
come «sospetto non confermato»; quello che richiede una scelta di progetto come «da valutare».

I numeri D1–D10 sono della Parte A del piano (D7 e D10 riservati); i difetti nuovi partono
da **D11**. I riferimenti di riga sono quelli **dopo** le correzioni di questo audit.

---

## G1 — Copia e disco

File rivisti: `fotofacile/core/adb_passi.py`, `fotofacile/core/ops.py`,
`fotofacile/core/trasporto_aiutante.py` (con il contesto di chi li chiama:
`core/transfer.py:_passi_di_copia`, `core/trasporto_win.py`, `ui/app.py:run_task/_chiusura`).
Due revisioni indipendenti (lettura diretta + revisore `caveman:cavecrew-reviewer`); sono
stati tenuti solo i difetti confermati leggendo il codice e riprodotti con un test.

### Ogni `.part` viene rimosso in ogni uscita (errore, annullo, `GeneratorExit`)?

**ok**, con i difetti D11 e D13 corretti nelle uscite «di lato».

- `AdbAPassi.copia`: il `.part` nasce dentro il `try` (`ProcessoEsterno.avvia`, `adb_passi.py:265`);
  il `finally` (`adb_passi.py:287-292`) interrompe il comando e, se la copia non è
  completata, cancella il `.part`. Vale per errore, `Annullato`, scadenza e `GeneratorExit`
  (un `finally` scatta anche alla `close()` del generatore). `_controlla_spazio`
  (`adb_passi.py:251`) sta prima del `try`, ma a quel punto il `.part` non esiste ancora.
- `AdbDemoAPassi.copia`: stesso schema, `finally` in `adb_passi.py:441-445`.
- `TrasportoAiutante.copia`: `finally` in `trasporto_aiutante.py:291-298`; se `avvia`
  fallisce dopo aver aperto il `.part`, `processo` resta `None` ma il `.part` viene tolto
  lo stesso (la pulizia non dipende da `processo`).
- `TrasportoWpdWindows.copia` (fuori gruppo, ma usa le stesse funzioni): su Windows il file
  aperto da PowerShell non si cancella subito; `_rimuovi_con_pazienza`
  (`trasporto_win.py:34-49`, chiamata in `:158`) riprova per 1,5 s.
- **difetto D11 (media)** — corretto. Nel collegamento diretto (macOS, Linux) e nella demo
  la cartella di destinazione veniva creata **fuori** dal `try` e il blocco principale
  della copia diretta non traduceva gli `OSError`. Un `OSError` grezzo attraversava
  `transfer` (che intercetta solo `Annullato` e `FotoFacileError`, `transfer.py:238-249`):
  l'intera copia si fermava — anche i file successivi — con «Qualcosa non ha funzionato».
  Ora `trasporto_aiutante.py:253-258`, `:287-290` e `adb_passi.py:409-414` traducono con
  `traduci_errore_file`, come già facevano `AdbAPassi.copia` e `TrasportoWpdWindows.copia`.
  Test: `test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile[aiutante|demo]`,
  `test_d11_errore_del_sistema_durante_la_copia_diretta_da_un_errore_comprensibile`.
- **difetto D13 (bassa)** — corretto. `ProcessoEsterno.avvia` creava il file degli errori
  fuori da ogni `try`: con il disco di sistema pieno usciva un `OSError` grezzo e il file di
  output temporaneo già creato restava in `/tmp`. Ora `ops.py:87-97` lo toglie e spiega
  l'errore. Test: `test_d13_file_degli_errori_impossibile_da_creare`.
- *Sospetto non confermato:* se `termina()` non riesce a uccidere il processo (anche `kill`
  scade, `ops.py:163-167`), su Windows `_pulisci_flussi` potrebbe sollevare `OSError`
  cancellando il file degli errori ancora aperto (`ops.py:257`): l'eccezione uscirebbe dal
  `finally` di `copia` prima della rimozione del `.part`. Richiede un processo non
  uccidibile su Windows: non riproducibile su questo Mac.
- *Da valutare:* il nome del `.part` contiene il numero del processo
  (`percorso_temporaneo`, `adb_passi.py:38-44`). Se il programma viene ucciso di netto
  (corrente staccata, «Termina processo») nessun `finally` scatta e il `.part` resta; alla
  volta successiva il numero è diverso e nessuno lo toglie. Una pulizia dei `*.part`
  orfani all'avvio della copia è una scelta di progetto (bisogna non toccare quelli di
  un'altra finestra aperta).

### `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema?

**ok** — della **cartella di destinazione**: `cartella = destinazione.parent`
(`adb_passi.py:63`), risalendo al primo antenato esistente (`:64-65`), poi
`shutil.disk_usage(cartella)` (`:67`). Un disco esterno viene quindi misurato per quello che è.
Con la dimensione nota si pretende che il file ci stia (`:70-73`); senza, solo 16 MB di
margine (`:74-77`). Test esistenti: `test_disco_pieno_viene_detto_prima_di_iniziare`,
`test_una_foto_piccola_si_copia_anche_con_poco_spazio`, `test_un_video_troppo_grande_viene_fermato_prima`.

- **difetto D12 (bassa)** — corretto. `_esito_di_copia` riconosceva il disco pieno cercando
  «spazio» anche nel **messaggio**, che contiene il nome del file: una foto chiamata
  «Spazio_bimbi.jpg» che falliva per il cavo staccato diventava «Non c'è più spazio».
  Ora si guarda solo il suggerimento, dove finisce il testo del comando (`adb_passi.py:92-96`).
  Test: `test_d12_il_nome_del_file_non_fa_credere_a_un_disco_pieno` (rosso prima) e
  `test_d12_il_disco_pieno_detto_dal_comando_si_riconosce_ancora` (guardia).
- *Da valutare (fuori gruppo, `core/trasporto_win.py:109`):* il collegamento Windows chiama
  `_controlla_spazio(destinazione)` **senza** la dimensione: un video più grande dello spazio
  libero non viene fermato prima, e una foto piccola viene rifiutata sotto i 16 MB liberi
  (proprio il caso corretto per gli altri collegamenti). In più WPD copia prima il file nella
  cartella di appoggio e poi nel `.part`, quindi serve circa il **doppio** dello spazio.
  Da decidere nel gruppo che rivede `trasporto_win.py`.
- *Nota:* i file di appoggio del comando (errori, elenchi) vanno nella cartella temporanea
  di sistema (`ops.py:88`, `:134`), non sul disco di destinazione: con il disco di sistema
  pieno ora l'errore è comprensibile (D13).

### Un processo figlio può restare vivo dopo la chiusura della finestra (zombie, `adb` compreso)?

**ok** per i processi avviati dal programma; **da valutare** per il server di `adb`.

- Alla chiusura `App._chiusura` chiama `annulla_task()` (`app.py:372`), che fa `close()` sul
  generatore in corso: il `GeneratorExit` fa scattare i `finally` che chiamano
  `ProcessoEsterno.termina()` (`adb_passi.py:176`, `:230`, `:290`, `:330`, `:353-356`;
  `trasporto_aiutante.py:180`, `:293`; `ops.py:193-194`). `termina` manda `terminate`, aspetta
  3 s, poi `kill` e altri 3 s (`ops.py:153-168`): il processo viene sempre **raccolto**
  (`wait`), quindi niente zombie. Poi `_pulisci_ambiente` (`app.py:379`) chiama
  `pulisci()`: `TrasportoAiutante.pulisci` interrompe anche ogni aiutante ancora registrato
  (`trasporto_aiutante.py:184-190`). I processi finiti vengono raccolti da `poll()` in
  `_dimentica_finiti` (`:136-142`). Rete di sicurezza: `ProcessoEsterno.__del__` (`ops.py:263-267`).
- Nipoti: su Windows PowerShell riceve `-PidSupervisionato` e si ferma quando l'aiutante
  muore (`aiutanti/wpd_win.py:82-97`); su Linux la copia legge il file nello stesso
  processo (`aiutanti/mtp_linux.py:619-643`), e `gio mount` ha un proprio timeout.
- *Da valutare:* `adb devices` avvia da sé il **server di adb**, che per come è fatto adb
  resta vivo dopo la chiusura del programma (è condiviso con altri strumenti, per esempio
  Android Studio). Non è uno zombie né un processo nostro; chiuderlo con `adb kill-server`
  all'uscita è una scelta di progetto (potrebbe disturbare altri programmi).
- *Sospetto non confermato (fuori gruppo, `ui/app.py:275-286`):* `run_task` sostituisce
  `self._task` senza chiudere il generatore precedente. Oggi i chiamanti controllano
  `task_in_corso` prima di avviare un lavoro, e con CPython il generatore abbandonato viene
  chiuso appena il suo ultimo `tick` esce; non è stato trovato un percorso che lo lasci vivo.

### Timeout: c'è un caso in cui `passo()` non termina mai?

**ok** — nessun ciclo senza uscita. Ogni ciclo `while processo.passo()` controlla
`scaduto()` a ogni giro: `ops.py:181-190` (`aspetta`), `adb_passi.py:214-224`
(`_esegui_ricerca`), `:266-275` (`copia`), `trasporto_aiutante.py:164-173` (`_generatore`),
`:272-281` (`copia`). `scaduto()` usa un orologio monotono (`ops.py:150-151`). Le sole attese
bloccanti sono limitate: `termina` al massimo 3 + 3 s (`ops.py:159-167`); `esito()` usa
`wait()` senza limite (`ops.py:201`) ma viene chiamato solo dopo che `passo()` ha detto che il
processo è finito.

- *Da valutare:* il tempo massimo della copia è **assoluto** dall'avvio (`TIMEOUT_COPIA`
  900 s con adb, `adb_passi.py:33`; 1800 s con l'aiutante, `trasporto_aiutante.py:46`), non
  un tempo di inattività: un video che sta ancora arrivando viene interrotto allo scadere.
  Verificato con un orologio accelerato: la copia viene fermata mentre il `.part` cresce
  (1024 → 6144 byte), con «La copia di v.mp4 è durata troppo tempo.». Un video da 10 GB a
  10 MB/s (circa 1000 s) non passa mai con adb, e l'errore non è ritentabile. Il docstring di
  `AdbAPassi.copia` («il tempo necessario è controllato guardando la dimensione del file a
  metà») promette di più di quello che fa. Passare a un timeout di inattività è una scelta di
  progetto (va coordinata con i tempi di `aiutanti/wpd_win.py:46-51`).
- *Sospetto non confermato (dal secondo revisore):* in `_rallenta_scrittura` un `os.close`
  che fallisce solleverebbe `OSError` (`trasporto_aiutante.py:430`). Non riproducibile senza
  simularlo; in ogni caso dopo D11 verrebbe tradotto in un errore comprensibile.

### Sospetto residuo D12 (aggiunto durante l'audit G2)

- *Da valutare:* dopo D12 il disco pieno si riconosce solo dal **suggerimento**
  (`adb_passi.py:96-97`), ma il suggerimento contiene l'ultima riga dell'errore del comando
  (`ops.py:_suggerimento`), e per adb quella riga riporta di solito il **percorso remoto**
  (per esempio `cat: /sdcard/DCIM/Spazio bimbi/a.jpg: No such file or directory`). Un file o
  una cartella con «Spazio» nel nome può quindi ancora far credere a un disco pieno. Non
  corretto: serve decidere come distinguere il testo del sistema dal nome del file (per
  esempio cercare solo «no space»/«enospc» e la frase italiana esatta dell'aiutante Windows).

---

## G2 — Collegamenti

File rivisti: `fotofacile/core/trasporto.py`, `trasporto_mac.py`, `trasporto_win.py`,
`trasporto_linux.py`, con quello che pilotano: `core/trasporto_aiutante.py`,
`core/scanner.py` (`build_scan_command`, `parse_stat_stream`), `core/adb.py:shell_quote`,
`core/adb_passi.py` (righe di comando di copia e cancellazione), `aiutanti/wpd_win.py`,
`aiutanti/wpd_win.ps1`, `aiutanti/ptp_mac.py`, `aiutanti/mtp_linux.py`, e il chiamante
`core/transfer.py:_passi_di_copia`. Due revisioni indipendenti (lettura diretta + revisore
`caveman:cavecrew-reviewer`); tenuti solo i difetti confermati leggendo il codice e
riprodotti con un test. PowerShell non si può eseguire su questo Mac: quello che riguarda
`wpd_win.ps1` è ragionato sul codice e dichiarato come tale.

### `TrasportoComposto`: cosa succede con due telefoni?

**ok** nel composto, con il difetto **D15** corretto nell'aiutante macOS.

- `TrasportoComposto.dispositivi` (`trasporto.py:265-276`) prova i collegamenti in ordine e
  restituisce **tutti** i telefoni del primo che ne vede almeno uno, ricordando quel
  collegamento (`_scegli`, `:325-328`). La pagina di collegamento usa il primo telefono
  pronto e lo annota nel registro se sono più d'uno (`ui/page_connect.py:286-293`), poi
  smette di sondare (`:298`): da lì in avanti `app.device` non cambia.
- Tutte le operazioni successive passano da `self.attivo` (`trasporto.py:248-250`,
  `:282`, `:295`, `:306`): ricerca, copia e cancellazione vanno allo **stesso**
  collegamento che ha fornito il seriale.
- **difetto D15 (media)** — corretto. L'aiutante macOS, se il telefono indicato con
  `--seriale` non c'era, ripiegava **in silenzio** sul primo telefono collegato
  (`aiutanti/ptp_mac.py:_apri_telefono`). Con due telefoni, copia e cancellazione
  potevano agire su quello non scelto. Ora con più telefoni si ferma con «Non trovo il
  telefono indicato: forse è stato scollegato.» (`ptp_mac.py:409-424`, uscita 3 come per
  Windows); con un telefono solo lo usa come prima, perché non è verificato su un telefono
  vero che l'identificativo (`serialNumber`/`UUIDString`, `ptp_mac.py:202-211`) resti lo
  stesso fra un avvio dell'aiutante e l'altro: rendere il controllo più severo potrebbe
  rompere il caso normale. Test: `test_d15_con_due_telefoni_non_si_usa_quello_sbagliato`
  (rosso prima), `test_d15_con_un_solo_telefono_si_usa_quello` (guardia).
- Windows: `Trova-Dispositivo` (`wpd_win.ps1:157-168`) esce con codice 3 se il seriale non
  corrisponde: **ok** (ragionato sul codice, non eseguito). Linux: `_monta` monta
  esattamente `mtp://<seriale>/` (`mtp_linux.py:416-437`) e il ripiego `jmtpfs` rifiuta
  di scegliere con più telefoni (`:380-387`): **ok**.
- *Da valutare:* l'ordine è «collegamento diretto, poi Debug USB»
  (`trasporto.py:349-357`), ma la docstring di `TrasportoComposto` (`:229-234`) dice che
  chi ha il Debug USB attivo usa il collegamento veloce. In realtà adb si usa solo se il
  collegamento diretto non vede **nessun** telefono. Conseguenze: su Windows, con il Debug
  USB attivo e il telefono in «Trasferimento file», la cancellazione non è disponibile
  anche se adb saprebbe farla; e un secondo telefono visibile solo via adb non compare.
  Scelta di progetto (ordine o docstring).
- *Sospetto non confermato:* dopo «Riavvia collegamento» `_scelto` torna `None`
  (`trasporto.py:315`) e `attivo` diventa il primo collegamento. Se il controllo successivo
  fallisce, `_controllo_fallito` (`ui/page_connect.py:271-283`) non azzera `app.device`:
  si potrebbe proseguire con un seriale di adb dato al collegamento diretto. Non trovato un
  percorso dell'interfaccia che lo permetta davvero (con un telefono solo, D15 lascia
  comunque usare quello).

### Il numero seriale è stabile fra ricerca e copia (stessa `serial` usata da `cancella`)?

**ok** — e il percorso remoto è lo stesso.

- Il seriale nasce una volta sola in `page_connect` (`app.device`) e viene passato uguale a
  ricerca (`ui/page_select.py:157-158`), piano e copia (`ui/page_transfer.py:119-138`) e da
  `transfer` sia a `copia` sia a `cancella` (`core/transfer.py:228-230`, `:285`).
- Il **percorso remoto** di `cancella` è lo stesso oggetto passato a `copia`:
  `pianificato.media.remote_path` (`transfer.py:230` e `:285`). Con adb entrambi passano da
  `shell_quote` allo stesso modo (`adb_passi.py:254` `exec-out cat` e `:322` `shell rm -f`);
  con gli aiutanti entrambi come `--percorso remoto` in un elenco di argomenti, senza shell
  (`trasporto_aiutante.py:266`, `:303`); l'aiutante macOS usa per entrambi `trova_file` con
  lo stesso confronto esatto (`ptp_mac.py:427-433`), quello Linux `percorso_di_filesystem`
  (`mtp_linux.py:484-496`, `:625`, `:652`).
- **difetto D14 (alta)** — corretto. `TrasportoMtpLinux.copia` non accettava
  `remoto_dimensione`, che `transfer` passa **sempre** (`transfer.py:236`, anche attraverso
  `TrasportoComposto.copia`, `trasporto.py:301`). Su Linux, con il collegamento diretto, ogni
  copia finiva in un `TypeError`: nessuna foto copiata. Ora la firma è quella del protocollo
  e il valore arriva a `TrasportoAiutante.copia` (`trasporto_linux.py:69-87`). Test:
  `test_d14_la_copia_diretta_su_linux_accetta_la_dimensione`.
- *Sospetto non confermato:* l'aiutante macOS ricava il seriale da `serialNumber`, poi
  `UUIDString`, poi il nome (`ptp_mac.py:202-211`). Due telefoni dello stesso modello senza
  i primi due avrebbero lo stesso seriale. Non verificabile senza telefoni veri.

### Nomi di file con `'`, `$`, `"`, emoji e `|` passano intatti da `wpd_win.ps1` e da `scanner.build_scan_command`?

**ok** per il quoting di shell (nessun comando eseguibile, nessuna uscita dalla cartella);
**difetto D16** per la codifica dei caratteri.

- `build_scan_command` (`scanner.py:112-126`): i nomi dei file **non** entrano mai nel
  comando; le radici sono costanti quotate con `shell_quote`; `find` stampa i percorsi,
  `while IFS= read -r f` li legge senza interpretarli e `stat … "$f"` li usa quotati.
  `parse_stat_stream` separa solo i primi due `|` (`scanner.py:96-97`), quindi un `|` nel
  nome resta. Verificato eseguendo il comando con `/bin/sh` su una cartella con
  `a'b.jpg`, `x$(touch PWNED).jpg`, ``q"uo`te`.jpg``, `pi|pe.jpg`, `emoji 😀 città.jpg`,
  `  spazi  .jpg`, `-meno.jpg`, `back\slash.jpg`, `$HOME.jpg`, `..jpg`, `a;rm -rf x.jpg`:
  tutti e 11 ritrovati intatti e riletti con `cat <shell_quote(percorso)>` (come fa
  `adb exec-out`), nessun `PWNED` creato. Un nome con un a-capo viene spezzato in due righe
  che `stat` non trova: il file viene saltato, senza danni.
- `shell_quote` (`adb.py:51-53`) chiude fra apici singoli e trasforma `'` in `'\''`: dentro
  gli apici `$`, `"`, `` ` ``, `|`, `;` sono letterali. Il percorso comincia sempre con `/`,
  quindi non può essere scambiato per un'opzione di `cat`/`rm`. Il seriale va ad adb come
  argomento separato (`-s`, `adb_passi.py:208`, `:254`, `:322`), senza shell.
- Gli aiutanti ricevono percorso e seriale come elementi di una lista (`subprocess`, niente
  shell: `ops.py:103-110`); `wpd_win.py` li passa a PowerShell ancora come lista
  (`wpd_win.py:86-107`, `:159-164`). Con `-File` PowerShell tratta gli argomenti come testo
  letterale (niente espansione di `$`); su Windows gli argomenti viaggiano in Unicode
  (`CreateProcessW`), quindi emoji e accenti arrivano intatti. Dentro lo script il percorso
  si usa solo per confronti di nomi (`Trova-Voce`, `wpd_win.ps1:246-274`) e i file locali
  solo con `-LiteralPath` (`:300`, `:311`, `:316`, `:330`, `:366`): nessun carattere jolly
  interpretato. *Non verificato su Windows:* il caso di `"` dentro un argomento (Python lo
  scrive come `\"`, PowerShell 5.1 dovrebbe rileggerlo come `"`).
- Uscita dalla cartella di destinazione: il nome di destinazione passa da `_nome_sicuro`
  (`planner.py:98-108`), che sostituisce `/`, `\` e `<>:"|?*` e trasforma `.` e `..` in
  `senza_nome`; con la struttura delle cartelle attiva lo stesso vale per ogni cartella
  (`planner.py:94`). Sul lato telefono l'aiutante Linux rifiuta `.` e `..`
  (`mtp_linux.py:484-496`). **ok**.
- **difetto D16 (media, Windows)** — corretto. L'elenco delle foto veniva riletto con la
  **codifica di sistema** (`trasporto_aiutante.py:210`, `:239`; `ops.py:220` per adb), ma è
  UTF-8: JSON scritto byte per byte dallo script Windows (`wpd_win.ps1:54-58`) e nomi dei
  file così come li scrive Android. Su Windows la codifica di sistema è cp1252:
  «Città 😀.jpg» diventava «CittÃ  ðŸ˜€.jpg», la copia chiedeva al telefono un file che non
  esiste e **ogni foto con accenti o emoji nel nome non veniva copiata** (con adb e con il
  collegamento diretto). Ora l'output si legge in UTF-8, e gli aiutanti Python scrivono JSON
  solo ASCII (`ptp_mac.py:393-397`, `mtp_linux.py:551-555`), così la lettura non dipende
  dalla loro codifica. Su questo Mac la codifica di sistema è sempre UTF-8: il test simula
  quella di Windows. Test: `test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji`,
  `test_d16_la_ricerca_con_adb_conserva_accenti_ed_emoji` (rossi prima),
  `test_d16_gli_aiutanti_scrivono_righe_leggibili_con_ogni_codifica[ptp_mac|mtp_linux]`.
- *Da valutare (bassa, Windows):* anche il **testo degli errori** (`ops.py:228`) si legge
  con la codifica di sistema, ma su Windows arriva misto: lo script PowerShell scrive UTF-8
  (`wpd_win.ps1:60-64`), `wpd_win.py` scrive con la codifica di sistema (`wpd_win.py:120-123`,
  `:166-171`). Oggi i messaggi di PowerShell compaiono nel «dettaglio» con gli accenti
  rovinati («piÃ¹»); il disco pieno si riconosce comunque («spazio» resta leggibile). Per
  sistemarlo bisogna far scrivere anche `wpd_win.py` in UTF-8 e poi leggere in UTF-8:
  non verificabile qui.
- **Sospetto non verificato (potenzialmente grave, solo Windows):** lo script usa
  `FolderItem.Name` come nome del file (`wpd_win.ps1:113-115`, usato in `:217-233` e
  `:262`). È il **nome mostrato** da Esplora file: con l'opzione predefinita di Windows
  «Nascondi le estensioni per i tipi di file conosciuti» potrebbe arrivare `IMG_001` invece
  di `IMG_001.jpg`, e allora `Genere-File` (`:194-201`) scarterebbe **tutte** le foto. Va
  provato su un Windows vero con un telefono; se confermato, il nome va letto da
  `ExtendedProperty("System.FileName")`. **Passato a G3**: rischio giudicato fondato e
  corretto in modo difensivo come **D17** (vedi «G3 — Aiutanti»); la correzione **non è
  verificata su un Windows vero**.
- *Sospetto non verificato (Windows):* un nome valido su Android ma non su Windows
  (`a|b.jpg`, `a:b.jpg`) va copiato con `CopyHere` nella cartella di appoggio; se Windows lo
  rifiuta (errori soppressi dal flag `0x400`, `wpd_win.ps1:105`) lo script aspetta 120 s
  prima di dire «Il telefono non ha consegnato il file.» (`:321-324`), e la copia viene
  ritentata. Non verificabile qui.
- *Sospetto non verificato:* `Trova-Voce` confronta i nomi con `-eq`, che in PowerShell
  **non** distingue maiuscole e minuscole (`wpd_win.ps1:262`): due file che differiscono solo
  per le maiuscole verrebbero confusi. Sulla memoria interna di Android (che non le
  distingue) non possono esistere; forse su una scheda SD.
- *Da valutare (bassa):* `leggi_elenco` e `parse_stat_stream` tolgono gli spazi in fondo alla
  riga (`trasporto_aiutante.py:377`, `scanner.py:93`). Un file chiamato `foto.jpg ` (con uno
  spazio finale) viene elencato come `foto.jpg` e la sua copia fallisce con «non trovo più il
  file»; senza la pulizia sarebbe stato ignorato (l'estensione sarebbe `jpg `). Effetto
  trascurabile, nessun file sbagliato toccato.
- *Da valutare (dal G1, `trasporto_win.py:109`):* il collegamento Windows controlla lo
  spazio **senza** la dimensione del file (`_controlla_spazio(destinazione)`): una foto
  piccola viene rifiutata sotto i 16 MB liberi. I file grandi sono comunque fermati dallo
  script (che pretende il doppio della dimensione più 4 MB, `wpd_win.ps1:298-306`) con un
  messaggio che si riconosce come disco pieno. Passare la dimensione (e quanto: una o due
  volte) è una scelta di progetto: non corretto.

---

## G3 — Aiutanti

File rivisti: `fotofacile/aiutanti/__init__.py`, `ptp_mac.py`, `mtp_linux.py`, `wpd_win.py`,
`wpd_win.ps1`, con quello che li avvia, li ferma e ne legge l'uscita: `cli.py:esegui_aiutante`,
`core/trasporto_aiutante.py` (`leggi_elenco`, `_generatore`, `copia`),
`core/trasporto_linux.py:pulisci`, `core/ops.py` (`termina`, `_suggerimento`). Due revisioni
(lettura diretta + revisore `caveman:cavecrew-reviewer`, che non ha trovato altri difetti
oltre a quelli già corretti); tenuti solo i difetti confermati leggendo il codice e
riprodotti con un test. PowerShell non si può eseguire su questo Mac:
quello che riguarda `wpd_win.ps1` è ragionato sul codice e dichiarato come tale. Dopo D17 i
numeri di riga di `wpd_win.ps1` citati nel G2 oltre la riga 201 sono scalati di 38–42 righe.

### Ogni uscita di errore ha codice 2/3 e messaggio umano su `stderr`?

**ok** per i codici, con il difetto **D20** corretto nel messaggio dell'aiutante macOS e il
difetto **D19** corretto nell'uscita per interruzione.

- `ptp_mac.main` (`ptp_mac.py:534-556`): comando mancante o sconosciuto → 2 con una frase;
  `NessunTelefono` → 3; tutto il resto → 2 (c'è un `except Exception`: nessuna eccezione esce
  da `main`). Anche `cli.esegui_aiutante` (`cli.py:288-310`) risponde 2 con una frase se
  l'aiutante non esiste o non si lascia importare.
- **difetto D20 (bassa, macOS)** — corretto. I guai previsti dell'aiutante macOS (file
  sparito, sessione che non si apre, file incompleto, argomento mancante) sono frasi italiane
  sollevate come `OSError`/`ValueError`, ma `main` le stampava con il nome della classe: la
  persona leggeva nel dettaglio dell'errore (`ops.py:_suggerimento`) «(dettaglio: OSError: Sul
  telefono non trovo più il file …)». Ora `ptp_mac.py:549-553` scrive solo la frase; gli
  errori imprevisti dicono ancora il loro tipo. Test:
  `test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici` (rosso prima),
  `test_d20_un_guaio_imprevisto_resta_riconoscibile` (guardia).
- `mtp_linux.main` (`mtp_linux.py:703-724`): `GuaioMtp` porta il suo codice (2, oppure 3 per
  `NessunTelefono`, `:59-79`) e scrive motivo e suggerimento; gli errori imprevisti → 2 con
  `Tipo: messaggio`. *Nota:* con Python < 3.12 `Path.is_file()`/`exists()` su un montaggio gvfs
  che risponde `EIO`/`EACCES` solleva invece di dire `False` (`comando_copia`,
  `comando_cancella`) e il dettaglio mostrato sarebbe tecnico («PermissionError: …»), sempre
  con codice 2. Con il Python del progetto (3.14) non succede.
- `wpd_win.py` (`:110-124`, `:127-173`): i codici di PowerShell diversi da 0/2/3 (per esempio 1
  per un errore di sintassi o di parametri) diventano 2 con una frase italiana; tempo scaduto
  e PowerShell mancante → 2 con una frase.
- `wpd_win.ps1` (ragionato, non eseguito): con `$ErrorActionPreference = "Stop"` (`:44`) ogni
  errore e ogni `throw` finiscono nel `catch` finale → messaggio + `exit 2` (`:470-481`);
  `Esci-SenzaTelefono` → `exit 3` (`:66-69`); la cancellazione → `exit 2` con due frasi
  (`:457-466`). `exit` dentro una funzione non è un'eccezione: il `catch` non trasforma il 3 in 2.
- **difetto D19 (bassa, macOS e Linux)** — corretto. Il programma principale ferma l'aiutante
  con SIGTERM (`ops.py:153-168`) quando si annulla, scade il tempo o si chiude la finestra.
  Senza un gestore Python moriva all'istante e **nessun `finally` scattava**: su macOS restava
  in `$TMPDIR` la cartella `fotofacile-ptp-*` con la foto scaricata (il ripiego per i telefoni
  che non consegnano a blocchi, `ptp_mac.py:352-390`); su Linux restavano vivi e orfani i
  comandi figli (`jmtpfs`, `gio mount`, che con un telefono bloccato può restare appeso) e la
  cartella di montaggio vuota. Ora `aiutanti/__init__.py:44-78` trasforma SIGTERM in
  `SystemExit(2)` per tutta la durata dell'aiutante (e poi rimette il gestore di prima, così
  chi chiama `esegui` nello stesso processo, come i test, non cambia): le pulizie scattano,
  `subprocess.run` uccide il comando figlio, e `_monta_jmtpfs` toglie la cartella di montaggio
  (`mtp_linux.py:399-405`). Su Windows il segnale non arriva (l'aiutante viene chiuso di
  netto): lì resta la sorveglianza di PowerShell (`-PidSupervisionato`, `wpd_win.ps1:71-84`).
  Test, con l'aiutante vero in un processo a parte fermato con `terminate()`:
  `test_d19_macos_interrotto_non_lascia_la_foto_nella_cartella_temporanea`,
  `test_d19_linux_interrotto_non_lascia_comandi_orfani` (entrambi rossi prima).

### Le righe JSON con `\n` dentro i nomi sono gestite?

**ok** per gli aiutanti Python (verificato); ragionato per PowerShell.

- `ptp_mac._stampa_riga` e `mtp_linux._stampa_riga` (`ptp_mac.py:396-400`,
  `mtp_linux.py:556-560`) usano `json.dumps` con `ensure_ascii`: `\n`, `\r` e anche i
  separatori che `str.splitlines()` taglierebbe in `leggi_elenco` (`\x85`, ` `) diventano
  sequenze di escape, una riga per file. Verificato con l'aiutante Linux su file veri chiamati
  `a\nb.jpg`, `c d.jpg`, `e\x85f.jpg`, `g\rh.jpg`: 4 righe più quella di fine, nomi
  intatti dopo `leggi_elenco`. Test di guardia:
  `test_aiutante_linux_nomi_con_a_capo_restano_una_riga` (`tests/test_trasporto.py`). Il
  percorso torna all'aiutante come elemento di una lista di argomenti (niente shell), quindi
  anche copia e cancellazione ricevono il nome intatto.
- `wpd_win.ps1`: `ConvertTo-Json -Compress` (`:283`) scrive una riga sola e trasforma in escape
  i caratteri di controllo (`\n`, `\r`). *Sospetto non verificato (Windows, bassa):* non è
  verificato che Windows PowerShell 5.1 trasformi in escape anche `\u0085`/` `/` `;
  se non lo fa, `leggi_elenco` (`trasporto_aiutante.py:367`, `splitlines()`) spezza la riga e
  quel solo file viene **saltato** (nessun danno ad altri file). Per chiuderlo basterebbe
  dividere solo su `"\n"` (fuori gruppo); non riproducibile qui.

### Il `.ps1` mantiene il BOM dopo ogni modifica?

**ok**. Dopo la modifica di D17 i primi tre byte di `wpd_win.ps1` sono `EF BB BF` (verificato
con `xxd`; `file` dice «UTF-8 (with BOM)»; fine riga invariati). Lo sorvegliano tre test:
`test_gli_script_powershell_hanno_il_bom` (`tests/test_regressioni.py:404-412`, tutti i `.ps1`
del progetto), `test_il_pacchetto_porta_l_aiutante_per_windows`
(`tests/test_pacchetto_windows.py:110-119`, la copia nel pacchetto per Windows) e la nuova
guardia `test_d17_lo_script_windows_resta_ben_formato` (BOM e parentesi bilanciate).

### Filtrare `.thumbnails`/`cache`/`Stickers` già qui costa meno che poi (vedi Task C4)?

**Da valutare nella Parte C** (non corretto, come previsto). Costo concreto: gli aiutanti
scendono in **ogni** cartella (`ptp_mac.cammina`, `mtp_linux.cammina`, `Elenca-Cartella`) e
`DCIM/.thumbnails` contiene di solito una miniatura per foto, quindi l'elenco e le righe JSON
possono raddoppiare. Pesa soprattutto su Windows, dove ogni file costa chiamate COM
(`Dimensione-Voce`, `Data-Voce`: fino a 4 `ExtendedProperty`) e, dopo D17 con le estensioni
nascoste, una in più per il nome. Saltare negli aiutanti le cartelle il cui nome comincia con
«.» eviterebbe la discesa (una riga per aiutante); `cache` e `Stickers` sono rari fra le
cartelle delle foto e si possono lasciare al filtro di pagina.

### Sospetto ereditato dal G2: `FolderItem.Name` senza estensione (`wpd_win.ps1`)

- **difetto D17 (alta, solo Windows)** — corretto in modo difensivo, **non verificato su un
  Windows vero**. Rischio giudicato fondato: `FolderItem.Name` è il nome visualizzato, lo
  stesso di Esplora file, che con «Nascondi le estensioni per i tipi di file conosciuti»
  (attiva di default) mostra «IMG_001» anche sulle foto del telefono. Con quel nome
  `Genere-File` (`:194-201`) non trova il punto e scarta il file: **nessuna foto elencata**
  con il collegamento diretto di Windows. Correzione: `Nome-File` (`wpd_win.ps1:203-227`) usa il
  nome mostrato se è già quello di una foto o di un video (nessun costo in più e comportamento
  identico a prima quando le estensioni sono visibili), altrimenti legge
  `ExtendedProperty("System.FileName")` e, come ultimo ripiego, aggiunge al nome mostrato
  `System.FileExtension`. `Elenca-Cartella` decide il genere sul nome completo (`:270-274`);
  `Trova-Voce` confronta con `Test-StessoNome` (`:229-239`, usato in `:304`), che chiede il
  nome completo solo quando il nome mostrato è l'inizio di quello cercato (una cartella con
  migliaia di foto non costa migliaia di domande in più per ogni copia); `Comando-Copia`
  aspetta il file con il nome completo (`:414`). Solo sintassi di Windows PowerShell 5.1. Test:
  `test_d17_lo_script_windows_usa_il_nome_completo_dei_file` (contratto sul testo dello
  script, rosso prima), `test_d17_lo_script_windows_resta_ben_formato` (guardia).
- *Da verificare su Windows vero:* (1) che `.Name` sul telefono arrivi davvero senza
  estensione con l'opzione attiva (se non succede D17 non cambia niente: il nome mostrato ha
  già l'estensione); (2) che `System.FileName` sia disponibile sulle voci WPD (se non lo è,
  resta il ripiego con `System.FileExtension`); (3) i tempi dell'elenco con molte foto e le
  estensioni nascoste. Limiti noti: se Windows mostrasse un nome che non è l'inizio del nome
  vero (non visto con Android), il file verrebbe elencato ma la copia direbbe «non trovo più il
  file» (prima non veniva proprio elencato); con le estensioni nascoste una cartella «X» e un
  file «X.jpg» nella stessa cartella si confondono in `Trova-Voce`.

### Altri controlli del gruppo

- **difetto D18 (alta, macOS)** — corretto. `ptp_mac.cammina` evitava le voci ripetute
  ricordando solo `id(voce)`. Ogni voce è un proxy PyObjC: quando una cartella è finita i suoi
  proxy vengono liberati e quelli della cartella successiva ne riusano la memoria, quindi lo
  stesso `id`. Misurato con PyObjC vero su questo Mac: **48 proxy su 50** di un secondo
  `NSArray` riusavano un `id` del primo (0 su 50 tenendo i riferimenti). Effetto: con più
  cartelle di foto (Camera, Screenshots, Pictures…) i file delle cartelle visitate dopo la
  prima **sparivano in silenzio** dall'elenco, e la loro copia (`trova_file`, che usa la stessa
  `cammina`) diceva «non trovo più il file». Ora le voci viste restano tenute
  (`ptp_mac.py:231-243`), così il loro `id` non può passare a un'altra voce; la difesa contro
  le voci ripetute resta. Non provato con un telefono vero. Test:
  `test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive` (proxy finti che, come
  quelli veri, riusano la memoria appena liberata; rosso prima: 6 file su 10),
  `test_d18_una_voce_ripetuta_si_elenca_una_volta_sola` (guardia).
- Pulizia in ogni uscita: `ptp_mac` chiude la sessione in un `finally` (`comando_elenca`,
  `comando_copia`, `comando_cancella`) e ferma la ricerca dei dispositivi (`trova_telefoni`,
  `:162-169`); la cartella del ripiego è un `TemporaryDirectory` (`:365`). `mtp_linux` usa solo
  `subprocess.run` con un tempo massimo (`_esegui`, `:94-111`), che uccide il figlio anche su
  `SystemExit` (dopo D19). `wpd_win.py` usa `subprocess.run` con un tempo massimo, che uccide
  PowerShell; `wpd_win.ps1` chiude il file letto in un `finally` (`:452-454`) e la cartella di
  appoggio è del programma principale. Con D19 tutto questo vale anche per l'interruzione;
  resta fuori solo SIGKILL (dopo 3 s), che non si può intercettare. **ok**.
- Linux, montaggi: i montaggi gvfs si indicano sempre per seriale (`gio mount
  mtp://<seriale>/`, `mtp_linux.py:439`; `smonta`, `:464-483`); le cartelle jmtpfs si
  cancellano solo se non sono più montate **e** sono nostre (`_smonta_percorso`,
  `_cartella_nostra`, `:319-355`); `TrasportoMtpLinux.pulisci` smonta solo i telefoni usati in
  questa sessione (`trasporto_linux.py:94-115`). **ok**, con tre note:
  - *Da valutare (bassa):* se il telefono era **già** montato dal desktop prima di FotoFacile
    (per esempio aperto in «File»), alla chiusura viene smontato lo stesso e la finestra di
    «File» sul telefono si chiude. La docstring (`trasporto_linux.py:97-99`) dice che è
    «quello che fa anche il gestore file», ma il gestore file non smonta quando si chiude la
    finestra. Ricordarsi se il montaggio c'era già è una scelta di progetto; nessun file toccato.
  - *Sospetto non confermato (bassa):* `_punto_jmtpfs` (`:357-367`) riusa come telefono
    qualunque cartella montata scritta nel file di stato, senza il controllo `_cartella_nostra`
    che protegge `rmtree`. Solo con un file di stato alterato a mano (lo scrive solo
    l'aiutante, con percorsi da `mkdtemp`) si potrebbero elencare o cancellare file di un altro
    montaggio. Non riproducibile senza alterarlo.
  - `comando_smonta` senza `--seriale` (`:675-691`) smonterebbe tutti i telefoni visti, anche
    quelli non nostri; oggi nessuno lo chiama così (`trasporto_linux.py:106` passa sempre il
    seriale).
- *Sospetto non confermato (macOS, serve un telefono):* `apri_sessione` ed `enumera`
  (`ptp_mac.py:172-199`) non distinguono «tempo scaduto» da «riuscito»: se il telefono non
  risponde entro 15 s / 120 s si prosegue, e un elenco vuoto o parziale verrebbe presentato
  come «0 foto» (l'aiutante Linux invece rifiuta apposta un «0 foto» tranquillo,
  `mtp_linux.py:516-522`). Correzione proposta: sollevare `OSError` quando `attesa.fatto` è
  falso. Non corretta: dipende da come ImageCaptureCore si comporta con un telefono bloccato.
- *Sospetto non confermato (macOS, serve un telefono):* `comando_cancella`
  (`ptp_mac.py:506-523`) passa `None` come blocco `deleteFailed` e considera riuscita la
  cancellazione se il completamento non riporta un errore, anche quando scadono i 15 s senza
  risposta. Una cancellazione non avvenuta verrebbe contata come fatta: il file resta sul
  telefono (direzione sicura, nessuna foto persa) ma il riepilogo sarebbe sbagliato.

---

## G4 — Download componente

File rivisti: `fotofacile/core/installer.py`, `fotofacile/core/adb.py`, `fotofacile/core/devices.py`,
con quello che scarica davvero il componente per la finestra (`core/ops.py:ScaricatoreAPassi`) e
chi lo avvia (`ui/page_connect.py:install_component`, `ui/app.py:run_task`). Per il sospetto
ereditato dal G1, anche `core/transfer.py:download_file_stream` (solo quel punto). Due
revisioni (lettura diretta + revisore `caveman:cavecrew-reviewer`); tenuti solo i difetti
confermati leggendo il codice e riprodotti con un test. Nessun test fa richieste di rete: le
risposte anomale sono simulate; il comportamento vero di `urllib` è stato misurato a parte con
un piccolo server su `127.0.0.1` (risposta troncata, risposta non HTTP, rete lenta).

Nota su come si arriva agli errori: `App.run_task` chiama `on_error` **solo** per i
`FotoFacileError` (`app.py:298-305`); qualunque altra eccezione diventa «Qualcosa non ha
funzionato» (`:306-315`) e `_componente_fallito` (`page_connect.py:398-402`) non viene chiamato,
quindi il pulsante «Installa componente mancante», disattivato all'avvio del download
(`:381`), **resta disattivato**. Per questo D22 e D23 non sono solo messaggi brutti.

### Zip-slip: l'estrazione rifiuta i percorsi con `..` o assoluti?

**ok** — per costruzione non si può uscire dalla cartella di appoggio. `_scompatta`
(`installer.py:190-206`) **appiattisce** ogni voce: prende solo l'ultimo pezzo del nome
(`Path(membro).name`, `:197`) e salta i nomi vuoti o che cominciano con «.» (`:198-199`, quindi
anche `..`). Verificato con un archivio costruito apposta, estratto con `_scompatta`: `../../fuori1`,
`/tmp/…-assoluto`, `C:/Windows/fuori4` finiscono **dentro** la cartella come `fuori1`,
`…-assoluto`, `fuori4`; `..` e `platform-tools/..` saltati; nessun file fuori, nessun file in
`/tmp`. Con `PureWindowsPath` (come su Windows) anche `a\..\..\fuori3`, `\\server\share\x`, `C:`,
`C:..` si riducono a un nome semplice o vengono saltati; su macOS/Linux la barra rovesciata è un
carattere normale e `a\..\..\fuori3` resta un **nome** (innocuo) dentro la cartella.
**Link simbolici:** `zipfile` non crea mai link; una voce marcata come link diventa un file
normale che contiene il testo del bersaglio (verificato: `collegamento` → file con `/etc/passwd`
dentro, `is_symlink()` falso). La cartella di appoggio è nuova (`TemporaryDirectory`, `:154`),
quindi non ci sono link preesistenti da seguire.

- *Da valutare (bassa, solo con un archivio manomesso):* su Windows un nome come `adb.exe:x`
  scriverebbe un flusso alternativo NTFS **dentro** la cartella, e i nomi di dispositivo
  (`CON`, `AUX.txt`) sui Windows più vecchi aprirebbero il dispositivo invece di un file. Nessuna
  uscita dalla cartella; l'archivio vero arriva da `dl.google.com` in HTTPS e con l'impronta del
  catalogo. Nessun limite alla dimensione estratta (una «bomba zip» riempirebbe il disco): stesso
  presupposto.
- *Sospetto non confermato (Linux/macOS, serve il pacchetto vero):* l'appiattimento porta
  in cima anche `lib64/…` (se il pacchetto la contiene). Se `adb` avesse bisogno di trovarla in
  `lib64/`, `_verifica_eseguibile` (`:209-227`) lo scoprirebbe e l'installazione fallirebbe con
  «Il componente scaricato non funziona su questo computer» senza toccare quella vecchia. Non
  verificabile senza scaricare il pacchetto.

### L'impronta è verificata **prima** di estrarre?

**ok**, con due limiti da valutare. L'impronta viene controllata dal `validatore`, che gira sul
file `.scarico` **prima** che prenda il suo nome (`ops.py:344-346`; `installer.py:278-280` per la
versione non a passi); l'estrazione (`installer.py:399`) avviene solo dopo. `controlla_archivio`
(`:295-331`) verifica in ordine dimensione minima (1 MB, `:309`), impronta (`:314-326`) e
struttura zip (`:327`). Un'impronta sbagliata → «non corrisponde a quello ufficiale», il file
viene tolto (`finally` di `scarica`) e il pacchetto non esiste mai. Test esistenti:
`test_archivio_manomesso_viene_rifiutato`, `test_archivio_con_impronta_giusta_viene_accettato`.

- *Precisazione:* non è SHA-256. Il catalogo di Google pubblica **SHA-1** (40 cifre); l'algoritmo
  si sceglie dalla lunghezza (`ALGORITMI_PER_LUNGHEZZA`, `:40`), quindi uno SHA-256 verrebbe
  controllato come tale se il catalogo lo pubblicasse.
- *Da valutare:* senza catalogo (rete lenta oltre 6 s, catalogo illeggibile) si scarica
  l'indirizzo «latest» **senza impronta** (`risolvi_sorgente`, `:363-373`, scelta documentata):
  restano HTTPS, dimensione minima, struttura zip e la prova `adb version`. Un'impronta di
  lunghezza sconosciuta viene ignorata invece di rifiutare il file (`:317-320`).

### Rete assente o lenta: c'è un timeout e un messaggio?

**ok** per rete assente e server in errore; **difetti D22 e D24** per risposte anomale e rete
lenta.

- Rete assente, nome del server non risolto, connessione rifiutata, HTTP non-200: `urlopen`
  solleva `URLError`/`HTTPError`, che sono `OSError` → «Non sono riuscito a scaricare il
  componente di collegamento.» + «Controlla la connessione a internet e riprova.»
  (`ops.py:350-355`). Test esistente: `test_download_senza_rete_spiega_cosa_fare`.
- Timeout: 60 s per ogni operazione del socket nel download (`ops.py:295`), 6 s per il catalogo
  (`installer.py:46`), 30 s per la prova di `adb` (`:215`). Lo scadere è un `TimeoutError`
  (`OSError`) → stesso messaggio.
- Reindirizzamenti: `urllib` li segue da solo (al massimo 10; un ciclo diventa `HTTPError`,
  quindi il messaggio sopra). *Da valutare:* accetta anche il passaggio da `https` a `http`; con
  l'impronta del catalogo un file alterato viene comunque rifiutato, senza catalogo no.
- Download interrotto: il file `.scarico` viene tolto in ogni uscita, compresi annullamento e
  `GeneratorExit` (`ops.py:356-363`), e `installa_a_passi` toglie anche il pacchetto
  (`installer.py:400-403`). Una risposta **troncata** (meno byte del dichiarato) viene
  scartata dal controllo di dimensione o dalla struttura zip. Test:
  `test_scaricatore_abbandonato_non_lascia_file_a_meta` e i nuovi test D22/D23.
- **difetto D22 (media)** — corretto. `http.client` segnala una risposta interrotta a metà di un
  trasferimento a pezzi (`IncompleteRead`) o una risposta non HTTP, per esempio di un proxy o di
  una rete con pagina di accesso (`BadStatusLine`), con eccezioni che **non** sono `OSError`
  (verificato con `urlopen` e un server locale). Uscivano grezze dal download e dal catalogo:
  «Qualcosa non ha funzionato» e pulsante «Installa» disattivato. Ora `ops.py:350-351`,
  `installer.py:88` e `:284` le trattano come gli errori di rete (il catalogo ripiega su
  «latest» come per gli altri guasti). Test:
  `test_d22_una_risposta_di_rete_anomala_da_un_errore_comprensibile[troncata|non_http]`.
- **difetto D24 (bassa)** — corretto. Ogni passo del download chiedeva `read(256 KB)`: su una
  rete lenta quella chiamata **aspetta** tutti i 256 KB. Misurato con un server locale che manda
  1 KB ogni 50 ms: `read(256 KB)` è tornata dopo **2,1 s**, `read1` subito. La finestra restava
  ferma per secondi a ogni passo (a 20 KB/s circa 13 s) e «Annulla» non rispondeva. Ora si usa
  `read1` (`ops.py:322-324`, `:333`): con lo stesso server il passo più lungo dura 55 ms. Test:
  `test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato` (contratto: la
  risposta finta fallisce se le si chiede `read`).
- *Da valutare:* restano bloccanti, per scelta (niente thread), l'apertura della connessione
  (fino a 60 s, e la risoluzione del nome non ha limite di tempo) e la lettura del catalogo
  (6 s per operazione, documentato in `installer.py:43-45`).

### Estrazione atomica e guai del disco

**ok** l'atomicità, **difetto D23** per i messaggi. `_estrai_e_sostituisci`
(`installer.py:151-187`) estrae in una cartella di appoggio accanto a quella finale (stesso
disco, quindi `replace` è un rinomina), prova `adb version` (`:166-169`), sposta la vecchia in
`platform-tools.precedente` (`:178`), mette la nuova al suo posto (`:180`) e rimette la vecchia se
questo fallisce (`:181-185`). Se il programma viene ucciso fra i due spostamenti, la volta dopo
la copia di ripiego viene rimessa a posto prima di cancellarla (`:171-175`); nel frattempo
`adb` non si trova e il pulsante «Installa» ricompare.

- **difetto D23 (media)** — corretto. I guai del **disco** non erano detti come tali: se la
  cartella `.fotofacile` non si poteva creare (un file con lo stesso nome, cartella personale
  protetta: `mkdir` fuori da ogni `try` in `ScaricatoreAPassi.scarica`) o il disco si riempiva
  durante l'estrazione (`_scompatta`/`replace` non protetti) usciva un `OSError` grezzo:
  «Qualcosa non ha funzionato» e pulsante disattivato. Se il disco si riempiva durante il
  download il messaggio diceva di controllare la connessione a internet. Ora `ops.py:275-281`
  (`_sul_disco`, usato in `:316`, `:326`, `:337`, `:343`) ed `extract_component`
  (`installer.py:144-148`) usano `errors.errore_disco_componente` (`errors.py:58-70`): «Non c'è
  abbastanza spazio sul disco per installare il componente…» oppure «Non riesco a salvare il
  componente… nella cartella …». Test: `test_d23_cartella_dei_dati_impossibile_da_creare`,
  `test_d23_disco_pieno_durante_l_installazione_del_componente[download|estrazione]` (tutti
  rossi prima; controllano anche che non restino pacchetto, `.scarico` o cartelle di appoggio).
  Ramo download, seconda passata (revisione): la prima correzione reggeva solo con un file non
  bufferizzato. `open(..., "wb")` dà un `BufferedWriter`: il `close()` del `with` ritentava lo
  svuotamento, falliva ancora con `OSError` e quell'errore copriva il «disco pieno», che tornava
  «controlla la connessione». Ora la chiusura è dentro `_sul_disco` (`ops.py:342-343`) e quella
  di riserva in `finally` ignora il secondo `OSError` (`:344-350`); il `.scarico` si toglie come
  prima. Coperto anche con file bufferizzato da
  `test_d23_disco_pieno_anche_con_il_file_bufferizzato` (rosso prima, verde dopo).
- *Sospetto/da valutare (minor del revisore):* `int(Content-Length)` con un valore non
  numerico solleva `ValueError`, che nessun `except` cattura (`ops.py:320`): «Qualcosa non ha
  funzionato» invece del messaggio di rete. Serve un server che sbaglia l'intestazione.
- *Sospetto/da valutare:* `scanner.py:95` usa `strip()`, che toglie anche U+2028, U+0085 e
  `\x1c`-`\x1f` in testa e in coda al nome: un file con uno di questi ai bordi potrebbe essere
  cercato con un nome diverso da quello vero (stessa famiglia di D26).
- *Sospetto/da valutare:* in `installer.py:190-206`, due voci dello zip che dopo l'appiattimento
  hanno lo stesso nome finale si sovrascrivono in silenzio (vince l'ultima). Il componente
  ufficiale non ha questo caso; uno zip manomesso sì.
- *Da valutare:* `download_file` e `install_component` (`installer.py:240-292`, `:334-360`)
  sono usati **solo dai test**: la finestra usa `installa_a_passi`. Hanno ricevuto la correzione
  D22 (una riga) ma non D23 (il loro `mkdir` è ancora fuori dal `try`, `:257`, `:348`).
  Rimuoverli o allinearli è una scelta di pulizia.
- *Sospetto non confermato (Windows):* reinstallare mentre il server di `adb` del componente è
  acceso: rinominare una cartella che contiene un eseguibile in uso potrebbe fallire con
  «accesso negato» (`:178`). Dopo D23 sarebbe un messaggio comprensibile, ma la situazione non si
  presenta dall'interfaccia (il pulsante compare solo se `adb` manca). Non verificabile qui.
- *Da valutare:* se il programma viene ucciso durante l'estrazione resta una cartella
  `fotofacile-estrai-*` in `.fotofacile` (nessuno la toglie dopo).

### Sospetto ereditato dal G1: `download_file_stream`

- **difetto D21 (bassa)** — corretto. `download_file_stream` creava la cartella di destinazione
  **fuori** dal `try` (stessa famiglia di D11): un `OSError` grezzo attraversava `transfer` e
  fermava l'intera copia. Lo usa `CopiatoreInterno`, cioè `transfer()` (riga di comando e test);
  la finestra usa gli altri copiatori, già corretti in D11. Ora la creazione sta nel `try`
  (`transfer.py:113`) e l'errore passa da `traduci_errore_file`: il file finisce fra i «non
  copiati» con il suo nome. Test: `test_d21_la_copia_interna_traduce_la_cartella_impossibile_da_creare`.

### `adb.py` e `devices.py`

**ok**, con note.

- `parse_devices` (`devices.py:49-75`) provato con un'uscita reale e strana di `adb devices -l`:
  righe `* daemon …` e l'intestazione saltate, `no permissions (…); see [http://…]` riconosciuto
  come «no permissions», dispositivi via rete (`adb-XYZ._adb-tls-connect._tcp.`, `192.168.1.5:5555`)
  letti con il loro stato. Gli stati sconosciuti (`authorizing`, `connecting`, `recovery`…)
  ricevono «Il telefono non è pronto.» (`page_connect.py:312-314`). I messaggi del server di adb
  vanno su `stderr`, che `parse_devices` non legge.
- `RealAdbBackend` (`adb.py:95-204`) nella finestra serve solo per `doctor` (`cli.py:77-83`, dentro
  un `except Exception`); il lavoro vero passa da `AdbAPassi`. *Da valutare:* `_run` legge con
  `text=True` (codifica di sistema, come prima di D16) e intercetta solo `FileNotFoundError`;
  `stream_file` non legge `stderr`. Oggi non toccano la persona.
- *Controllato (dal secondo revisore), non è un difetto:* in `stream_file` il `Popen`
  (`adb.py:176`) sta fuori dal `try`, ma `stream_file` è un generatore: il `Popen` parte al primo
  `next`, che in `download_file_stream` è dentro il `try` (`transfer.py:114-121`), quindi un `adb`
  sparito diventa un `OSError` tradotto da `traduci_errore_file`, non un errore grezzo (il testo
  parla del cavo, non del componente: solo riga di comando). L'`assert` di `:183` non può
  fallire con `stdout=subprocess.PIPE`.
- `find_adb` (`adb.py:56-92`) cerca prima il componente scaricato in `.fotofacile`, poi i percorsi
  noti e il `PATH`: coerente con `component_dir`.

---

## G5 — Dati e resoconti

File rivisti: `fotofacile/core/report.py`, `format.py`, `demo.py`, `scanner.py`, con chi li usa:
`ui/page_transfer.py` (avanzamento, resoconto), `ui/page_select.py` (cartelle, date),
`ui/page_options.py`, `core/planner.py:build_plan` (per le conseguenze delle maiuscole). Due
revisioni (lettura diretta + revisore `caveman:cavecrew-reviewer`); ogni caso limite è stato
provato chiamando le funzioni vere.

### `format_size` / `format_eta` con 0, negativi, `None`, valori enormi?

**ok** per i valori che arrivano davvero, con il difetto **D25** corretto nel testo.

- `format_size` (`format.py:10-19`): 0 → «0 B»; negativi → «0 B» (`max(…, 0)`, `:12`); 10²⁰ →
  «90949470,2 TB» (nessun errore, l'ultima unità assorbe tutto). `None` solleverebbe `TypeError`,
  ma nessun chiamante lo passa: le dimensioni sono sempre `int` (`scanner.py:103`,
  `trasporto_aiutante.py:381`), i totali sono somme, e lo spazio libero `None` viene controllato
  prima (`page_options.py:155-157`). *Da valutare (cosmetico):* 1 048 575 byte diventano
  «1024,0 KB» invece di «1,0 MB» (l'unità si sceglie prima di arrotondare).
- `format_eta` (`:43-48`): `None` → «calcolo in corso…»; 0, negativi e meno di un secondo →
  «meno di un secondo»; 10⁹ s → «circa 277777 ore e 46 minuti». Infinito o NaN solleverebbero
  (`int(round(…))`, `:29`), ma la stima è `restanti / velocità` con velocità > 0 e tempo trascorso
  almeno 1 ms (`transfer.py:218-223`): sempre finita. `format_speed` (`:22-25`) mostra «—» per 0 e
  negativi.
- **difetto D25 (bassa)** — corretto. Il singolare valeva solo per la prima unità: il tempo
  restante e la «Durata» del resoconto dicevano «1 minuto e 1 secondi» e «1 ora e 1 minuti».
  Ora `format.py:35` e `:39`. Test: `test_d25_un_secondo_e_un_minuto_restano_al_singolare`.
- *Sospetto non confermato (Windows):* `parse_date` (`:55-65`) intercetta solo `ValueError`;
  su Windows `datetime(…).timestamp()` per date molto vecchie potrebbe sollevare `OSError`
  (la data minima si scrive a mano in `page_select.py:220`). Non riproducibile su questo Mac.
  `format_date` (`:51-52`) non è usata da nessuno.

### `save_report` in una cartella non scrivibile?

**ok**. `save_report` (`report.py:71-86`) prova la cartella delle foto, poi il Desktop **solo se
esiste già** (`_cartelle_di_riserva`, `:56-68`), poi `.fotofacile`; ogni tentativo è dentro il
`try` (compreso `mkdir`, `:76-82`). Provato: cartella delle foto in sola lettura → il resoconto
finisce in `.fotofacile`; tutto bloccato (anche la cartella personale) → `FotoFacileError`
«Non sono riuscito a salvare il resoconto.» con il suggerimento di copiare il testo da
«Dettagli»; la pagina lo mostra come avviso (`page_transfer.py:239-255`). Test esistenti:
`test_salvataggio_resoconto_su_cartella_non_scrivilibile_usa_il_desktop`,
`test_resoconto_non_crea_il_desktop_se_non_esiste`.

- *Da valutare (bassa):* se il disco si riempie **mentre** scrive, nella cartella resta un
  resoconto troncato e quello completo va nella cartella di riserva; due resoconti salvati nello
  stesso secondo si sovrascrivono (il nome ha la precisione del secondo).
- `build_report` (`:18-53`): con telefono sconosciuto la pagina passa un `DeviceInfo` di ripiego
  (`page_transfer.py:205-211`); nessun campo può mancare. **ok**.

### `group_folders` con percorsi identici a meno delle maiuscole?

**ok** in `group_folders`; **da valutare** una conseguenza latente nel piano.

- `group_folders` (`scanner.py:155-170`) raggruppa per percorso **esatto** (`file.parent`): due
  cartelle `DCIM/Camera` e `DCIM/camera` restano due righe distinte, ognuna con i suoi file e la
  sua etichetta; la scelta in `page_select.py:218-228` confronta lo stesso percorso esatto, quindi
  spuntarne una non prende i file dell'altra. Provato.
- *Da valutare (latente, fuori gruppo: `planner.py:246-260`):* con «mantieni le cartelle» e un
  disco che non distingue le maiuscole (macOS, Windows), `_Esistenza` confronta il nome del file
  senza maiuscole ma usa come chiave il **percorso della cartella** così com'è. Provato:
  `DCIM/Camera/IMG_1.jpg` e `DCIM/camera/IMG_1.jpg` (foto diverse) ricevono due destinazioni
  che sul disco sono **lo stesso file** (`out/DCIM/Camera/IMG_1.jpg`, `out/DCIM/camera/IMG_1.jpg`):
  la seconda copia sovrascriverebbe la prima, e con «cancella dal telefono» la prima foto
  andrebbe persa. In copia piatta invece il secondo diventa `IMG_1 (1).jpg`, come deve. Non
  raggiungibile con un telefono vero: la memoria interna di Android e le schede SD (FAT/exFAT)
  non distinguono le maiuscole, quindi le due cartelle non possono esistere insieme. Non
  corretto: da sistemare solo se un giorno arrivano sorgenti che le distinguono.

### Altri controlli: `parse_stat_stream` con righe strane, `demo.py`

- **difetto D26 (bassa)** — corretto. `parse_stat_stream` divideva l'elenco con `splitlines()`,
  che taglia anche su caratteri che possono stare nel nome di un file (U+2028, U+0085, `\x1c`…),
  mentre il comando sul telefono produce una riga per file divisa solo da «\n» (`read -r`,
  `scanner.py:127`). Il file `a.jpg<U+2028>b.jpg` spariva e al suo posto compariva `a.jpg`: un
  file diverso (se esiste) con la dimensione sbagliata, che la verifica della dimensione poi
  scartava. Ora `scanner.py:92-94` divide solo su «\n»; le righe `\r\n` dei vecchi telefoni si
  leggono come prima (`strip`, `:95`). Test: `test_d26_nomi_con_separatori_unicode_restano_un_file_solo`.
- Le altre righe strane vengono saltate senza fermare la ricerca (`:96-110`): senza «|», con due
  campi soli, con dimensione o data non numeriche, con estensione non multimediale; un «|» nel
  nome resta (si separano solo i primi due). Provato anche: `1_0|…` viene letto come 10 e
  `-3|-9|…` come dimensione e data negative (Python accetta `_` e il segno in `int`): `stat` non
  produce mai queste forme, e una dimensione sbagliata viene comunque fermata dalla verifica dopo
  la copia (`transfer.py:252-260`). Gli spazi in fondo al nome: vedi la nota del G2.
- `demo.py` **ok**: nomi difficili (accenti, emoji, apostrofo, `#`, `&`) per provare il resto del
  programma; contenuto deterministico dal percorso (`:90-98`); `file_count` negativo → nessun
  file (`:36`); un percorso sconosciuto dà un `AdbError` comprensibile (`:84-89`, `:101-105`).
  La data dei file dipende dall'ora di avvio (`:52`): i test non ne dipendono.

---

## G6 — Avvio e CLI

File rivisti: `fotofacile/cli.py`, `fotofacile/__main__.py`, `fotofacile.py`, con quello che serve
all'avvio dal programma impacchettato: `core/osutil.py:comando_se_stesso`, `scripts/build_app.py`
(opzioni di PyInstaller), `ui/widgets.py:tk_available`. Due revisioni (lettura diretta + revisore
`caveman:cavecrew-reviewer`); tenuti solo i difetti confermati leggendo il codice e riprodotti con
un test. Il comportamento con `sys.stdout`/`sys.stderr` a `None` (programma `--windowed` su
Windows) è stato **misurato** con Python 3.14 mettendo a `None` i due flussi.

### `--selftest` distingue «grafica rotta» da «avvio sbagliato» anche da eseguibile congelato?

**In parte**: lo distingue il **testo**, non il codice di uscita; dal `.exe` di Windows il testo
oggi si perde (**D7**, pianificato nel Task D2), e prima di **D31** su Windows poteva mancare anche
fuori dal `.exe`.

- Codici di `main` (`cli.py:373-386`): `0` finestra costruita (i quattro passi, `cli.py:146-173`);
  `1` qualunque eccezione durante la costruzione (`cli.py:170-171`), con `"motivo": "TclError: …"`
  per la grafica e un altro tipo (`ImportError: …`, `AttributeError: …`) per un pacchetto rotto;
  `2` opzione sbagliata (argparse). Provato: `--selftets` → 2, `--selftest` → 0, `TclError`
  simulato → 1 con il motivo (test esistenti `test_autocollaudo_riporta_esito_*`).
- Programma congelato: nessun punto dell'avvio dipende da `sys._MEIPASS`; l'unico uso di
  `sys.frozen` è `comando_se_stesso` (`osutil.py:121-122`), che richiama l'eseguibile stesso
  (`sys.executable`), e `--selftest` non avvia processi figli. `build_app.py:66-78` porta dentro
  tutto `fotofacile` e la cartella degli aiutanti. Un guasto **prima** di `main` (bootloader,
  modulo mancante) non arriva a `selftest`: niente JSON, codice diverso da 0 e, con `--windowed`
  su Windows, la finestra d'errore di PyInstaller.
- **Con `sys.stdout` a `None`** `print` non solleva niente (misurato: `print` su `None` non fa
  nulla; anche `print(..., file=None)`), e nemmeno argparse (`--version`, `--help`, opzione
  sbagliata: misurato, `SystemExit` 0/0/2, nessun `AttributeError`). Quindi nessun `print` del
  percorso di avvio (`main`, `selftest`, `doctor`, `avviso_visibile`, `esegui_aiutante`) può
  fermare il programma: ma quello che stampa **non si vede**. (Il revisore ha segnalato il
  contrario per `cli.py:99`, `:158`, `:257`, `:316-325`: **non confermato**, misurato.)
- **difetto D31 (media, Windows)** — corretto. Quando l'uscita **esiste** ma non è la finestra
  dei comandi (un file: `py fotofacile.py doctor > diagnosi.txt`; la pipeline; `build_app.py
  --verify`) Python su Windows scrive nella codifica del sistema, cp1252, che non ha la riga
  «──────» della diagnosi: `print` si fermava con `UnicodeEncodeError`, codice 1 e nessuna
  diagnosi. Stessa sorte per `--selftest` con un motivo che contiene caratteri fuori da cp1252 (un
  nome utente in cirillico nel percorso) e per `avviso_visibile`, che stampava **prima** di
  mostrare l'avviso. Riprodotto qui con `PYTHONIOENCODING=cp1252 python fotofacile.py doctor`
  (codice 1, traccia). Ora `_stampa` (`cli.py:69-80`, usata in `:113`, `:172`, `:271`) sostituisce
  con «?» solo i caratteri che l'uscita non sa scrivere. `esegui_aiutante` scrive su `stderr`, che
  in Python usa già `backslashreplace`: niente da fare. Test:
  `test_d31_la_diagnosi_esce_anche_in_un_file_con_la_codifica_di_windows`,
  `test_d31_l_autocollaudo_esce_anche_con_la_codifica_di_windows`,
  `test_d31_l_avviso_di_avvio_non_si_ferma_sulla_codifica` (tutti rossi prima).
- *Da valutare:* un codice di uscita diverso per «grafica rotta» (`TclError`) e per «pacchetto
  rotto» (ogni altra eccezione) renderebbe la differenza visibile anche senza leggere il testo.
  Cambia il contratto della pipeline: da decidere nel Task D2/D4.

**Cosa dovrà coprire il Task D2** (non implementato qui, come richiesto):

1. `doctor` (`cli.py:113-125`) e `selftest` (`cli.py:172`) scrivono con `_stampa`: `emetti`
   dovrà usare `_stampa` (non un `print` nudo, altrimenti D31 torna) quando `sys.stdout` esiste,
   e il file (`diagnosi.txt`, `selftest.txt`, in UTF-8) quando è `None`.
2. Per la pipeline conviene che `selftest.txt` venga scritto **anche** con esito positivo: la sua
   assenza è la prova di un «avvio sbagliato» (il programma non è arrivato a `selftest`), il
   `motivo` distingue `TclError` dal resto.
3. `avviso_visibile` (`cli.py:259-279`): su Windows mostra l'avviso solo con `print` (niente
   `osascript`); con `--windowed` chi apre il programma e la finestra non parte **non vede
   niente**, resta solo `avvio.log`. Il piano di D2 non lo nomina: da aggiungere (per esempio
   `ctypes.windll.user32.MessageBoxW`, oppure `emetti` + apertura del registro).
4. `--version` e `--help` dal `.exe` non mostrano niente (argparse su `None`): bassa, da valutare.
5. `esegui_aiutante` (`cli.py:318-340`): nessun intervento; il processo figlio riceve sempre file
   veri come uscite (`ProcessoEsterno`). *Da verificare su Windows vero (D6):* che
   `FotoFacile.exe --aiutante wpd_win …` lanciato con le uscite rediritte abbia `sys.stderr`
   diverso da `None` (ragionato: il CRT eredita gli handle; non verificabile qui).

### `scrivi_log_avvio` cresce senza limite? Lo stesso `avvio.log` viene ruotato?

**difetti D27 e D28**, corretti.

- **difetto D27 (bassa)** — corretto. `scrivi_log_avvio` apriva `~/.fotofacile/avvio.log` in
  aggiunta, senza limite né rotazione: due righe a ogni apertura, più gli avvisi interi. Ora, oltre
  `LIMITE_LOG_AVVIO` = 256 KB (`cli.py:178`), il registro ricomincia da capo e la parte precedente
  resta in `avvio.log.1` (una copia sola, sostituita alla rotazione successiva, `cli.py:194-199`);
  se la rotazione non riesce (copia aperta da un'altra finestra su Windows) si continua ad
  aggiungere. Spazio massimo circa 512 KB. Test:
  `test_d27_il_registro_di_avvio_non_cresce_per_sempre` (rosso prima),
  `test_d27_un_registro_piccolo_continua_a_crescere` (guardia).
- **difetto D28 (media)** — corretto. `start_gui` (prima riga, `cli.py:287`) e `avviso_visibile`
  (`:270`) scrivevano il registro fuori da ogni `try`. Se non si poteva scrivere (disco pieno, un
  file al posto della cartella `.fotofacile`, cartella personale protetta) usciva un `OSError`
  grezzo: **il programma non si apriva affatto** (dal `.exe`, la finestra d'errore di PyInstaller)
  e l'avviso che doveva spiegare il problema non compariva. Ora `scrivi_log_avvio`
  (`cli.py:181-204`) rinuncia in silenzio e restituisce `None`. Test (una cartella impossibile da
  creare, un registro impossibile da aprire):
  `test_d28_il_programma_si_apre_anche_se_il_registro_non_si_scrive[…]`,
  `test_d28_l_avviso_compare_anche_se_il_registro_non_si_scrive[…]` (tutti rossi prima).
- **Isolamento dei test** — corretto (commit `test:`, non è un difetto del programma). Tre test di
  `tests/test_cli.py` avviavano la grafica finta senza isolare la cartella personale: ogni
  esecuzione della suite aggiungeva cinque righe al **vero** `~/.fotofacile/avvio.log` di chi la
  eseguiva (su questo Mac: 583 righe e 62 KB in due giorni, tutte dei test). Ora un fixture
  automatico del modulo punta `HOME`/`USERPROFILE` a una cartella di prova; verificato che dopo
  tutta la suite il registro vero non cambia (dimensione e data identiche).

### Altri controlli del gruppo

- `fotofacile.py` e `__main__.py`: `raise SystemExit(main())`, nient'altro; `main` intercetta
  `--aiutante` prima di argparse (`cli.py:377-378`), così gli argomenti dell'aiutante non vengono
  letti come opzioni di FotoFacile. **ok**.
- `contesto_grafico_dubbio` (`cli.py:207-217`) vale solo su macOS; dal `.app` aperto dal Finder
  c'è `__CFBundleIdentifier`, quindi niente prova. `prova_finestra` (`:220-227`) richiama sé stesso
  con `--prova-finestra` (corretto per il congelato, B16/C4). **ok**.
- *Da valutare (Parte C):* `ui/widgets.py:32-45` (`_prova_finestra` di `tk_available`) usa ancora
  `sys.executable -c`, che nel programma impacchettato non funziona (stesso problema di B16). Oggi
  la usano solo i test (`tests/conftest.py`): non va usata nel programma.

---

## G7 — Pagine e app

File rivisti: `fotofacile/ui/app.py`, `ui/page_connect.py`, `ui/page_select.py`,
`ui/page_options.py`, `ui/page_transfer.py` (e `ui/widgets.py` per `Banner`/`StepIndicator`). Due
revisioni (lettura diretta + revisore `caveman:cavecrew-reviewer`). Come richiesto dal piano, la
Parte C **riscriverà** le quattro pagine e `widgets.py`: i difetti **dentro le pagine** sono solo
annotati per la Parte C (nessuno è una perdita di foto né un blocco totale); quelli di `app.py`,
che sopravvive, sono corretti. Le prove sono state fatte con la finestra vera (script a parte e
test con la finestra condivisa).

### Nessun `after` resta pendente alla chiusura?

**ok**.

- `_chiusura` (`app.py:361-388`): `stop_all_polling` ferma il sondaggio del passo 1
  (`page_connect.py:234-242`, `after_cancel` di `_tick_id`) e l'attesa del passo 2
  (`page_select.py:113-120`); `after_cancel` del primo piano (`app.py:381-386`, B23).
- Il `tick` di `run_task` (`app.py:320`, `:322`) non viene annullato con `after_cancel`, ma
  `annulla_task` cambia l'epoca (`:330`) e un `tick` vecchio esce subito (`:292-293`); dopo
  `destroy` il `mainloop` finisce e nessun `after` viene più eseguito (il revisore lo segnala come
  rischio: non confermato, non esiste un percorso che lo esegua). Pagine e `widgets.py` non hanno
  altri `after`; la finestra di aiuto è figlia della pagina e viene distrutta con lei.

### `go_to` durante un task attivo lascia stato incoerente?

**difetto D29** in `go_to` stesso; per il task in corso **ok** con note per la Parte C.

- **difetto D29 (media)** — corretto. `go_to` chiamava `on_show` della pagina e **dopo**
  aggiornava `current_page`, l'indicatore dei passi e chiudeva l'avviso. Effetti misurati con la
  finestra vera: (1) ogni messaggio scritto da `on_show` spariva subito, compreso «Sto copiando le
  foto: non scollegare il telefono.» (`page_transfer.py:97`), «Ultimo passo prima della copia…»
  (`page_options.py:99-102`) e «Sto cercando le foto sul telefono…» al primo ingresso nel passo 2;
  (2) quando `on_show` rimanda a un'altra pagina (`page_transfer.py:85-96`, `page_select.py:136-149`)
  la finestra mostrava «Destinazione» ma teneva `current_page = "transfer"`, l'indicatore sul passo
  4, l'avviso del motivo **nascosto**, e «Indietro» restava sulla stessa pagina. È la causa comune
  di C17, allora corretto pagina per pagina. Ora lo stato si aggiorna prima e `on_show` viene
  chiamato per ultimo (`app.py:247-255`). Test: `test_d29_il_messaggio_scritto_all_ingresso_resta_visibile`,
  `test_d29_una_pagina_che_rimanda_altrove_lascia_la_finestra_coerente` (rossi prima; usano pagine
  finte, quindi reggono alla Parte C). Tre test di `test_ui_app.py` davano per buono il
  comportamento sbagliato (entrare in «Scegli le foto» senza telefono, in «Copia» senza opzioni) e
  sono stati adattati; il collaudo `tests/pilota_app.py` dà `"ok": true`, 54 file, nessun `.part`,
  nessuna sottocartella.
- Task in corso e cambio di pagina: `go_to` non ferma il lavoro (il revisore lo propone come
  difetto: **non confermato**). Durante la copia non si può cambiare pagina (il passo 4 non ha
  «Indietro», «Chiudi» è spento fino alla fine, `page_transfer.py:74-79`); una ricerca lasciata a
  metà con «Indietro» finisce da sola e il passo 2 si rimette in ordine (`page_select.py:100-105`,
  C3). Note per la Parte C:
  - *da risolvere in Parte C (C6/C7):* `_scansione_finita` e `_scansione_fallita`
    (`page_select.py:166-194`) scrivono l'avviso anche se nel frattempo si è tornati al passo 1:
    «Trovate 54 foto e video.» compare sotto «Collega il telefono».
  - *da risolvere in Parte C (C6):* «Riprova il collegamento» (`page_connect.py:411-428`) avvia
    `riavvia()` senza guardare `task_in_corso`: il lavoro precedente viene abbandonato (e chiuso
    solo al suo `tick` successivo). «Prova senza telefono» durante un controllo del telefono vero
    (`page_connect.py:430-435`) può lasciare per un giro il seriale del telefono vero con il
    collegamento demo; si rimette a posto al sondaggio successivo. Nessun file toccato.
  - *latente, per la Parte C (C5/C7/C9):* `start_scan` (`page_select.py:156-164`) passa
    `app.cancel_event` **senza** azzerarlo (lo fanno `start_transfer` e `install_component`), e
    `ricostruisci_pagine` (`app.py:217-227`) non lo azzera. Dopo «Interrompi» al passo 4 l'evento
    resta acceso; oggi non si può tornare al passo 2 dopo una copia, ma se la Parte C aggiunge un
    ritorno (o `cambia_scala` → `ricostruisci_pagine` a metà uso) la ricerca con adb o con
    l'aiutante partirebbe già annullata: `Annullato` non è un `FotoFacileError`, quindi «Qualcosa
    non ha funzionato» e pulsanti spenti. Con il telefono demo non si vede (non legge l'evento).
- `ricostruisci_pagine` (`app.py:217-227`): ferma sondaggi e task, ricrea le pagine e apre il
  passo 1. Non azzera `device`, `media_files`, `options`, `cancel_event` (vedi sopra): oggi la
  chiamano solo i test (`conftest.azzera`, che azzera tutto a mano); la Parte C (C5) la userà a
  metà uso. **ok** oggi, nota per C5.

### Doppio clic rapido su «Copia le foto»?

**Nessun doppio avvio misurato; la conferma della cancellazione si aggira** (da risolvere in Parte
C, C8).

- Senza «cancella dal telefono»: il primo clic porta subito al passo 4 (`page_options.py:211`) e
  il secondo cade sulla pagina «Copia». Misurato con la finestra vera a 1020×780: «Copia le foto»
  occupa y 438-491, i pulsanti del passo 4 y 363-416: il secondo clic cade nel vuoto (non su
  «Interrompi»).
- **Da risolvere in Parte C (C8), non corretto:** con «Cancella le foto dal telefono dopo averle
  copiate» spuntata, il primo clic mette `_conferma_eliminazione = True` e chiede di premere di
  nuovo (`page_options.py:199-206`): un **doppio clic** conferma da solo, senza leggere l'avviso
  (riprodotto con due `invoke()`: pagina «transfer», `delete_after = True`). Non è una perdita di
  foto (si cancella solo dopo copia e verifica della dimensione, e la casella va spuntata apposta),
  quindi resta alla Parte C, che passa a `messagebox.askyesno`. Nota per C8: dare `default="no"`
  alla domanda, perché anche `Invio` tenuto premuto (tasto previsto da C5) non la confermi da solo.
  Stessa pagina: `_conferma_eliminazione` si azzera solo cambiando la casella (`:105-111`), non
  tornando indietro e rientrando.
- *Sospetto non confermato (dal revisore):* un secondo `go_to("transfer")` avvierebbe una seconda
  copia, perché `start_transfer` non guarda `task_in_corso` (`page_transfer.py:84-99`, `:116-143`).
  Serve che il secondo clic arrivi **al pulsante nascosto** (evento già in coda prima del cambio
  di pagina, oppure il tasto spazio con il fuoco rimasto sul pulsante): non riprodotto. Ragionato
  sulle conseguenze: il `.part` ha lo stesso nome nelle due copie (stesso processo), quindi al più
  un file fallisce o viene copiato come «nome (1)»; nessuna foto viene cancellata senza essere
  stata copiata. *Da risolvere in Parte C (C9):* una riga di guardia in `start_transfer`.

### Altri controlli del gruppo

- **difetto D30 (bassa)** — corretto. `_chiusura` chiedeva «Sto ancora copiando le foto. Vuoi
  interrompere e chiudere?» con **qualunque** lavoro in corso. Al passo 1 il telefono viene
  controllato ogni 2 s, e su macOS, senza telefono, ogni controllo dura fino a 6 s
  (`aiutanti/ptp_mac.py:31`, `:137-163`): chi chiudeva il programma prima di collegare il telefono
  si sentiva chiedere di interrompere una copia inesistente. Ora la domanda compare solo al passo 4
  (`app.py:368`, affidabile dopo D29); gli altri lavori si interrompono come prima con
  `annulla_task`. Test: `test_d30_chiudere_mentre_si_cerca_il_telefono_non_parla_di_copia` (rosso
  prima), `test_d30_durante_la_copia_la_domanda_resta` (guardia).
- `_chiusura` con copia in corso (**ok**): `askyesno` (durante la domanda la copia continua) → «Sì»
  → `cancel_event.set`, `annulla_task` chiude il generatore: il `GeneratorExit` salva la cronologia
  (D2), ferma il processo e toglie il `.part` (G1); poi `_pulisci_ambiente` e `destroy`. «No» → si
  continua. La finestra può restare ferma fino a 6 s mentre `termina` aspetta il processo (G1).
- *Sospetto già annotato nel G1 (non confermato):* `run_task` (`app.py:278-322`) sostituisce il
  task senza chiudere quello precedente; la chiusura arriva al `tick` successivo del vecchio.
- *Da risolvere in Parte C (C9):* `start_transfer` intercetta solo `OSError`
  (`page_transfer.py:120-128`): dopo «Non riesco a leggere la cartella di destinazione» restano
  accesi solo «Interrompi» (inutile) e nessun «Indietro»; si esce solo chiudendo la finestra.
  `show_error` (`:145-153`) lascia spento «Salva resoconto». Il riepilogo dice «in 1 secondi»
  (`:190-191`, stessa famiglia di D25) e «Ne ho saltati 1».
- *Da risolvere in Parte C (C7):* il campo della data (`page_select.py:61-66`) è già sostituito
  dal menu dei periodi nel piano.

---

## G8 — Script di build (sola lettura)

File letti: `scripts/build_app.py`, `scripts/crea_installer_mac.py`, `scripts/make_icon.py`,
`scripts/crea_pacchetto_windows.py`, `scripts/run_tests.sh`, `installer/windows/FotoFacile.iss`,
`installer/windows/InstallaFotoFacile.ps1`, `DisinstallaFotoFacile.ps1`, `Installa FotoFacile.bat`,
`.github/workflows/build-installers.yml`. Nessuna modifica: le correzioni vere sono nella Parte D.

### Cosa sostituirà la Parte D

| Oggi | Task | Cosa cambia |
|---|---|---|
| `FotoFacile.iss`: `#define Versione "0.1.0"` scritto a mano (`:11`), `ISCC` senza `/DVersione` (workflow `:66`) | D0, D1, D4 | versione letta da `fotofacile/__init__.py` (`scripts/leggi_versione.py`) |
| `FotoFacile.iss`: il LEGGIMI usato **sia** come licenza da accettare **sia** come informazioni (`:39-40`); `[Run]` con `doctor` dopo l'installazione (`:61`), che dal `.exe` `--windowed` non mostra niente (D7) | D1, D2 | script riscritto con `Benvenuto.txt`; `doctor` scrive `diagnosi.txt` |
| `Installa FotoFacile.bat`, `InstallaFotoFacile.ps1`, `DisinstallaFotoFacile.ps1`, `crea_pacchetto_windows.py` | D3 | eliminati (i due `.ps1` hanno il BOM: verificato con `xxd`) |
| workflow, passo «Versione portatile (zip)»: importa `scripts.crea_pacchetto_windows` (`:62`) | D3, D4 | solo `shutil.make_archive` |
| workflow, job `windows`: nessun test, nessuna prova dell'installatore, niente somme di controllo; testo della Release che manda al «Debug USB» (`:99-101`) | D4 | test su Windows, `prova-installazione.ps1` (installa, avvia, disinstalla), `SHA256SUMS.txt`, testo nuovo |
| `doctor`/`--selftest` muti dal `.exe` | D2 | `emetti` (vedi i punti in G6) |

### Difetti che la Parte D **non** copre (da aggiungere alla Parte D)

- **`scripts/build_app.py:116-131` (`crea_archivio`), media, solo Windows/Linux:** fuori da macOS
  il «pacchetto» è l'**eseguibile** (`pacchetto_creato`, `:91-96`), e `pacchetto.rglob("*")` su un
  file non trova niente: l'archivio da condividere esce **vuoto**. Verificato con una cartella
  finta `dist/FotoFacile/{FotoFacile.exe,_internal/python312.dll}`: zip con 0 voci. Anche
  `dimensione_mb` (`:208`) riporta solo la dimensione dell'eseguibile. La pipeline usa `--no-zip`
  e non lo vede; chi costruisce a mano su Windows o Linux sì. Correzione: archiviare
  `pacchetto.parent` quando non è un `.app`.
- **`scripts/crea_installer_mac.py:31-32` (`LEGGIMI` dentro il `.dmg`), media:** dice di premere
  «Come si attiva il Debug USB?», un pulsante che non esiste più («Il telefono non viene
  riconosciuto?»), e presenta il Debug USB come la strada normale, contro D9 («Trasferimento
  file»). La Parte D è solo Windows: da correggere insieme al testo della Release (D4) o in E1.
- **Workflow, job `windows`, «Verifica l'eseguibile» (`:56-60`), da verificare:** l'eseguibile
  `--windowed` viene lanciato direttamente da PowerShell. PowerShell non aspetta i programmi con
  finestra (sottosistema GUI) e non aggiorna `$LASTEXITCODE` quando non li aspetta: il passo
  potrebbe risultare verde anche con l'autocollaudo fallito. Non verificabile da qui. Il Task D4
  tiene questa forma nel passo «Verifica l'eseguibile (autocollaudo)»; `prova-installazione.ps1`
  invece usa giustamente `Start-Process -Wait -PassThru` e controlla `ExitCode`: usare la stessa
  forma anche nel passo di build.
- **Workflow, job `macos` (`:32-34`), da valutare:** `--selftest || echo ::warning::` trasforma in
  avviso **qualunque** fallimento, anche un pacchetto rotto (per esempio PyObjC mancante). Con il
  JSON del `selftest` si può tenere l'avviso solo per `TclError` (niente sessione grafica) e far
  fallire il resto.
- *Nota:* la pipeline usa Python 3.12 (`:25`, `:51`), lo sviluppo 3.14: i test oggi girano solo su
  3.14. Il Task D4 aggiunge i test su Windows (3.12): bene.
- `scripts/make_icon.py`: **ok**. Rigenerato in una cartella temporanea: `fotofacile.png` e
  `fotofacile.ico` identici byte per byte a quelli in `assets/` (quindi `build_app.py:185-187` non
  cambia le icone). `scripts/run_tests.sh`: **ok**.
- `build_app.py:141-160` riscrive a ogni costruzione `Avvia FotoFacile.command`, che è nel
  repository: oggi il contenuto coincide (nessuna modifica dopo la costruzione), **ok**.

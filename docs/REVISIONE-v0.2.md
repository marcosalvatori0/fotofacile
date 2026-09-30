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

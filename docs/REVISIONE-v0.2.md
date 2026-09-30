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

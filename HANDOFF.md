# Handoff: FotoFacile — app desktop per copiare foto da Android

**Aggiornato**: 2026-09-30 (fine della revisione v0.2, Parti A–D)
**Versione**: `0.2.0` (unico punto di verità: `fotofacile/__init__.py`; la legge `scripts/leggi_versione.py`)
**Branch**: `revisione-v0.2` (HEAD `7226f8b`). **Non è stato unito a `main` e non è stato pubblicato nulla**:
niente push, niente tag, niente Release. `main` è ancora alla v0.1.0.
**Stato**: **636 test verdi**, `pyflakes fotofacile scripts` vuoto. Completate le Parti A, B (tranne B2),
C (tranne C10) e D (D0–D4). Restano da fare le cose elencate in «Not Yet Done», quasi tutte **dipendono da Marco**
(un Windows vero, un telefono vero, la sua conferma per pubblicare).
Repo GitHub `marcosalvatori0/fotofacile` (pubblico). La Release `v0.1.0` è **vecchia** (contiene ancora i `.bat`
e non ha nulla della revisione).
**Non verificato** (vedi «Not Yet Done»): l'installatore Windows non è mai stato costruito né eseguito su un Windows
vero; nessuna operazione con un telefono Android reale su nessun sistema.

---

**Pulizia del repository (2026-09-30):** tolti `LEGGIMI - Installazione.txt` (le istruzioni sono nel README e nel testo della Release) e
`Avvia FotoFacile.command` (lo ricrea `python3 scripts/build_app.py`, non è più versionato); cancellati i file generati (`build/`, `dist/`,
cache). Restano codice, test, `installer/windows/` (serve alla pipeline e ai test), workflow, `docs/`, grafo e questo file.
**Attenzione:** sul Mac di Marco gira anche l'app Codex sulla stessa cartella e in questa sessione ha cancellato dal disco file
tracciati (`installer/`, `requirements*.txt`): controllare `git status` all'inizio di ogni sessione e ripristinare con `git checkout -- <file>`.

## Goal

Permettere a **persone non tecniche** (anche anziane) di copiare foto e video da un telefono Android al computer
con una procedura guidata in italiano, senza gestore file e senza gergo tecnico. Multi-piattaforma
(Windows/macOS/Linux), **senza Debug USB da attivare** e senza dipendenze obbligatorie per chi usa
il programma. I file arrivano **direttamente nella cartella scelta**.

---

## Completed

### Parte A — correzioni dell'audit (D1–D31)
- [x] Audit di tutto il codice per gruppi (G1–G8) e correzione di 31 difetti (`D1`–`D31`), ciascuno con un test
  in `tests/test_regressioni.py`. Il testo completo (domande, risposte, righe di codice) è in
  **`docs/REVISIONE-v0.2.md`**. Quelli che contano di più: le foto copiate conservano la data di scatto (D1),
  la cronologia si salva e si unisce (D2, D6), un disco pieno non fa mai perdere file (D11–D13, D23),
  su Windows le foto si riconoscono anche con le estensioni nascoste (D17, **non provato su Windows vero**),
  la copia non sovrascrive mai un file esistente, i processi figli si puliscono se l'aiutante è interrotto (D19),
  il registro di avvio non cresce all'infinito (D27–D28).

### Parte B — WebP
- [x] Riconoscimento del formato vero dei file (contenuto, non estensione) e comando `formati` (B1).
- [x] Conversione opzionale dei WebP in **JPG/PNG** con Pillow durante la copia, senza mai perdere né
  sovrascrivere un file (B3, B4; fuzzer da 18000 scenari, 0 perdite). Casella «Trasforma le immagini WebP in JPG»
  nel passo 3 (solo se Pillow c'è) e riga «Conversione WebP» in `doctor` (B5). Pillow è nel pacchetto (`build_app.py`).

### Parte C — nuova interfaccia (4 passi, pensata per chi non è pratico)
- [x] **Testo grande e regolabile**: pulsanti `A−` / `A+` (passo 1), scala 1,0 / 1,25 / 1,5 (predefinita 1,25) salvata nelle impostazioni personali
  (`~/.fotofacile/impostazioni.json`, `core/impostazioni.py`). Font minimo 14 pt; `TestoAdattivo` a capo automatico.
  Al cambio di scala pagine, banner e registro si ricostruiscono.
- [x] **Invio** = azione principale della pagina (o preme il pulsante che ha il focus), **Esc** = indietro.
- [x] **Dettagli nascosti**: il registro tecnico sta dietro «Mostra i dettagli» e non si apre da solo.
- [x] **Passo 1** «Collega il telefono al computer»: tre istruzioni fisse, indicatore ✔/⚠ grande; dopo 3 tentativi senza
  telefono compare il pulsante grande «Il telefono non viene riconosciuto? Ti aiuto io»; riga secondaria «Serve aiuto?»,
  «Riprova», «Installa componente mancante», «Prova senza telefono», `A−`/`A+`.
- [x] **Passo 2** «Scegli le foto»: **nomi veri delle cartelle** (`core/nomi_cartelle.py`: Camera → «Foto e video scattati
  con il telefono», WhatsApp, Schermate…), menu **del periodo** (tutte / ultimo mese / 3 mesi / anno), «Mostra anche
  miniature e sticker» (nascosti di default), «Seleziona tutte» / «Togli la selezione».
- [x] **Passo 3** «Dove salvo le foto?»: riassunto a parole («Copierò N foto…»), spazio disponibile, «Altre opzioni ▸»
  chiuse (ricrea cartelle, salta già copiate, WebP, cancella dal telefono). **Cancellare dal telefono** chiede subito
  conferma con una finestra (predefinito «No») e lascia un promemoria rosso sempre visibile.
- [x] **Passo 4** «Copia in corso»: **percentuale grande**, tempo residuo a parole («manca circa 2 minuti»), «Interrompi»,
  a fine copia «Apri la cartella delle foto» / «Salva resoconto» / «Chiudi»; dopo un errore compare «Indietro».
- [x] **Correzioni dalla revisione di C6–C9** (wave finale, `7226f8b`): Invio sul pulsante che ha il focus, pulsanti principali
  sempre visibili a testo grande, promemoria di cancellazione, errori imprevisti di `run_task` mostrati con una via d'uscita.
  Dettaglio in `docs/REVISIONE-v0.2.md`, sezione «Parte C e D».
- [x] Tema chiaro/scuro (`clam`), contrasto WCAG ≥ 7, focus ben visibile.

### Parte D — installatore Windows
- [x] Script **Inno Setup** `installer/windows/FotoFacile.iss` (italiano, per utente, **senza amministratore**, installa in
  `%LOCALAPPDATA%\Programs` (`{autopf}` con privilegi minimi), collegamenti su Desktop e menu Start, collegamento «Diagnosi», disinstallazione in Impostazioni → App).
- [x] Via tutti i `.bat`/`.ps1` d'installazione e la cartella «FotoFacile per Windows»: su Windows resta **solo**
  `FotoFacile-Setup-<versione>.exe` (più `FotoFacile-portable.zip`).
- [x] `doctor` e `--selftest` funzionano anche dal programma installato (senza finestra nera): scrivono
  `diagnosi.txt` / `selftest.txt` in `%USERPROFILE%\.fotofacile` (`FOTOFACILE_NO_OPEN=1` = non aprire il Blocco note).
- [x] Pipeline `.github/workflows/build-installers.yml`: job Windows costruisce l'exe, lo verifica (`verifica-eseguibile.ps1`),
  crea lo zip portatile e il Setup, e **lo installa davvero, lo avvia, lo disinstalla** (`prova-installazione.ps1`),
  poi `SHA256SUMS.txt`. Corretto anche un bug vero di `build_app.py` (zip vuoto su Windows/Linux).
  **La pipeline non è mai stata eseguita** (vedi «Not Yet Done» a).

### Prima della revisione (v0.1, sempre valido)
- [x] Scelta automatica del collegamento (`core/trasporto*.py`, `fotofacile/aiutanti/`): macOS PTP/ImageCaptureCore,
  Windows WPD/PowerShell, Linux MTP `gio`/`jmtpfs`; ADB solo come scorciatoia. **Copia piatta** predefinita.
- [x] Motore **senza thread** (generatori avanzati da `after()`), copia `.part` + rinomina atomica, verifica dimensioni,
  dedup, cancella-dopo-copia con conferma, installazione di platform-tools con impronta ufficiale, modalità demo.
- [x] Diagnostica: `doctor` («Modi di collegamento», «Conversione WebP»), `--selftest`, `--prova-finestra`,
  `--aiutante` (interna), registro `~/.fotofacile/avvio.log`.
- [x] Collaudo end-to-end dell'app vera (`tests/pilota_app.py`) e aiutante macOS avviato davvero (senza telefono).
- [x] Graphify (`graphify-out/`) aggiornato dopo le Parti A e B; dopo la C e la D è stato rigenerato ma **non committato**.

---

## Not Yet Done — serve Marco

- [~] **(a) D5 — pubblicare e ottenere il `.exe`**: **FATTO a metà il 2026-09-30** con l'ok di Marco: push del branch `revisione-v0.2`
  e pipeline lanciata a mano (`workflow_dispatch`, run 36721726035, **verde**: installa in silenzio, avvia `--selftest`, `doctor`,
  disinstalla). Il primo giro era fallito per un errore di sintassi PowerShell (`"$exe:"` → `"${exe}:"`), già corretto. Artefatto:
  `FotoFacile-Setup-0.2.0.exe` (SHA-256 `dfb8d2ff…ac3fa22`), copiato sulla Scrivania di Marco. **Restano da fare, con la conferma
  di Marco:** tag `v0.2.0` + Release pubblica e unione di `revisione-v0.2` in `main`.
  La **prima esecuzione probabilmente richiederà piccole correzioni**; rischi non verificati (dal report D4, nessun Windows,
  Inno Setup né PowerShell disponibili qui):
  1. I due `.ps1` (`verifica-eseguibile.ps1`, `prova-installazione.ps1`) non sono mai stati eseguiti: possibili errori di sintassi o logica.
  2. Percorso di `ISCC.exe` dopo `choco install innosetup` (atteso `C:\Program Files (x86)\Inno Setup 6\`; il workflow lo cerca con
     `Program Files*\Inno Setup *`) e presenza di `compiler:Languages\Italian.isl`.
  3. Che `sys.stdout` sia `None` nell'exe `--windowed` avviato da `Start-Process`; altrimenti `selftest` stampa e non scrive `selftest.txt`
     e la verifica fallisce (con messaggio chiaro).
  4. Che il disinstallatore silenzioso di Inno rimuova exe e chiave HKCU entro 90 s.
  5. I **test su Windows** (`pytest tests -x`) non sono mai girati là: il passo ha `continue-on-error: true` (avviso giallo). Quando sono
     puliti, togliere quella riga.
  6. L'**autocollaudo macOS ora è bloccante**: se il runner `macos-14` non ha sessione grafica il job fallisce e con lui la Release (il
     rimedio è saltare/adattare il passo, non rimettere `|| echo`).
  7. `SHA256SUMS.txt` esce solo dal job Windows (il `.dmg` non ha checksum); l'upload usa `if: always()` (pubblica anche artefatti parziali,
     solo come artefatto del run, non come Release); nessun controllo che il tag coincida con `__version__`; `doctor` sul runner
     può rallentare cercando `adb`.
  Dopo la pubblicazione: unire `revisione-v0.2` in `main` (il LEGGIMI interno del `.dmg` è già stato corretto: non cita più «Come si attiva il Debug USB?»).
- [ ] **(b) D6 — prove manuali su un Windows vero** (Marco): installare il `Setup.exe`, avviare, disinstallare; in particolare
  **D17** (foto riconosciute con le estensioni dei file nascoste in Esplora risorse), il collegamento **«Diagnosi»** del menu Start
  (deve aprire il Blocco note con il rapporto), l'avviso blu **SmartScreen** «Windows ha protetto il PC» → «Ulteriori informazioni»
  → «Esegui comunque» (l'installer non è firmato), collegamento diretto (WPD) con un telefono.
- [ ] **(c) B2 — diagnosi dei WebP con i file di Marco**: serve la sua cartella di WebP (e il sistema) per capire perché certe immagini
  non si aprono; il resto della Parte B è fatto.
- [ ] **(d) Cartella vecchia `~/Desktop/FotoFacile per Windows/`** (fuori dal repo, contiene i `.bat` superati): **chiedere a Marco**
  se cancellarla. Non è stata toccata.
- [ ] **(e) C10 — rimandato**: verifiche automatiche di leggibilità (nessun testo sotto i 14 pt, contrasto, nessun pulsante fuori
  schermo) e **verifica a schermo** delle 4 pagine a scala 1,0/1,25/1,5 (`launchctl asuser` + `screencapture`). Il brief è in
  `.superpowers/sdd/task-C10-brief.md`. Limiti già noti: a 1,5× con «Altre opzioni» aperte le ultime caselle possono finire sotto il
  bordo (il pulsante principale no); a 1,5× il passo 2 lascia ~84 px per l'elenco (scorrevole).
- [ ] **(f) Minor aperti** (nessuno bloccante):
  - Parte C: `TestoAdattivo` senza minimo di larghezza (`max(1, …)`, ok grazie a `minsize` dell'app); fixture `focus` dei test dipende
    dall'ambiente; `_dimensiona_finestra` non fissa la posizione; `_chiama_azione` non controlla il pulsante spento (lo fa ogni pagina);
    test del focus solo su `Big`/`Checkbutton`; `Checkbutton` dell'elenco non va a capo con nomi lunghissimi; `bind_all` della rotellina
    (tolti a `SelectPage.destroy`, resta da tenere d'occhio); minor sulla selezione del passo 2 (`page_select`, vedi `progress.md`: `_ridisegna` e le spunte);
    `page_transfer._torna_indietro` e `page_select` ripetono `set_status` dopo `go_to` (commento fuorviante dopo D29).
  - Parte B (`carryover.md`): mancano test di `rifiuta_se_esiste` su `AdbAPassi` e `TrasportoWpdWindows`; **NFC/NFD** su APFS
    (`planner._Esistenza._chiave` e `riservati` senza normalizzazione: il secondo file finisce in `failed` a ogni giro); un `a.JPG`
    «bugiardo» su FS **case-sensitive** diventa `a (1).jpg`; `_rimetti_estensione_webp` duplica `_libero`; conversione: `samefile` con
    hardlink, `.conv` preesistente, test mancanti per `unlink`/999 tentativi.
  - Parte A: test per `mtime == 0`; race residua fra due salvataggi simultanei della cronologia (`.tmp` condiviso); HRESULT non
    controllato (D8); D12 residuo col nome del file nel dettaglio del comando; timeout assoluto di copia, `.part` orfani, `adb` vivo dopo
    la chiusura, mount gvfs preesistente smontato (Linux), doppia estensione `x.jpg.jpg` con estensioni nascoste (Windows): «da valutare».
  - Parte D: autocollaudo macOS bloccante in CI (rischio sopra); `SHA256SUMS` solo per Windows; workflow su Python 3.12, sviluppo su 3.14.
  - Trailer di alcuni commit della Parte A (`7a12bab`, forse `4a4e690`) dice «Haiku 4.5» invece di «Sonnet 5.5».
- [ ] **(g) Nessun telefono Android vero è mai stato collegato, su nessun sistema** (né diretto né con ADB): autorizzazione, ricerca
  reale, copia e cancellazione da provare. **È la verifica più importante che manca.**
  - Windows diretto (WPD): mai eseguito su hardware; `wpd_win.ps1` coperto solo da test di contratto e parsing.
  - Linux diretto (`gio`/`jmtpfs`): solo test simulati.
  - macOS diretto: verificato solo fino a «nessun telefono collegato».
- [ ] Limite di progetto (non un difetto): con il collegamento diretto di **Windows** la cancellazione dal telefono non è disponibile
  (Failed Approaches #17).
- [ ] Opzionale: firma del `.exe` (evita SmartScreen) e firma/notarizzazione del `.app` macOS (senza firma: clic destro → Apri).

---

## Failed Approaches (Don't Repeat These)

1. **Thread per il lavoro in background.** Su **macOS + Tk 9** (Python 3.14 Homebrew) creare un
   thread mentre la finestra è aperta **blocca il processo**; con Tk 8.5 (Python di sistema)
   funziona. Provato anche un thread che non tocca Tk: blocca ugualmente. **Soluzione**: generatori
   a passi avanzati da `after()`. **Non reintrodurre `threading`** (rimane solo
   `threading.Event` per l'annullamento, che va bene).
2. **MTP via «Android File Transfer» (macOS)**: inaffidabile (cartelle vuote, copie interrotte).
   Il percorso nuovo **non è AFM**: su macOS si usa **PTP via ImageCaptureCore**, che è cosa
   diversa. Attenzione: non è ancora stato provato con un telefono vero, quindi non è una smentita.
3. **Più finestre Tk nello stesso processo di test**: crash `SIGTRAP` (exit 133). **Soluzione**:
   una sola finestra per sessione (`tests/conftest.py`) + `ricostruisci_pagine()` + `azzera()`.
4. **`time.sleep()` nei cicli di attesa dei test grafici**: lento e fragile. **Soluzione**:
   `tests/aiuto.py:attendi()` usa `update()` + `time.monotonic()`.
5. **Verificare la GUI da tool di automazione**: un processo in background **non ha accesso al
   window server** → `tkinter.Tk()` si blocca, e i processi che *provano a mostrare* la finestra
   morivano con `EXC_BREAKPOINT SIGTRAP` dentro `showRootWindow` (`libtcl9tk9.0.dylib`).
   **Soluzione**: `launchctl asuser $(id -u) env PYTHONPATH="$PWD" .venv/bin/python script.py`
   + `screencapture -x`. Le schermate hanno rivelato due bug veri.
6. **Temi nativi `aqua`/`vista`**: ignorano i colori impostati → in modalità scura testo scuro su
   fondo scuro, finestra apparentemente vuota. **Soluzione**: tema `clam` + tavolozza rilevata dal
   sistema + test di contrasto WCAG.
7. **Pagine figlie della finestra invece del contenitore**: coprivano l'indicatore dei passi.
   **Soluzione**: `super().__init__(parent.container)` in tutte le pagine.
8. **`os.path.normcase` per confrontare le maiuscole**: su POSIX è un no-op. **Soluzione**:
   `str.casefold()` in `core/planner.py`.
9. **`USERPROFILE` impostato nei test su macOS**: `core/osutil.py` lo preferisce a `HOME` (giusto
   per Windows) → i test scrivevano nella cartella di sessione. **Soluzione**: la fixture lo
   imposta solo su Windows.
10. **Test che dipendono dalla cartella utente reale**: dopo che l'app ha installato platform-tools,
    i test trovavano un `adb` vero. **Soluzione**: `HOME`/`USERPROFILE` temporanei.
11. **`explorer` su Windows esce con codice 1** anche quando la cartella si apre: giudicare dal
    codice dava un falso errore. Ora su Windows non si controlla.
12. **Cross-compilare l'eseguibile Windows da macOS**: impossibile (PyInstaller non fa
    cross-compilazione; niente Wine). Un `.exe` così prodotto sarebbe **non verificabile**.
    **Soluzione**: la pipeline GitHub su runner Windows vero (dalla v0.2 produce il `Setup.exe`; la cartella con i `.bat` non esiste più).
13. **(storico: i `.bat` sono stati eliminati in v0.2)** **Caret di `cmd` dentro gli snippet Python dei `.bat`.** `sys.version_info ^>= (3, 9)`: il caret
    arriva **letteralmente a Python** → `SyntaxError` → il controllo di Python falliva sempre.
    **Soluzione** (poi superata dall'eliminazione dei `.bat`): niente caret e un test che compilava ogni
    snippet `-c "..."` degli script.
14. **Workflow GitHub che non parte al primo tag.** Il tag era stato pubblicato pochi secondi dopo
    il branch. **Soluzione**: ripubblicare il tag.
15. **Verifiche dipendenti dal tempo**: `assert app.attributes("-topmost")` falliva per un `after`.
    **Soluzione**: registrare le chiamate e verificare l'intenzione, non lo stato dopo il timer.
16. **Comandi distruttivi concatenati**: un `git checkout` in coda a un comando lungo ha
    ripristinato `theme.py` appena riscritto, perdendo il lavoro. Mai mettere
    `git checkout`/`git clean` nello stesso comando di altro lavoro.
17. **Cancellare i file dal telefono con il collegamento diretto di Windows**: l'unico accesso non
    amministrativo (`Shell.Application`) offre `InvokeVerb("delete")`, che apre una richiesta di
    conferma; con `-NonInteractive` resterebbe appesa per sempre. **Soluzione**: dichiarare che con
    quel collegamento la cancellazione non è disponibile, invece di rischiare un blocco.
18. **`.ps1` senza BOM.** Sembrava una buona idea («il BOM rompe cmd.exe»), ma è **sbagliato**:
    cmd.exe non esegue i `.ps1`. Windows PowerShell 5.1 legge i file senza BOM con la codifica
    ANSI: gli accenti delle frasi italiane diventano illeggibili e `$tipo -eq "Dispositivo
    portatile"` non trova più nulla su Windows italiano. **Soluzione**: i `.ps1` **hanno** il BOM
    (oggi: `wpd_win.ps1` e i due script della pipeline in `installer/windows/`; i `.bat` non esistono più). C'è un test che lo verifica.
19. **Riprovare lo stesso collegamento dopo un errore.** Il confronto `self.app.remote is not
    precedente` era sempre vero (gli oggetti sono ricostruiti a ogni tentativo) → ciclo infinito
    di tentativi e messaggio d'errore mai mostrato. **Soluzione**: `App._gia_provati`, un insieme
    di nomi già provati.
20. **Generatore chiuso ≠ processo interrotto.** `GeneratorExit` non è né `OSError` né
    `FotoFacileError`, quindi `except` non lo prende. Dove serve pulizia va sempre un `finally`.
21. **`app.update()` sulla finestra condivisa dei test.** Una volta ha bloccato la suite. Nei test usare
    `update_idletasks()` (o `tests/aiuto.py:attendi()`), e sostituire `app.run_task` con un finto quando
    si provano i flussi d'errore.
22. **Layout a misura di schermo grande.** Con scala 1,5 i pulsanti «Copia le foto» e «Copia» finivano fuori
    schermo (avanti/copia sotto «Altre opzioni», percentuale troppo alta). **Soluzione**: pulsanti principali
    sopra le scelte rare, percentuale a 40 pt; c'è un test (salta se lo schermo è più basso di 800 px). Ogni
    nuova pagina va provata a scala 1,5.
23. **Invio globale.** `<Return>` lanciava l'azione principale anche con il focus su un pulsante diverso
    (es. «Indietro»). **Soluzione**: `App._tasto_invio` preme il pulsante col focus (se non spento).

---

## Key Decisions

| Decisione | Perché |
|---|---|
| **Scelta automatica del collegamento** (`core/trasporto.py`) | Nessuno deve attivare il Debug USB; chi ce l'ha già attivo usa il percorso veloce senza saperlo |
| **Diretto per sistema** (PTP/ImageCaptureCore, WPD, MTP/`gio`) | È il comportamento normale di ogni telefono appena collegato: niente impostazioni da cambiare |
| **Aiutanti come processi separati** (PyObjC, PowerShell, `gio`) | I cicli di eventi nativi (Cocoa, COM) non si possono mescolare con Tk; un processo a parte si può interrompere senza bloccare la finestra |
| **PyObjC solo nell'aiutante** | Import costoso e inutile se il collegamento diretto non serve; senza PyObjC il trasporto non è «disponibile» e si ripiega su ADB |
| **Copia piatta predefinita** | Chi usa il programma vuole le foto, non l'albero delle cartelle del telefono |
| **Windows: `CopyHere` passa da una cartella di appoggio** | `CopyHere` è asincrono e non sa scrivere su un flusso |
| **Niente thread**: generatori a passi con `after()` | Tk 9 su macOS si blocca con qualunque thread; UI reattiva e test deterministici |
| Un solo modo di rilanciare sé stessi: `osutil.comando_se_stesso()` | C'era già stato un bug di percorso di una cartella: un'unica funzione evita che si ripeta |
| Tema **`clam`** + tavolozze chiara/scura | Gli unici colori che i temi nativi non possono ignorare |
| `.part` + `fsync` + `os.replace` + verifica dimensione | Mai file troncati o foto perse; annullamento senza residui |
| Nome del `.part` con il numero di processo | Due istanze aperte sulla stessa cartella non si rovinano a vicenda |
| `FotoFacileError(message, hint)` ovunque | Messaggi umani + azione suggerita, mai stack trace |
| Il consiglio generico **più** il testo d'errore del comando | Quest'ultimo è spesso la spiegazione più precisa («il telefono è bloccato») |
| Errori non ritentabili non vengono ritentati | Non ricopiare 3 volte un file su disco pieno |
| Windows = `Setup.exe` (Inno Setup) costruito dalla pipeline | Unico modo onesto di ottenere un `.exe` verificato (su un runner Windows vero); niente `.bat` da lanciare a mano |
| Installer **per utente, senza amministratore** | Un anziano non ha (né deve avere) i permessi; niente richiesta UAC |
| Testo grande di serie (scala 1,25) e regolabile con `A−`/`A+` | Il pubblico principale legge male i caratteri piccoli; la scelta si ricorda |
| Passi con **un solo pulsante grande**, il resto in «Altre opzioni» / «Mostra i dettagli» | Meno scelte = meno errori; le rare restano raggiungibili |
| Cancellare dal telefono: **conferma a finestra subito** (predefinito «No») + promemoria rosso | L'azione non si annulla; mai attivarla per sbaglio con un doppio clic |
| Nomi veri delle cartelle (`core/nomi_cartelle.py`) | «Camera» e «Screenshots» non dicono niente a chi non è pratico |
| `run_task` chiama sempre `on_error` (anche per eccezioni impreviste) | Nessuna pagina resta senza via d'uscita |
| Versione in un solo punto (`fotofacile/__init__.py`) | Installer, pipeline e programma non possono discordare |

---

## Current State

**Working**: avvio → 4 passi → copia → resoconto, in modalità demo e (su macOS) fino al riconoscimento del
telefono con il collegamento diretto; scelta automatica dei trasporti; copia piatta; conversione WebP;
nuova interfaccia (testo regolabile, Invio/Esc, nomi veri, conferma di cancellazione); `doctor`;
`--selftest`; script Inno Setup e pipeline scritti e provati **solo nei test statici**.
**636 test verdi**, `pyflakes` vuoto.

**Broken**: nulla di noto nella suite.

**Non verificato** (non è la stessa cosa di «funziona»): **tutta la catena Windows** (pipeline, `.ps1`, Inno Setup,
installazione vera, D17, WPD), collegamento diretto Linux e macOS con un telefono, qualsiasi operazione con un telefono
Android reale. Vedi «Not Yet Done».

**Git**: il lavoro è **committato** su `revisione-v0.2` (HEAD `7226f8b`, `git log --oneline main..HEAD` = tutta la revisione).
Fuori dai commit restano solo i file rigenerati di `graphify-out/` (di proposito). Nessun remoto aggiornato.

---

## Files to Know

| File | Perché è importante |
|---|---|
| `fotofacile/core/trasporto.py` | Protocollo `Trasporto`, `TrasportoAdb`, `TrasportoDemo`, `TrasportoComposto`, `trasporti_disponibili()` |
| `fotofacile/core/trasporto_aiutante.py` | Dialogo con gli aiutanti (righe JSON), `comando_aiutante()`, `ambiente_aiutante()`, copia `.part` con `fsync`, pulizia dei processi |
| `fotofacile/core/trasporto_mac.py` / `trasporto_win.py` / `trasporto_linux.py` | Il collegamento diretto di ciascun sistema |
| `fotofacile/aiutanti/` | `ptp_mac.py` (ImageCaptureCore), `wpd_win.py` + `wpd_win.ps1` (WPD/PowerShell), `mtp_linux.py` (gio/jmtpfs) |
| `fotofacile/core/osutil.py` | Differenze di sistema **e** `comando_se_stesso()` / `cartella_progetto()`: l'unico posto da cui si rilanciano i processi figli |
| `fotofacile/core/ops.py` | `ProcessoEsterno` (stdout sempre su file, `leggi_output`, `env`), `ScaricatoreAPassi`, `Annullato` |
| `fotofacile/core/planner.py` | Nomi sicuri, collisioni, accorciamento percorsi **senza mai toccare la radice scelta**; `preserve_structure=False` |
| `fotofacile/core/installer.py` | platform-tools con impronta ufficiale ed estrazione **atomica** |
| `fotofacile/core/adb_passi.py` | `AdbAPassi`/`AdbDemoAPassi`, `percorso_temporaneo()`, `_controlla_spazio()`, `_dimensione_prevista()` |
| `fotofacile/ui/app.py` | `usa_collegamento_migliore`, `cambia_collegamento`, `_gia_provati`, `run_task` (epoca anti-abbandono), `ricostruisci_pagine` |
| `fotofacile/ui/page_connect.py` | Sondaggio con `after_cancel`, finestra di aiuto riusata, ripiego automatico su un altro collegamento |
| `fotofacile/ui/theme.py` | Tavolozze, `contrasto()` WCAG, `tema_testo()`/`tema_tela()`/`tema_finestra()` per i widget Tk classici |
| `docs/REVISIONE-v0.2.md` | **Leggere per primo**: audit per gruppi (D1–D31), poi «Parte C e D» (interfaccia e installatore) |
| `docs/PIANO-REVISIONE.md` | Difetti `B1–B24` e `C1–C19` della v0.1 (storico) |
| `.superpowers/sdd/progress.md` | Registro di tutte le task (A, B, C, D) con i minor aperti; `task-*-report.md` e `carryover.md` hanno i dettagli |
| `fotofacile/core/impostazioni.py` | Impostazioni personali (`~/.fotofacile/impostazioni.json`, scala del testo) |
| `fotofacile/core/nomi_cartelle.py` | Nomi comprensibili delle cartelle e riconoscimento di miniature/sticker |
| `fotofacile/ui/widgets.py` | `TestoAdattivo`, `Banner`, `LogPane`, `StepIndicator`, `PathChooser` |
| `fotofacile/ui/page_select.py` / `page_options.py` / `page_transfer.py` | Passi 2, 3, 4 (`azione_principale`/`azione_indietro` = Invio/Esc) |
| `fotofacile/cli.py` | `doctor`, `--selftest`, `emetti()` (stampa o scrive `diagnosi.txt`/`selftest.txt` senza terminale) |
| `installer/windows/FotoFacile.iss` | Script Inno Setup (+ `Benvenuto.txt`, `verifica-eseguibile.ps1`, `prova-installazione.ps1` usati dalla pipeline) |
| `scripts/leggi_versione.py` | Legge la versione da `fotofacile/__init__.py` per la pipeline |
| `tests/test_regressioni.py` | Un test per ogni bug corretto; il commento dice cosa succedeva **prima** |
| `tests/test_trasporto.py` | Scelta automatica, contratto degli aiutanti, WPD/Linux simulati |
| `tests/conftest.py` | Finestra condivisa + `azzera()`: capire questo file evita crash e test fragili |
| `tests/pilota_app.py` | Collaudo end-to-end dell'app vera (`FF_DEST`, `FF_ESITO`) |
| `scripts/build_app.py` | Build multipiattaforma + icona + `--add-data` degli aiutanti + PyObjC su macOS |
| `.github/workflows/build-installers.yml` | Installer macOS (dmg) + Windows (Inno Setup, con prova d'installazione) + Release (solo su tag `v*`) — **mai eseguita** |

---

## Code Context

```python
# core/trasporto.py — il contratto usato dalla grafica
class Trasporto(Protocol):
    nome: str; spiegazione: str
    def disponibile(self) -> bool
    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]
    def cerca_media(self, serial, include_videos=True, annulla=None) -> Generator[float, None, list[MediaFile]]
    def copia(self, serial, remoto, destinazione, on_scritti=None, annulla=None,
              remoto_dimensione: int | None = None) -> Generator[float, None, int]
    def cancella(self, serial, remoto) -> Generator[float, None, None]
    def riavvia(self) -> Generator[float, None, None]
    def pulisci(self) -> None
def trasporti_disponibili(env=None, sistema=None, adb_path=None) -> list[Trasporto]

# core/osutil.py — un solo modo di rilanciare sé stessi (dal sorgente E dal pacchetto)
def comando_se_stesso(*argomenti) -> list[str]   # → [python, <progetto>/fotofacile.py, *arg]
def cartella_progetto() -> Path                  # per PYTHONPATH del figlio

# core/trasporto_aiutante.py
def comando_aiutante(nome) -> list[str]          # = comando_se_stesso("--aiutante", nome)
def ambiente_aiutante() -> dict                  # aggiunge PYTHONPATH dal sorgente
def leggi_dispositivi(testo) -> list[DeviceInfo]
def leggi_elenco(testo) -> list[MediaFile]       # righe JSON, quelle rotte vengono ignorate

# core/ops.py
class ProcessoEsterno:
    def __init__(self, args, timeout=30.0, umano="", hint="", output_file=None,
                 orologio=time.monotonic, leggi_output=True, env=None) -> None
    def avvia(self) -> None                      # stdout SEMPRE su file, mai su tubo
    def passo(self) -> bool
    def aspetta(self) -> Generator[float, None, RisultatoComando]   # try/finally: termina()
    def esito(self) -> RisultatoComando
    def termina(self) -> None

# core/adb_passi.py — aiuti condivisi con gli altri trasporti
def percorso_temporaneo(destinazione: Path) -> Path      # <nome>.<pid>.part
def _controlla_spazio(destinazione, dimensione=None) -> None
def _dimensione_prevista(dimensione) -> int | None

# core/planner.py
@dataclass(frozen=True)
class TransferOptions:
    destination: Path
    preserve_structure: bool = False             # copia piatta (era True)
    skip_existing: bool = True
    delete_after: bool = False
    include_videos: bool = True
    date_from: int | None = None

# ui/app.py
class App(tk.Tk):
    INTERVALLO_PASSI = 0.02
    def usa_collegamento_migliore(self) -> bool  # azzera _gia_provati e sceglie il primo
    def cambia_collegamento(self) -> bool        # passa a uno NON ancora provato; False se finiti
    def run_task(self, generatore, on_done=None, on_error=None, intervallo=None) -> None
    def annulla_task(self) -> None
    def ricostruisci_pagine(self) -> None        # ora chiama go_to("connect")
    @property
    def remote(self) -> Trasporto | None         # proprietà, con setter (i test fanno app.remote = None)

# ui/theme.py — i widget Tk classici non seguono gli stili ttk: vanno colorati a mano
def tema_testo(testo: tk.Text) -> None           # sfondo E testo E cursore E selezione
def tema_tela(tela: tk.Canvas) -> None
def tema_finestra(finestra: tk.Misc) -> None
```

Stato condiviso fra le pagine: `app.device`, `app.media_files`, `app.options`, `app.results`,
`app.cancel_event`, `app.remote` (`Trasporto` | `None`), `app.history()`.

---

## Setup per Windows

L'utente scarica `FotoFacile-Setup-<versione>.exe` (Inno Setup, `installer/windows/FotoFacile.iss`,
costruito dalla pipeline GitHub), fa doppio clic e preme «Avanti». Chi non vuole installare nulla
usa `FotoFacile-portable.zip`. Non ci sono più `.bat`/`.ps1` d'installazione né la cartella
«FotoFacile per Windows» (task D3). `fotofacile/aiutanti/wpd_win.ps1` **resta**: è l'aiutante
che parla con il telefono, e viaggia con il programma (`build_app.py --add-data`).
Il Setup **non si può costruire da macOS**: lo fa il job Windows della pipeline (Python 3.12, PyInstaller, Pillow, Inno Setup da
Chocolatey). Diagnosi dal programma installato: menu Start → «FotoFacile - Diagnosi» (scrive `%USERPROFILE%\.fotofacile\diagnosi.txt`).

---

## Resume Instructions

1. **Ambiente e test**
   ```bash
   cd ~/Desktop/Programmazione/FotoFacile
   .venv/bin/python -m pytest tests | tail -3        # atteso: 636 passed
   ```
   - Nota: `pytest.ini` aggiunge già `-q`, quindi un doppio `-q` nasconde la riga di riepilogo.
   - Se fallisce: `.venv/bin/python -m pytest tests --tb=short` e guarda i primi 3 errori; i test
     grafici si saltano da soli se l'ambiente non apre finestre (non è un errore).

2. **Diagnosi e modi di collegamento**
   ```bash
   .venv/bin/python fotofacile.py doctor
   ```
   - Atteso su questo Mac: «Collegamento diretto — disponibile» e «Collegamento rapido — disponibile».
   - Se «Collegamento diretto» non è disponibile su macOS: `.venv/bin/python -m pip install -r requirements.txt`.

3. **Contratto dell'aiutante senza telefono** (macOS)
   ```bash
   .venv/bin/python fotofacile.py --aiutante ptp_mac dispositivi   # atteso: {"dispositivi": []}
   .venv/bin/python fotofacile.py --aiutante ptp_mac elenca        # atteso: «Non vedo nessun telefono…», uscita 3
   ```
   - `--aiutante` è **interna** (non compare in `--help`); vale anche da pacchetto PyInstaller.

4. **Collaudo dell'app vera** (finestra + copia su disco)
   ```bash
   FF_DEST="/tmp/collaudo-foto" FF_ESITO="/tmp/esito.json" .venv/bin/python tests/pilota_app.py
   # senza sessione grafica:
   launchctl asuser $(id -u) env PYTHONPATH="$PWD" "$PWD/.venv/bin/python" "$PWD/tests/pilota_app.py"
   ```
   - Atteso: `"ok": true`, 54 file, `"errori": []`, nessun `.part`, **nessuna sottocartella**
     dentro `/tmp/collaudo-foto` (copia piatta).

5. **Guardare la finestra**
   ```bash
   launchctl asuser $(id -u) env PYTHONPATH="$PWD" "$PWD/.venv/bin/python" -c \
     "from fotofacile.ui.app import App; a=App(demo_mode=True); a.after(4000, a.destroy); a.mainloop()" &
   sleep 3; screencapture -x /tmp/schermo.png
   ```

6. **Windows**: il `Setup.exe` si costruisce solo dalla pipeline (`.github/workflows/build-installers.yml`).
   Test statici di aiutante, `.iss` e workflow: `.venv/bin/python -m pytest tests/test_aiutante_windows.py tests/test_installer_iss.py tests/test_installer_pacchetti.py tests/test_workflow.py -o addopts="" -q`.
   Prima di lanciare la pipeline leggere «Not Yet Done» (a): serve la conferma di Marco per push/tag.

7. **Build macOS**: `pip install -r requirements.txt`, poi `python3 scripts/build_app.py --verify` →
   `dist/FotoFacile.app`; l'autocollaudo deve rispondere `{"ok": true}`.

8. **Dopo ogni modifica al codice: `graphify update .`** (obbligatorio).

9. **Prima di ogni consegna**: `.venv/bin/python -m pyflakes fotofacile scripts` deve essere vuoto.

10. **Modifiche future**: test prima, mai `tkinter` dentro `core/`, mai thread, ogni nuova pagina
    dentro `app.container`, **mai PyObjC nel processo principale**, e se cambia il contratto degli
    aiutanti vanno aggiornati tutti e tre + `trasporto_aiutante.py`.

---

## Setup Required

- Python 3.9+ con Tkinter (qui: 3.14.7, Tk 9.0); `.venv` già pronto con `pytest`, `pyinstaller`, `pyflakes`.
- **Solo macOS / uso dal sorgente**: `.venv/bin/python -m pip install -r requirements.txt` (PyObjC,
  collegamento diretto). Windows e Linux non hanno bisogno di niente.
- Graphify: `uv tool install graphifyy` (interprete in `graphify-out/.graphify_python`).
- Grafica da automazione: `launchctl asuser $(id -u)` + `PYTHONPATH` esplicito + `screencapture`.
- Nessuna chiave API.
- Windows: nessun prerequisito sul PC di destinazione (il `Setup.exe` contiene già tutto). Per sviluppare la conversione WebP dal sorgente: `pip install pillow` (facoltativo).

---

## Edge Cases & Error Handling

- Nessun telefono / non autorizzato / `offline` / `no permissions` → messaggi dedicati
  (`core/devices.STATE_MESSAGE`); con il collegamento diretto «nessun telefono» è un elenco vuoto.
- Collegamento diretto non disponibile → si usa ADB; se non c'è nemmeno quello, compare
  «Installa componente mancante» e la pagina lo dice.
- Più collegamenti insieme → `TrasportoComposto` usa il primo che vede davvero il telefono; se uno
  solleva un errore si passa al successivo. **Una sola volta per modo** (`App._gia_provati`).
- Cavo solo-ricarica o driver mancante → suggerimenti espliciti nell'aiuto e nello stato.
- Spazio su disco → `_controlla_spazio(dest, dimensione)` blocca **solo** se il file non ci sta
  davvero; senza dimensione nota chiede un margine minimo di 16 MB.
- Disco pieno a metà copia (il comando esterno fallisce, non Python) → `_esito_di_copia` riconosce
  «no space» e dà il messaggio dedicato.
- Annullamento a metà file → `Annullato` → `.part` rimosso, risultati parziali validi.
- Abbandono del lavoro (indietro, nuova ricerca, chiusura) → `annulla_task()` chiude il generatore;
  i trasporti terminano i processi aiutanti (`finally`, non `except`) e rimuovono il `.part`.
- Telefono bloccato durante l'elenco → timeout dell'aiutante con errore umano.
- Aiutante che scrive molto sull'uscita degli errori → il testo viene aggiunto al suggerimento
  (prima veniva scartato).
- Linux: il montaggio gvfs è del desktop → si ricordano i telefoni usati e li si smonta alla
  chiusura, senza mai toccare cartelle non nostre.
- Windows: cancellazione non disponibile con WPD → messaggio + suggerimento; la cartella di
  appoggio della copia viene sempre rimossa.
- Errore di disco/permessi → `errors.traduci_errore_file` → messaggio + suggerimento, nessun retry.
- Cronologia non scrivibile/corrotta/malformata → voci ignorate, avviso, copia comunque riuscita.
- Destinazione non leggibile o relativa → errore umano nella pagina 3/4, pagina ancora usabile.
- Finestra non apribile → messaggio chiaro + `avvio.log` + `doctor`; `--selftest` distingue
  «grafica rotta» da «avvio sbagliato».
- Modalità scura/chiara → rilevata a ogni avvio; se il rilevamento fallisce resta la chiara.

---

## Warnings

- **Mai importare PyObjC/ImageCaptureCore nel processo principale**: solo in
  `fotofacile/aiutanti/ptp_mac.py`. Il main verifica con `importlib.util.find_spec` (economico).
- **Contratto degli aiutanti**: comandi `dispositivi` / `elenca` / `copia` / `cancella`; uscita
  standard a righe JSON (`{"dispositivi": [...]}`, una riga per file + `{"fine": true}`, i byte
  della copia su stdout), messaggi per l'utente su stderr, codici 0/2/3. Se cambia, vanno aggiornati
  **tutti e tre** gli aiutanti e `core/trasporto_aiutante.py`.
- **Codifica degli script PowerShell**: i `.ps1` (`wpd_win.ps1` e i due di `installer/windows/`, questi con
  fine riga CRLF) **devono avere** il BOM UTF-8 (PowerShell 5.1 legge
  senza BOM come ANSI: accenti illeggibili e confronti di testo rotti); eventuali
  `.bat` **non devono** averlo (cmd.exe non lo salta: `'ï»¿@echo' non riconosciuto`; oggi non ce ne sono).
- **`wpd_win.ps1` deve viaggiare con il programma**: è incluso da `build_app.py` (`--add-data`). Senza, il collegamento diretto di Windows non funziona.
- **Un solo modo di rilanciare sé stessi**: usare `osutil.comando_se_stesso()`. Il bug di una
  cartella in `comando_aiutante()` ha reso morto tutto il collegamento diretto dal sorgente.
- **Non riprovare lo stesso collegamento**: `App._gia_provati` esiste per questo. Un confronto fra
  oggetti ricostruiti è sempre vero → ciclo infinito.
- **`finally`, non `except`**: `GeneratorExit` non è né `OSError` né `FotoFacileError`.
- **`--aiutante` e `--prova-finestra`** sono opzioni **interne**, nascoste da `--help`.
- **Non reintrodurre thread**: su macOS + Tk 9 bloccano l'app (Failed Approaches #1).
- **Tema `clam` obbligatorio**: `aqua`/`vista` ignorano i colori.
- **Le pagine vanno dentro `app.container`** (`super().__init__(parent.container)`).
- **I widget Tk classici** (`tk.Text`, `tk.Canvas`) non seguono gli stili ttk: usare
  `theme.tema_testo()` / `tema_tela()` / `tema_finestra()`, altrimenti in modalità scura il testo
  resta nero su fondo scuro.
- Non mettere `git checkout`/`git clean` nello stesso comando di altro lavoro.
- I test grafici **si saltano** se `tk_available()` fallisce: è l'ambiente, non il codice.
- I test devono sempre isolare `HOME`/`USERPROFILE`: sul Mac dell'utente esiste un `adb` vero.
- `graphify-out/` contiene file pesanti (~1 MB `graph.json`, 3,6 MB `graph.svg`): rigenerali con
  `graphify update .`, non modificarli a mano.
- Il `.app` non è firmato: prima apertura con clic destro → «Apri». L'`.exe` Windows non può essere
  creato da macOS.
- Se aggiungi una pagina, aggiorna `azzera()` in `tests/conftest.py`.
- **La scala del testo è globale** (`theme.imposta_scala`): i test che creano un `App` proprio la spostano; la fixture autouse
  `scala_testo_normale` la riporta a 1,0. Ogni pagina nuova: nessun `font()` sotto 14, nessun `wraplength` fisso (usare `TestoAdattivo`).
- **Il `.iss` e i `.ps1` non sono mai stati eseguiti**: non fidarsi finché non gira la pipeline (vedi «Not Yet Done» a).
- **Non pubblicare** (push, tag, Release) senza chiedere a Marco.

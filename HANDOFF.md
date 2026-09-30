# Handoff: FotoFacile — app desktop per copiare foto da Android

**Generato**: 2026-09-28 (aggiornato **dopo** la seconda revisione indipendente)
**Branch**: `main` (repo locale, nessun remoto configurato)
**Stato**: **Completo nella parte testabile** — **383 test verdi**. Consegnati: scelta automatica
del collegamento (**niente Debug USB obbligatorio**), **copia piatta** predefinita, correzione di
tutti i difetti `B1–B24` e `C1–C19` elencati in `docs/PIANO-REVISIONE.md`.
Repo GitHub pubblico `marcosalvatori0/fotofacile` con pipeline che costruisce gli installer su
runner macOS e Windows; Release `v0.1.0` con `FotoFacile-Setup-0.1.0.exe`, `FotoFacile-portable.zip`,
`FotoFacile-0.1.0.dmg`.
**Non verificati** (vedi «Not Yet Done»): collegamenti diretti di Windows e Linux su hardware
reale, collegamento diretto macOS con un telefono vero, qualsiasi operazione con un telefono
Android reale.

---

## Goal

Permettere a **persone non tecniche** di copiare foto e video da un telefono Android al computer
con una procedura guidata in italiano, senza gestore file e senza gergo tecnico. Multi-piattaforma
(Windows/macOS/Linux), **senza Debug USB da attivare** e senza dipendenze obbligatorie per chi usa
il programma. I file arrivano **direttamente nella cartella scelta**, con la possibilità di
ricreare le cartelle del telefono se serve.

---

## Completed

### Collegamento senza Debug USB (novità principale)
- [x] Livello di trasporto che sceglie da sé il collegamento: `core/trasporto.py`,
  `core/trasporto_aiutante.py`, `core/trasporto_mac.py`, `core/trasporto_win.py`,
  `core/trasporto_linux.py` + `fotofacile/aiutanti/`.
- [x] **macOS**: PTP/MTP via `ImageCaptureCore` (PyObjC) — lo stesso meccanismo di «Acquisizione immagini».
- [x] **Windows**: WPD via `Shell.Application` in PowerShell (`aiutanti/wpd_win.ps1`).
- [x] **Linux**: MTP via `gio`/gvfs, ripiego `jmtpfs`.
- [x] **ADB** resta solo come *scorciatoia* se il Debug USB è già attivo; mai obbligatorio.
- [x] `TrasportoComposto` prova i collegamenti in ordine e usa il primo che vede davvero il telefono.
- [x] Le istruzioni «Debug USB» restano come **ultima spiaggia** dietro «Il telefono non viene riconosciuto?».

### Copia piatta
- [x] `TransferOptions.preserve_structure=False`: le foto finiscono direttamente nella cartella
  scelta (`Immagini/FotoFacile/<modello>/<data>`), senza `DCIM/Camera/...`.
- [x] La struttura si riattiva con la casella «Ricrea anche le cartelle del telefono».
- [x] Collisioni risolte con `nome (1).jpg`, `nome (2).jpg` — il contatore **sopravvive** all'accorciamento.

### Revisione completa
- [x] **Fase 1–3**: tutti i difetti `B1–B24` di `docs/PIANO-REVISIONE.md`.
- [x] **Fase 4** (seconda revisione indipendente): tutti i difetti `C1–C19`. I tre più gravi:
  - `comando_aiutante()` sbagliava di una cartella il percorso di avvio → **tutto il collegamento
    diretto era morto dal sorgente**. Ora `osutil.comando_se_stesso()` + `fotofacile/__main__.py`.
  - `_controllo_fallito` riprovava lo stesso collegamento **all'infinito** (confronto sempre vero).
    Ora `App._gia_provati` + `App.cambia_collegamento()`.
  - `_scansione_in_corso` non veniva azzerato quando il lavoro era abbandonato altrove →
    schermata bloccata per sempre su «Sto cercando…».
- [x] Diagnostica arricchita: `doctor` mostra la sezione **«Modi di collegamento»**.

### Resto
- [x] App completa: 4 passi guidati (collegamento → scelta foto → destinazione → copia).
- [x] Motore **senza thread**: generatori a passi avanzati da `after()`, copia `.part` + rinomina
  atomica, verifica dimensioni, dedup per dispositivo, cancella-dopo-copia con conferma, retry
  solo sugli errori transitori.
- [x] Installazione automatica di platform-tools con **verifica dell'impronta ufficiale** e
  estrazione **atomica**; **modalità demo** senza telefono.
- [x] Tema chiaro/scuro secondo il sistema (`clam` + tavolozze, contrasto WCAG ≥ 7). I `tk.Text`
  (area «Dettagli» e finestra di aiuto) ora hanno `foreground` esplicito: prima erano nero su
  fondo scuro, cioè invisibili.
- [x] Diagnostica: `doctor`, `--selftest`, `--prova-finestra`, `--aiutante` (interna);
  registro `~/.fotofacile/avvio.log`; avviso nativo se la finestra non si può aprire.
- [x] **383 test verdi** (erano 293), inclusi `tests/test_regressioni.py` (un test per ogni bug
  corretto, con il commento che spiega cosa succedeva **prima**), `tests/test_trasporto.py`,
  `tests/test_icona.py`, `tests/test_app_completa.py` (app vera in sottoprocesso).
- [x] **Verificato a schermo** in modalità scura: area «Dettagli» e finestra di aiuto leggibili.
- [x] **Collaudo end-to-end dell'app vera**: 54/54 file copiati (60,9 MB) in 11 s, 0 errori,
  0 `.part` residui, **nessuna sottocartella creata**.
- [x] **Aiutante macOS avviato davvero**, dal percorso reale usato dall'app e da una cartella
  estranea: `{"dispositivi": []}` con uscita 0.
- [x] **(v0.1, superato in v0.2: sostituito dal `Setup.exe`, task D3)** Pacchetto Windows ricreato sulla Scrivania: `~/Desktop/FotoFacile per Windows/`
  (51 file, 0,39 MB) — `Avvia FotoFacile.bat`, `Crea l'eseguibile per Windows.bat`,
  `Installa FotoFacile.bat`, `LEGGIMI - Windows.txt`, tutto `fotofacile/` (compreso
  `aiutanti/wpd_win.ps1`), `requirements.txt`.
- [x] **Graphify completo e aggiornato**: `graphify-out/` con 1579 nodi, 3747 archi, 86 comunità.

---

## Not Yet Done

- [ ] **Nessun telefono Android vero è mai stato collegato** (né diretto né con ADB):
  autorizzazione, ricerca reale dei media, copia e cancellazione restano da provare su un
  dispositivo. **È la verifica più importante che manca.**
- [ ] **Collegamento diretto Windows mai provato su hardware reale**: non c'è una macchina Windows.
  `wpd_win.ps1` esiste e i test coprono contratto, parsing e cartella di appoggio, ma **nessuna
  copia vera** è mai passata da `Shell.Application`. PowerShell non esiste su questa macchina:
  le modifiche agli script sono state verificate solo staticamente (bilanciamento, sintassi degli
  snippet Python, BOM).
- [ ] **Collegamento diretto Linux mai provato su hardware reale**: nessun desktop con `gio`/gvfs
  e nessun `jmtpfs` in questo ambiente; montaggio, elenco e smontaggio coperti solo da test simulati.
- [ ] **Collegamento diretto macOS verificato solo fino a «nessun telefono collegato»**:
  l'aiutante parte, `dispositivi` → `{"dispositivi": []}` (uscita 0), `elenca` → «Non vedo nessun
  telefono collegato.» (uscita 3). Riconoscimento di un telefono vero e copia **mai eseguiti**.
- [ ] **Nessuna build rifatta dopo la revisione**: `dist/` e la Release `v0.1.0` sono **precedenti**
  ai trasporti e a PyObjC. La pipeline GitHub li ricostruirà al prossimo tag.
- [ ] Limite di progetto (non un difetto): con il collegamento diretto di **Windows** la
  cancellazione dal telefono non è disponibile (vedi Failed Approaches #17).
- [ ] Opzionale: firma/notarizzazione del `.app` macOS (senza firma: clic destro → Apri la prima volta).

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
    (oggi resta solo `wpd_win.ps1`; i `.bat` non esistono più). C'è un test che lo verifica.
19. **Riprovare lo stesso collegamento dopo un errore.** Il confronto `self.app.remote is not
    precedente` era sempre vero (gli oggetti sono ricostruiti a ogni tentativo) → ciclo infinito
    di tentativi e messaggio d'errore mai mostrato. **Soluzione**: `App._gia_provati`, un insieme
    di nomi già provati.
20. **Generatore chiuso ≠ processo interrotto.** `GeneratorExit` non è né `OSError` né
    `FotoFacileError`, quindi `except` non lo prende. Dove serve pulizia va sempre un `finally`.

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

---

## Current State

**Working**: avvio → 4 passi → copia → resoconto, in modalità demo e (su macOS) fino al
riconoscimento del telefono con il collegamento diretto; scelta automatica dei trasporti;
copia piatta; `doctor` con «Modi di collegamento»; `--selftest`; cartella Windows; grafo graphify.
**383 test verdi**, lint pulito (`pyflakes`).

**Broken**: nulla di noto nella suite.

**Non verificato** (non è la stessa cosa di «funziona»): collegamento diretto Windows e Linux
(mai eseguiti su hardware reale), collegamento diretto macOS con un telefono vero, qualsiasi
operazione con un telefono Android reale. Vedi «Not Yet Done».

**Uncommitted Changes**: tutta la revisione (trasporti, copia piatta, `B1–B24`, `C1–C19`,
asset/icone, `.github/workflows`), i nuovi `requirements.txt`, `docs/PIANO-REVISIONE.md`,
`tests/test_regressioni.py`, `tests/test_trasporto.py`, `tests/test_icona.py`, `fotofacile/__main__.py`,
`fotofacile/aiutanti/`, la documentazione aggiornata e `graphify-out/` rigenerato.

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
| `docs/PIANO-REVISIONE.md` | Elenco completo dei difetti `B1–B24` e `C1–C19` con gravità: è il documento da leggere per capire cosa è stato corretto e perché |
| `tests/test_regressioni.py` | Un test per ogni bug corretto; il commento dice cosa succedeva **prima** |
| `tests/test_trasporto.py` | Scelta automatica, contratto degli aiutanti, WPD/Linux simulati |
| `tests/conftest.py` | Finestra condivisa + `azzera()`: capire questo file evita crash e test fragili |
| `tests/pilota_app.py` | Collaudo end-to-end dell'app vera (`FF_DEST`, `FF_ESITO`) |
| `scripts/build_app.py` | Build multipiattaforma + icona + `--add-data` degli aiutanti + PyObjC su macOS |
| `.github/workflows/build-installers.yml` | Installer macOS (dmg) + Windows (Inno Setup) + Release |

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

---

## Resume Instructions

1. **Ambiente e test**
   ```bash
   cd ~/Desktop/Programmazione/FotoFacile
   .venv/bin/python -m pytest tests | tail -3        # atteso: 383 passed
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
   Test dell'aiutante e dell'installer: `.venv/bin/python -m pytest tests/test_aiutante_windows.py tests/test_installer_pacchetti.py -q`.

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
- Windows: nessun prerequisito sul PC di destinazione (il `Setup.exe` contiene già tutto).

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
- **Codifica degli script PowerShell**: i `.ps1` **devono avere** il BOM UTF-8 (PowerShell 5.1 legge
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

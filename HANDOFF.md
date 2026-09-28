# Handoff: FotoFacile — app desktop per copiare foto da Android

**Generato**: 2026-09-28 17:05
**Branch**: `main` (repo locale, nessun remoto configurato)
**Stato**: **Completo e verificato** (283 test verdi). Build macOS verificata, pacchetto Windows pronto sulla Scrivania. Restano solo due cose: collaudo con un telefono vero e creazione dell'eseguibile Windows (possibile **solo** su Windows).

## Goal

Permettere a **persone non tecniche** di copiare foto e video da un telefono Android al computer con una procedura guidata in italiano, senza gestore file e senza gergo tecnico. Multi-piattaforma (Windows/macOS/Linux), **zero dipendenze da installare** per chi usa il programma.

## Completed

- [x] App completa: 4 passi guidati (collegamento → scelta foto → destinazione → copia), in italiano semplice, con aiuto «Debug USB» per marca (Samsung, Xiaomi, Google, Huawei, Oppo…).
- [x] Motore **senza thread** (`core/ops.py`, `core/adb_passi.py`, `App.run_task`): copia `.part` + rinomina atomica, verifica dimensioni, dedup per dispositivo, cancella-dopo-copia con conferma, retry solo sugli errori transitori.
- [x] Installazione automatica di platform-tools e **modalità demo** senza telefono (`--demo`).
- [x] **Tema chiaro/scuro** secondo il sistema (`clam` + tavolozze, contrasto WCAG ≥ 7) — il difetto che faceva sembrare l'app vuota.
- [x] Diagnostica: `doctor` (sistema/telefono) e **`--selftest`** (apre e chiude la finestra, stampa `{"ok": true}`); registro `~/.fotofacile/avvio.log`; avviso nativo se la finestra non si può aprire.
- [x] **283 test verdi** (`pytest`), inclusi `tests/test_robustezza.py`, `tests/test_app_completa.py` (app vera in sottoprocesso), `tests/test_pacchetto_windows.py`.
- [x] **Verificato a schermo** (screenshot in modalità scura): indicatore dei 4 passi visibile, testo leggibile, nessun riquadro vuoto.
- [x] **Collaudo end-to-end in finestra reale**: 54/54 file copiati (60,9 MB) in 10 s, 0 errori, 0 `.part` residui, resoconto ok.
- [x] **Build macOS**: `dist/FotoFacile.app` (25,9 MB, icona generata da `scripts/make_icon.py`) + `.zip` (10,9 MB), verificata con `--selftest` dal pacchetto; quarantena rimossa; scorciatoia `Avvia FotoFacile.command`.
- [x] **Pacchetto Windows sulla Scrivania**: `~/Desktop/FotoFacile per Windows/` (35 file) — `Avvia FotoFacile.bat` (avvia subito; installa Python con winget se manca), `Crea l'eseguibile per Windows.bat` (crea e verifica `dist\FotoFacile\FotoFacile.exe`), `LEGGIMI - Windows.txt`.
- [x] **Graphify completo**: `graphify-out/` con `graph.json` (1021 nodi, 2500 archi), `GRAPH_REPORT.md`, `graph.html`, `graph.svg`, `graph.graphml`, `wiki/` (48 articoli), `manifest.json`, `cost.json`, `reflections/LESSONS.md`.
- [x] Revisione indipendente (`review`): 19 rilievi, corretti tutti i critici/alti (specifica §10-bis).

## Not Yet Done

- [ ] **Collaudo con un telefono Android vero** (autorizzazione Debug USB, copia reale, cancellazione dal telefono). Unica verifica mancante: in automazione non c'era un dispositivo.
- [ ] **Creazione dell'eseguibile Windows**: richiede un PC Windows (doppio clic su `Crea l'eseguibile per Windows.bat`). Da macOS è impossibile — vedi Failed Approaches.
- [ ] Limiti dichiarati non implementati: estrazione del componente non atomica; messaggio dedicato per «disco pieno» nel percorso reale; barra di avanzamento del singolo file distinta da quella generale; verifica hash del download.
- [ ] Opzionale: firma/notarizzazione del `.app` macOS (senza firma: clic destro → Apri la prima volta).

## Failed Approaches (Don't Repeat These)

1. **Thread per il lavoro in background.** Su **macOS + Tk 9** (Python 3.14 Homebrew) creare un thread mentre la finestra è aperta **blocca il processo**; con Tk 8.5 (Python di sistema) funziona. Provato anche un thread che non tocca Tk: blocca ugualmente. **Soluzione**: generatori a passi avanzati da `after()` (`core/ops.py`, `core/adb_passi.py`, `App.run_task`). Non reintrodurre `threading`.
2. **MTP / Android File Transfer**: su macOS inaffidabile (cartelle vuote, copie interrotte). ADB è l'unico metodo solido, e l'app se lo installa da sola.
3. **Più finestre Tk nello stesso processo di test**: crash `SIGTRAP` (exit 133). **Soluzione**: una sola finestra per sessione (`tests/conftest.py`) + `ricostruisci_pagine()` + `azzera()` fra i test.
4. **`time.sleep()` nei cicli di attesa dei test grafici**: lento e fragile. **Soluzione**: `tests/aiuto.py:attendi()` usa `update()` + `time.monotonic()`.
5. **Verificare la GUI da tool di automazione**: un processo in background **non ha accesso al window server** → `tkinter.Tk()` si blocca, e i processi che *provano a mostrare* la finestra morivano con `EXC_BREAKPOINT SIGTRAP` dentro `showRootWindow` (`libtcl9tk9.0.dylib`), visibile nei crash report. **Soluzione**: `launchctl asuser $(id -u) env PYTHONPATH="$PWD" .venv/bin/python script.py` + `screencapture -x` per guardare il risultato. Le schermate hanno rivelato due bug veri (tema illeggibile, indicatore coperto).
6. **Temi nativi `aqua`/`vista`**: ignorano i colori impostati (sfondo dei `TLabel` compreso) → in modalità scura testo scuro su fondo scuro, finestra apparentemente vuota. **Soluzione**: tema `clam` + tavolozza chiara/scura rilevata dal sistema + test di contrasto WCAG.
7. **Pagine figlie della finestra invece del contenitore**: `ConnectPage(self)` + `page.grid(row=0, …)` metteva le pagine nella stessa riga dell'intestazione, **coprendo l'indicatore dei passi** e lasciando un buco nel layout. **Soluzione**: `super().__init__(parent.container)` in tutte le pagine.
8. **`os.path.normcase` per confrontare le maiuscole**: su POSIX è un no-op → i confronti case-insensitive non funzionavano. **Soluzione**: `str.casefold()` in `core/planner.py`.
9. **`USERPROFILE` impostato nei test su macOS**: `core/osutil.py` lo preferisce a `HOME` (giusto per Windows) → i test sul resoconto scrivevano nella cartella di sessione. **Soluzione**: la fixture imposta `USERPROFILE` solo su Windows.
10. **Test che dipendono dalla cartella utente reale**: dopo che l'app ha installato platform-tools, `test_find_adb_*` trovava un `adb` vero e falliva. **Soluzione**: i test passano `HOME`/`USERPROFILE` temporanei.
11. **`explorer` su Windows esce con codice 1** anche quando la cartella si apre: giudicare dal codice dava un falso errore. Ora su Windows non si controlla; su macOS/Linux apertura fire-and-forget con `Popen`.
12. **Cross-compilare l'eseguibile Windows da macOS**: impossibile (PyInstaller non fa cross-compilazione; niente Wine sulla macchina). Un `.exe` così prodotto sarebbe **non verificabile**, quindi non è stato consegnato: al suo posto la cartella con i `.bat` (avvio immediato + creazione eseguibile con un doppio clic su Windows).
13. **Comandi distruttivi concatenati**: un `git checkout` messo in coda a un comando lungo ha ripristinato `fotofacile/ui/theme.py` appena riscritto, perdendo il lavoro. Mai mettere `git checkout`/`git clean` nello stesso comando di altro lavoro.
14. **Verifiche dipendenti dal tempo**: `assert app.attributes("-topmost")` falliva perché un `after` lo ripristinava. **Soluzione**: registrare le chiamate e verificare l'intenzione, non lo stato dopo il timer.

## Key Decisions

| Decisione | Perché |
|---|---|
| Trasporto **ADB**, non MTP | Unico metodo affidabile su macOS/Linux/Windows |
| **Niente thread**: generatori a passi con `after()` | Tk 9 su macOS si blocca con qualunque thread; UI reattiva e test deterministici |
| Solo **libreria standard** (Tkinter) | L'utente finale non deve installare nulla |
| Tema **`clam`** + tavolozze chiara/scura | Gli unici colori che i temi nativi non possono ignorare; leggibilità garantita |
| `.part` + `os.replace` + verifica dimensione | Mai file troncati o foto perse; annullamento senza residui |
| `FotoFacileError(message, hint)` ovunque | Messaggi umani + azione suggerita, mai stack trace |
| Errori non ritentabili non vengono ritentati | Non ricopiare 3 volte un file su disco pieno |
| Nomi file resi sicuri per Windows **sempre** | La cartella resta usabile su qualunque sistema |
| `--selftest` | Verifica una build/installazione in un secondo, senza toccare foto |
| Registro `~/.fotofacile/avvio.log` + avviso nativo | «Il programma non si apre» non deve restare senza spiegazione |
| Pacchetto Windows = cartella con `.bat` | Unico modo onesto di ottenere un `.exe` verificato (su Windows, con un doppio clic) |

## Current State

**Working**: tutto (avvio → 4 passi → copia → resoconto), demo mode, `doctor`, `--selftest`, app macOS, cartella Windows, grafo graphify. 283 test verdi.

**Broken**: nulla di noto. Limiti dichiarati nella specifica §10-bis.

**Uncommitted Changes**: `graphify-out/` (rigenerato dall'ultimo `graphify update`) — va committato.

## Files to Know

| File | Perché è importante |
|---|---|
| `fotofacile/core/ops.py` | Cuore cooperativo: `ProcessoEsterno`, `ScaricatoreAPassi`, `Annullato`, `esegui_fino_alla_fine` |
| `fotofacile/core/adb_passi.py` | Operazioni adb a passi (`AdbAPassi`, `AdbDemoAPassi`), copia `.part`, ripiego scansione |
| `fotofacile/core/transfer.py` | `transfer_steps()` (retry, verifica, cronologia, cancella-dopo) e `transfer()` diretto |
| `fotofacile/core/planner.py` | Nomi sicuri multipiattaforma, collisioni (maiuscole incluse), dedup, spazio |
| `fotofacile/core/osutil.py` | Differenze di sistema: `sistema_scuro`-helper, `flag_nascosta()` (niente finestre nere su Windows), apertura cartella |
| `fotofacile/ui/app.py` | `run_task` (passi + epoca anti-abbandono), `annulla_task`, `ricostruisci_pagine`, `_chiusura` con conferma, `_porta_in_primo_piano` |
| `fotofacile/ui/theme.py` | Tavolozze chiara/scura, `sistema_scuro()`, `contrasto()` WCAG, stile `clam` |
| `fotofacile/ui/page_*.py` | Le 4 schermate; **costruite dentro `app.container`** (regola di layout) |
| `tests/conftest.py` | Finestra condivisa + `azzera()`: capire questo file evita crash e test fragili |
| `tests/pilota_app.py` | Collaudo end-to-end dell'app vera (variabili `FF_DEST`, `FF_ESITO`) |
| `scripts/build_app.py` | Build multipiattaforma, icona, quarantena, scorciatoia, `--verify` |
| `scripts/crea_pacchetto_windows.py` | Crea la cartella per Windows (sorgente + `.bat` + LEGGIMI) |
| `~/Desktop/FotoFacile per Windows/` | Pacchetto pronto: avvio a doppio clic o creazione eseguibile |
| `graphify-out/wiki/index.md` | Punto d'ingresso del grafo della conoscenza |

## Code Context

```python
# core/ops.py — l'unica forma di "asincronia" ammessa
class ProcessoEsterno:
    def avvia(self) -> None
    def passo(self) -> bool                      # True se ancora in corso
    def aspetta(self) -> Generator[float, None, RisultatoComando]   # si guida con next()
    def esito(self) -> RisultatoComando           # solleva FotoFacileError se fallito
    def termina(self) -> None                     # chiude i flussi, cancella i file temporanei
def esegui_fino_alla_fine(generatore): ...        # per test e riga di comando

# core/adb_passi.py — interfaccia usata dalla GUI (AdbDemoAPassi è identico, senza telefono)
class AdbAPassi:
    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]
    def cerca_media(self, serial, comando, timeout=..., annulla=None, ripiega=True) -> Generator[float, None, list[MediaFile]]
    def copia(self, serial, remoto, destinazione, on_scritti=None, annulla=None, timeout=...) -> Generator[float, None, int]
    def cancella(self, serial, remoto) -> Generator[float, None, None]
    def riavvia(self) -> Generator[float, None, None]
    def pulisci(self) -> None

# core/transfer.py
def transfer_steps(plan, options, copiatore, serial, history=None, on_progress=None,
                   annulla=None, retries=2, orologio=time.monotonic) -> Generator[float, None, TransferResults]
def transfer(adb, serial, plan, options, ...) -> TransferResults      # involucro diretto

# ui/theme.py
PALETTE: dict[str, dict[str, str]]                 # "chiaro" | "scuro"
COLORI: dict[str, str]                             # aggiornata IN LOCO da apply_theme
def sistema_scuro(system=None, runner=None) -> bool
def contrasto(primo: str, secondo: str) -> float    # WCAG
def apply_theme(root, available_families=None, scuro=None) -> None

# ui/app.py
class App(tk.Tk):
    INTERVALLO_PASSI = 0.02
    def run_task(self, generatore, on_done=None, on_error=None, intervallo=None) -> None
    def annulla_task(self) -> None                  # incrementa l'epoca e chiude il generatore
    def ricostruisci_pagine(self) -> None
    def log(self, testo) -> None                    # mostra l'area «Dettagli» al primo messaggio
    @property
    def task_in_corso(self) -> bool

# core/osutil.py
def flag_nascosta(system=None) -> int               # CREATE_NO_WINDOW su Windows, 0 altrove
def open_in_file_manager(path, system=None, runner=None) -> None   # Popen / os.startfile

# scripts/crea_pacchetto_windows.py
def crea_pacchetto(destinazione: Path | None = None) -> Path       # default: ~/Desktop/FotoFacile per Windows
```

Stato condiviso fra le pagine: `app.device`, `app.media_files`, `app.options`, `app.results`,
`app.cancel_event`, `app.remote` (`AdbAPassi` | `AdbDemoAPassi` | `None`), `app.history()`.

## Resume Instructions

1. Ambiente e test:
   ```bash
   cd ~/Desktop/Programmazione/FotoFacile
   .venv/bin/python -m pytest tests -q          # atteso: 283 passed
   ```
   - Se fallisce: `.venv/bin/python -m pytest tests -q --tb=short` e guarda i primi 3 errori; i test grafici si saltano da soli se l'ambiente non apre finestre (non è un errore).

2. Collaudo dell'app vera (finestra + copia su disco):
   ```bash
   FF_DEST="/tmp/collaudo-foto" FF_ESITO="/tmp/esito.json" .venv/bin/python tests/pilota_app.py
   # senza sessione grafica (tool di automazione):
   launchctl asuser $(id -u) env PYTHONPATH="$PWD" "$PWD/.venv/bin/python" "$PWD/tests/pilota_app.py"
   cat /tmp/esito.json
   ```
   - Atteso: `"ok": true`, 54 file copiati, `/tmp/collaudo-foto` piena, nessun `.part`.
   - Se fallisce: `"motivo"` in `esito.json` dice la pagina e l'errore.

3. Guardare davvero la finestra (per controllare colori/layout):
   ```bash
   launchctl asuser $(id -u) env PYTHONPATH="$PWD" "$PWD/.venv/bin/python" -c \
     "from fotofacile.ui.app import App; a=App(demo_mode=True); a.after(4000, a.destroy); a.mainloop()" &
   sleep 3; screencapture -x /tmp/schermo.png    # poi guarda l'immagine
   ```

4. Cartella Windows: ricrearla e verificarla
   ```bash
   .venv/bin/python scripts/crea_pacchetto_windows.py
   ls "$HOME/Desktop/FotoFacile per Windows"
   ```
   - Atteso: 35 file, fra cui `Avvia FotoFacile.bat`, `Crea l'eseguibile per Windows.bat`, `LEGGIMI - Windows.txt`.
   - Se manca qualcosa: `.venv/bin/python -m pytest tests/test_pacchetto_windows.py -q`.

5. Build macOS: `python3 scripts/build_app.py --verify` → `dist/FotoFacile.app`; l'autocollaudo deve rispondere `{"ok": true}`.

6. Dopo ogni modifica al codice: `graphify update .` (obbligatorio). Per interrogare il grafo: `graphify query "<domanda>"` o `graphify-out/wiki/index.md`.

7. Modifiche future: **test prima** (`pytest`), mai `tkinter` dentro `core/`, mai thread, e ogni nuova pagina va costruita dentro `app.container`.

## Setup Required

- Python 3.9+ con Tkinter (qui: 3.14.7, Tk 9.0); `.venv` già pronto con `pytest` e `pyinstaller`.
- Graphify: `uv tool install graphifyy` (interprete annotato in `graphify-out/.graphify_python`).
- Per la grafica da automazione: `launchctl asuser $(id -u)` + `PYTHONPATH` esplicito + `screencapture`.
- Nessuna chiave API (l'estrazione semantica di graphify è stata fatta dall'agente).
- Windows: nessun prerequisito sul PC di destinazione se si usa l'eseguibile; per crearlo serve Python sul PC dove si lancia il `.bat` (il file lo installa da sé con winget).

## Edge Cases & Error Handling

- Nessun telefono / non autorizzato / `offline` / `no permissions` → messaggi dedicati (`core/devices.STATE_MESSAGE`).
- Cavo solo-ricarica o driver mancante → suggerimenti espliciti nell'aiuto e nello stato.
- Annullamento a metà file → `Annullato` → `.part` rimosso, risultati parziali validi.
- Abbandono del lavoro (indietro, nuova ricerca, chiusura) → `annulla_task()` chiude il generatore; `AdbAPassi.copia` termina il processo e rimuove il `.part`.
- Errore di disco/permessi → `errors.traduci_errore_file` → messaggio + suggerimento, nessun retry.
- Cronologia non scrivibile/corrotta → avviso in `TransferResults.warnings`, copia comunque riuscita.
- Destinazione non leggibile o relativa → errore umano nella pagina 3/4, pagina ancora usabile.
- Componente guasto/assente → il pulsante «Installa componente mancante» torna attivo.
- Finestra non apribile (Linux senza `python3-tk`, automazione) → messaggio chiaro + `avvio.log` + `doctor`; con `--selftest` si distingue «grafica rotta» da «avvio sbagliato».
- Modalità scura/chiara → rilevata a ogni avvio; se il rilevamento fallisce resta la tavolozza chiara (leggibile).

## Warnings

- **Non reintrodurre thread**: su macOS + Tk 9 bloccano l'app (Failed Approaches #1).
- **Tema `clam` obbligatorio**: `aqua`/`vista` ignorano i colori e in modalità scura rendono l'app illeggibile.
- **Le pagine vanno dentro `app.container`** (`super().__init__(parent.container)`), altrimenti coprono l'intestazione.
- Non mettere `git checkout`/`git clean` nello stesso comando di altro lavoro: ha già fatto perdere una riscrittura di `theme.py`.
- I test grafici **si saltano** se `tk_available()` (prova in sottoprocesso con timeout) fallisce: è l'ambiente, non il codice.
- I test devono sempre isolare `HOME`/`USERPROFILE`: sul Mac dell'utente esiste un `adb` vero installato dall'app.
- `graphify-out/` contiene file pesanti (graph.json ~1 MB, graph.svg 3,6 MB): rigenerali con `graphify update .`, non modificarli a mano.
- Il `.app` non è firmato: prima apertura con clic destro → «Apri». L'`.exe` Windows non può essere creato da macOS.
- `find_adb()` cerca anche `~/.fotofacile/platform-tools`: se un'installazione è interrotta a metà il file può esistere ma non funzionare — il messaggio di stato lo segnala e il pulsante di installazione si riattiva.
- Se aggiungi una pagina, aggiorna `azzera()` in `tests/conftest.py` (altrimenti lo stato sporca i test successivi).

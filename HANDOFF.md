# Handoff: FotoFacile — app desktop per copiare foto da Android

**Generato**: 2026-09-28 16:20
**Branch**: `main` (repo locale, nessun remoto configurato)
**Stato**: **Completo e verificato** (259 test verdi, build macOS verificata). Resta solo il collaudo con un telefono vero.

## Goal

Permettere a **persone non tecniche** di copiare foto e video da un telefono Android al computer
con una procedura guidata in italiano, senza gestore file e senza gergo tecnico. Multi-piattaforma
(Windows/macOS/Linux), zero dipendenze da installare per chi usa il programma.

## Completed

- [x] App completa: 4 passi guidati (collegamento → scelta foto → destinazione → copia), tema Tkinter, messaggi in italiano semplice, aiuto «Debug USB» per marca.
- [x] Motore senza thread (`core/ops.py`, `core/adb_passi.py`, `App.run_task`), copia sicura `.part` + rinomina atomica, verifica dimensioni, dedup per dispositivo, cancella-dopo-copia con conferma.
- [x] Installazione automatica di platform-tools (Windows/macOS/Linux) e modalità demo senza telefono.
- [x] `doctor` (diagnosi) e `--selftest` (autocollaudo) da riga di comando.
- [x] **259 test automatici verdi** (`python .venv/bin/python -m pytest tests -q`), inclusi `tests/test_robustezza.py` (errori di disco, abbandono a metà copia, cronologia non scrivibile) e `tests/test_app_completa.py` (app vera in sottoprocesso).
- [x] **Verifica criterio 1 fatta**: la finestra si apre (via `launchctl asuser`, vedi sotto).
- [x] **Collaudo completo in finestra reale**: 54/54 file copiati (60,9 MB) in 10 s, 0 errori, 0 file `.part` residui, resoconto generato.
- [x] **Build** `dist/FotoFacile.app` (27 MB) + `dist/FotoFacile-0.1.0-darwin-arm64.zip` (11 MB), con icona generata da `scripts/make_icon.py`; verificata con `--selftest` dal pacchetto → `{"ok": true, ...}`.
- [x] **Graphify completo**: `graphify-out/` con `graph.json` (900+ nodi), `GRAPH_REPORT.md`, `graph.html`, `graph.svg`, `graph.graphml`, `wiki/` (47 articoli), `manifest.json`, `cost.json`.
- [x] Revisione indipendente (`review`) con 19 rilievi: corretti i critici/alti (vedi «10-bis» nella specifica).

## Not Yet Done

- [ ] **Collaudo con un telefono Android vero** (collegamento, autorizzazione Debug USB, copia reale, cancellazione dal telefono). È l'unica cosa non verificata: in automazione non c'era un dispositivo.
- [ ] Limiti dichiarati non implementati: estrazione del componente non atomica; messaggio dedicato per «disco pieno» nel percorso reale; barra di avanzamento del singolo file distinta da quella generale; verifica hash del download.
- [ ] Opzionale: pacchetto per Windows/Linux (lo script è pronto e multipiattaforma, va eseguito su quei sistemi).
- [ ] Opzionale: firma/notarizzazione del `.app` macOS (senza firma serve clic destro → Apri la prima volta).

## Failed Approaches (Don't Repeat These)

1. **Thread per il lavoro in background.** Con **macOS + Tk 9** (Python 3.14 di Homebrew) creare un thread mentre la finestra è aperta **blocca l'intero processo**. Provato con script minimi: bloccano sia un thread che tocca Tk sia uno che non lo tocca affatto; con Tk 8.5 (Python di sistema) funziona. **Soluzione adottata**: motore cooperativo a generatori avanzati da `after()` (`core/ops.py`, `core/adb_passi.py`, `App.run_task`). Non reintrodurre `threading`.
2. **MTP / Android File Transfer** per il trasferimento: su macOS non affidabile, cartelle vuote o copie interrotte. **ADB** è l'unico metodo solido: l'app lo installa da sola.
3. **Più finestre Tk nello stesso processo di test** (una `App` per test): crash `SIGTRAP` (exit 133). **Soluzione**: una sola finestra condivisa per sessione (`tests/conftest.py`), più `app.ricostruisci_pagine()` e `azzera()` fra i test.
4. **`time.sleep()` dentro i cicli di attesa dei test grafici**: nella sessione grafica dell'utente è ok, ma rende i test lenti e fragili → `tests/aiuto.py:attendi()` usa `update()` + `time.monotonic()`.
5. **Verificare la GUI lanciando processi in background dal tool**: su macOS un processo in background **non accede al window server** e `tkinter.Tk()` si blocca. Nemmeno `open`/`osascript` funzionano in modo affidabile da qui. **Cosa funziona**: `launchctl asuser $(id -u) <python> <script>` (con `PYTHONPATH` esplicito) — con questo la finestra si apre davvero.
6. **`os.path.normcase` per confrontare le maiuscole**: su macOS/POSIX è un no-op → i confronti case-insensitive non funzionavano. **Soluzione**: `str.casefold()` esplicito in `core/planner.py`.
7. **`USERPROFILE` impostato nei test su macOS**: `core/osutil.py` lo preferisce a `HOME` (giusto per Windows) → i test sul resoconto finivano nella cartella di sessione. **Soluzione**: la fixture di sessione imposta `USERPROFILE` solo su Windows.
8. **`explorer` su Windows esce con codice 1** anche quando la cartella si apre: giudicare dal codice di uscita dava un falso errore. Ora su Windows non si controlla il codice; su macOS/Linux l'apertura è fire-and-forget con `Popen`.

## Key Decisions

| Decisione | Perché |
|---|---|
| Trasporto **ADB**, non MTP | Unico metodo affidabile su macOS/Linux/Windows; MTP instabile |
| **Niente thread**: generatori a passi con `after()` | Tk 9 su macOS si blocca con qualunque thread; interfaccia reattiva e test deterministici |
| Solo **libreria standard** (Tkinter) | L'utente finale non deve installare nulla |
| `.part` + `os.replace` + verifica dimensione | Mai file troncati o foto perse; annullamento senza residui |
| `FotoFacileError(message, hint)` ovunque | Messaggi umani + azione suggerita; niente stack trace a schermo |
| Errori **non ritentabili** non vengono ritentati | Non ricopiare 3 volte un file su disco pieno |
| Nomi file resi sicuri per Windows sempre | La cartella di destinazione resta usabile su qualunque sistema |
| Una sola finestra nei test + `ricostruisci_pagine()` | Evita i crash di Tk e l'isolamento fra test |
| `tests/pilota_app.py` come collaudo end-to-end | Verifica la vera app (finestra) senza intervento umano |

## Current State

**Working**: tutto il percorso (avvio → 4 passi → copia → resoconto), modalità demo, `doctor`, `--selftest`, build `.app`, 259 test.

**Broken**: nulla di noto. Limiti dichiarati nella specifica §10-bis.

**Uncommitted Changes**: `graphify-out/` (grafo, wiki, export) e `HANDOFF.md` — da committare.

## Files to Know

| File | Perché è importante |
|---|---|
| `fotofacile/core/ops.py` | Cuore cooperativo: `ProcessoEsterno`, `ScaricatoreAPassi`, `Annullato`, `esegui_fino_alla_fine` |
| `fotofacile/core/adb_passi.py` | Operazioni adb a passi (`AdbAPassi`, `AdbDemoAPassi`), copia `.part`, ripiego scansione |
| `fotofacile/core/transfer.py` | `transfer_steps()` (orchestrazione: retry, verifica, cronologia, cancella-dopo) e `transfer()` diretto |
| `fotofacile/core/planner.py` | Nomi sicuri multipiattaforma, collisioni (anche maiuscole), dedup, spazio |
| `fotofacile/ui/app.py` | `run_task` (passi + epoca anti-abbandono), `annulla_task`, `ricostruisci_pagine`, `_chiusura` con conferma |
| `fotofacile/ui/page_*.py` | Le 4 schermate; `page_connect.connect_now()` è il rilevamento del telefono |
| `tests/conftest.py` | Finestra condivisa + `azzera()`: capire questo file evita crash e test fragili |
| `tests/pilota_app.py` | Collaudo end-to-end dell'app vera (usa variabili `FF_DEST`, `FF_ESITO`) |
| `scripts/build_app.py`, `scripts/make_icon.py` | Build multipiattaforma e icona senza dipendenze |
| `docs/superpowers/specs/2026-09-28-fotofacile-design.md` | Specifica + §10-bis con le correzioni della revisione |
| `graphify-out/wiki/index.md` | Punto d'ingresso del grafo della conoscenza |

## Code Context

```python
# core/ops.py — l'unica forma di "asincronia" ammessa
class ProcessoEsterno:
    def avvia(self) -> None
    def passo(self) -> bool                       # True se ancora in corso
    def scaduto(self) -> bool
    def aspetta(self) -> Generator[float, None, RisultatoComando]   # si guida con next()
    def esito(self) -> RisultatoComando           # solleva FotoFacileError se fallito
    def termina(self) -> None                     # chiude i flussi e cancella i file temp

def esegui_fino_alla_fine(generatore):            # per test e riga di comando
    ...

# core/adb_passi.py — interfaccia usata dalla GUI
class AdbAPassi:
    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]
    def cerca_media(self, serial, comando, timeout=..., annulla=None, ripiega=True) -> Generator[float, None, list[MediaFile]]
    def copia(self, serial, remoto, destinazione, on_scritti=None, annulla=None, timeout=...) -> Generator[float, None, int]
    def cancella(self, serial, remoto) -> Generator[float, None, None]
    def riavvia(self) -> Generator[float, None, None]
    def pulisci(self) -> None
# AdbDemoAPassi: stessa interfaccia, telefono finto (modalità demo e test GUI)

# core/transfer.py
def transfer_steps(plan, options, copiatore, serial, history=None, on_progress=None,
                   annulla=None, retries=2, orologio=time.monotonic) -> Generator[float, None, TransferResults]
def transfer(adb, serial, plan, options, ...) -> TransferResults      # involucro diretto
# `copiatore` deve avere copia(...) e cancella(...) come generatori

# ui/app.py
class App(tk.Tk):
    INTERVALLO_PASSI = 0.02        # secondi fra due passi (0.0 nei test)
    def run_task(self, generatore, on_done=None, on_error=None, intervallo=None) -> None
    def annulla_task(self) -> None     # incrementa l'epoca e chiude il generatore
    def ricostruisci_pagine(self) -> None
    @property
    def task_in_corso(self) -> bool
```

Stato condiviso fra le pagine: `app.device`, `app.media_files`, `app.options`, `app.results`,
`app.cancel_event`, `app.remote` (`AdbAPassi` | `AdbDemoAPassi` | `None`), `app.history()`.

## Resume Instructions

1. Ambiente:
   ```bash
   cd ~/Desktop/Programmazione/FotoFacile
   .venv/bin/python -m pytest tests -q          # atteso: 259 passed
   ```
2. Collaudo dell'app vera (finestra + copia su disco), nell'ambiente di automazione serve `launchctl`:
   ```bash
   FF_DEST="/tmp/collaudo-foto" FF_ESITO="/tmp/esito.json" \
     .venv/bin/python tests/pilota_app.py        # in Terminale normale
   # da un tool di automazione (senza window server):
   launchctl asuser $(id -u) "$PWD/.venv/bin/python" "$PWD/tests/pilota_app.py"
   ```
   Atteso: `"ok": true`, 54 file copiati, `/tmp/collaudo-foto` piena, nessun `.part`.
   Se fallisce: guarda `FF_ESITO` (`"motivo"` dice la pagina e l'errore) e `app.log_pane`.
3. Collaudo con telefono vero: `python3 fotofacile.py` → segui i 4 passi → verifica che i file
   siano in `~/Pictures/FotoFacile/<telefono>/<data>` e che un secondo giro non ricopi nulla.
4. Modifiche al codice: **test prima** (`pytest`), poi implementazione. Se tocchi `core/`, non
   importare `tkinter`; se tocchi la GUI, non introdurre thread.
5. Dopo modifiche al codice: `graphify update .` (obbligatorio per tenere il grafo attuale); per
   interrogarlo: `graphify query "<domanda>"` oppure leggi `graphify-out/wiki/index.md`.
6. Nuova build: `python3 scripts/build_app.py --verify` → `dist/FotoFacile.app`.

## Setup Required

- Python 3.9+ con Tkinter (qui: 3.14.7, Tk 9.0); `.venv` già creato con `pytest` e `pyinstaller`.
- Per la build: `pip install pyinstaller` (già presente nel venv).
- Per graphify: `uv tool install graphifyy` (interprete annotato in `graphify-out/.graphify_python`).
- Per il collaudo grafico da tool di automazione: `launchctl asuser $(id -u) …` e `PYTHONPATH` esplicito.
- Nessuna chiave API richiesta (l'estrazione semantica di graphify è stata fatta dall'agente).

## Edge Cases & Error Handling

- Nessun telefono / non autorizzato / `offline` / `no permissions` → messaggi dedicati in `core/devices.STATE_MESSAGE`.
- Cavo solo-ricarica o driver mancante → suggerimenti espliciti nell'aiuto e nel messaggio di stato.
- Annullamento a metà file → `Annullato` → `.part` rimosso, nessun file troncato, risultati parziali validi.
- Abbandono del lavoro (indietro, nuova ricerca, chiusura) → `App.annulla_task()` chiude il generatore: `AdbAPassi.copia` termina il processo e cancella il `.part`.
- Errore di disco/permessi → `errors.traduci_errore_file` → messaggio + suggerimento; non ritentato.
- Cronologia non scrivibile/corrotta → avviso in `TransferResults.warnings`, copia comunque riuscita.
- Destinazione non leggibile o relativa → la pagina 3/4 mostra un errore umano e resta usabile.
- Componente guasto/assente → il pulsante «Installa componente mancante» torna attivo.
- Nessuna finestra grafica (Linux senza `python3-tk`) → `start_gui` spiega il problema e suggerisce `doctor`.

## Warnings

- **Non reintrodurre thread**: su macOS + Tk 9 bloccano l'app (vedi Failed Approaches #1).
- I test grafici **si saltano da soli** se `tk_available()` (prova in sottoprocesso con timeout) fallisce: non è un errore, è l'ambiente.
- `graphify-out/` contiene file pesanti (graph.json ~1 MB, graph.svg 3,6 MB): non modificarli a mano, rigenerali con `graphify update .`.
- Il `.app` non è firmato: la prima apertura richiede clic destro → «Apri» (su macOS recenti).
- `find_adb()` cerca anche `~/.fotofacile/platform-tools`: se un'installazione è interrotta a metà, quel file può esistere ma non funzionare — il messaggio di stato lo segnala e il pulsante di installazione si riattiva.
- `tests/conftest.py` azzera la finestra condivisa: se aggiungi una pagina, aggiorna `azzera()` (altrimenti lo stato sporca i test successivi).

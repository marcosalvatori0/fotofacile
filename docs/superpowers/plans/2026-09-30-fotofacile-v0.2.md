# FotoFacile v0.2 — Piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Portare FotoFacile alla v0.2: (A) revisione completa con correzione dei difetti, (B) risoluzione del problema «le immagini escono in WebP», (C) interfaccia molto più semplice e leggibile per persone anziane, (D) un vero programma di installazione Windows (`FotoFacile-Setup-0.2.0.exe`, niente `.bat`/`.ps1` per l'utente).

**Architecture:** Quattro parti indipendenti, da fare in quest'ordine: **A → B → C → D → E (chiusura)**. A e B toccano solo `fotofacile/core/` e i test; C tocca solo `fotofacile/ui/` (più `core/impostazioni.py` e `core/nomi_cartelle.py`); D tocca `installer/`, `scripts/`, `.github/` e pochissimo `cli.py`. La parte D può andare in un worktree parallelo (`superpowers:using-git-worktrees`) dopo il task D0, perché non dipende da A–C tranne che per la versione e per Pillow nel pacchetto.

**Tech Stack:** Python ≥ 3.9 (qui 3.14.7, Tk 9), Tkinter/ttk tema `clam`, pytest (`filterwarnings = error`), Pillow (opzionale, solo per la conversione WebP), PyInstaller, Inno Setup 6 (compilato su runner GitHub `windows-2022`), GitHub Actions.

## Global Constraints

Valgono per **ogni** task (copiate da `HANDOFF.md`, che le ha stabilite con test e incidenti veri):

- Lingua di tutta l'interfaccia, dei messaggi e dei commenti: **italiano corretto con gli accenti** («è», «già», «perché»). Nomi di codice in italiano come il resto del progetto.
- **Niente thread** (`threading` solo per `threading.Event`): su macOS + Tk 9 bloccano l'app. Lavoro lungo = generatori a passi avanzati da `App.run_task` (`after()`).
- **Mai PyObjC nel processo principale** (solo in `fotofacile/aiutanti/ptp_mac.py`). Mai `tkinter` dentro `fotofacile/core/`.
- Tema **`clam`** obbligatorio; tavolozza con contrasto WCAG ≥ 7 (`theme.contrasto`). I widget Tk classici (`tk.Text`, `tk.Canvas`, `Toplevel`) si colorano con `tema_testo`/`tema_tela`/`tema_finestra`.
- Le pagine vivono in `app.container` (`super().__init__(parent.container)`). Se si aggiunge o si rinomina un attributo di pagina usato da `tests/conftest.py:azzera()`, **aggiornare `azzera()` nello stesso task**.
- I `.ps1` **hanno** il BOM UTF-8, i `.bat` **no**; i file di testo letti da Inno Setup con accenti hanno il BOM UTF-8.
- `.venv/bin/python -m pytest tests` deve restare **tutto verde** a fine di ogni task (baseline verificata il 2026-09-30: **385 passed**); `.venv/bin/python -m pyflakes fotofacile scripts` deve restare **vuoto** (baseline: vuoto).
- I test isolano `HOME`/`USERPROFILE` (fixture `casa_temporanea`): sul Mac di Marco esiste un `adb` vero. I test grafici usano la finestra condivisa (`app`, `root`) e si saltano se `tk_available()` è falso.
- Dopo ogni modifica al codice: `graphify update .`. Prima di ogni commit: pytest + pyflakes.
- **Mai** mettere `git checkout` / `git clean` nello stesso comando di altro lavoro.
- Azioni verso l'esterno (push, tag, Release, pubblicazione) **solo dopo conferma esplicita di Marco**: nei task sono marcate «⚠ CHIEDI».
- Commit: messaggi in italiano, prefisso `fix:`/`feat:`/`test:`/`docs:`/`chore:`, e la riga finale `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

**Nota di metodo (comando `grep`):** su questa macchina `grep` nel terminale di Claude Code è un alias rotto («claude native binary not installed»): usare `/usr/bin/grep` oppure lo strumento di ricerca.

---

## Cosa abbiamo trovato leggendo il codice (base del piano)

Difetti **reali e verificati leggendo il sorgente** (numerati `D1…` per continuare `B1–B24`/`C1–C19` di `docs/PIANO-REVISIONE.md`):

| # | Dove | Difetto | Gravità |
|---|---|---|---|
| D1 | `core/transfer.py` | Le foto copiate ricevono la data di **oggi**: la data originale (`MediaFile.mtime`) non viene mai applicata (`os.utime` non compare nel progetto). In Esplora file/Foto tutte le immagini risultano di oggi e l'ordinamento per data è inutile. | **Alta** |
| D2 | `core/transfer.py` | `history.save()` sta solo in coda a `transfer_steps`: se il generatore viene chiuso (finestra chiusa durante la copia → `GeneratorExit`) la cronologia dei file già copiati **non si salva**. | Media |
| D3 | `core/transfer.py` | Se la cancellazione dal telefono fallisce → `except FotoFacileError: pass`: l'utente crede che le foto siano state tolte dal telefono. | Media |
| D4 | `core/transfer.py` | Se un file fallisce, `bytes_total` resta invariato: la barra non arriva mai al 100 % e il tempo residuo è sbagliato. | Bassa |
| D5 | `ui/page_select.py` | `_scansione_fallita(_errore)` **butta via il motivo**: l'utente vede solo «Ricerca non riuscita.» senza spiegazione né suggerimento. | Media |
| D6 | `core/history.py` | `save()` sovrascrive il file: due copie del programma aperte insieme (o due account) si cancellano a vicenda le voci. | Bassa |
| D7 | `cli.py` / Windows | Il `.exe` PyInstaller è `--windowed`: `sys.stdout` è `None`, quindi `FotoFacile.exe doctor` **non mostra niente** e la verifica della pipeline («doctor») è vuota. | Media |
| D8 | tutta la grafica su Windows | Manca la dichiarazione DPI: su schermi ≥ 125 % Windows **ingrandisce a bitmap** la finestra → testo sfocato (grave per chi vede poco). | Media |
| D9 | `ui/page_connect.py` | Non si dice mai di scegliere **«Trasferimento file»** sul telefono: il predefinito di Android è «Ricarica via USB» e il collegamento diretto (MTP/PTP) **non vede niente** finché non si cambia. È la causa più probabile di «telefono non riconosciuto». | **Alta** |
| D10 | `ui/*` | Testi da 11–12 pt, date da scrivere a mano (`AAAA-MM-GG`), percorsi tecnici come nomi di cartella, area «Dettagli» tecnica sempre visibile: pensati per chi conosce il computer. | UX (parte C) |

Ipotesi sul **WebP** (da confermare con il task B2 — non date per certe):
- **H1** i file sono davvero `.webp` sul telefono: sticker di WhatsApp/Telegram (`…/WhatsApp Stickers/`), immagini salvate da Chrome/Instagram/Facebook in `Download`, `Android/media`. Il programma cerca in `Android/media` e `Download` (`scanner.DEFAULT_ROOTS`) e i collegamenti diretti percorrono **tutta** la memoria → li porta tutti.
- **H2** il telefono (o l'app di scatto) salva davvero in WebP.
- **H3** qualcuno (telefono/driver) rinomina o converte durante il trasferimento. Il codice copia i byte **senza toccarli** (verificato in `transfer.py`, `ptp_mac.leggi_file`): se i file fuori sono WebP, lo erano già dentro.

In ogni caso Marco vuole immagini apribili ovunque: si aggiunge la **conversione WebP → JPG/PNG** (opzione, attiva di default) e il **filtro sticker/miniature**.

---

# PARTE 0 — Punto di partenza

### Task 0: Salvare il lavoro non committato e creare il ramo

**Files:** nessun file di codice.

Il `HANDOFF.md` dice che **tutta** la revisione precedente (trasporti, copia piatta, B1–B24, C1–C19, icone, workflow) è ancora non committata. Perderla sarebbe il danno peggiore possibile: si mette al sicuro prima di toccare altro.

- [ ] **Step 1: Verificare la baseline**

Run: `cd ~/Desktop/Programmazione/FotoFacile && .venv/bin/python -m pytest tests 2>&1 | tail -2 && .venv/bin/python -m pyflakes fotofacile scripts`
Expected: `385 passed` e nessun output da pyflakes.

- [ ] **Step 2: ⚠ CHIEDI a Marco** se committare tutto l'esistente su `main` in commit logici (o su un ramo). Proposta: ramo `revisione-v0.2` creato **dopo** un commit del lavoro pendente su `main`.

- [ ] **Step 3: Commit del lavoro pendente (dopo il «sì»), in gruppi**

```bash
git add fotofacile tests scripts installer .github requirements*.txt fotofacile.py
git commit -m "feat: collegamento diretto (PTP/WPD/MTP), copia piatta, correzioni B1-B24 e C1-C19

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
git add docs README.md HANDOFF.md "LEGGIMI - Installazione.txt" assets
git commit -m "docs: piano di revisione, handoff, README e nuove icone

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
git add graphify-out
git commit -m "chore: grafo rigenerato

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
git status --short | head
```
Expected: `git status` vuoto (o solo file ignorati).

- [ ] **Step 4: Creare il ramo di lavoro**

Run: `git switch -c revisione-v0.2`
Expected: `Switched to a new branch 'revisione-v0.2'`.

---

# PARTE A — Revisione completa e correzione dei difetti

Regola per ogni difetto: **test che fallisce → correzione minima → test verde → commit**. I test nuovi vanno in `tests/test_regressioni.py` (che ha già lo stile «commento che dice cosa succedeva prima»), salvo dove indicato.

### Task A1: D1 — Conservare la data originale delle foto

**Files:**
- Modify: `fotofacile/core/transfer.py` (funzione nuova `_applica_data`, chiamata in `transfer_steps`)
- Test: `tests/test_regressioni.py` (in coda)

**Interfaces:**
- Produces: `_applica_data(percorso: Path, mtime: int) -> None` (interna a `core/transfer.py`).

- [ ] **Step 1: Scrivere il test che fallisce** (in coda a `tests/test_regressioni.py`)

```python
# ── D1 ─────────────────────────────────────────────────────────────────────
# Prima: le foto copiate avevano la data di «adesso»; la data di scatto andava persa e
# in Esplora file / Foto tutto risultava di oggi.
class _TelefonoFinto:
    """Il minimo che serve a `transfer`: due metodi."""

    def __init__(self, contenuti: dict[str, bytes]) -> None:
        self.contenuti = contenuti
        self.cancellati: list[str] = []

    def stream_file(self, serial, remote_path, chunk_size=65536):
        yield self.contenuti[remote_path]

    def delete_file(self, serial, remote_path):
        self.cancellati.append(remote_path)


def _piano_singolo(tmp_path, percorso="/sdcard/DCIM/Camera/a.jpg", dati=b"x" * 10, mtime=1_500_000_000):
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile

    media = MediaFile(remote_path=percorso, size=len(dati), mtime=mtime, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out")
    return build_plan([media], opzioni), opzioni, _TelefonoFinto({percorso: dati})


def test_d1_la_copia_conserva_la_data_di_scatto(tmp_path):
    from fotofacile.core.transfer import transfer

    piano, opzioni, telefono = _piano_singolo(tmp_path)
    esiti = transfer(telefono, "S1", piano, opzioni)
    assert len(esiti.copied) == 1
    assert int(esiti.copied[0].stat().st_mtime) == 1_500_000_000
```

- [ ] **Step 2: Vederlo fallire**

Run: `.venv/bin/python -m pytest tests/test_regressioni.py::test_d1_la_copia_conserva_la_data_di_scatto -v`
Expected: FAIL (`assert <data di oggi> == 1500000000`).

- [ ] **Step 3: Implementare**

In `fotofacile/core/transfer.py`, dopo `_chiudi`:

```python
def _applica_data(percorso: Path, mtime: int) -> None:
    """Rimette sul file copiato la data originale della foto (se il telefono la conosce).

    Serve a chi ordina per data in Esplora file, Foto o Finder. Un errore qui non deve mai
    far fallire una copia già riuscita.
    """
    if not mtime or mtime < 0:
        return
    try:
        os.utime(percorso, (mtime, mtime))
    except OSError:  # pragma: no cover - file di rete o permessi particolari
        pass
```

In `transfer_steps`, subito dopo `esiti.copied.append(pianificato.dest_path)` — **prima** di `history.record` — aggiungere:

```python
        _applica_data(pianificato.dest_path, pianificato.media.mtime)
```

- [ ] **Step 4: Vederlo passare**

Run: `.venv/bin/python -m pytest tests/test_regressioni.py::test_d1_la_copia_conserva_la_data_di_scatto -v && .venv/bin/python -m pytest tests -x 2>&1 | tail -2`
Expected: PASS, poi tutta la suite verde.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/transfer.py tests/test_regressioni.py
git commit -m "fix(D1): le foto copiate conservano la data di scatto

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A2: D2 + D3 + D4 — Cronologia sempre salvata, cancellazione fallita segnalata, barra coerente

**Files:**
- Modify: `fotofacile/core/transfer.py` (`transfer_steps` diventa un involucro; il corpo attuale diventa `_passi_di_copia`)
- Test: `tests/test_regressioni.py`

**Interfaces:**
- Consumes: `_TelefonoFinto`, `_piano_singolo` (Task A1).
- Produces: `transfer_steps(...)` **con la stessa firma di prima**; `_passi_di_copia(esiti, plan, options, copiatore, serial, history, on_progress, annulla, retries, orologio)`.

- [ ] **Step 1: Scrivere i tre test che falliscono**

```python
# ── D2 ─────────────────────────────────────────────────────────────────────
# Prima: se il lavoro veniva abbandonato (finestra chiusa) la cronologia non si salvava.
def test_d2_la_cronologia_si_salva_anche_se_il_lavoro_viene_chiuso(tmp_path):
    from fotofacile.core.history import History
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import CopiatoreInterno, transfer_steps

    file = [
        MediaFile(f"/sdcard/DCIM/Camera/{i}.jpg", size=5, mtime=1000 + i, kind="photo") for i in range(3)
    ]
    telefono = _TelefonoFinto({f.remote_path: b"12345" for f in file})
    opzioni = TransferOptions(destination=tmp_path / "out")
    piano = build_plan(file, opzioni)
    cronologia = History(tmp_path / "h.json")
    cronologia.load()
    generatore = transfer_steps(piano, opzioni, CopiatoreInterno(telefono), "S1", history=cronologia)
    next(generatore)  # il primo file viene copiato…
    generatore.close()  # …poi la finestra si chiude
    riletta = History(tmp_path / "h.json")
    riletta.load()
    assert riletta.count("S1") >= 1


# ── D3 ─────────────────────────────────────────────────────────────────────
# Prima: se la cancellazione dal telefono falliva non lo sapeva nessuno.
def test_d3_cancellazione_fallita_diventa_un_avviso(tmp_path):
    from fotofacile.core.errors import FotoFacileError
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import transfer

    class Rifiuta(_TelefonoFinto):
        def delete_file(self, serial, remote_path):
            raise FotoFacileError("Il telefono non lo permette.", "")

    media = MediaFile("/sdcard/DCIM/Camera/a.jpg", size=3, mtime=1000, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out", delete_after=True)
    esiti = transfer(Rifiuta({media.remote_path: b"abc"}), "S1", build_plan([media], opzioni), opzioni)
    assert esiti.deleted_from_phone == 0
    assert any("a.jpg" in avviso and "telefono" in avviso for avviso in esiti.warnings)


# ── D4 ─────────────────────────────────────────────────────────────────────
# Prima: con un file fallito il totale restava alto e la barra non arrivava mai al 100 %.
def test_d4_il_totale_non_conta_i_file_falliti(tmp_path):
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import Progress, transfer

    buono = MediaFile("/sdcard/DCIM/Camera/ok.jpg", size=4, mtime=1, kind="photo")
    rotto = MediaFile("/sdcard/DCIM/Camera/rotto.jpg", size=99, mtime=1, kind="photo")
    # `rotto` dichiara 99 byte ma il telefono ne consegna 3: la verifica lo scarta
    telefono = _TelefonoFinto({buono.remote_path: b"abcd", rotto.remote_path: b"abc"})
    opzioni = TransferOptions(destination=tmp_path / "out")
    viste: list[Progress] = []
    esiti = transfer(
        telefono, "S1", build_plan([buono, rotto], opzioni), opzioni,
        on_progress=lambda p: viste.append(Progress(**vars(p))), retries=0,
    )
    assert len(esiti.failed) == 1
    assert viste[-1].bytes_done == viste[-1].bytes_total == 4
```

- [ ] **Step 2: Vederli fallire**

Run: `.venv/bin/python -m pytest tests/test_regressioni.py -k "d2 or d3 or d4" -v`
Expected: 3 FAIL.

- [ ] **Step 3: Implementare**

In `fotofacile/core/transfer.py`:

(a) Cambiare la testata di `transfer_steps` in `_passi_di_copia`, aggiungendo `esiti` come primo parametro e togliendo la riga `esiti = TransferResults(...)`:

```python
def _passi_di_copia(
    esiti: TransferResults,
    plan: TransferPlan,
    options: TransferOptions,
    copiatore,
    serial: str,
    history: History | None,
    on_progress: Callable[[Progress], None] | None,
    annulla,
    retries: int,
    orologio: Callable[[], float],
) -> Generator[float, None, TransferResults]:
    """Il corpo della copia; il salvataggio della cronologia sta nell'involucro."""
    avanzamento = Progress(total_files=plan.file_count, bytes_total=plan.total_bytes)
```
(il resto del corpo invariato).

(b) Nel corpo, **togliere** l'intero blocco finale `if history is not None: try: history.save() ... esiti.warnings.append(...)` (le ultime righe prima di `return esiti`), lasciando solo:

```python
    esiti.bytes_copied = avanzamento.bytes_done
    esiti.elapsed = max(orologio() - inizio, 0.0)
    _pubblica(on_progress, avanzamento, orologio, ultimo, forza=True)
    return esiti
```

(c) D4: nel ramo `if not riuscito:` sostituire con

```python
        if not riuscito:
            # Il file non arriverà mai: lo si toglie dal totale, così la barra e il tempo
            # residuo restano coerenti fino alla fine.
            avanzamento.bytes_total = max(avanzamento.bytes_total - pianificato.media.size, 0)
            esiti.failed.append((pianificato.media, messaggio))
            continue
```

(d) D3: sostituire l'`except FotoFacileError: pass` della cancellazione con

```python
            except FotoFacileError as errore:
                esiti.warnings.append(
                    f"Non sono riuscito a togliere {pianificato.media.name} dal telefono: "
                    f"{errore.message}"
                )
```

(e) Aggiungere l'involucro **con la firma originale** e il salvataggio sicuro:

```python
def _salva_cronologia(history: History | None, esiti: TransferResults) -> None:
    if history is None:
        return
    try:
        history.save()
    except OSError:
        # Le foto sono già al sicuro: non riuscire a ricordare cosa è stato copiato
        # non deve rovinare il risultato (al massimo la prossima volta si ricontrolla).
        esiti.warnings.append(
            "Non sono riuscito a salvare l'elenco dei file copiati: "
            "alla prossima copia il programma ricontrollerà tutto."
        )


def transfer_steps(
    plan: TransferPlan,
    options: TransferOptions,
    copiatore,
    serial: str,
    history: History | None = None,
    on_progress: Callable[[Progress], None] | None = None,
    annulla=None,
    retries: int = 2,
    orologio: Callable[[], float] = time.monotonic,
) -> Generator[float, None, TransferResults]:
    """Copia il piano sul disco a piccoli passi, verificando ogni file.

    ``copiatore`` deve esporre ``copia(serial, remoto, destinazione, on_scritti, annulla)``
    come generatore (lo fanno sia :class:`CopiatoreInterno` sia ``AdbAPassi``).
    La cronologia si salva **sempre** (``finally``): un ``GeneratorExit`` — finestra chiusa
    durante la copia — non è né ``OSError`` né ``FotoFacileError`` e un ``except`` non lo vede.
    """
    esiti = TransferResults(skipped=plan.skipped_duplicates + plan.skipped_existing)
    interno = _passi_di_copia(
        esiti, plan, options, copiatore, serial, history, on_progress, annulla, retries, orologio
    )
    try:
        return (yield from interno)
    finally:
        interno.close()
        _salva_cronologia(history, esiti)
```

- [ ] **Step 4: Verde**

Run: `.venv/bin/python -m pytest tests/test_regressioni.py tests/test_transfer.py tests/test_robustezza.py -v 2>&1 | tail -5 && .venv/bin/python -m pytest tests 2>&1 | tail -2`
Expected: tutti PASS. Se un vecchio test in `test_transfer.py` verificava `warnings` sul salvataggio fallito, deve continuare a passare (la logica è identica, cambia solo dove sta).

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/transfer.py tests/test_regressioni.py
git commit -m "fix(D2,D3,D4): cronologia salvata sempre, cancellazione fallita segnalata, totale coerente

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A3: D5 — Mostrare il motivo quando la ricerca delle foto fallisce

**Files:**
- Modify: `fotofacile/ui/page_select.py:166` (`_scansione_fallita`)
- Test: `tests/test_regressioni.py`

- [ ] **Step 1: Test che fallisce**

```python
# ── D5 ─────────────────────────────────────────────────────────────────────
# Prima: `_scansione_fallita(_errore)` buttava via il motivo; restava «Ricerca non riuscita.»
def test_d5_ricerca_fallita_spiega_il_motivo(app):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.core.errors import FotoFacileError
    from tests.aiuto import attendi

    class Bloccato:
        nome = "prova"
        spiegazione = ""

        def cerca_media(self, serial, include_videos=True, annulla=None):
            raise FotoFacileError("Il telefono è bloccato.", "Sblocca lo schermo e riprova.")
            yield 0.0  # pragma: no cover - lo rende un generatore

        def pulisci(self):
            pass

    app.remote = Bloccato()
    app.device = DeviceInfo(serial="S1", state="device", model="Prova", product="")
    pagina = app.pages["select"]
    pagina.start_scan()
    assert attendi(app, lambda: not pagina._scansione_in_corso)
    assert app.banner.message_text == "Il telefono è bloccato."
    assert "Sblocca" in app.banner.hint_text
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_regressioni.py::test_d5_ricerca_fallita_spiega_il_motivo -v` — Expected: FAIL (`'Sto cercando le foto…' == 'Il telefono è bloccato.'`).

- [ ] **Step 3: Implementare** — sostituire in `page_select.py`:

```python
    def _scansione_fallita(self, errore) -> None:
        self._scansione_in_corso = False
        self.bottone_cerca.state(["!disabled"])
        self.casella_video.state(["!disabled"])
        self.riepilogo.configure(text="Ricerca non riuscita.", foreground=COLORI["avviso"])
        self.app.set_status(errore.message, hint=errore.hint, kind="errore")
        self.app.log(f"Ricerca non riuscita: {errore.message} {errore.hint}".strip())
```

- [ ] **Step 4:** Run: stesso test + `.venv/bin/python -m pytest tests/test_page_select.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/page_select.py tests/test_regressioni.py
git commit -m "fix(D5): la ricerca fallita mostra il motivo e cosa fare

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A4: D6 — La cronologia non cancella più le voci di un'altra copia del programma

**Files:**
- Modify: `fotofacile/core/history.py` (`save`)
- Test: `tests/test_history.py`

- [ ] **Step 1: Test che fallisce** (in coda a `tests/test_history.py`)

```python
def test_due_istanze_non_si_cancellano_le_voci(tmp_path):
    percorso = tmp_path / "h.json"
    prima, seconda = History(percorso), History(percorso)
    prima.load()
    seconda.load()
    prima.record("S1", "DCIM/a.jpg", 1, 1, "/x/a.jpg")
    seconda.record("S1", "DCIM/b.jpg", 2, 2, "/x/b.jpg")
    prima.save()
    seconda.save()  # prima: cancellava la voce di `prima`
    finale = History(percorso)
    finale.load()
    assert finale.contains("S1", "DCIM/a.jpg", 1, 1)
    assert finale.contains("S1", "DCIM/b.jpg", 2, 2)
```
(assicurarsi che `History` sia già importato nel file di test; altrimenti `from fotofacile.core.history import History`.)

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_history.py -k due_istanze -v` — Expected: FAIL (`assert False`).

- [ ] **Step 3: Implementare** — in `History.save` unire con quanto c'è già su disco (le voci in memoria vincono):

```python
    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Un'altra copia del programma può aver scritto nel frattempo: si riparte da ciò che
        # c'è su disco e si sovrappongono le voci di questa sessione (vincono le più recenti).
        su_disco = History(self.path)
        su_disco.load()
        for seriale, voci in self._dati.items():
            su_disco._dati.setdefault(seriale, {}).update(voci)
        self._dati = su_disco._dati
        temporaneo = self.path.with_name(self.path.name + ".tmp")
        contenuto = {"version": VERSIONE, "devices": self._dati}
        temporaneo.write_text(json.dumps(contenuto, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(temporaneo, self.path)
```
Attenzione: `load()` mette da parte un file corrotto (rinomina in `.corrupt-…`): comportamento voluto, resta.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_history.py tests/test_robustezza.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/history.py tests/test_history.py
git commit -m "fix(D6): la cronologia unisce le voci invece di sovrascrivere

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A5: D8 — Nitidezza su Windows (dichiarare il DPI)

**Files:**
- Modify: `fotofacile/core/osutil.py` (funzione nuova), `fotofacile/cli.py` (`start_gui`)
- Test: `tests/test_osutil.py`

**Interfaces:**
- Produces: `rendi_consapevole_dpi(sistema: str | None = None, windll=None) -> bool` in `core/osutil.py`.

- [ ] **Step 1: Test che fallisce** (in coda a `tests/test_osutil.py`)

```python
def test_dpi_non_fa_nulla_fuori_da_windows():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    assert rendi_consapevole_dpi(sistema="darwin") is False
    assert rendi_consapevole_dpi(sistema="linux") is False


def test_dpi_su_windows_chiede_la_consapevolezza_per_monitor():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    chiamate = []

    class Shcore:
        def SetProcessDpiAwareness(self, valore):
            chiamate.append(valore)
            return 0

    class Windll:
        shcore = Shcore()

    assert rendi_consapevole_dpi(sistema="win32", windll=Windll()) is True
    assert chiamate == [2]  # 2 = per-monitor


def test_dpi_ripiega_sulla_vecchia_funzione():
    from fotofacile.core.osutil import rendi_consapevole_dpi

    chiamate = []

    class Shcore:
        def SetProcessDpiAwareness(self, _valore):
            raise OSError("non disponibile")

    class User32:
        def SetProcessDPIAware(self):
            chiamate.append("vecchia")
            return 1

    class Windll:
        shcore = Shcore()
        user32 = User32()

    assert rendi_consapevole_dpi(sistema="win32", windll=Windll()) is True
    assert chiamate == ["vecchia"]
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_osutil.py -k dpi -v` — Expected: FAIL (`ImportError`).

- [ ] **Step 3: Implementare** — in coda a `core/osutil.py`:

```python
def rendi_consapevole_dpi(sistema: str | None = None, windll=None) -> bool:
    """Su Windows dichiara che il programma gestisce da sé la scala dello schermo.

    Senza questo, con lo schermo al 125 % o più Windows ingrandisce la finestra come una
    figura e il testo diventa sfocato: un problema serio per chi vede poco. Va chiamata
    **prima** di creare la finestra. Fuori da Windows non fa niente.
    """
    if (sistema or sys.platform) != "win32":
        return False
    try:
        if windll is None:
            import ctypes

            windll = ctypes.windll  # type: ignore[attr-defined]
        try:
            windll.shcore.SetProcessDpiAwareness(2)  # per-monitor
            return True
        except (AttributeError, OSError):
            windll.user32.SetProcessDPIAware()
            return True
    except (AttributeError, OSError, ImportError):
        return False
```
(`sys` è già importato in `osutil.py`; se non lo fosse, aggiungere `import sys`.)

In `cli.start_gui`, subito prima di `applicazione = App(demo_mode=demo)`:

```python
    from .core.osutil import rendi_consapevole_dpi

    rendi_consapevole_dpi()
```

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_osutil.py tests/test_cli.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/osutil.py fotofacile/cli.py tests/test_osutil.py
git commit -m "fix(D8): su Windows la finestra dichiara il DPI (testo nitido)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A6: D9 — Dire di scegliere «Trasferimento file» sul telefono

**Files:**
- Modify: `fotofacile/ui/page_connect.py` (`CONSIGLI_SENZA_DEBUG`, testo introduttivo, dettaglio quando non c'è telefono)
- Test: `tests/test_page_connect.py`

- [ ] **Step 1: Test che fallisce**

```python
def test_l_aiuto_cita_trasferimento_file():
    from fotofacile.ui.page_connect import build_help_text_generico

    testo = build_help_text_generico()
    assert "Trasferimento file" in testo
    # deve venire PRIMA di qualunque accenno al Debug USB
    assert testo.index("Trasferimento file") < testo.index("Debug USB")


def test_senza_telefono_il_dettaglio_ricorda_trasferimento_file(app):
    pagina = app.pages["connect"]
    pagina._dispositivi_ricevuti([])
    assert "Trasferimento file" in pagina.dettaglio.cget("text")
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_connect.py -k trasferimento -v` — Expected: 2 FAIL.

- [ ] **Step 3: Implementare** — in `page_connect.py`:

Sostituire `CONSIGLI_SENZA_DEBUG` con:

```python
CONSIGLI_SENZA_DEBUG = (
    "Il telefono non viene riconosciuto.",
    "",
    "Prova in quest'ordine:",
    "1. Sblocca lo schermo del telefono.",
    "2. Scorri dall'alto verso il basso: vedrai un messaggio come «Ricarica via USB».",
    "   Toccalo e scegli «Trasferimento file» (a volte si chiama «File» o «MTP»).",
    "3. Se compare una richiesta, tocca «Consenti».",
    "4. Usa un altro cavo USB (alcuni cavi servono solo per ricaricare) o un'altra porta,",
    "   senza adattatori né hub.",
    "5. Scollega e ricollega il cavo tenendo il telefono sbloccato.",
    "",
    "Se non basta, l'ultima possibilità è attivare il «Debug USB»: scegli la marca del"
    " telefono qui sopra e segui i passaggi.",
)
```

Nel ramo `if not dispositivi:` di `_dispositivi_ricevuti`:

```python
            self.set_message("Non vedo ancora nessun telefono.")
            self.dettaglio.configure(
                text=(
                    "Sul telefono scorri dall'alto verso il basso e, al posto di «Ricarica via USB», "
                    "scegli «Trasferimento file». Poi sblocca lo schermo."
                )
            )
            return
```

Il vecchio test che confrontava il testo «Non vedo ancora nessun telefono: collegalo con il cavo e sbloccalo.» va aggiornato al nuovo (`grep` nel file dei test con `/usr/bin/grep -n "Non vedo ancora" tests`).

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_page_connect.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/page_connect.py tests/test_page_connect.py
git commit -m "fix(D9): l'aiuto spiega di scegliere «Trasferimento file» sul telefono

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task A7: Audit sistematico dei moduli non ancora riletti (D11…)

**Files:**
- Create: `docs/REVISIONE-v0.2.md` (registro dei risultati)
- Modify: quanto serve, un gruppo per volta; test in `tests/test_regressioni.py`

Questo task **non** ha codice pre-scritto perché i difetti non si conoscono ancora: ha un procedimento rigido e un elenco di domande precise. Ogni difetto trovato segue **lo stesso ciclo dei task A1–A6** (test rosso → correzione → verde → commit `fix(Dn): …`) e va registrato con numero, gravità e file.

Procedimento per **ogni gruppo** della tabella:

- [ ] **Step 1:** Orientarsi: `graphify query "<gruppo>"`.
- [ ] **Step 2:** Rivedere con il comando `code-review` (skill `code-review`, livello `high`) sui file del gruppo, oppure con l'agente `caveman:cavecrew-reviewer`. Per i moduli critici (G1, G2) farlo **due volte con revisori diversi** e tenere solo i difetti confermati leggendo il codice.
- [ ] **Step 3:** Rispondere per iscritto (in `docs/REVISIONE-v0.2.md`) a **ogni** domanda della tabella: «ok» + motivo, oppure numero del difetto.
- [ ] **Step 4:** Per ogni difetto: test rosso, correzione minima, `pytest tests` verde, commit.
- [ ] **Step 5:** `.venv/bin/python -m pyflakes fotofacile scripts` vuoto, poi `graphify update .`.

| Gruppo | File | Domande a cui rispondere |
|---|---|---|
| G1 Copia e disco | `core/adb_passi.py`, `core/ops.py`, `core/trasporto_aiutante.py` | Ogni `.part` viene rimosso in **ogni** uscita (errore, annullo, `GeneratorExit`)? `_controlla_spazio` conta lo spazio della cartella di destinazione o del disco di sistema? Un processo figlio può restare vivo dopo la chiusura della finestra (zombie, `adb` compreso)? Timeout: c'è un caso in cui `passo()` non termina mai? |
| G2 Collegamenti | `core/trasporto.py`, `trasporto_mac.py`, `trasporto_win.py`, `trasporto_linux.py` | `TrasportoComposto`: cosa succede con due telefoni? Il numero seriale è stabile fra ricerca e copia (stessa `serial` usata da `cancella`)? Nomi di file con `'`, `$`, `"`, emoji e `|` passano intatti da `wpd_win.ps1` e da `scanner.build_scan_command` (quoting di shell)? |
| G3 Aiutanti | `aiutanti/ptp_mac.py`, `aiutanti/mtp_linux.py`, `aiutanti/wpd_win.py` + `.ps1` | Ogni uscita di errore ha codice 2/3 e messaggio umano su `stderr`? Le righe JSON con `\n` dentro i nomi sono gestite? Il `.ps1` mantiene il BOM dopo ogni modifica? Filtrare `.thumbnails`/`cache`/`Stickers` già qui costa meno che poi (vedi Task C4)? |
| G4 Download componente | `core/installer.py`, `core/adb.py`, `core/devices.py` | **Zip-slip**: l'estrazione rifiuta i percorsi con `..` o assoluti? L'impronta SHA-256 è verificata **prima** di estrarre? Rete assente/lenta: c'è un timeout e un messaggio? |
| G5 Dati e resoconti | `core/report.py`, `core/format.py`, `core/demo.py`, `core/scanner.py` | `format_size`/`format_eta` con 0, negativi, `None`, valori enormi? `save_report` in una cartella non scrivibile? `group_folders` con percorsi identici a meno delle maiuscole? |
| G6 Avvio e CLI | `cli.py`, `__main__.py`, `fotofacile.py` | `--selftest` distingue «grafica rotta» da «avvio sbagliato» **anche da eseguibile congelato**? `scrivi_log_avvio` cresce senza limite? Lo stesso `avvio.log` viene ruotato? |
| G7 Pagine e app | `ui/app.py`, `ui/page_*.py` | Nessun `after` resta pendente alla chiusura? `go_to` durante un task attivo lascia stato incoerente? Doppio clic rapido su «Copia le foto»? |
| G8 Script di build | `scripts/*.py`, `installer/windows/*.ps1`, `.github/workflows/*.yml` | Solo lettura qui: le correzioni vere sono nella Parte D. Annotare cosa la Parte D sostituirà. |

- [ ] **Step 6: Chiusura del task** — aggiungere in `docs/PIANO-REVISIONE.md` la sezione «Terza revisione (D1–Dn)» con la tabella dei difetti trovati (quella all'inizio di questo piano + i nuovi) e committare:

```bash
git add docs tests fotofacile
git commit -m "docs: terza revisione (D1-Dn) con l'elenco dei difetti corretti

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

# PARTE B — Il problema del WebP

### Task B1: Riconoscere il formato vero dei file + comando `formati`

**Files:**
- Create: `fotofacile/core/formati.py`
- Modify: `fotofacile/cli.py` (nuovo comando `formati <cartella>`)
- Test: `tests/test_formati.py`

**Interfaces:**
- Produces:
  - `formato_reale(inizio: bytes) -> str` → uno di `"jpeg" "png" "gif" "webp" "heic" "avif" "bmp" "tiff" "mp4" "sconosciuto"`.
  - `formato_del_file(percorso: Path) -> str`
  - `analizza_cartella(cartella: Path) -> dict[str, dict[str, int]]` → `{estensione_minuscola: {formato_reale: conteggio}}`.

- [ ] **Step 1: Test che fallisce** — `tests/test_formati.py`:

```python
from pathlib import Path

from fotofacile.core.formati import analizza_cartella, formato_del_file, formato_reale


def test_riconosce_i_formati_dai_primi_byte():
    assert formato_reale(b"\xff\xd8\xff\xe0" + b"\0" * 8) == "jpeg"
    assert formato_reale(b"\x89PNG\r\n\x1a\n" + b"\0" * 4) == "png"
    assert formato_reale(b"RIFF\x10\0\0\0WEBPVP8 ") == "webp"
    assert formato_reale(b"\0\0\0\x18ftypheic" + b"\0" * 4) == "heic"
    assert formato_reale(b"\0\0\0\x1cftypavif" + b"\0" * 4) == "avif"
    assert formato_reale(b"\0\0\0\x18ftypisom" + b"\0" * 4) == "mp4"
    assert formato_reale(b"qualcosa di strano") == "sconosciuto"
    assert formato_reale(b"") == "sconosciuto"


def test_un_wav_non_e_webp():
    # anche i WAV iniziano con «RIFF»: conta la parola «WEBP» in posizione 8
    assert formato_reale(b"RIFF\x10\0\0\0WAVEfmt ") == "sconosciuto"


def test_analizza_cartella_trova_estensioni_bugiarde(tmp_path: Path):
    (tmp_path / "finta.jpg").write_bytes(b"RIFF\x10\0\0\0WEBPVP8 ")
    (tmp_path / "vera.jpg").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 8)
    (tmp_path / "sticker.webp").write_bytes(b"RIFF\x10\0\0\0WEBPVP8 ")
    (tmp_path / "sotto").mkdir()
    (tmp_path / "sotto" / "a.JPG").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 8)
    risultato = analizza_cartella(tmp_path)
    assert risultato["jpg"] == {"webp": 1, "jpeg": 2}
    assert risultato["webp"] == {"webp": 1}
    assert formato_del_file(tmp_path / "vera.jpg") == "jpeg"
    assert formato_del_file(tmp_path / "non-esiste.jpg") == "sconosciuto"
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_formati.py -v` — Expected: FAIL (`ModuleNotFoundError`).

- [ ] **Step 3: Implementare** — `fotofacile/core/formati.py`:

```python
"""Formato **vero** di un file immagine o video, riconosciuto dai primi byte.

L'estensione si può sbagliare o essere cambiata; i primi byte no. Serve a due cose:
capire perché una cartella piena di foto contiene file WebP e decidere se convertirli.
"""

from __future__ import annotations

from pathlib import Path

_MARCHI_HEIF = {b"heic": "heic", b"heix": "heic", b"mif1": "heic", b"msf1": "heic", b"heim": "heic",
                b"heis": "heic", b"hevc": "heic", b"avif": "avif", b"avis": "avif"}


def formato_reale(inizio: bytes) -> str:
    """Riconosce il formato dai primi 12 byte (bastano per tutti quelli elencati)."""
    if inizio[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if inizio[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if inizio[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if inizio[:4] == b"RIFF" and inizio[8:12] == b"WEBP":
        return "webp"
    if inizio[:2] == b"BM":
        return "bmp"
    if inizio[:4] in (b"II*\0", b"MM\0*"):
        return "tiff"
    if inizio[4:8] == b"ftyp":
        return _MARCHI_HEIF.get(inizio[8:12], "mp4")
    return "sconosciuto"


def formato_del_file(percorso: Path) -> str:
    """Formato vero di un file; ``"sconosciuto"`` se non si può leggere."""
    try:
        with open(percorso, "rb") as file:
            return formato_reale(file.read(12))
    except OSError:
        return "sconosciuto"


def analizza_cartella(cartella: Path) -> dict[str, dict[str, int]]:
    """Conta i file per estensione e per formato vero: ``{"jpg": {"webp": 1, "jpeg": 2}}``."""
    conteggi: dict[str, dict[str, int]] = {}
    for percorso in Path(cartella).rglob("*"):
        if not percorso.is_file():
            continue
        estensione = percorso.suffix.lstrip(".").lower() or "(nessuna)"
        formato = formato_del_file(percorso)
        per_estensione = conteggi.setdefault(estensione, {})
        per_estensione[formato] = per_estensione.get(formato, 0) + 1
    return conteggi
```

In `fotofacile/cli.py`: aggiungere `"formati"` ai `choices` di `comando`, un argomento posizionale opzionale `cartella`, e il ramo in `main`:

```python
    parser.add_argument("cartella", nargs="?", help="con «formati»: la cartella da analizzare")
```
e in `main`, prima di `selftest`:
```python
    if argomenti_letti.comando == "formati":
        return comando_formati(argomenti_letti.cartella)
```
con
```python
def comando_formati(cartella: str | None) -> int:
    """Mostra, per ogni estensione, quali formati veri contiene (serve a capire il WebP)."""
    from .core.formati import analizza_cartella

    if not cartella or not Path(cartella).is_dir():
        print("Indica una cartella esistente:  fotofacile formati <cartella>")
        return 2
    risultato = analizza_cartella(Path(cartella))
    if not risultato:
        print("La cartella non contiene file.")
        return 0
    print(f"Formati trovati in {cartella}:")
    for estensione, per_formato in sorted(risultato.items()):
        dettaglio = ", ".join(f"{quanti} {formato}" for formato, quanti in sorted(per_formato.items()))
        print(f"  .{estensione}: {dettaglio}")
    return 0
```
Il `choices=["doctor"]` diventa `choices=["doctor", "formati"]`, e la `help` dell'argomento `comando` si aggiorna di conseguenza.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_formati.py tests/test_cli.py -v` — Expected: PASS. Aggiungere a `tests/test_cli.py` un test di `comando_formati` (cartella inesistente → codice 2; cartella con un `.webp` → stampa `.webp: 1 webp`) usando `capsys`.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/formati.py fotofacile/cli.py tests/test_formati.py tests/test_cli.py
git commit -m "feat: riconoscimento del formato vero dei file e comando «formati»

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task B2: Capire da dove vengono i WebP (con i dati veri di Marco)

**Files:**
- Modify: `docs/REVISIONE-v0.2.md` (sezione «WebP: diagnosi»)

Nessun codice: è il passaggio che decide cosa serve davvero. **Serve Marco** per due dati.

- [ ] **Step 1: ⚠ CHIEDI a Marco**: (a) la cartella dove il programma ha salvato le immagini del suo test (o `~/.fotofacile/avvio.log` e il resoconto salvato), (b) sistema del computer (Windows/macOS/Linux) e modello del telefono.
- [ ] **Step 2:** Eseguire `.venv/bin/python fotofacile.py formati "<cartella>"` e incollare l'output nel documento.
- [ ] **Step 3: Interpretare con questa tabella e scrivere la conclusione nel documento:**

| Risultato di `formati` | Significato | Azione |
|---|---|---|
| Molti `.webp` con formato `webp`, e le loro cartelle di origine (resoconto) sono `WhatsApp Stickers`, `Download`, `Android/media/...` | **H1**: sono sticker/immagini web reali | Task B3–B5 (conversione) **+** Task C4 (nascondere sticker e miniature di default) |
| `.jpg` con formato `webp` (estensione bugiarda) | Un'app/collegamento ha rinominato | Task B4 già copre: il file viene riconosciuto dal contenuto, non dal nome |
| Anche le foto della fotocamera (`DCIM/Camera`) sono `webp` | **H2**: il telefono salva in WebP | Task B3–B5; ricordare a Marco dell'impostazione della fotocamera del telefono |
| Nessun WebP nella cartella | Il test era su un'altra cartella / un'altra versione | Chiedere il resoconto e ripetere |

- [ ] **Step 4:** Registrare la conclusione (una frase) e committare: `git add docs && git commit -m "docs: diagnosi del WebP"` (con la riga `Co-Authored-By`).

> Se Marco non è raggiungibile ora, si procede comunque con B3–B5 e C4: coprono H1, H2 e H3 insieme, e B2 resta come verifica a posteriori.

### Task B3: Conversione WebP → JPG/PNG

**Files:**
- Create: `fotofacile/core/conversione.py`
- Modify: `requirements.txt`, `requirements-dev.txt`
- Test: `tests/test_conversione.py`

**Interfaces:**
- Consumes: `formato_del_file` (Task B1).
- Produces:
  - `pillow_disponibile() -> bool`
  - `e_webp(percorso: Path) -> bool`
  - `converti_webp(percorso: Path, qualita: int = 95) -> Path` → percorso finale: `.jpg` (opaco), `.png` (con trasparenza), oppure il file **rinominato `.webp`** se animato. Mantiene EXIF, profilo colore e **data del file**. Scrive su un temporaneo e rimpiazza in modo atomico; l'originale sparisce solo a conversione riuscita.

- [ ] **Step 1: Dipendenze** — `requirements-dev.txt`: aggiungere `pillow>=10`. `requirements.txt`: aggiungere in fondo

```
# Opzionale: senza Pillow il programma funziona, ma non può trasformare le immagini WebP in JPG.
pillow>=10
```

Run: `.venv/bin/python -m pip install -r requirements-dev.txt && .venv/bin/python -c "from PIL import features; print(features.check('webp'))"`
Expected: `True`.

- [ ] **Step 2: Test che fallisce** — `tests/test_conversione.py`:

```python
import os
from pathlib import Path

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image, features  # noqa: E402

from fotofacile.core.conversione import converti_webp, e_webp, pillow_disponibile  # noqa: E402

pytestmark = pytest.mark.skipif(not features.check("webp"), reason="questo Pillow non sa il WebP")


def _webp(percorso: Path, modo="RGB", colore=(200, 20, 20), dimensione=(16, 16)) -> Path:
    Image.new(modo, dimensione, colore).save(percorso, "WEBP")
    return percorso


def test_pillow_e_riconoscimento():
    assert pillow_disponibile() is True


def test_e_webp_guarda_il_contenuto_non_il_nome(tmp_path):
    finto = _webp(tmp_path / "foto.jpg")  # contenuto WebP, nome .jpg
    assert e_webp(finto) is True
    (tmp_path / "vero.jpg").write_bytes(b"\xff\xd8\xff\xe0" + b"\0" * 16)
    assert e_webp(tmp_path / "vero.jpg") is False
    assert e_webp(tmp_path / "non-esiste.jpg") is False


def test_immagine_opaca_diventa_jpg_e_conserva_la_data(tmp_path):
    sorgente = _webp(tmp_path / "a.webp")
    os.utime(sorgente, (1_500_000_000, 1_500_000_000))
    finale = converti_webp(sorgente)
    assert finale == tmp_path / "a.jpg"
    assert not sorgente.exists()
    assert not list(tmp_path.glob("*.conv"))
    with Image.open(finale) as immagine:
        assert immagine.format == "JPEG"
    assert int(finale.stat().st_mtime) == 1_500_000_000


def test_nome_gia_jpg_viene_rimpiazzato_sul_posto(tmp_path):
    sorgente = _webp(tmp_path / "a.jpg")  # WebP travestito da JPG
    finale = converti_webp(sorgente)
    assert finale == sorgente
    with Image.open(finale) as immagine:
        assert immagine.format == "JPEG"


def test_trasparenza_diventa_png(tmp_path):
    sorgente = _webp(tmp_path / "sticker.webp", modo="RGBA", colore=(10, 200, 10, 90))
    finale = converti_webp(sorgente)
    assert finale.suffix == ".png"
    with Image.open(finale) as immagine:
        assert immagine.format == "PNG"


def test_animazione_resta_webp_con_estensione_giusta(tmp_path):
    fotogrammi = [Image.new("RGB", (8, 8), (i * 40, 0, 0)) for i in range(4)]
    animata = tmp_path / "gif-animata.jpg"
    fotogrammi[0].save(animata, "WEBP", save_all=True, append_images=fotogrammi[1:], duration=80, loop=0)
    finale = converti_webp(animata)
    assert finale == tmp_path / "gif-animata.webp"
    assert finale.exists() and not animata.exists()


def test_file_rovinato_solleva_e_non_tocca_l_originale(tmp_path):
    rotto = tmp_path / "rotto.webp"
    rotto.write_bytes(b"RIFF\x04\0\0\0WEBPzzzz")
    with pytest.raises(Exception):
        converti_webp(rotto)
    assert rotto.exists()
    assert not list(tmp_path.glob("*.conv"))
```

- [ ] **Step 3:** Run: `.venv/bin/python -m pytest tests/test_conversione.py -v` — Expected: FAIL (`ModuleNotFoundError`).

- [ ] **Step 4: Implementare** — `fotofacile/core/conversione.py`:

```python
"""Conversione delle immagini WebP in JPG (o PNG se hanno trasparenza).

Il WebP non si apre con molti programmi (Foto di Windows 10 senza estensione, vecchi
visualizzatori, stampanti, siti). JPG e PNG sì. Pillow è **opzionale**: senza, il programma
copia i WebP così come sono.
"""

from __future__ import annotations

import os
from pathlib import Path

from .formati import formato_del_file


def pillow_disponibile() -> bool:
    """True se Pillow c'è e sa leggere il WebP."""
    try:
        from PIL import features
    except ImportError:
        return False
    return bool(features.check("webp"))


def e_webp(percorso: Path) -> bool:
    """True se il **contenuto** del file è WebP, qualunque sia il nome."""
    return formato_del_file(Path(percorso)) == "webp"


def _libero(percorso: Path, occupato_da: Path | None) -> Path:
    """Un nome non ancora usato (aggiunge « (1)», « (2)»…); ``occupato_da`` è il file stesso."""
    if not percorso.exists() or (occupato_da is not None and percorso == occupato_da):
        return percorso
    for contatore in range(1, 1000):
        candidato = percorso.with_name(f"{percorso.stem} ({contatore}){percorso.suffix}")
        if not candidato.exists():
            return candidato
    return percorso


def converti_webp(percorso: Path, qualita: int = 95) -> Path:
    """Converte **sul posto** un file WebP e restituisce il percorso finale.

    - opaco → ``.jpg`` (qualità alta, EXIF e profilo colore conservati);
    - con trasparenza → ``.png``;
    - animato → resta WebP, ma con l'estensione giusta.

    Si scrive su un file temporaneo e lo si rimpiazza solo a lavoro finito: se qualcosa va
    storto l'originale è intatto. La data del file viene conservata.
    """
    from PIL import Image

    sorgente = Path(percorso)
    stato = sorgente.stat()
    temporaneo = sorgente.with_name(sorgente.name + ".conv")
    try:
        with Image.open(sorgente) as immagine:
            if getattr(immagine, "is_animated", False):
                finale = _libero(sorgente.with_suffix(".webp"), sorgente)
                temporaneo = None  # niente da scrivere: basta rinominare
            else:
                trasparente = immagine.mode in ("RGBA", "LA", "PA") or "transparency" in immagine.info
                opzioni: dict = {}
                if immagine.info.get("exif"):
                    opzioni["exif"] = immagine.info["exif"]
                if immagine.info.get("icc_profile"):
                    opzioni["icc_profile"] = immagine.info["icc_profile"]
                if trasparente:
                    formato, estensione, pronta = "PNG", ".png", immagine.convert("RGBA")
                else:
                    formato, estensione, pronta = "JPEG", ".jpg", immagine.convert("RGB")
                    opzioni.update(quality=qualita, subsampling=0)
                finale = _libero(sorgente.with_suffix(estensione), sorgente)
                with open(temporaneo, "wb") as uscita:
                    pronta.save(uscita, formato, **opzioni)
                    uscita.flush()
                    os.fsync(uscita.fileno())
        # l'immagine è chiusa: ora si può rimpiazzare anche su Windows
        if temporaneo is not None:
            os.replace(temporaneo, finale)
            if finale != sorgente:
                sorgente.unlink()
        elif finale != sorgente:
            os.replace(sorgente, finale)
        os.utime(finale, (stato.st_atime, stato.st_mtime))
        return finale
    except BaseException:
        if temporaneo is not None:
            temporaneo.unlink(missing_ok=True)
        raise
```

- [ ] **Step 5:** Run: `.venv/bin/python -m pytest tests/test_conversione.py -v` — Expected: 7 PASS. Se `pytest` segnala un `DeprecationWarning` di Pillow (`filterwarnings = error`), correggere la chiamata incriminata, **non** allentare `pytest.ini`.

- [ ] **Step 6: Commit**

```bash
git add fotofacile/core/conversione.py requirements.txt requirements-dev.txt tests/test_conversione.py
git commit -m "feat: conversione delle immagini WebP in JPG/PNG (opzionale, con Pillow)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task B4: Usare la conversione dentro la copia (nomi previsti dal piano + passo di conversione)

**Files:**
- Modify: `fotofacile/core/planner.py` (`TransferOptions.converti_webp`, `destination_for`, `build_plan`), `fotofacile/core/transfer.py` (`_passi_di_copia`)
- Test: `tests/test_planner.py`, `tests/test_regressioni.py` (o `tests/test_transfer.py`)

**Interfaces:**
- Consumes: `e_webp`, `converti_webp` (Task B3); `_TelefonoFinto`, `_piano_singolo` (Task A1).
- Produces: `TransferOptions.converti_webp: bool = False`; `destination_for(remote_path, destination, preserve_structure, case_insensitive=None, converti_webp=False) -> Path`.

Progetto: il **piano** prevede già il nome finale `.jpg` per i `.webp` (così anche «già presente» e le collisioni funzionano). La copia scrive i byte nel percorso pianificato, poi, **a copia verificata**, se il contenuto è WebP lo si converte. Se la conversione fallisce il file resta salvo, con estensione `.webp` corretta, più un avviso: **mai perdere una foto per colpa della conversione**.

- [ ] **Step 1: Test che falliscono**

In `tests/test_planner.py`:

```python
def test_webp_pianificato_con_estensione_jpg(tmp_path):
    from fotofacile.core.planner import destination_for

    assert destination_for("/sdcard/Pictures/a.webp", tmp_path, False, converti_webp=True) == tmp_path / "a.jpg"
    assert destination_for("/sdcard/Pictures/a.WEBP", tmp_path, False, converti_webp=True) == tmp_path / "a.jpg"
    assert destination_for("/sdcard/Pictures/a.webp", tmp_path, False) == tmp_path / "a.webp"
    assert destination_for("/sdcard/Pictures/a.png", tmp_path, False, converti_webp=True) == tmp_path / "a.png"


def test_webp_convertito_non_si_scambia_per_gia_presente(tmp_path):
    (tmp_path / "a.jpg").write_bytes(b"x" * 100)  # una foto diversa, stesso nome e stessa dimensione
    file = [foto("/sdcard/Pictures/a.webp", size=100)]
    piano = build_plan(file, TransferOptions(destination=tmp_path, converti_webp=True))
    assert [f.dest_path.name for f in piano.files] == ["a (1).jpg"]
    assert piano.skipped_existing == 0
```

In `tests/test_regressioni.py`:

```python
# ── WebP ───────────────────────────────────────────────────────────────────
def _webp_bytes(modo="RGB", colore=(9, 99, 199)) -> bytes:
    import io

    from PIL import Image

    scarico = io.BytesIO()
    Image.new(modo, (12, 12), colore).save(scarico, "WEBP")
    return scarico.getvalue()


def test_la_copia_converte_i_webp_in_jpg(tmp_path):
    pytest = __import__("pytest")
    pytest.importorskip("PIL")
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import transfer

    dati = _webp_bytes()
    media = MediaFile("/sdcard/Pictures/a.webp", size=len(dati), mtime=1_500_000_000, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out", converti_webp=True)
    esiti = transfer(_TelefonoFinto({media.remote_path: dati}), "S1", build_plan([media], opzioni), opzioni)
    assert [p.name for p in esiti.copied] == ["a.jpg"]
    assert esiti.copied[0].read_bytes()[:3] == b"\xff\xd8\xff"
    assert int(esiti.copied[0].stat().st_mtime) == 1_500_000_000
    assert not esiti.warnings


def test_conversione_fallita_conserva_il_file_come_webp(tmp_path, monkeypatch):
    from fotofacile.core import transfer as modulo
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile

    dati = _webp_bytes()
    media = MediaFile("/sdcard/Pictures/a.webp", size=len(dati), mtime=5, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out", converti_webp=True)

    def rotta(_percorso):
        raise ValueError("Pillow non ci riesce")

    monkeypatch.setattr(modulo, "converti_webp", rotta)
    esiti = modulo.transfer(_TelefonoFinto({media.remote_path: dati}), "S1", build_plan([media], opzioni), opzioni)
    assert [p.name for p in esiti.copied] == ["a.webp"]  # estensione corretta, foto salva
    assert esiti.copied[0].read_bytes() == dati
    assert any("a.webp" in avviso for avviso in esiti.warnings)
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_planner.py tests/test_regressioni.py -k "webp" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare — planner** (`fotofacile/core/planner.py`)

Aggiungere il campo a `TransferOptions` (dopo `date_from`):

```python
    #: Trasforma i file WebP in JPG (o PNG se trasparenti): si aprono con qualsiasi programma.
    converti_webp: bool = False
```

Sostituire `destination_for` con:

```python
def destination_for(
    remote_path: str,
    destination: Path,
    preserve_structure: bool,
    case_insensitive: bool | None = None,
    converti_webp: bool = False,
) -> Path:
    """Percorso di destinazione del file, con nomi validi su ogni sistema operativo.

    La cartella scelta dall'utente non viene **mai** riscritta: se il percorso è troppo lungo
    si accorciano solo le cartelle provenienti dal telefono e, se serve, il nome del file.
    Con ``converti_webp`` un ``.webp`` viene pianificato come ``.jpg``.
    """
    radice = Path(destination)
    relativo = relative_path(remote_path)
    nome = _nome_sicuro(relativo.rsplit("/", 1)[-1])
    if converti_webp and nome.lower().endswith(".webp"):
        nome = nome[: -len(".webp")] + ".jpg"
    if not preserve_structure:
        return _limita_percorso(radice / nome, radice)
    cartelle = [_nome_sicuro(parte) for parte in relativo.split("/")[:-1] if parte]
    return _limita_percorso(radice.joinpath(*cartelle, nome), radice)
```

In `build_plan`, sostituire dal calcolo di `destinazione` fino a `esistenza.registra(...)` con:

```python
        convertito = options.converti_webp and file.name.lower().endswith(".webp")
        destinazione = destination_for(
            file.remote_path,
            options.destination,
            options.preserve_structure,
            case_insensitive=sensibile,
            converti_webp=convertito,
        )
        esistente = esistenza.trova(destinazione)
        if esistente is not None:
            # «già presente» vale solo se il nome è identico: se differisce solo per le
            # maiuscole (FOTO.JPG contro foto.jpg) si tratta di un file diverso, e su un
            # disco non sensibile alle maiuscole sovrascriverlo perderebbe una foto.
            # Un WebP che verrà convertito non ha una dimensione confrontabile: un file con
            # lo stesso nome si considera **diverso** (al massimo resta un doppione).
            uguale = esistente.name == destinazione.name and not convertito
            if uguale and file.size and _dimensione(esistente) == file.size:
                piano.skipped_existing += 1
                continue
            destinazione = esistenza.nome_libero(destinazione, options.destination)
        esistenza.registra(destinazione)
```

- [ ] **Step 4: Implementare — transfer** (`fotofacile/core/transfer.py`)

In cima: `from .conversione import converti_webp, e_webp`.

In `_passi_di_copia`, sostituire il blocco che va da `esiti.copied.append(pianificato.dest_path)` a `history.record(...)` con:

```python
        finale = pianificato.dest_path
        if options.converti_webp and e_webp(finale):
            try:
                finale = converti_webp(finale)
            except Exception as errore:  # la conversione non deve mai far perdere una foto
                finale = _rimetti_estensione_webp(finale)
                esiti.warnings.append(
                    f"Non sono riuscito a trasformare {finale.name} in JPG ({errore}): "
                    "l'ho lasciata così com'è."
                )
            yield 0.0  # la conversione occupa un attimo: si lascia respirare la finestra
        _applica_data(finale, pianificato.media.mtime)
        esiti.copied.append(finale)
        if history is not None:
            history.record(
                serial,
                pianificato.rel_path,
                pianificato.media.size,
                pianificato.media.mtime,
                str(finale),
            )
```
e, vicino a `_applica_data`:

```python
def _rimetti_estensione_webp(percorso: Path) -> Path:
    """Dà al file l'estensione ``.webp`` (il contenuto è WebP): meglio onesto che «.jpg»."""
    if percorso.suffix.lower() == ".webp":
        return percorso
    nuovo = percorso.with_suffix(".webp")
    contatore = 0
    while nuovo.exists():
        contatore += 1
        nuovo = percorso.with_name(f"{percorso.stem} ({contatore}).webp")
    try:
        os.replace(percorso, nuovo)
    except OSError:  # pragma: no cover - meglio un nome sbagliato che nessun file
        return percorso
    return nuovo
```
(`_applica_data` di A1 viene chiamata qui: togliere la chiamata precedente aggiunta in A1, per non farla due volte.)

- [ ] **Step 5:** Run: `.venv/bin/python -m pytest tests -x 2>&1 | tail -3` — Expected: verde.

- [ ] **Step 6: Commit**

```bash
git add fotofacile/core/planner.py fotofacile/core/transfer.py tests
git commit -m "feat: la copia trasforma i WebP in JPG/PNG senza mai perdere un file

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task B5: Casella nella pagina «Destinazione», voce nella diagnosi, Pillow nel pacchetto

**Files:**
- Modify: `fotofacile/ui/page_options.py`, `tests/conftest.py`, `fotofacile/cli.py` (`build_doctor_report`, `doctor`), `scripts/build_app.py`, `.github/workflows/build-installers.yml` (dipendenze)
- Test: `tests/test_page_options.py`, `tests/test_cli.py`

**Interfaces:**
- Consumes: `pillow_disponibile` (B3), `TransferOptions.converti_webp` (B4).
- Produces: `OptionsPage.converti_webp: tk.BooleanVar`; `build_doctor_report(..., conversione_webp: bool | None = None)`.

- [ ] **Step 1: Test che falliscono**

`tests/test_page_options.py`:

```python
def test_la_conversione_webp_e_attiva_se_pillow_c_e(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options, "pillow_disponibile", lambda: True)
    app.ricostruisci_pagine()
    pagina = app.pages["options"]
    assert pagina.converti_webp.get() is True
    assert pagina.build_options().converti_webp is True


def test_senza_pillow_la_conversione_e_spenta(app, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options, "pillow_disponibile", lambda: False)
    app.ricostruisci_pagine()
    pagina = app.pages["options"]
    assert pagina.converti_webp.get() is False
    assert pagina.build_options().converti_webp is False
```

`tests/test_cli.py`:

```python
def test_la_diagnosi_riferisce_la_conversione_webp():
    from fotofacile.cli import build_doctor_report

    base = dict(adb_path=None, adb_version="", system="linux", python_version="3.12", tk_version="8.6",
                devices=[], app_folder="/x", writing_ok=True)
    assert "Conversione WebP: disponibile" in build_doctor_report(**base, conversione_webp=True)
    assert "Conversione WebP: non disponibile" in build_doctor_report(**base, conversione_webp=False)
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_options.py tests/test_cli.py -k "webp" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare**

`page_options.py`: importare `from ..core.conversione import pillow_disponibile`; nel costruttore, accanto alle altre variabili:

```python
        # Attiva di default solo se possibile: senza Pillow non si può convertire.
        self._conversione_possibile = pillow_disponibile()
        self.converti_webp = tk.BooleanVar(value=self._conversione_possibile)
```
e, fra le caselle (dopo «Salta le foto che ho già copiato», righe `1` → spostare le successive di uno), solo se possibile:

```python
        if self._conversione_possibile:
            ttk.Checkbutton(
                scelte,
                text="Trasforma le immagini WebP in JPG (si aprono con qualsiasi programma)",
                variable=self.converti_webp,
                command=self._aggiorna_spazio,
            ).grid(row=2, column=0, sticky="w", pady=3)
```
(la casella «Cancella…» passa a `row=3`, `avviso_eliminazione` a `row=4` in `_eliminazione_cambiata`). In `build_options()` aggiungere `converti_webp=self.converti_webp.get() and self._conversione_possibile,`.

`tests/conftest.py:azzera`, sezione `opzioni`: aggiungere `opzioni.converti_webp.set(opzioni._conversione_possibile)`.

`cli.py`: aggiungere il parametro `conversione_webp: bool | None = None` a `build_doctor_report` e, dopo la riga «Scrittura», 

```python
    if conversione_webp is not None:
        righe.append(f"Conversione WebP: {'disponibile' if conversione_webp else 'non disponibile'}")
```
e in `doctor()` passare `conversione_webp=pillow_disponibile()` (import locale da `.core.conversione`).

`scripts/build_app.py` (`comando_pyinstaller`): dopo gli `--add-data`, aggiungere

```python
    # Pillow serve solo alla conversione WebP → JPG; PyInstaller ha un suo «hook» ma
    # i codec (_webp) vanno chiesti espressamente.
    comando += ["--collect-submodules", "PIL", "--collect-binaries", "PIL"]
```

`.github/workflows/build-installers.yml`: in **entrambi** i job la riga delle dipendenze diventa `python -m pip install --upgrade pip pyinstaller pillow` (nel job macOS c'è già `-r requirements.txt`, che ora include Pillow).

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests -x 2>&1 | tail -3 && .venv/bin/python -m pyflakes fotofacile scripts` — Expected: verde, pyflakes vuoto.

- [ ] **Step 5: Verifica a mano con l'app demo** (facoltativa ma consigliata): `.venv/bin/python fotofacile.py doctor | /usr/bin/grep WebP` → `Conversione WebP: disponibile`.

- [ ] **Step 6: Commit**

```bash
git add fotofacile scripts tests .github
git commit -m "feat: opzione «Trasforma i WebP in JPG», voce in diagnosi, Pillow nel pacchetto

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

# PARTE C — Interfaccia semplice e leggibile (anche per gli anziani)

**Principi di progetto** (ogni task li rispetta; il task C10 li verifica con test automatici e con schermate):

1. **Un solo compito per schermata**, un solo pulsante grande («Avanti»); il resto è secondario e più piccolo.
2. **Testo grande**: base 14 pt × scala scelta dall'utente (normale 100 %, grande 125 %, molto grande 150 %); nessun testo sotto i 14 pt a scala 100 %. Titoli 28 pt.
3. **Parole di tutti i giorni**: mai «Debug USB», «serial», «MTP», «percorso» nella schermata principale; «Trasferimento file» sì, perché è il nome che il telefono mostra.
4. **Mai solo il colore**: ogni messaggio ha un simbolo (✔ ⚠ ✖ ℹ) e un testo.
5. **Niente da scrivere a mano** (date → menu a scelta; cartelle → pulsante «Cambia cartella»).
6. **Le decisioni pericolose** (cancellare dal telefono) passano da una finestra di conferma con «Sì/No» esplicito.
7. **Tastiera**: `Invio` = pulsante principale, `Esc` = Indietro, focus ben visibile.
8. **I dettagli tecnici** stanno dietro un piccolo «Mostra i dettagli», chiusi di default.

### Task C1: Impostazioni dell'utente (dimensione del testo)

**Files:**
- Create: `fotofacile/core/impostazioni.py`
- Test: `tests/test_impostazioni.py`

**Interfaces:**
- Produces:
  - `SCALE_AMMESSE = (1.0, 1.25, 1.5)`, `SCALA_PREDEFINITA = 1.25`
  - `class Impostazioni: scala_testo: float`; `Impostazioni.carica(percorso: Path | None = None) -> Impostazioni`; `.salva(percorso: Path | None = None) -> None`
  - `scala_vicina(valore: object) -> float`

- [ ] **Step 1: Test che fallisce** — `tests/test_impostazioni.py`:

```python
from fotofacile.core.impostazioni import (
    SCALA_PREDEFINITA,
    SCALE_AMMESSE,
    Impostazioni,
    scala_vicina,
)


def test_predefinito_quando_il_file_non_esiste(tmp_path):
    assert Impostazioni.carica(tmp_path / "no.json").scala_testo == SCALA_PREDEFINITA


def test_salva_e_ricarica(tmp_path):
    percorso = tmp_path / "i.json"
    Impostazioni(scala_testo=1.5).salva(percorso)
    assert Impostazioni.carica(percorso).scala_testo == 1.5


def test_file_rovinato_o_valori_strani_non_rompono_niente(tmp_path):
    percorso = tmp_path / "i.json"
    percorso.write_text("{non è json", encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA
    percorso.write_text('{"scala_testo": "enorme"}', encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA
    percorso.write_text("[1, 2]", encoding="utf-8")
    assert Impostazioni.carica(percorso).scala_testo == SCALA_PREDEFINITA


def test_la_scala_si_riporta_alla_piu_vicina_ammessa():
    assert scala_vicina(1.3) == 1.25
    assert scala_vicina(9) == SCALE_AMMESSE[-1]
    assert scala_vicina(0) == SCALE_AMMESSE[0]
    assert scala_vicina(None) == SCALA_PREDEFINITA


def test_salvataggio_in_cartella_non_scrivibile_non_solleva(tmp_path):
    bloccato = tmp_path / "file"
    bloccato.write_text("x")
    Impostazioni(scala_testo=1.0).salva(bloccato / "dentro.json")  # «file» non è una cartella
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_impostazioni.py -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — `fotofacile/core/impostazioni.py`:

```python
"""Impostazioni personali (per ora: la dimensione del testo), salvate fra un avvio e l'altro."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .osutil import app_dir

SCALE_AMMESSE = (1.0, 1.25, 1.5)
SCALA_PREDEFINITA = 1.25  # gli anziani sono il pubblico principale: si parte già «grande»


def scala_vicina(valore: object) -> float:
    """Riporta un valore qualunque alla scala ammessa più vicina (o al predefinito)."""
    if isinstance(valore, bool) or not isinstance(valore, (int, float)):
        return SCALA_PREDEFINITA
    return min(SCALE_AMMESSE, key=lambda ammessa: abs(ammessa - float(valore)))


def percorso_impostazioni() -> Path:
    return app_dir() / "impostazioni.json"


@dataclass
class Impostazioni:
    scala_testo: float = SCALA_PREDEFINITA

    @classmethod
    def carica(cls, percorso: Path | None = None) -> "Impostazioni":
        """Legge le impostazioni; qualunque problema porta ai valori predefiniti."""
        destinazione = Path(percorso) if percorso is not None else percorso_impostazioni()
        try:
            contenuto = json.loads(destinazione.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        if not isinstance(contenuto, dict):
            return cls()
        return cls(scala_testo=scala_vicina(contenuto.get("scala_testo")))

    def salva(self, percorso: Path | None = None) -> None:
        """Scrive le impostazioni; se non si può, pazienza (non è mai un errore per l'utente)."""
        destinazione = Path(percorso) if percorso is not None else percorso_impostazioni()
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
            destinazione.write_text(json.dumps({"scala_testo": self.scala_testo}), encoding="utf-8")
        except OSError:
            pass
```

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_impostazioni.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/impostazioni.py tests/test_impostazioni.py
git commit -m "feat: impostazioni personali (dimensione del testo)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C2: Tema con scala del testo, font più grandi e focus visibile

**Files:**
- Modify: `fotofacile/ui/theme.py`
- Test: `tests/test_theme.py`

**Interfaces:**
- Produces: `imposta_scala(valore: float) -> None`, `scala_attuale() -> float`; `font(size, bold)` **moltiplica** per la scala (arrotonda); `apply_theme(root, available_families=None, scuro=None, scala=None)`; nuovi stili `Passo.TLabel`, `Grande.TCheckbutton`, `Link.TButton`.

- [ ] **Step 1: Test che falliscono** (in coda a `tests/test_theme.py`)

```python
def test_la_scala_ingrandisce_i_font():
    from fotofacile.ui import theme

    try:
        theme.imposta_scala(1.0)
        base = theme.font(14)[1]
        theme.imposta_scala(1.5)
        assert theme.font(14)[1] == round(base * 1.5)
        assert theme.scala_attuale() == 1.5
    finally:
        theme.imposta_scala(1.0)


def test_scala_fuori_dai_limiti_viene_riportata():
    from fotofacile.ui import theme

    try:
        theme.imposta_scala(9)
        assert theme.scala_attuale() == 1.5
        theme.imposta_scala(0.1)
        assert theme.scala_attuale() == 1.0
    finally:
        theme.imposta_scala(1.0)


def test_nessun_testo_sotto_14_punti_a_scala_normale():
    from fotofacile.ui import theme

    theme.imposta_scala(1.0)
    for usato in (theme.font(14), theme.font(14, bold=True), theme.font(28, bold=True)):
        assert usato[1] >= 14
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_theme.py -k "scala or 14" -v` — Expected: FAIL (`AttributeError: imposta_scala`).

- [ ] **Step 3: Implementare** — in `theme.py`:

Importare `from ..core.impostazioni import SCALE_AMMESSE, scala_vicina` e aggiungere, sotto `_SCURO = False`:

```python
_SCALA = 1.0


def imposta_scala(valore: float) -> None:
    """Sceglie la dimensione del testo (1.0 normale, 1.25 grande, 1.5 molto grande)."""
    global _SCALA
    _SCALA = min(max(float(valore), SCALE_AMMESSE[0]), SCALE_AMMESSE[-1])


def scala_attuale() -> float:
    return _SCALA
```

Sostituire `font`:

```python
def font(size: int = 14, bold: bool = False) -> tuple:
    """Tupla (famiglia, dimensione[, stile]): la dimensione segue la scala scelta dall'utente."""
    punti = max(1, round(size * _SCALA))
    return (_FAMIGLIA, punti, "bold") if bold else (_FAMIGLIA, punti)
```

In `apply_theme`, aggiungere il parametro `scala: float | None = None`; subito dopo `_SCURO = modalita`: `if scala is not None: imposta_scala(scala)`. Poi ritoccare gli stili:

```python
    stile.configure(".", background=COLORI["sfondo"], foreground=COLORI["testo"], font=font(14))
    stile.configure("Titolo.TLabel", font=font(28, bold=True), background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.configure("Sottotitolo.TLabel", font=font(16), background=COLORI["sfondo"], foreground=COLORI["tenue"])
    stile.configure("Passo.TLabel", font=font(14), background=COLORI["sfondo"], foreground=COLORI["tenue"])
    stile.configure("Successo.TLabel", background=COLORI["sfondo"], foreground=COLORI["successo"], font=font(16, bold=True))
    stile.configure(
        "Big.TButton",
        font=font(18, bold=True),
        padding=(round(28 * _SCALA), round(16 * _SCALA)),
        background=COLORI["primario"],
        foreground=COLORI["pannello"] if not modalita else COLORI["sfondo"],
    )
    stile.configure("Secondary.TButton", font=font(14), padding=(round(16 * _SCALA), round(10 * _SCALA)))
    stile.configure("Link.TButton", font=font(13), padding=(6, 4), background=COLORI["sfondo"], foreground=COLORI["primario"], borderwidth=0)
    stile.map("Link.TButton", foreground=[("active", COLORI["primario_attivo"])], background=[("active", COLORI["sfondo"])])
    stile.configure("TCheckbutton", background=COLORI["sfondo"], foreground=COLORI["testo"], font=font(15), padding=(4, 6))
    # anello di messa a fuoco ben visibile per chi usa la tastiera
    for nome in ("Big.TButton", "Secondary.TButton", "Link.TButton", "TCheckbutton"):
        stile.map(nome, focuscolor=[("focus", COLORI["primario"])])
```
(Sono le stesse `stile.configure` già presenti con valori aggiornati: **sostituire** le righe omonime, non duplicarle. `Tenue`, `Avviso`, `Errore`, `TEntry`, `TCombobox` restano ma con `font=font(14)` dove non specificato.)

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_theme.py -v && .venv/bin/python -m pytest tests -x 2>&1 | tail -3` — Expected: PASS. Se un test esistente confrontava una dimensione di font esatta (per esempio `font(12) == (fam, 12)`), aggiornarlo al nuovo default 14: la richiesta è proprio ingrandire.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/theme.py tests/test_theme.py
git commit -m "feat(ui): tema con scala del testo, font più grandi e focus visibile

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C3: Componenti nuovi: testo che si adatta, avvisi con simbolo, indicatore «Passo N di 4»

**Files:**
- Modify: `fotofacile/ui/widgets.py`
- Test: `tests/test_widgets.py`

**Interfaces:**
- Produces:
  - `class TestoAdattivo(ttk.Label)` — `wraplength` segue la larghezza reale della cella.
  - `Banner.SIMBOLI = {"info": "ℹ", "successo": "✔", "avviso": "⚠", "errore": "✖"}`; `Banner.show(message, hint="", kind="info")` **invariato nella firma**; `message_text` resta il testo **senza** simbolo (i test lo confrontano).
  - `StepIndicator` con etichetta aggiuntiva `riga_passo` («Passo 2 di 4»); `set_step`, `current`, `_etichette` **invariati**.
  - `PathChooser` invariato nella firma; il pulsante diventa «Cambia cartella…».

- [ ] **Step 1: Test che falliscono** (in coda a `tests/test_widgets.py`)

```python
def test_banner_mette_un_simbolo_oltre_al_colore(root):
    from fotofacile.ui.widgets import Banner

    banner = Banner(root)
    banner.show("Tutto bene.", kind="successo")
    assert banner._messaggio.cget("text").startswith("✔")
    assert banner.message_text == "Tutto bene."  # il testo «pulito» non cambia
    banner.show("Attenzione.", kind="avviso")
    assert banner._messaggio.cget("text").startswith("⚠")
    banner.show("Errore.", kind="errore")
    assert banner._messaggio.cget("text").startswith("✖")


def test_step_indicator_dice_a_che_punto_si_e(root):
    from fotofacile.ui.widgets import StepIndicator

    indicatore = StepIndicator(root, ("Uno", "Due", "Tre", "Quattro"))
    indicatore.set_step(1)
    assert indicatore.riga_passo.cget("text") == "Passo 2 di 4: Due"


def test_testo_adattivo_segue_la_larghezza(root):
    from tkinter import ttk

    from fotofacile.ui.widgets import TestoAdattivo

    root.geometry("500x200")
    contenitore = ttk.Frame(root)
    contenitore.pack(fill="both", expand=True)
    contenitore.columnconfigure(0, weight=1)
    etichetta = TestoAdattivo(contenitore, text="parola " * 60)
    etichetta.grid(row=0, column=0, sticky="ew")
    root.update()
    largo = int(str(etichetta.cget("wraplength")))
    root.geometry("900x200")
    root.update()
    assert int(str(etichetta.cget("wraplength"))) > largo > 0
```
(la fixture `root` è un `Toplevel` nascosto: se `geometry` non ridimensiona in un Toplevel `withdraw`n, usare `root.deiconify()` all'inizio del test e `root.withdraw()` alla fine.)

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_widgets.py -k "simbolo or passo or adattivo" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — in `widgets.py`:

```python
class TestoAdattivo(ttk.Label):
    """Etichetta a più righe il cui testo va a capo in base allo spazio davvero disponibile.

    I testi con ``wraplength`` fisso (860 pixel) uscivano dalla finestra quando la si
    restringeva o si ingrandiva il testo. Va messa in una cella con ``sticky="ew"`` e colonna
    con ``weight=1``.
    """

    MARGINE = 8

    def __init__(self, parent: tk.Misc, **opzioni) -> None:
        opzioni.setdefault("justify", "left")
        super().__init__(parent, **opzioni)
        self.bind("<Configure>", self._adatta)

    def _adatta(self, evento: tk.Event) -> None:
        nuovo = max(200, evento.width - self.MARGINE)
        if int(str(self.cget("wraplength")) or 0) != nuovo:
            self.configure(wraplength=nuovo)
```

`Banner`: usare `TestoAdattivo` al posto dei due `ttk.Label` con `wraplength=860`, aggiungere la costante e usarla in `show`:

```python
    SIMBOLI = {"info": "ℹ", "successo": "✔", "avviso": "⚠", "errore": "✖"}
    ...
        simbolo = self.SIMBOLI.get(kind, "ℹ")
        self._messaggio.configure(text=f"{simbolo}  {message}", foreground=colore)
```
(`font(15, bold=True)` → `font(18, bold=True)`; suggerimento `font(14)`; `sticky="ew"` per entrambe.)

`StepIndicator`: aggiungere in `__init__`, sopra alle etichette (spostare queste alla `row=1`):

```python
        self.riga_passo = ttk.Label(self, text="", style="Passo.TLabel")
        self.riga_passo.grid(row=0, column=0, columnspan=len(self.steps) + 1, sticky="w", pady=(0, 4))
```
e in `set_step` (dopo aver fissato `self.current`):

```python
        self.riga_passo.configure(
            text=f"Passo {self.current + 1} di {len(self.steps)}: {self.steps[self.current]}"
        )
```
i font delle etichette diventano `font(14, bold=True)` per il passo attuale, `font(14)` per gli altri.

`LogPane`: `font(11)` → `font(13)`. `PathChooser`: pulsante `text="Cambia cartella…"`, `font(14)` sul campo, e in `browse` aggiungere `parent=self.winfo_toplevel()` a `askdirectory`.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_widgets.py tests/test_page_connect.py tests/test_ui_app.py -v` — Expected: PASS (correggere solo eventuali confronti su testi del banner che ora hanno il simbolo: vanno fatti su `message_text`).

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/widgets.py tests/test_widgets.py
git commit -m "feat(ui): testo che si adatta, avvisi con simbolo, indicatore «Passo N di 4»

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C4: Nomi comprensibili per le cartelle e filtro sticker/miniature

**Files:**
- Create: `fotofacile/core/nomi_cartelle.py`
- Modify: `fotofacile/core/scanner.py` (`MediaFolder.label` usa il nome comprensibile)
- Test: `tests/test_nomi_cartelle.py`, `tests/test_scanner.py`

**Interfaces:**
- Produces: `nome_amichevole(percorso_remoto: str) -> str`; `e_rumore(percorso_remoto: str) -> bool` (miniature, cache, sticker).

- [ ] **Step 1: Test che fallisce** — `tests/test_nomi_cartelle.py`:

```python
import pytest

from fotofacile.core.nomi_cartelle import e_rumore, nome_amichevole


@pytest.mark.parametrize(
    "percorso, atteso",
    [
        ("/sdcard/DCIM/Camera", "Foto e video scattati con il telefono"),
        ("/storage/emulated/0/DCIM/Camera", "Foto e video scattati con il telefono"),
        ("/sdcard/DCIM/Screenshots", "Schermate salvate"),
        ("/sdcard/Pictures/Screenshots", "Schermate salvate"),
        ("/sdcard/Pictures/WhatsApp Images", "Foto ricevute su WhatsApp"),
        ("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images", "Foto ricevute su WhatsApp"),
        ("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video", "Video ricevuti su WhatsApp"),
        ("/sdcard/Download", "Scaricati da internet"),
        ("/sdcard/Movies", "Video"),
        ("/sdcard/Pictures/Vacanze 2024", "Vacanze 2024"),
    ],
)
def test_nomi_amichevoli(percorso, atteso):
    assert nome_amichevole(percorso) == atteso


def test_percorso_sconosciuto_usa_l_ultima_cartella():
    assert nome_amichevole("/sdcard/Boh/Cose Mie") == "Cose Mie"
    assert nome_amichevole("/") == "Memoria del telefono"


@pytest.mark.parametrize(
    "percorso",
    [
        "/sdcard/DCIM/.thumbnails",
        "/sdcard/Pictures/.cache",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Stickers",
        "/sdcard/Telegram/Telegram Stickers",
        "/sdcard/Android/data/com.app/cache/images",
    ],
)
def test_rumore_riconosciuto(percorso):
    assert e_rumore(percorso) is True


@pytest.mark.parametrize(
    "percorso",
    ["/sdcard/DCIM/Camera", "/sdcard/Pictures/WhatsApp Images", "/sdcard/Download", "/sdcard/Pictures/Cache di famiglia"],
)
def test_le_cartelle_normali_non_sono_rumore(percorso):
    assert e_rumore(percorso) is False
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_nomi_cartelle.py -v` — Expected: FAIL (`ModuleNotFoundError`).

- [ ] **Step 3: Implementare** — `fotofacile/core/nomi_cartelle.py`:

```python
"""Nomi comprensibili per le cartelle del telefono e riconoscimento di sticker e miniature."""

from __future__ import annotations

# (frammento del percorso in minuscolo, nome da mostrare): vince il **primo** che combacia.
_NOMI = (
    ("whatsapp stickers", "Sticker di WhatsApp"),
    ("whatsapp images", "Foto ricevute su WhatsApp"),
    ("whatsapp video", "Video ricevuti su WhatsApp"),
    ("whatsapp animated gifs", "Animazioni ricevute su WhatsApp"),
    ("dcim/camera", "Foto e video scattati con il telefono"),
    ("screenshots", "Schermate salvate"),
    ("/download", "Scaricati da internet"),
    ("/movies", "Video"),
)

_SEGMENTI_RUMORE = frozenset(
    {".thumbnails", "thumbnails", ".cache", "cache", "whatsapp stickers", "telegram stickers", "stickers"}
)

_PREFISSI = ("/storage/emulated/0/", "/storage/self/primary/", "/sdcard/")


def _minuscolo(percorso: str) -> str:
    return percorso.lower().rstrip("/")


def nome_amichevole(percorso_remoto: str) -> str:
    """Il nome da mostrare a una persona: «Foto ricevute su WhatsApp», non un percorso."""
    minuscolo = _minuscolo(percorso_remoto)
    for frammento, nome in _NOMI:
        if minuscolo.endswith(frammento) or (frammento + "/") in (minuscolo + "/"):
            if frammento.startswith("/") and not minuscolo.endswith(frammento):
                continue
            return nome
    pulito = percorso_remoto.rstrip("/")
    for prefisso in _PREFISSI:
        if pulito.startswith(prefisso):
            pulito = pulito[len(prefisso):]
            break
    return pulito.rsplit("/", 1)[-1] or "Memoria del telefono"


def e_rumore(percorso_remoto: str) -> bool:
    """True per cartelle che quasi nessuno vuole: miniature, cache, sticker."""
    return any(parte in _SEGMENTI_RUMORE for parte in _minuscolo(percorso_remoto).split("/"))
```

In `core/scanner.py`, `_label` non cambia (resta il percorso «tecnico» usato dai test e dal resoconto); la pagina usa `nome_amichevole` per **mostrare** (Task C7). Aggiungere a `MediaFolder` una proprietà:

```python
    @property
    def nome(self) -> str:
        """Nome comprensibile per la grafica (l'etichetta tecnica resta in ``label``)."""
        from .nomi_cartelle import nome_amichevole

        return nome_amichevole(self.remote_path)
```

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_nomi_cartelle.py tests/test_scanner.py -v` — Expected: PASS. Il test `("/download")` non deve confondersi con `/sdcard/Pictures/Cache di famiglia` (nome con «cache» dentro una frase): il confronto per segmento intero lo garantisce.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/core/nomi_cartelle.py fotofacile/core/scanner.py tests/test_nomi_cartelle.py
git commit -m "feat: nomi comprensibili per le cartelle e riconoscimento di sticker/miniature

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C5: Cornice dell'app: dimensione del testo, tastiera, dettagli nascosti

**Files:**
- Modify: `fotofacile/ui/app.py`
- Test: `tests/test_ui_app.py`

**Interfaces:**
- Consumes: `Impostazioni`, `SCALE_AMMESSE` (C1); `imposta_scala`, `apply_theme(scala=)` (C2).
- Produces:
  - `App.__init__(..., scuro: bool | None = None, scala: float | None = None)` (i parametri servono a test e a `scripts/scatti_interfaccia.py`).
  - `App.cambia_scala(direzione: int) -> bool` (`+1`/`-1`; `False` se già al limite); salva l'impostazione e ricostruisce le pagine.
  - Ogni pagina può definire `azione_principale()` e `azione_indietro()`; `Invio`/`Esc` li chiamano.
  - `App.mostra_dettagli(mostra: bool)`, `App.dettagli_visibili: bool` (chiusi di default; `log()` **non** li apre più da solo).

- [ ] **Step 1: Test che falliscono** (in `tests/test_ui_app.py`)

```python
def test_i_dettagli_restano_chiusi_finche_l_utente_non_li_apre(app):
    app.log("riga tecnica")
    assert app.dettagli_visibili is False
    assert "riga tecnica" in app.log_pane.get_text()  # il registro si riempie comunque
    app.mostra_dettagli(True)
    assert app.dettagli_visibili is True
    app.mostra_dettagli(False)
    assert app.dettagli_visibili is False


def test_cambia_scala_ingrandisce_salva_e_rispetta_i_limiti(app, casa_temporanea):
    from fotofacile.core.impostazioni import Impostazioni
    from fotofacile.ui import theme

    try:
        app.cambia_scala(-1)
        app.cambia_scala(-1)
        app.cambia_scala(-1)
        assert theme.scala_attuale() == 1.0
        assert app.cambia_scala(-1) is False  # già al minimo
        assert app.cambia_scala(+1) is True
        assert theme.scala_attuale() == 1.25
        assert Impostazioni.carica().scala_testo == 1.25  # è stato salvato
    finally:
        theme.imposta_scala(1.0)


def test_invio_preme_il_pulsante_principale_della_pagina(app):
    chiamate = []
    app.pages["connect"].azione_principale = lambda: chiamate.append("avanti")
    app.go_to("connect")
    app.event_generate("<Return>")
    app.update()
    assert chiamate == ["avanti"]


def test_esc_torna_indietro(app):
    from fotofacile.core.devices import DeviceInfo

    app.device = DeviceInfo(serial="S1", state="device", model="Prova", product="")
    app.go_to("options")
    app.event_generate("<Escape>")
    app.update()
    assert app.current_page == "select"
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_ui_app.py -k "dettagli or scala or invio or esc" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — in `ui/app.py`:

1. Importi: `from ..core.impostazioni import SCALE_AMMESSE, Impostazioni`; `from .theme import apply_theme, imposta_scala, scala_attuale`.

2. Firma: `def __init__(self, backend=None, demo_mode=False, adb_path=None, scuro=None, scala=None)`. All'inizio, dopo `super().__init__()`:

```python
        self._scala_iniziale = scala if scala is not None else Impostazioni.carica().scala_testo
        self.title("FotoFacile — copia le foto dal telefono al computer")
        self._dimensiona_finestra()
        apply_theme(self, scuro=scuro, scala=self._scala_iniziale)
```
(togliere le vecchie righe `self.geometry("1020x780")`, `self.minsize(920, 700)`, `apply_theme(self)`.)

```python
    def _dimensiona_finestra(self) -> None:
        """Dimensione iniziale proporzionata al testo, ma mai più grande dello schermo."""
        scala = scala_attuale() if hasattr(self, "_scala_iniziale") else 1.0
        larghezza = min(int(1000 * max(scala, 1.0)), self.winfo_screenwidth() - 60)
        altezza = min(int(760 * max(scala, 1.0)), self.winfo_screenheight() - 100)
        self.geometry(f"{larghezza}x{altezza}")
        self.minsize(min(820, larghezza), min(620, altezza))
```
(chiamarla **dopo** `apply_theme` con la scala già impostata: spostare la chiamata dopo `apply_theme`.)

3. Dettagli chiusi con un link:

```python
        self.area_dettagli = ttk.Frame(self)
        self.area_dettagli.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 14))
        self.bottone_dettagli = ttk.Button(
            self.area_dettagli, text="Mostra i dettagli", style="Link.TButton",
            command=lambda: self.mostra_dettagli(not self.dettagli_visibili),
        )
        self.bottone_dettagli.grid(row=0, column=0, sticky="w")
        self.log_pane = LogPane(self.area_dettagli, height=6)
        self.log_pane.grid(row=1, column=0, sticky="ew")
        self.log_pane.grid_remove()
        self.dettagli_visibili = False
        self.area_dettagli.columnconfigure(0, weight=1)
```
(niente `self.area_dettagli.grid_remove()` finale: l'area con il solo link resta sempre visibile e piccola; **`tests/conftest.py:azzera` va aggiornato**: al posto di `applicazione.area_dettagli.grid_remove()` usare `applicazione.mostra_dettagli(False)`.)

```python
    def mostra_dettagli(self, mostra: bool) -> None:
        self.dettagli_visibili = bool(mostra)
        if mostra:
            self.log_pane.grid()
            self.bottone_dettagli.configure(text="Nascondi i dettagli")
        else:
            self.log_pane.grid_remove()
            self.bottone_dettagli.configure(text="Mostra i dettagli")
```
`log()` diventa solo `self.log_pane.append(testo)`.

4. Scala e tastiera:

```python
    def cambia_scala(self, direzione: int) -> bool:
        """Ingrandisce (+1) o rimpicciolisce (-1) il testo; salva la scelta e ridisegna."""
        indice = min(range(len(SCALE_AMMESSE)), key=lambda i: abs(SCALE_AMMESSE[i] - scala_attuale()))
        nuovo = indice + (1 if direzione > 0 else -1)
        if not 0 <= nuovo < len(SCALE_AMMESSE):
            return False
        imposta_scala(SCALE_AMMESSE[nuovo])
        Impostazioni(scala_testo=SCALE_AMMESSE[nuovo]).salva()
        apply_theme(self, scala=SCALE_AMMESSE[nuovo])
        self._dimensiona_finestra()
        self.ricostruisci_pagine()
        return True

    def _tasto_invio(self, _evento=None) -> None:
        self._chiama_azione("azione_principale")

    def _tasto_esc(self, _evento=None) -> None:
        self._chiama_azione("azione_indietro")

    def _chiama_azione(self, nome: str) -> None:
        azione = getattr(self.pages.get(self.current_page), nome, None)
        if callable(azione):
            azione()
```
In `__init__`, dopo la costruzione delle pagine: `self.bind("<Return>", self._tasto_invio)`, `self.bind("<Escape>", self._tasto_esc)`.

`ricostruisci_pagine` deve funzionare a metà uso: (ricrea da zero, ok; il pulsante di cambio testo compare solo nel passo 1, vedi C6). Le pagine `select`, `options` e `transfer` definiranno `azione_principale`/`azione_indietro` nei task C7–C9; la pagina `connect` in C6.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests -x 2>&1 | tail -3` — Expected: verde. (Il test `test_esc_torna_indietro` richiede `azione_indietro` su `options`: se il Task C8 non è ancora fatto, **rimandare** quel singolo test al Task C8 e marcarlo `xfail` qui con motivo esplicito, poi toglierlo lì.)

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/app.py tests
git commit -m "feat(ui): dimensione del testo scelta dall'utente, tasti Invio/Esc, dettagli nascosti

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C6: Passo 1 «Collega il telefono» — tre gesti chiari e aiuto al momento giusto

**Files:**
- Modify: `fotofacile/ui/page_connect.py`
- Test: `tests/test_page_connect.py`

**Interfaces:**
- Consumes: `TestoAdattivo` (C3), `App.cambia_scala` (C5).
- Produces: `ConnectPage.azione_principale()` (= `_avanti`), `ConnectPage.SOGLIA_AIUTO = 3`, `ConnectPage._senza_telefono: int`, `ConnectPage.bottone_testo_piu`, `.bottone_testo_meno`.

- [ ] **Step 1: Test che falliscono**

```python
def test_le_tre_istruzioni_sono_sempre_visibili(app):
    pagina = app.pages["connect"]
    testo = " ".join(str(w.cget("text")) for w in pagina.winfo_children() if hasattr(w, "cget") and "text" in w.keys())
    assert "cavo USB" in testo and "sblocca" in testo.lower() and "Trasferimento file" in testo


def test_l_aiuto_grande_compare_solo_dopo_qualche_tentativo(app):
    pagina = app.pages["connect"]
    assert pagina._senza_telefono == 0
    for _ in range(pagina.SOGLIA_AIUTO - 1):
        pagina._dispositivi_ricevuti([])
    assert not pagina.aiuto_evidente.winfo_ismapped() and not pagina.aiuto_evidente.grid_info()
    pagina._dispositivi_ricevuti([])
    assert pagina.aiuto_evidente.grid_info()  # ora è visibile


def test_trovato_il_telefono_l_aiuto_sparisce(app):
    from fotofacile.core.devices import DeviceInfo

    pagina = app.pages["connect"]
    for _ in range(pagina.SOGLIA_AIUTO):
        pagina._dispositivi_ricevuti([])
    pagina._dispositivi_ricevuti([DeviceInfo(serial="S1", state="device", model="Pixel", product="")])
    assert pagina._senza_telefono == 0
    assert not pagina.aiuto_evidente.grid_info()


def test_i_pulsanti_del_testo_cambiano_la_scala(app, monkeypatch):
    chiamate = []
    monkeypatch.setattr(app, "cambia_scala", lambda d: chiamate.append(d) or True)
    pagina = app.pages["connect"]
    pagina.bottone_testo_piu.invoke()
    pagina.bottone_testo_meno.invoke()
    assert chiamate == [1, -1]


def test_invio_su_questo_passo_va_avanti_solo_col_telefono_pronto(app):
    pagina = app.pages["connect"]
    app.device = None
    pagina.azione_principale()
    assert app.current_page == "connect"
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_connect.py -k "istruzioni or aiuto or pulsanti_del_testo or invio" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — riscrivere `__init__` di `ConnectPage` (le **funzioni** di sondaggio, `_controllo_fallito`, `install_component` ecc. **restano identiche**; cambia solo la parte costruttiva). Disposizione, dall'alto:

```python
        self.SOGLIA_AIUTO = 3  # controlli consecutivi senza telefono prima di mostrare l'aiuto grande
        self._senza_telefono = 0

        ttk.Label(self, text="Collega il telefono al computer", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 8)
        )
        passi = ttk.Frame(self)
        passi.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        passi.columnconfigure(0, weight=1)
        for indice, testo in enumerate(
            (
                "Collega il telefono al computer con il cavo USB.",
                "Accendi e sblocca lo schermo del telefono.",
                "Se il telefono lo chiede, tocca «Consenti» e scegli «Trasferimento file».",
            )
        ):
            TestoAdattivo(passi, text=f"{indice + 1}.  {testo}", font=font(17)).grid(
                row=indice, column=0, sticky="ew", pady=4
            )

        self.indicatore = TestoAdattivo(self, text="", font=font(20, bold=True))
        self.indicatore.grid(row=2, column=0, sticky="ew", pady=(10, 2))
        self.dettaglio = TestoAdattivo(self, text="", style="Tenue.TLabel", font=font(15))
        self.dettaglio.grid(row=3, column=0, sticky="ew")

        # Compare solo dopo qualche controllo a vuoto: prima sarebbe rumore.
        self.aiuto_evidente = ttk.Button(
            self, text="Il telefono non viene riconosciuto? Ti aiuto io", style="Big.TButton", command=self.show_help
        )
        self.aiuto_evidente.grid(row=4, column=0, sticky="w", pady=(14, 0))
        self.aiuto_evidente.grid_remove()

        navigazione = ttk.Frame(self)
        navigazione.grid(row=5, column=0, sticky="ew", pady=(18, 0))
        self.bottone_avanti = ttk.Button(navigazione, text="Avanti  →", style="Big.TButton", command=self._avanti)
        self.bottone_avanti.grid(row=0, column=1, sticky="e")
        navigazione.columnconfigure(1, weight=1)

        # ─ cose secondarie, piccole e in fondo ─
        altro = ttk.Frame(self)
        altro.grid(row=6, column=0, sticky="ew", pady=(26, 0))
        self.bottone_aiuto = ttk.Button(altro, text="Serve aiuto?", style="Link.TButton", command=self.show_help)
        self.bottone_aiuto.grid(row=0, column=0, padx=(0, 10))
        self.bottone_ricarica = ttk.Button(altro, text="Riprova", style="Link.TButton", command=self.restart_connection)
        self.bottone_ricarica.grid(row=0, column=1, padx=10)
        self.bottone_installa = ttk.Button(altro, text="Installa componente mancante", style="Link.TButton", command=self.install_component)
        self.bottone_installa.grid(row=0, column=2, padx=10)
        ttk.Button(altro, text="Prova senza telefono", style="Link.TButton", command=self.enable_demo).grid(row=0, column=3, padx=10)
        ttk.Label(altro, text="Testo:", style="Tenue.TLabel").grid(row=0, column=4, padx=(30, 4))
        self.bottone_testo_meno = ttk.Button(altro, text="A−", style="Secondary.TButton", width=3, command=lambda: self.app.cambia_scala(-1))
        self.bottone_testo_meno.grid(row=0, column=5)
        self.bottone_testo_piu = ttk.Button(altro, text="A+", style="Secondary.TButton", width=3, command=lambda: self.app.cambia_scala(1))
        self.bottone_testo_piu.grid(row=0, column=6, padx=(4, 0))

        self.columnconfigure(0, weight=1)
```
(importare `TestoAdattivo` da `.widgets`; togliere l'etichetta lunga della modalità demo.)

Logica:

```python
    def azione_principale(self) -> None:
        self._avanti()
```
In `_dispositivi_ricevuti`: nel ramo `pronto is not None` azzerare `self._senza_telefono = 0; self.aiuto_evidente.grid_remove()`; nei rami «nessun telefono» o «telefono non pronto» incrementare il contatore e, se `>= SOGLIA_AIUTO`, `self.aiuto_evidente.grid()`. In `_controllo_fallito` idem (l'errore conta come «senza telefono»).

`set_message`: usare `tono` per il colore **e** un simbolo davanti (✔ successo, ⚠ avviso) come in `Banner.SIMBOLI`.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_page_connect.py tests/test_ui_app.py -v` — Expected: PASS. Aggiornare i vecchi test che cercavano i testi cambiati («Il telefono non viene riconosciuto?» → «Serve aiuto?»/«Ti aiuto io», «Riprova il collegamento» → «Riprova») **cercando con** `/usr/bin/grep -rn "non viene riconosciuto\|Riprova il collegamento" tests`. Aggiornare `azzera()` di `conftest.py` se usa attributi rimossi (`pagina.bottone_avanti` resta).

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/page_connect.py tests
git commit -m "feat(ui): passo 1 con tre gesti chiari, aiuto al momento giusto e testo regolabile

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C7: Passo 2 «Scegli le foto» — cartelle con nomi veri, un solo menu per il periodo

**Files:**
- Modify: `fotofacile/ui/page_select.py`
- Test: `tests/test_page_select.py`

**Interfaces:**
- Consumes: `MediaFolder.nome`, `e_rumore` (C4); `TestoAdattivo` (C3).
- Produces:
  - `PERIODI: tuple[tuple[str, int | None], ...]` = `(("Tutte le foto", None), ("Dell'ultimo mese", 30), ("Degli ultimi 3 mesi", 90), ("Dell'ultimo anno", 365))` (giorni).
  - `SelectPage.periodo: tk.StringVar` (nome scelto nel menu), `SelectPage.mostra_rumore: tk.BooleanVar` (default `False`), `SelectPage.data_minima` **resta** come `tk.StringVar` calcolata (`AAAA-MM-GG` o vuota) così `selected_files()` e `conftest.azzera()` non cambiano.
  - `SelectPage.seleziona_tutto(valore: bool)`, `SelectPage.azione_principale()`, `SelectPage.azione_indietro()`.

- [ ] **Step 1: Test che falliscono**

```python
def _con_file(app, file):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.core.scanner import group_folders

    app.device = DeviceInfo(serial="S1", state="device", model="Prova", product="")
    pagina = app.pages["select"]
    pagina._files = list(file)
    pagina._folders = group_folders(pagina._files)
    pagina.rebuild_list(pagina._folders)
    return pagina


def _f(percorso, size=1000, mtime=1_700_000_000):
    from fotofacile.core.scanner import MediaFile

    return MediaFile(percorso, size=size, mtime=mtime, kind="photo")


def test_le_cartelle_mostrano_il_nome_comprensibile(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg"), _f("/sdcard/Pictures/WhatsApp Images/b.jpg")])
    testi = [str(w.cget("text")) for w in pagina.lista.winfo_children()]
    assert any("Foto e video scattati con il telefono" in t for t in testi)
    assert any("Foto ricevute su WhatsApp" in t for t in testi)
    assert not any("/sdcard" in t for t in testi)  # niente percorsi tecnici


def test_sticker_e_miniature_sono_nascosti_di_default(app):
    pagina = _con_file(
        app,
        [
            _f("/sdcard/DCIM/Camera/a.jpg"),
            _f("/sdcard/DCIM/.thumbnails/t.jpg"),
            _f("/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Stickers/s.webp"),
        ],
    )
    assert [f.name for f in pagina.selected_files()] == ["a.jpg"]
    pagina.mostra_rumore.set(True)
    pagina._ridisegna()
    assert sorted(f.name for f in pagina.selected_files()) == ["a.jpg", "s.webp", "t.jpg"]


def test_seleziona_tutto_e_nessuna(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg"), _f("/sdcard/Download/b.jpg")])
    pagina.seleziona_tutto(False)
    assert pagina.selected_files() == []
    assert str(pagina.bottone_avanti.state()) .find("disabled") != -1
    pagina.seleziona_tutto(True)
    assert len(pagina.selected_files()) == 2


def test_il_periodo_sostituisce_la_data_scritta_a_mano(app, monkeypatch):
    import time

    from fotofacile.ui import page_select

    adesso = 1_700_000_000
    monkeypatch.setattr(page_select.time, "time", lambda: adesso)
    vecchia = _f("/sdcard/DCIM/Camera/vecchia.jpg", mtime=adesso - 200 * 86400)
    recente = _f("/sdcard/DCIM/Camera/recente.jpg", mtime=adesso - 5 * 86400)
    pagina = _con_file(app, [vecchia, recente])
    assert len(pagina.selected_files()) == 2
    pagina.periodo.set("Dell'ultimo mese")
    pagina._periodo_cambiato()
    assert [f.name for f in pagina.selected_files()] == ["recente.jpg"]
    pagina.periodo.set("Tutte le foto")
    pagina._periodo_cambiato()
    assert len(pagina.selected_files()) == 2


def test_invio_e_esc_su_questo_passo(app):
    pagina = _con_file(app, [_f("/sdcard/DCIM/Camera/a.jpg")])
    app.go_to("select")
    pagina.azione_indietro()
    assert app.current_page == "connect"
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_select.py -k "nome_comprensibile or sticker or seleziona_tutto or periodo or esc" -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — in `page_select.py`:

Importi: `import time`, `from datetime import datetime`, `from ..core.nomi_cartelle import e_rumore`, `from .widgets import TestoAdattivo`.

Costante e variabili:

```python
PERIODI = (
    ("Tutte le foto", None),
    ("Dell'ultimo mese", 30),
    ("Degli ultimi 3 mesi", 90),
    ("Dell'ultimo anno", 365),
)
```
nel costruttore: `self.periodo = tk.StringVar(value=PERIODI[0][0])`, `self.mostra_rumore = tk.BooleanVar(value=False)`; il campo `Entry` della data **sparisce** e al suo posto:

```python
        ttk.Label(opzioni, text="Quali foto vuoi?").grid(row=0, column=1, padx=(24, 8))
        menu = ttk.Combobox(opzioni, textvariable=self.periodo, values=[nome for nome, _ in PERIODI],
                            state="readonly", width=22, font=font(14))
        menu.grid(row=0, column=2)
        menu.bind("<<ComboboxSelected>>", lambda _e: self._periodo_cambiato())
```
Sotto: due pulsanti `Seleziona tutte` / `Toglie la selezione` (`style="Secondary.TButton"`, comando `lambda: self.seleziona_tutto(True/False)`) sopra alla lista, e la casella `Mostra anche miniature e sticker` (`variable=self.mostra_rumore`, `command=self._ridisegna`) in fondo alle opzioni.

Logica:

```python
    def _periodo_cambiato(self) -> None:
        giorni = dict(PERIODI).get(self.periodo.get())
        if giorni is None:
            self.data_minima.set("")
        else:
            self.data_minima.set(datetime.fromtimestamp(time.time() - giorni * 86400).strftime("%Y-%m-%d"))
        self._aggiorna_totale()

    def _cartelle_visibili(self):
        if self.mostra_rumore.get():
            return list(self._folders)
        return [c for c in self._folders if not e_rumore(c.remote_path)]

    def _ridisegna(self) -> None:
        self.rebuild_list(self._cartelle_visibili())

    def seleziona_tutto(self, valore: bool) -> None:
        for variabile in self.folder_vars.values():
            variabile.set(valore)
        self._aggiorna_totale()

    def azione_principale(self) -> None:
        self.go_next()

    def azione_indietro(self) -> None:
        self.app.go_to("prev")
```
`_scansione_finita`: costruire l'elenco con `self.rebuild_list(self._cartelle_visibili())`. `rebuild_list`: testo della casella = `f"{cartella.nome}  —  {cartella.file_count} file, {format_size(cartella.total_size)}"`, `variabile` **creata con `value=True`**; `selected_labels()` continua a restituire solo cartelle **visibili e spuntate**, quindi i file di cartelle nascoste non entrano (è il comportamento voluto: il test `sticker_e_miniature` lo verifica).

Tasto rotellina sul `Canvas` (chi ha il mouse deve poter scorrere): dopo la costruzione del canvas

```python
        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind_all(evento, self._rotellina, add="+")
```
con

```python
    def _rotellina(self, evento) -> None:
        if self.app.current_page != "select":
            return
        passo = -1 if getattr(evento, "num", 0) == 4 or getattr(evento, "delta", 0) > 0 else 1
        self.canvas.yview_scroll(passo, "units")
```
e la lista si adatta alla larghezza: `self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._finestra_lista, width=e.width))` con `self._finestra_lista = self.canvas.create_window(...)`.

Testi: sottotitolo «Togli la spunta alle cartelle che non ti servono.» con `TestoAdattivo`; riepilogo `font(18, bold=True)`; errore data: la voce di errore sulla data **sparisce** (non si scrive più a mano).

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_page_select.py -v` — Expected: PASS. Adattare i vecchi test che scrivevano `data_minima.set("2024-…")` a mano: `data_minima` funziona ancora (è la stessa variabile), quindi devono passare invariati; quelli sull'errore di data non valida vanno **rimossi** insieme alla funzione che non esiste più (annotarlo nel commit).

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/page_select.py tests
git commit -m "feat(ui): passo 2 con nomi veri delle cartelle, menu del periodo e filtro sticker

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C8: Passo 3 «Destinazione» — una frase chiara, «Altre opzioni» chiuse, conferma per cancellare

**Files:**
- Modify: `fotofacile/ui/page_options.py`
- Test: `tests/test_page_options.py`

**Interfaces:**
- Produces: `OptionsPage.altre_opzioni_aperte: bool`, `OptionsPage.mostra_altre(mostra: bool)`, `OptionsPage.riassunto: TestoAdattivo`, `OptionsPage.azione_principale()`, `OptionsPage.azione_indietro()`; la cancellazione dal telefono usa `tkinter.messagebox.askyesno` (importato come `messagebox` **nel modulo**, così i test lo sostituiscono con `monkeypatch.setattr(page_options.messagebox, "askyesno", ...)`).

Le variabili `mantieni_cartelle`, `salta_gia_copiate`, `elimina_dopo_copia`, `converti_webp` e `chooser` **restano** (usate da `conftest.azzera`, dai test e da B5).

- [ ] **Step 1: Test che falliscono**

```python
def test_il_riassunto_dice_cosa_succedera(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    testo = str(pagina.riassunto.cget("text"))
    assert "Copierò" in testo and str(tmp_path) in testo


def test_le_altre_opzioni_sono_chiuse_all_inizio(app, tmp_path):
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    assert pagina.altre_opzioni_aperte is False
    pagina.mostra_altre(True)
    assert pagina.altre_opzioni_aperte is True


def test_cancellare_dal_telefono_chiede_conferma_con_una_finestra(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    domande = []
    monkeypatch.setattr(page_options.messagebox, "askyesno", lambda titolo, testo, **k: domande.append(testo) or False)
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    assert domande, "la conferma deve comparire subito, quando si mette la spunta"
    assert "telefono" in domande[0].lower()
    assert pagina.elimina_dopo_copia.get() is False  # ha risposto «No»: la spunta torna a posto


def test_rispondere_si_lascia_la_spunta(app, tmp_path, monkeypatch):
    from fotofacile.ui import page_options

    monkeypatch.setattr(page_options.messagebox, "askyesno", lambda *a, **k: True)
    _prepara(app, tmp_path)
    pagina = app.pages["options"]
    pagina.on_show()
    pagina.elimina_dopo_copia.set(True)
    pagina._eliminazione_cambiata()
    assert pagina.elimina_dopo_copia.get() is True
    pagina.go_next()
    assert app.current_page == "transfer"
    assert app.options.delete_after is True
```
Il vecchio `test_cancellazione_dal_telefono_richiede_conferma` (doppio «Copia le foto») va **sostituito** dai due sopra.

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_options.py -v` — Expected: i quattro nuovi FAIL.

- [ ] **Step 3: Implementare** — in `page_options.py`:

Importare `from tkinter import messagebox, ttk` e `TestoAdattivo`. Disposizione:

```python
        ttk.Label(self, text="Dove salvo le foto?", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        self.riassunto = TestoAdattivo(self, text="", font=font(17))
        self.riassunto.grid(row=1, column=0, sticky="ew", pady=(4, 10))
        self.chooser = PathChooser(self, on_change=lambda _p: self._aggiorna_spazio())
        self.chooser.grid(row=2, column=0, sticky="ew")
        self.spazio = TestoAdattivo(self, text="", font=font(15, bold=True))
        self.spazio.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        self.dettaglio_salti = TestoAdattivo(self, text="", style="Tenue.TLabel", font=font(13))
        self.dettaglio_salti.grid(row=4, column=0, sticky="ew")

        self.altre_opzioni_aperte = False
        self.bottone_altre = ttk.Button(self, text="Altre opzioni ▸", style="Link.TButton",
                                        command=lambda: self.mostra_altre(not self.altre_opzioni_aperte))
        self.bottone_altre.grid(row=5, column=0, sticky="w", pady=(12, 0))
        self.scelte = ttk.Frame(self)           # le tre/quattro caselle di prima, invariate
        self.scelte.grid(row=6, column=0, sticky="w")
        self.scelte.grid_remove()
```
(il frame `scelte` contiene le stesse `Checkbutton` di prima, con la casella WebP di B5; `avviso_eliminazione` resta nel frame ma **non serve più** a confermare: rimane come promemoria rosso mentre la spunta è attiva.)

```python
    def mostra_altre(self, mostra: bool) -> None:
        self.altre_opzioni_aperte = bool(mostra)
        if mostra:
            self.scelte.grid()
            self.bottone_altre.configure(text="Altre opzioni ▾")
        else:
            self.scelte.grid_remove()
            self.bottone_altre.configure(text="Altre opzioni ▸")

    def _eliminazione_cambiata(self) -> None:
        if self.elimina_dopo_copia.get():
            conferma = messagebox.askyesno(
                "Togliere le foto dal telefono?",
                "Dopo la copia le foto verranno TOLTE dal telefono.\n\n"
                "Prima di chiudere il programma controlla che siano nella cartella scelta.\n\n"
                "Vuoi davvero toglierle dal telefono?",
                icon="warning",
                default="no",
                parent=self,
            )
            if not conferma:
                self.elimina_dopo_copia.set(False)
        if self.elimina_dopo_copia.get():
            self.avviso_eliminazione.grid(row=3, column=0, sticky="w")
        else:
            self.avviso_eliminazione.grid_remove()
        self._aggiorna_spazio()
```
In `go_next` **eliminare** il blocco `if opzioni.delete_after and not self._conferma_eliminazione: …` (e l'attributo `_conferma_eliminazione`; toglierlo anche da `conftest.azzera`).

`_aggiorna_spazio` scrive anche il riassunto:

```python
        quanti = piano.file_count
        self.riassunto.configure(
            text=f"Copierò {quanti} {'foto o video' if quanti != 1 else 'foto'} "
                 f"({format_size(piano.total_bytes)}) in questa cartella:  {self.chooser.get()}"
        )
```
(ma il testo lungo del percorso è già mostrato dal campo: la frase va bene se breve — se `quanti == 0`: «Non c'è niente di nuovo da copiare: le foto erano già state salvate.»)

Il pulsante principale: «Copia le foto  →» con `style="Big.TButton"` (invariato); `azione_principale = go_next`; `azione_indietro = lambda: self.app.go_to("prev")`.

Le `ttk.Label` di stato con testo di errore restano `errore`/`successo`, ma il colore va accompagnato da un simbolo: prefissare `✔ ` (spazio sufficiente) o `✖ ` in `_aggiorna_spazio`.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests -x 2>&1 | tail -3` — Expected: verde. Togliere l'`xfail` di `test_esc_torna_indietro` (C5).

- [ ] **Step 5: Commit**

```bash
git add fotofacile/ui/page_options.py tests
git commit -m "feat(ui): passo 3 con riassunto chiaro, altre opzioni chiuse e conferma prima di cancellare

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C9: Passo 4 «Copia» — una percentuale grande, un «Fatto!» chiaro

**Files:**
- Modify: `fotofacile/ui/page_transfer.py`
- Test: `tests/test_page_transfer.py`

**Interfaces:**
- Produces: `TransferPage.percentuale: ttk.Label` (numero grande, es. «37 %»), `TransferPage.azione_principale()` (= apri la cartella a copia finita, altrimenti niente), `TransferPage.azione_indietro()` (nessuna azione: durante la copia non si torna indietro), `TransferPage.mostra_altri_pulsanti`. I widget `barra_totale`, `barra_file`, `riepilogo`, `riepilogo_errori`, `bottone_apri`, `bottone_salva`, `bottone_chiudi`, `bottone_annulla`, `stato`, `etichetta_file`, `dettagli` **restano** (usati da `conftest.azzera` e dai test).

- [ ] **Step 1: Test che falliscono**

```python
def test_la_percentuale_grande_segue_l_avanzamento(app):
    from fotofacile.core.transfer import Progress

    pagina = app.pages["transfer"]
    pagina.update_progress(Progress(total_files=4, done_files=1, bytes_done=37, bytes_total=100))
    assert pagina.percentuale.cget("text") == "37 %"


def test_il_tempo_residuo_e_scritto_a_parole(app):
    from fotofacile.core.transfer import Progress

    pagina = app.pages["transfer"]
    pagina.update_progress(Progress(total_files=4, done_files=1, bytes_done=10, bytes_total=100,
                                    speed_bps=1.0, eta_seconds=125))
    assert "circa 2 minuti" in pagina.dettagli.cget("text")


def test_a_fine_copia_c_e_un_fatto_chiaro_e_gli_avvisi_si_vedono(app):
    from fotofacile.core.transfer import TransferResults
    from pathlib import Path

    pagina = app.pages["transfer"]
    esiti = TransferResults(copied=[Path("/x/a.jpg"), Path("/x/b.jpg")], bytes_copied=2048, elapsed=3.0,
                            warnings=["Non sono riuscito a togliere a.jpg dal telefono: bloccato."])
    pagina.show_summary(esiti)
    assert pagina.riepilogo.cget("text").startswith("✔")
    assert "2" in pagina.riepilogo.cget("text")
    assert "a.jpg" in pagina.riepilogo_errori.cget("text")  # l'avviso non va perso
    assert pagina.percentuale.cget("text") == "100 %"


def test_l_apertura_della_cartella_e_il_pulsante_principale_a_fine_copia(app, monkeypatch, tmp_path):
    from fotofacile.core.planner import TransferOptions
    from fotofacile.core.transfer import TransferResults
    from fotofacile.ui import page_transfer

    aperte = []
    monkeypatch.setattr(page_transfer, "open_in_file_manager", lambda p: aperte.append(p))
    app.options = TransferOptions(destination=tmp_path)
    pagina = app.pages["transfer"]
    pagina.azione_principale()  # durante la copia non fa niente
    assert aperte == []
    pagina.show_summary(TransferResults())
    pagina.azione_principale()
    assert aperte == [tmp_path]
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_page_transfer.py -v` — Expected: i nuovi FAIL.

- [ ] **Step 3: Implementare** — in `page_transfer.py`:

Nel costruttore, dopo `self.stato`:

```python
        self.percentuale = ttk.Label(self, text="0 %", font=font(48, bold=True))
        self.percentuale.grid(row=2, column=0, sticky="w")
        self.barra_totale = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", maximum=100)
        self.barra_totale.grid(row=3, column=0, sticky="ew", pady=(4, 6))
```
(scalare le righe seguenti; `etichetta_file` e `barra_file` restano ma **piccole**: `font(13)`; `barra_file` con `pady` ridotto.)

`update_progress` aggiunge: `self.percentuale.configure(text=f"{int(min(percentuale, 100))} %")` e il testo dei dettagli a parole:

```python
        self.dettagli.configure(
            text=(
                f"{progresso.done_files} foto su {progresso.total_files}  •  "
                f"{format_size(progresso.bytes_done)} di {format_size(progresso.bytes_total)}  •  "
                f"{parole_tempo_residuo(progresso.eta_seconds)}"
            )
        )
```
con, in `core/format.py`, la funzione (con il suo test in `tests/test_format.py`):

```python
def parole_tempo_residuo(secondi: float | None) -> str:
    """«manca circa 2 minuti» — a parole, senza cronometri."""
    if secondi is None or secondi < 0:
        return "calcolo il tempo che manca…"
    if secondi < 45:
        return "manca meno di un minuto"
    minuti = round(secondi / 60)
    if minuti < 60:
        return f"manca circa {minuti} minut{'o' if minuti == 1 else 'i'}"
    ore, resto = divmod(minuti, 60)
    return f"manca circa {ore} or{'a' if ore == 1 else 'e'}" + (f" e {resto} minuti" if resto else "")
```
(Il test del tempo sopra chiede «circa 2 minuti»: 125 s → `round(2.08)` = 2 → «manca circa 2 minuti». ✔)

`show_summary`: il riepilogo comincia con «✔ » per il successo, «⚠ » se `cancelled` o se ci sono `failed`; `self.percentuale.configure(text="100 %")` se non annullata; le righe di `riepilogo_errori` uniscono `failed` **e** `warnings`:

```python
        righe = []
        if risultati.failed:
            primi = ", ".join(media.name for media, _m in risultati.failed[:5])
            righe.append(f"Non copiati ({len(risultati.failed)}): {primi}")
        righe.extend(risultati.warnings)
        self.riepilogo_errori.configure(text="\n".join(righe))
```
Pulsanti: `bottone_apri` con `style="Big.TButton"` e testo «Apri la cartella delle foto»; «Salva resoconto» e «Chiudi» restano `Secondary.TButton`; `bottone_annulla` «Interrompi» resta `Secondary`. Testo dello stato: «Sto copiando le foto… non scollegare il telefono.» in `Sottotitolo` (già).

```python
    def azione_principale(self) -> None:
        if self.results is not None:
            self.open_folder()

    def azione_indietro(self) -> None:
        return None  # durante e dopo la copia non si torna indietro con Esc
```
`show_error` prefissa «✖ » al messaggio.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests -x 2>&1 | tail -3` — Expected: verde. Test `tests/test_app_completa.py` (app vera in sottoprocesso) deve continuare a dare `ok: true`.

- [ ] **Step 5: Commit**

```bash
git add fotofacile tests
git commit -m "feat(ui): passo 4 con percentuale grande, tempo a parole e «Fatto!» chiaro

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task C10: Controlli automatici di leggibilità + verifica a schermo

**Files:**
- Create: `tests/test_accessibilita.py`, `scripts/scatti_interfaccia.py`
- Modify: (nessuno, salvo correzioni emerse)

**Interfaces:**
- Consumes: tutto il Parte C; `App(scuro=, scala=)` (C5).

- [ ] **Step 1: Scrivere i controlli** — `tests/test_accessibilita.py`:

```python
"""Controlli automatici di leggibilità: falliscono se qualcuno rimpicciolisce di nuovo il testo."""

import tkinter.font as tkfont

import pytest

from fotofacile.ui import theme
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="questo ambiente non apre finestre")

PAGINE = ("connect", "select", "options", "transfer")


def _tutti(widget):
    yield widget
    for figlio in widget.winfo_children():
        yield from _tutti(figlio)


def _punti(widget) -> int | None:
    try:
        nome = widget.cget("font")
    except Exception:
        return None
    if not nome:
        return None
    try:
        return abs(int(tkfont.Font(font=nome).actual("size")))
    except Exception:
        return None


@pytest.mark.parametrize("pagina", PAGINE)
def test_nessun_testo_sotto_i_13_punti_a_scala_normale(app, pagina):
    app.cambia_scala(-1) if theme.scala_attuale() > 1.0 else None
    theme.imposta_scala(1.0)
    app.ricostruisci_pagine()
    troppo_piccoli = []
    for widget in _tutti(app.pages[pagina]):
        punti = _punti(widget)
        if punti is not None and 0 < punti < 13:
            troppo_piccoli.append((widget.winfo_class(), str(widget.cget("text"))[:30], punti))
    assert not troppo_piccoli, troppo_piccoli
    theme.imposta_scala(1.0)


@pytest.mark.parametrize("modo", ["chiaro", "scuro"])
def test_contrasto_di_ogni_coppia_testo_sfondo(modo):
    tavolozza = theme.PALETTE[modo]
    for testo in ("testo", "tenue", "primario", "successo", "avviso", "errore"):
        for sfondo in ("sfondo", "pannello"):
            assert theme.contrasto(tavolozza[testo], tavolozza[sfondo]) >= 4.5, (modo, testo, sfondo)
    assert theme.contrasto(tavolozza["testo"], tavolozza["sfondo"]) >= 7


@pytest.mark.parametrize("pagina", PAGINE)
def test_le_istruzioni_non_escono_dalla_finestra_a_scala_massima(app, pagina):
    theme.imposta_scala(1.5)
    try:
        app.ricostruisci_pagine()
        app.go_to(pagina)
        app.deiconify()
        app.update()
        larghezza = app.winfo_width()
        for widget in _tutti(app.pages[pagina]):
            if widget.winfo_ismapped():
                assert widget.winfo_rootx() - app.winfo_rootx() <= larghezza, widget
    finally:
        theme.imposta_scala(1.0)
        app.withdraw()
```
(Se un controllo fallisce mostra **quale** widget: si corregge quel widget, non il test.)

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_accessibilita.py -v` — Expected: PASS; se falliscono, correggere i font/wraplength nei file di pagina (non abbassare le soglie).

- [ ] **Step 3: Script per le schermate** — `scripts/scatti_interfaccia.py` (uso: `launchctl asuser $(id -u) env PYTHONPATH="$PWD" .venv/bin/python scripts/scatti_interfaccia.py <cartella> <chiaro|scuro> <1.0|1.25|1.5>`):

```python
"""Scatta una schermata per ognuno dei 4 passi: serve a guardare davvero l'interfaccia."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from fotofacile.core.devices import DeviceInfo
from fotofacile.ui.app import App

PASSI = ("connect", "select", "options", "transfer")


def main(cartella: str, modo: str, scala: float) -> int:
    uscita = Path(cartella)
    uscita.mkdir(parents=True, exist_ok=True)
    app = App(demo_mode=True, scuro=(modo == "scuro"), scala=scala)
    app.geometry("+40+40")
    app.device = DeviceInfo(serial="DEMO1", state="device", model="Pixel demo", product="")
    stato = {"i": 0}

    def scatta() -> None:
        chiave = PASSI[stato["i"]]
        if chiave == "select":
            app.pages["select"].on_show()
        app.go_to(chiave)
        app.update()
        app.after(1800, salva)

    def salva() -> None:
        chiave = PASSI[stato["i"]]
        subprocess.run(["screencapture", "-x", str(uscita / f"{chiave}-{modo}-{scala}.png")], check=False)
        stato["i"] += 1
        if stato["i"] >= len(PASSI):
            app.destroy()
            return
        if PASSI[stato["i"]] == "options":
            app.media_files = list(app.pages["select"].selected_files())
        app.after(200, scatta)

    app.after(1500, scatta)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2], float(sys.argv[3])))
```

- [ ] **Step 4: Scattare e guardare** — per le sei combinazioni principali (chiaro/scuro × 1.0/1.25/1.5):

```bash
S=/private/tmp/claude-501/-Users-marcosalvatori-Desktop-Programmazione-FotoFacile/ba28d30c-d803-4908-858c-75baca40746e/scratchpad/scatti
for modo in chiaro scuro; do for scala in 1.0 1.25 1.5; do
  launchctl asuser $(id -u) env PYTHONPATH="$PWD" "$PWD/.venv/bin/python" scripts/scatti_interfaccia.py "$S" $modo $scala
done; done
ls "$S" | wc -l   # atteso: 24
```
Poi **guardare ogni PNG con lo strumento Read** e compilare questa lista, correggendo cosa non passa:
  - [ ] nessun testo tagliato o fuori finestra a 150 %;
  - [ ] in ogni schermata **un solo** pulsante grande e in evidenza;
  - [ ] in scuro tutto leggibile (nessun nero su scuro);
  - [ ] i simboli ✔ ⚠ ✖ si vedono con il font scelto (se compaiono quadrati, sostituire con testo «OK:», «Attenzione:», «Errore:»);
  - [ ] «Passo N di 4» sempre visibile.

- [ ] **Step 5: Collaudo end-to-end** — `FF_DEST=/tmp/collaudo-foto FF_ESITO=/tmp/esito.json .venv/bin/python tests/pilota_app.py` (con `launchctl asuser …` se serve, come in `HANDOFF.md`). Expected: `"ok": true`, 54 file, nessun `.part`, nessuna sottocartella. Se `pilota_app.py` cerca testi cambiati (es. «Copia le foto»), aggiornarlo.

- [ ] **Step 6:** `.venv/bin/python -m pytest tests 2>&1 | tail -2 && .venv/bin/python -m pyflakes fotofacile scripts` poi

```bash
git add tests/test_accessibilita.py scripts/scatti_interfaccia.py fotofacile tests
git commit -m "test(ui): controlli automatici di leggibilità e script per le schermate

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

---

# PARTE D — Programma di installazione per Windows (`.exe`)

**Cosa si ottiene:** `FotoFacile-Setup-0.2.0.exe`, un vero installatore (Inno Setup) con procedura guidata **in italiano**, finestra ingrandita, collegamenti su Desktop e menu Start, voce in «App e funzionalità», disinstallazione pulita, **senza diritti di amministratore**. Niente `.bat`/`.ps1` per l'utente.

**Limite che va detto chiaro a Marco:** questo Mac **non può** compilare un `.exe` per Windows (PyInstaller non fa cross-compilazione, Inno Setup gira solo su Windows). Il `.exe` si costruisce **sul runner Windows di GitHub Actions**, che esiste già in `.github/workflows/build-installers.yml`; Marco lo scarica da lì. Il piano lo rende affidabile e **verificato automaticamente** (installa, avvia, disinstalla dentro il runner).

**Cosa NON si può verificare da qui:** l'aspetto dell'installatore su un vero Windows e il collegamento con un vero telefono. Task D6 dà a Marco la lista di prove da fare a mano.

### Task D0: Portare la versione a 0.2.0 in un solo punto

**Files:**
- Modify: `fotofacile/__init__.py`
- Create: `scripts/leggi_versione.py`
- Test: `tests/test_versione.py`

**Interfaces:**
- Produces: `fotofacile.__version__ == "0.2.0"`; `python scripts/leggi_versione.py` stampa `0.2.0` (usato da CI per passare `/DVersione=` a Inno Setup).

- [ ] **Step 1: Test che fallisce** — `tests/test_versione.py`:

```python
import re
import subprocess
import sys
from pathlib import Path

import fotofacile

RADICE = Path(__file__).resolve().parent.parent


def test_la_versione_ha_la_forma_giusta():
    assert re.fullmatch(r"\d+\.\d+\.\d+", fotofacile.__version__)


def test_lo_script_stampa_la_stessa_versione():
    esito = subprocess.run([sys.executable, str(RADICE / "scripts" / "leggi_versione.py")],
                           capture_output=True, text=True, check=True)
    assert esito.stdout.strip() == fotofacile.__version__


def test_lo_script_iss_non_ha_una_versione_scritta_a_mano_diversa():
    iss = (RADICE / "installer" / "windows" / "FotoFacile.iss").read_text(encoding="utf-8-sig")
    # la versione arriva da /DVersione=…; il valore di ripiego deve coincidere con quello vero
    trovata = re.search(r'#define Versione "([^"]+)"', iss)
    assert trovata and trovata.group(1) == fotofacile.__version__
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_versione.py -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — `fotofacile/__init__.py`: `__version__ = "0.2.0"`. `scripts/leggi_versione.py`:

```python
#!/usr/bin/env python3
"""Stampa la versione di FotoFacile: la pipeline la passa a Inno Setup (/DVersione=…)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fotofacile  # noqa: E402

print(fotofacile.__version__)
```
(il terzo test passerà dopo il Task D1, che riscrive il file `.iss`: tenere questo test `xfail` con motivo «serve il Task D1» e toglierlo in D1.)

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_versione.py -v` — Expected: 2 PASS + 1 XFAIL.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/__init__.py scripts/leggi_versione.py tests/test_versione.py
git commit -m "chore: versione 0.2.0 con un solo punto di verità

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task D1: Riscrivere lo script di Inno Setup (semplice, grande, in italiano)

**Files:**
- Modify: `installer/windows/FotoFacile.iss` (riscritto)
- Create: `installer/windows/Benvenuto.txt` (**con BOM UTF-8**)
- Test: `tests/test_installer_iss.py`

**Interfaces:**
- Consumes: `dist\FotoFacile\` (cartella creata da PyInstaller), `assets\fotofacile.ico`.
- Produces: `dist\installer\FotoFacile-Setup-<Versione>.exe`; `AppId` **invariato** (`{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}`) così chi ha già installato la 0.1.0 viene **aggiornato** invece di duplicato.

- [ ] **Step 1: Test che fallisce** — `tests/test_installer_iss.py`:

```python
import re
from pathlib import Path

import pytest

import fotofacile

RADICE = Path(__file__).resolve().parent.parent
ISS = RADICE / "installer" / "windows" / "FotoFacile.iss"


@pytest.fixture(scope="module")
def iss() -> str:
    return ISS.read_text(encoding="utf-8-sig")


def _direttiva(iss: str, nome: str) -> str:
    trovata = re.search(rf"^{nome}=(.*)$", iss, re.MULTILINE)
    assert trovata, f"manca {nome}="
    return trovata.group(1).strip()


def test_versione_di_ripiego_uguale_a_quella_del_programma(iss):
    assert re.search(rf'#define Versione "{re.escape(fotofacile.__version__)}"', iss)
    assert "#ifndef Versione" in iss  # la pipeline può passarla con /DVersione=


def test_l_id_dell_applicazione_non_cambia_mai(iss):
    # cambiarlo farebbe installare la 0.2 accanto alla 0.1 invece di aggiornarla
    assert "AppId={{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}" in iss


def test_installa_senza_amministratore_e_senza_finestra_di_scelta(iss):
    assert _direttiva(iss, "PrivilegesRequired") == "lowest"
    assert "PrivilegesRequiredOverridesAllowed" not in iss  # niente domanda incomprensibile


def test_finestra_ingrandita_e_stile_moderno(iss):
    assert _direttiva(iss, "WizardStyle") == "modern"
    assert int(_direttiva(iss, "WizardSizePercent").split(",")[0]) >= 120


def test_solo_windows_10_o_successivo_a_64_bit(iss):
    assert _direttiva(iss, "MinVersion") == "10.0"
    assert _direttiva(iss, "ArchitecturesAllowed") == "x64compatible"
    assert _direttiva(iss, "ArchitecturesInstallIn64BitMode") == "x64compatible"


def test_lingua_italiana(iss):
    assert 'MessagesFile: "compiler:Languages\\Italian.isl"' in iss


def test_niente_bat_ne_powershell_per_l_utente(iss):
    assert ".bat" not in iss.lower()
    assert ".ps1" not in iss.lower()


def test_i_file_di_testo_con_accenti_hanno_il_bom():
    grezzo = (RADICE / "installer" / "windows" / "Benvenuto.txt").read_bytes()
    assert grezzo.startswith(b"\xef\xbb\xbf"), "Inno Setup legge come ANSI i testi senza BOM"


def test_c_e_il_collegamento_alla_diagnosi(iss):
    assert 'Parameters: "doctor"' in iss


def test_disinstallazione_chiede_prima_di_togliere_i_dati_personali(iss):
    assert "[Code]" in iss and "MsgBox" in iss and ".fotofacile" in iss
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_installer_iss.py -v` — Expected: FAIL (più di un test).

- [ ] **Step 3: Implementare** — `installer/windows/Benvenuto.txt` (salvare con BOM UTF-8; da Python: `Path(...).write_text(testo, encoding="utf-8-sig")`):

```
Benvenuto in FotoFacile

FotoFacile copia le foto e i video dal tuo telefono Android al computer, con pochi
passaggi e senza cartelle difficili da trovare.

Cosa succede adesso:
  1. Premi «Avanti» per installare il programma.
  2. Alla fine trovi l'icona «FotoFacile» sul Desktop.
  3. Apri il programma, collega il telefono con il cavo e segui le istruzioni.

Non serve attivare nessuna impostazione speciale sul telefono: basta scegliere
«Trasferimento file» quando il telefono lo chiede.

Windows potrebbe mostrare un avviso blu «Windows ha protetto il PC» perché il
programma è nuovo: premi «Ulteriori informazioni» e poi «Esegui comunque».
```

`installer/windows/FotoFacile.iss` (riscritto):

```ini
; FotoFacile — programma di installazione per Windows (Inno Setup 6)
;
; Crea  dist\installer\FotoFacile-Setup-<versione>.exe  con una procedura guidata in
; italiano: installa il programma, crea i collegamenti e registra la disinstallazione in
; «App e funzionalità». Non richiede i diritti di amministratore.
;
; Si compila su Windows (lo fa la pipeline GitHub, vedi .github/workflows):
;   ISCC.exe /DVersione=0.2.0 installer\windows\FotoFacile.iss

#ifndef Versione
  #define Versione "0.2.0"
#endif
#define NomeApp "FotoFacile"
#define Editore "FotoFacile"
#define Sito "https://github.com/marcosalvatori0/fotofacile"
#define Eseguibile "FotoFacile.exe"
#define CartellaSorgente "..\..\dist\FotoFacile"

[Setup]
; NON cambiare mai l'AppId: serve a riconoscere una versione già installata e ad aggiornarla.
AppId={{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}
AppName={#NomeApp}
AppVersion={#Versione}
AppVerName={#NomeApp} {#Versione}
AppPublisher={#Editore}
AppPublisherURL={#Sito}
AppSupportURL={#Sito}
AppUpdatesURL={#Sito}
VersionInfoVersion={#Versione}
VersionInfoDescription=Programma di installazione di {#NomeApp}
DefaultDirName={autopf}\{#NomeApp}
DisableProgramGroupPage=yes
DisableDirPage=auto
; installazione nel profilo dell'utente: nessun permesso di amministratore, nessuna domanda
PrivilegesRequired=lowest
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\..\dist\installer
OutputBaseFilename={#NomeApp}-Setup-{#Versione}
Compression=lzma2
SolidCompression=yes
; finestra più grande e testo leggibile
WizardStyle=modern
WizardSizePercent=120,120
DisableWelcomePage=no
InfoBeforeFile=Benvenuto.txt
SetupIconFile=..\..\assets\fotofacile.ico
UninstallDisplayName={#NomeApp}
UninstallDisplayIcon={app}\{#Eseguibile}
; se il programma è aperto durante un aggiornamento, chiede di chiuderlo
CloseApplications=yes
RestartApplications=no
ShowLanguageDialog=no
LanguageDetectionMethod=none

[Languages]
Name: "italiano"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "Crea un'icona sul Desktop"; GroupDescription: "Collegamenti:"
Name: "startmenuicon"; Description: "Crea un collegamento nel menu Start"; GroupDescription: "Collegamenti:"

[Files]
Source: "{#CartellaSorgente}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: desktopicon; Comment: "Copia le foto dal telefono Android al computer"
Name: "{autoprograms}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: startmenuicon; Comment: "Copia le foto dal telefono Android al computer"
Name: "{autoprograms}\{#NomeApp} - Diagnosi"; Filename: "{app}\{#Eseguibile}"; Parameters: "doctor"; Tasks: startmenuicon; Comment: "Se qualcosa non va: mostra un rapporto da mandare a chi ti aiuta"

[Run]
Filename: "{app}\{#Eseguibile}"; Description: "Apri {#NomeApp} adesso"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
// Alla disinstallazione si chiede se togliere anche le impostazioni e l'elenco dei file
// già copiati. Le FOTO copiate non si toccano mai.
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  CartellaDati: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    CartellaDati := ExpandConstant('{%USERPROFILE}\.fotofacile');
    if DirExists(CartellaDati) and (not UninstallSilent) then
    begin
      if MsgBox('Vuoi togliere anche le impostazioni e l''elenco delle foto già copiate?' + #13#10 +
                'Le foto copiate NON vengono cancellate.', mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
        DelTree(CartellaDati, True, True, True);
    end;
  end;
end;
```
(`installer/windows/FotoFacile.iss` va salvato **con BOM UTF-8** perché contiene accenti: `Path.write_text(..., encoding="utf-8-sig")`; il test `test_versione` lo legge già con `utf-8-sig`.) Se `app_dir()` non fosse `~/.fotofacile` su Windows, correggere il percorso in `[Code]`: verificare con `/usr/bin/grep -n "def app_dir" -A8 fotofacile/core/osutil.py`.

Togliere l'`xfail` del terzo test di `tests/test_versione.py`.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_installer_iss.py tests/test_versione.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add installer/windows/FotoFacile.iss installer/windows/Benvenuto.txt tests
git commit -m "feat(installer): script Inno Setup riscritto (italiano, finestra grande, senza amministratore)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task D2: `doctor` e `--selftest` funzionano anche dal `.exe` senza finestra nera (D7)

**Files:**
- Modify: `fotofacile/cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces: `emetti(testo: str, nome_file: str = "diagnosi.txt", env=None) -> Path | None` — stampa su `stdout` se esiste; altrimenti (eseguibile `--windowed`, `sys.stdout is None`) scrive `app_dir()/nome_file` e, su Windows, lo apre nel Blocco note. Restituisce il file scritto, oppure `None`.

- [ ] **Step 1: Test che falliscono**

```python
def test_emetti_stampa_quando_c_e_un_terminale(capsys, tmp_path):
    from fotofacile.cli import emetti

    assert emetti("ciao", env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}) is None
    assert "ciao" in capsys.readouterr().out


def test_emetti_scrive_un_file_senza_terminale(monkeypatch, tmp_path):
    import sys

    from fotofacile.cli import emetti

    monkeypatch.setattr(sys, "stdout", None)
    aperti = []
    percorso = emetti(
        "rapporto", env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)},
        apri=lambda p: aperti.append(p),
    )
    assert percorso is not None and percorso.read_text(encoding="utf-8") == "rapporto"
    assert aperti == [percorso]
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_cli.py -k emetti -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — in `cli.py`:

```python
def emetti(testo: str, nome_file: str = "diagnosi.txt", env: Mapping[str, str] | None = None, apri=None) -> Path | None:
    """Mostra un rapporto: sul terminale se c'è, altrimenti in un file che si apre da solo.

    Il programma installato su Windows non ha finestra nera (``sys.stdout`` è ``None``):
    senza questo, «FotoFacile - Diagnosi» dal menu Start non farebbe vedere niente.
    """
    if sys.stdout is not None:
        print(testo)
        return None
    percorso = app_dir(dict(env) if env is not None else None) / nome_file
    try:
        percorso.parent.mkdir(parents=True, exist_ok=True)
        percorso.write_text(testo, encoding="utf-8")
    except OSError:
        return None
    if apri is None and sys.platform == "win32":  # pragma: no cover - solo su Windows
        apri = os.startfile  # type: ignore[attr-defined]
    if apri is not None:
        try:
            apri(percorso)
        except OSError:  # pragma: no cover - meglio nessun Blocco note che un errore
            pass
    return percorso
```
In `doctor()` sostituire `print(build_doctor_report(...))` con `emetti(build_doctor_report(...), env=ambiente)`. In `selftest()` (cercare le `print(...)` di esito) usare `emetti(json.dumps(...), "selftest.txt")` **senza** aprire il file: aggiungere il parametro `apri=lambda _p: None` in quel punto, così CI può leggere `selftest.txt` ma non si apre niente. Aggiornare il test esistente di `selftest` se controlla l'output.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_cli.py -v` — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add fotofacile/cli.py tests/test_cli.py
git commit -m "fix(D7): doctor e selftest funzionano anche dal programma installato (senza finestra nera)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task D3: Togliere `.bat`/`.ps1` dell'installazione dal percorso dell'utente

**Files:**
- Delete: `installer/windows/Installa FotoFacile.bat`, `installer/windows/InstallaFotoFacile.ps1`, `installer/windows/DisinstallaFotoFacile.ps1`, `scripts/crea_pacchetto_windows.py`
- Modify o Delete (dopo aver letto cosa coprono): `tests/test_pacchetto_windows.py`, `tests/test_installer_pacchetti.py`
- Modify: `README.md`, `LEGGIMI - Installazione.txt`, `.github/workflows/build-installers.yml` (passo «Versione portatile»), `HANDOFF.md`

**Cuidado:** `fotofacile/aiutanti/wpd_win.ps1` **NON** è un installatore: è l'aiutante che parla con il telefono su Windows e **deve restare** (con il BOM). Non toccarlo.

- [ ] **Step 1: Capire cosa coprono i test da rimuovere**

Run: `.venv/bin/python -m pytest tests/test_pacchetto_windows.py tests/test_installer_pacchetti.py --collect-only -q 2>&1 | head -60`
Poi leggere i due file (`Read`) e classificare **ogni** test: (a) riguarda i `.bat`/`.ps1` d'installazione → si elimina; (b) riguarda `wpd_win.ps1` (BOM, sintassi) o snippet Python valido in generale → si **sposta** in un nuovo `tests/test_aiutante_windows.py`.

- [ ] **Step 2: Spostare i test da conservare** (in particolare quello che verifica che `wpd_win.ps1` inizi con il BOM UTF-8 e che i `.bat` rimasti non lo abbiano — se dopo D3 non restano `.bat`, il secondo controllo cade).

- [ ] **Step 3: Cancellare** i file elencati sopra con `git rm` (un comando **solo**, senza altro lavoro concatenato):

```bash
git rm "installer/windows/Installa FotoFacile.bat" installer/windows/InstallaFotoFacile.ps1 installer/windows/DisinstallaFotoFacile.ps1 scripts/crea_pacchetto_windows.py
```
e i test classificati (a). Rimuovere dalla cartella sulla Scrivania la vecchia `~/Desktop/FotoFacile per Windows/` **solo dopo aver chiesto a Marco** (⚠ CHIEDI: è fuori dal repository).

- [ ] **Step 4: Aggiornare la documentazione**: `LEGGIMI - Installazione.txt` → sezione Windows: «Scarica `FotoFacile-Setup-<versione>.exe`, fai doppio clic, premi Avanti fino alla fine» (+ nota sull'avviso blu «Windows ha protetto il PC» e il percorso «Ulteriori informazioni → Esegui comunque»); nessun accenno ai `.bat`. `README.md`: stesso testo nella sezione Windows; tabella dei file scaricabili (installer, zip portatile, dmg). Nel workflow, il passo «Versione portatile (zip)» usa `python -c "import scripts.crea_pacchetto_windows …"`: sostituirlo con solo `shutil.make_archive` (l'import inutile va tolto, altrimenti il passo si rompe):

```yaml
      - name: Versione portatile (zip)
        run: python -c "import shutil; shutil.make_archive('dist/FotoFacile-portable', 'zip', 'dist', 'FotoFacile')"
```

- [ ] **Step 5:** Run: `.venv/bin/python -m pytest tests 2>&1 | tail -3 && .venv/bin/python -m pyflakes fotofacile scripts` — Expected: verde e vuoto. Verificare che nulla nel repository citi più i file rimossi: `/usr/bin/grep -rn "crea_pacchetto_windows\|InstallaFotoFacile\|Installa FotoFacile.bat" --include='*' . --exclude-dir=.venv --exclude-dir=graphify-out --exclude-dir=.git --exclude-dir=dist --exclude-dir=build` → nessun risultato (a parte `docs/` storici e `HANDOFF.md`, da aggiornare in E).

- [ ] **Step 6: Commit**

```bash
git add -A installer scripts tests README.md "LEGGIMI - Installazione.txt" .github
git commit -m "chore(installer): via i .bat e i .ps1 d'installazione: resta solo il Setup.exe

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task D4: Pipeline GitHub: costruire, **installare davvero**, provare e disinstallare

**Files:**
- Modify: `.github/workflows/build-installers.yml` (job `windows`)
- Create: `installer/windows/prova-installazione.ps1` (usato **solo dalla CI**, con BOM)
- Test: `tests/test_workflow.py`

**Interfaces:**
- Consumes: `scripts/leggi_versione.py` (D0), `FotoFacile.iss` (D1), `emetti` (D2).
- Produces: artefatti `FotoFacile-Setup-<v>.exe`, `FotoFacile-portable.zip`, `SHA256SUMS.txt`, `log-installazione.txt`.

- [ ] **Step 1: Test che fallisce** — `tests/test_workflow.py`:

```python
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parent.parent
FLUSSO = RADICE / ".github" / "workflows" / "build-installers.yml"


@pytest.fixture(scope="module")
def testo() -> str:
    return FLUSSO.read_text(encoding="utf-8")


def test_la_versione_arriva_dal_codice_non_da_un_numero_scritto_due_volte(testo):
    assert "scripts/leggi_versione.py" in testo
    assert "/DVersione=" in testo


def test_l_installer_viene_provato_davvero_su_windows(testo):
    assert "/VERYSILENT" in testo
    assert "prova-installazione.ps1" in testo


def test_ci_sono_i_checksum_e_il_log(testo):
    assert "SHA256SUMS.txt" in testo
    assert "log-installazione.txt" in testo


def test_pillow_e_nel_pacchetto_windows(testo):
    assert "pillow" in testo.lower()
```

- [ ] **Step 2:** Run: `.venv/bin/python -m pytest tests/test_workflow.py -v` — Expected: FAIL.

- [ ] **Step 3: Implementare** — `installer/windows/prova-installazione.ps1` (salvare con **BOM UTF-8**):

```powershell
# Prova automatica dell'installatore (SOLO per la pipeline GitHub, mai per l'utente).
# Installa in una cartella temporanea, controlla che il programma parta e lo disinstalla.
param(
    [Parameter(Mandatory = $true)][string]$Installatore,
    [string]$Cartella = "$env:RUNNER_TEMP\prova-fotofacile"
)
$ErrorActionPreference = "Stop"
$log = Join-Path (Get-Location) "log-installazione.txt"

function Fallisci($messaggio) {
    Write-Host "ERRORE: $messaggio" -ForegroundColor Red
    if (Test-Path $log) { Get-Content $log -Tail 40 }
    exit 1
}

# 1. installazione silenziosa
$argomenti = @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-", "/DIR=$Cartella", "/LOG=$log")
$p = Start-Process -FilePath $Installatore -ArgumentList $argomenti -Wait -PassThru
if ($p.ExitCode -ne 0) { Fallisci "l'installatore è uscito con codice $($p.ExitCode)" }

$exe = Join-Path $Cartella "FotoFacile.exe"
if (-not (Test-Path $exe)) { Fallisci "FotoFacile.exe non è stato installato in $Cartella" }
if (-not (Test-Path (Join-Path $Cartella "unins000.exe"))) { Fallisci "manca il programma di disinstallazione" }

# 2. voce in «App e funzionalità»
$chiave = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}_is1"
if (-not (Test-Path $chiave)) { Fallisci "manca la voce di disinstallazione nel registro" }

# 3. il programma installato parte (l'autocollaudo apre e chiude la finestra)
$s = Start-Process -FilePath $exe -ArgumentList "--selftest" -Wait -PassThru
if ($s.ExitCode -ne 0) { Fallisci "l'autocollaudo del programma installato è fallito (codice $($s.ExitCode))" }

# 4. la diagnosi produce un rapporto leggibile (l'exe non ha finestra nera: scrive un file)
$d = Start-Process -FilePath $exe -ArgumentList "doctor" -Wait -PassThru
$rapporto = Join-Path $env:USERPROFILE ".fotofacile\diagnosi.txt"
if (-not (Test-Path $rapporto)) { Fallisci "la diagnosi non ha scritto il rapporto" }
Get-Content $rapporto

# 5. disinstallazione silenziosa e pulita
$u = Start-Process -FilePath (Join-Path $Cartella "unins000.exe") -ArgumentList @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART") -Wait -PassThru
if ($u.ExitCode -ne 0) { Fallisci "la disinstallazione è uscita con codice $($u.ExitCode)" }
Start-Sleep -Seconds 3
if (Test-Path $exe) { Fallisci "dopo la disinstallazione FotoFacile.exe c'è ancora" }
if (Test-Path $chiave) { Fallisci "dopo la disinstallazione la voce nel registro c'è ancora" }
Write-Host "Installazione, avvio e disinstallazione: tutto ok." -ForegroundColor Green
```

Job `windows` del workflow: sostituire i passi da «Installa le dipendenze» in avanti con:

```yaml
      - name: Installa le dipendenze (PyInstaller e Pillow per la conversione WebP)
        run: python -m pip install --upgrade pip pyinstaller pillow
      - name: Leggi la versione
        id: versione
        shell: bash
        run: echo "v=$(python scripts/leggi_versione.py)" >> "$GITHUB_OUTPUT"
      - name: Esegui i test
        run: python -m pip install pytest && python -m pytest tests -x
      - name: Crea l'eseguibile
        run: python scripts/build_app.py --no-zip
      - name: Verifica l'eseguibile (autocollaudo)
        run: dist\FotoFacile\FotoFacile.exe --selftest
        timeout-minutes: 5
      - name: Versione portatile (zip)
        run: python -c "import shutil; shutil.make_archive('dist/FotoFacile-portable', 'zip', 'dist', 'FotoFacile')"
      - name: Installa Inno Setup
        run: choco install innosetup --no-progress -y
      - name: Crea il programma di installazione (.exe)
        run: '& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "/DVersione=${{ steps.versione.outputs.v }}" installer\windows\FotoFacile.iss'
      - name: Prova davvero l'installatore (installa, avvia, disinstalla)
        shell: pwsh
        run: ./installer/windows/prova-installazione.ps1 -Installatore "dist/installer/FotoFacile-Setup-${{ steps.versione.outputs.v }}.exe"
        timeout-minutes: 10
      - name: Somme di controllo
        shell: pwsh
        run: |
          Get-ChildItem dist/installer/*.exe, dist/*.zip | ForEach-Object {
            "$((Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower())  $($_.Name)"
          } | Set-Content dist/SHA256SUMS.txt
          Get-Content dist/SHA256SUMS.txt
      - name: Carica gli installer
        uses: actions/upload-artifact@v4
        with:
          name: FotoFacile-Windows
          path: |
            dist/installer/*.exe
            dist/*.zip
            dist/SHA256SUMS.txt
            log-installazione.txt
```
(Il passo dei test su Windows serve a intercettare i difetti specifici di quella piattaforma; se si rivelasse lento o instabile — test grafici su un runner senza schermo si saltano da soli — si toglie e si annota in `HANDOFF.md`.) Nel testo della Release (`body:`) sostituire le istruzioni obsolete sul Debug USB con: «Collega il telefono, sbloccalo e scegli “Trasferimento file”» e la nota sull'avviso blu di Windows; aggiungere `artefatti/**/SHA256SUMS.txt` a `files:`.

- [ ] **Step 4:** Run: `.venv/bin/python -m pytest tests/test_workflow.py tests/test_installer_iss.py -v` — Expected: PASS. Validare la sintassi YAML: `.venv/bin/python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/build-installers.yml'))"` (se `yaml` manca: `pip install pyyaml` nel venv di sviluppo).

- [ ] **Step 5: Commit**

```bash
git add .github installer tests
git commit -m "ci(windows): l'installatore viene provato davvero (installa, avvia, disinstalla) e ha i checksum

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

### Task D5: Costruire davvero il `.exe` su GitHub e scaricarlo

**Files:** nessun file di codice (azioni su GitHub).

Il repository è `marcosalvatori0/fotofacile`. Il ramo `revisione-v0.2` va **pubblicato** perché GitHub Actions lo possa costruire: è un'azione verso l'esterno.

- [ ] **Step 1: ⚠ CHIEDI a Marco** il permesso di pubblicare il ramo e lanciare la pipeline. Senza il «sì» il task si ferma qui.
- [ ] **Step 2:** Solo dopo il «sì»: `git push -u origin revisione-v0.2`
- [ ] **Step 3:** Lanciare a mano (non serve il tag): `gh workflow run build-installers.yml --ref revisione-v0.2` e seguire: `gh run list --workflow=build-installers.yml --limit 1` poi `gh run watch <id> --exit-status`.
- [ ] **Step 4: Se un passo fallisce** — leggere il log (`gh run view <id> --log-failed`), correggere **una causa alla volta**, aggiungere un test che la copre se possibile, rilanciare. Errori attesi e dove guardare: `choco install innosetup` (versione/rete), percorso di `ISCC.exe`, accenti nel `.iss` (BOM), `--selftest` senza schermo sul runner (già gestito con `timeout` e `|| echo` nel job macOS; per Windows il runner ha una sessione grafica: se il `--selftest` fallisse lì, è un difetto vero da correggere).
- [ ] **Step 5:** Scaricare l'installatore per Marco: `gh run download <id> -n FotoFacile-Windows -D ~/Desktop/FotoFacile-Windows-0.2.0`, verificare la somma: `shasum -a 256 -c ~/Desktop/FotoFacile-Windows-0.2.0/SHA256SUMS.txt` (dalla cartella scaricata).
- [ ] **Step 6: ⚠ CHIEDI** se pubblicare anche la Release: `git tag v0.2.0` **dopo** che il ramo è su GitHub da almeno un minuto (Failed Approach #14: un tag spinto insieme al ramo non fa partire il flusso), poi `git push origin v0.2.0`. Il workflow crea la Release da solo.

### Task D6: Prove a mano su un vero Windows (da parte di Marco)

**Files:**
- Create: `docs/PROVE-WINDOWS.md`

Non si può automatizzare, e va detto: **nessuna copia da un telefono vero è mai stata provata su Windows**. Il documento è una lista da spuntare, in italiano semplice.

- [ ] **Step 1:** Scrivere `docs/PROVE-WINDOWS.md` con queste sezioni e le caselle da spuntare:
  1. **Installazione**: doppio clic sul Setup → si apre in italiano, finestra grande; niente richiesta di amministratore; compaiono le due caselle «Icona sul Desktop» e «Menu Start»; alla fine «Apri FotoFacile adesso».
  2. **Avviso SmartScreen**: compare «Windows ha protetto il PC»? (atteso: sì, il programma non è firmato) → «Ulteriori informazioni» → «Esegui comunque». Annotare lo screenshot.
  3. **Avvio**: l'icona sul Desktop apre il programma; il testo è nitido (DPI) su uno schermo al 125–150 %.
  4. **Telefono vero**: cavo → sblocca → «Trasferimento file» → il passo 1 mostra il telefono; **annotare marca/modello e cosa compare**.
  5. **Copia vera**: 5 foto → verificare data (Esplora file → colonna «Data») uguale a quella di scatto, **niente file `.webp`** (a meno di animazioni), nessun file `.part`.
  6. **WebP**: cartella con sticker → per default non compaiono; con «Mostra anche miniature e sticker» sì e vengono convertiti in JPG/PNG.
  7. **Cancellazione**: con collegamento diretto su Windows è **non disponibile** (limite dichiarato): verificare che il messaggio sia chiaro.
  8. **Diagnosi**: menu Start → «FotoFacile - Diagnosi» → si apre il Blocco note con il rapporto.
  9. **Aggiornamento**: installare la 0.2.0 sopra una 0.1.0 già presente → aggiorna, non duplica.
  10. **Disinstallazione**: «App e funzionalità» → Disinstalla → chiede se togliere le impostazioni → le foto copiate restano.
- [ ] **Step 2:** Commit: `git add docs/PROVE-WINDOWS.md && git commit -m "docs: prove da fare a mano su un vero Windows" ` (con la riga `Co-Authored-By`).

---

# PARTE E — Chiusura

### Task E1: Documentazione, grafo e controllo finale

**Files:**
- Modify: `README.md`, `HANDOFF.md`, `docs/PIANO-REVISIONE.md`, `docs/REVISIONE-v0.2.md`

- [ ] **Step 1: Tutta la suite e il lint**

Run: `.venv/bin/python -m pytest tests 2>&1 | tail -3 && .venv/bin/python -m pyflakes fotofacile scripts`
Expected: tutti verdi (il numero sale oltre 385: annotarlo), pyflakes vuoto.

- [ ] **Step 2: Rilettura finale con revisione indipendente** — `code-review` livello `high` sull'intero ramo (`git diff main...revisione-v0.2`); correggere i difetti confermati con lo stesso ciclo rosso/verde; ripetere finché non ne emergono di nuovi.

- [ ] **Step 3: Collaudo end-to-end** (come in `HANDOFF.md`, punto 4): `pilota_app.py` → `"ok": true`, 54 file, nessun `.part`, nessuna sottocartella.

- [ ] **Step 4: Aggiornare i documenti** — `HANDOFF.md` (stato: nuovo numero di test, Parte A–D fatte, cosa **non** è verificato: telefono vero, Windows vero, macOS con telefono; nuovi Failed Approaches se ce ne sono stati; sostituire la sezione «Setup per Windows» con la descrizione del `Setup.exe`); `README.md` (schermate nuove, sezione Windows, WebP); `docs/PIANO-REVISIONE.md` (sezione D1–Dn).

- [ ] **Step 5: Grafo** — `graphify update .`

- [ ] **Step 6: Commit finale**

```bash
git add -A docs README.md HANDOFF.md graphify-out
git commit -m "docs: handoff, README e revisione aggiornati alla v0.2

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 7: ⚠ CHIEDI** se unire `revisione-v0.2` in `main` (`superpowers:finishing-a-development-branch`).

---

## Auto-revisione del piano

**1. Copertura delle richieste di Marco**
- «Migliorare l'interfaccia, più user friendly per gli anziani» → Parte C (C1–C10) + D9/A6 (istruzione «Trasferimento file») + principi 1–8 con test automatici (C10).
- «Revisione completa del codice, fixare bug ed errori» → Parte A: sei difetti concreti (A1–A6, D1–D9) **più** audit sistematico in otto gruppi (A7) con domande precise, registro e chiusura.
- «Le immagini sono uscite in WebP» → Parte B: strumento di diagnosi sui dati veri (B1–B2), conversione sicura (B3–B4), opzione e pacchetto (B5), filtro sticker/miniature (C4, C7).
- «Setup installer per Windows, non bat, un eseguibile» → Parte D: Inno Setup riscritto (D1), `.bat`/`.ps1` rimossi (D3), pipeline che **installa e disinstalla davvero** (D4), costruzione e download (D5), prove a mano (D6).
- «Piano completo con superpowers» → questo documento nel formato `superpowers:writing-plans`.

**2. Segnaposto** — nessun «TBD/TODO». L'unico task senza codice pre-scritto è A7 (audit), per natura: ha procedimento, tabella di domande e criterio di uscita. Il task B2 dipende da dati di Marco e lo dice.

**3. Coerenza dei nomi** — `_TelefonoFinto`/`_piano_singolo` (A1) riusati in A2/B4; `converti_webp` è insieme il campo di `TransferOptions`, la funzione di `core/conversione.py` e la `BooleanVar` di `OptionsPage` (nomi identici di proposito, ruoli diversi: in `transfer.py` la funzione è importata come `converti_webp` e l'opzione letta come `options.converti_webp`); `pillow_disponibile` (B3) importata in `page_options` (B5) con lo stesso nome monkeypatchato dai test; `mostra_dettagli`/`dettagli_visibili` (C5) usati da `conftest.azzera`; `azione_principale`/`azione_indietro` definite in C6–C9 e chiamate in C5; `Impostazioni`/`SCALE_AMMESSE` (C1) usate in C2 e C5.

**Rischi noti**
- Il tema `clam` può non avere il glifo di ✔ ⚠ ✖ in tutti i font: C10 lo verifica a schermo e prevede il ripiego a parole.
- Il cambio di dimensione del testo ricrea le pagine: per questo i pulsanti stanno **solo** nel passo 1 (nessuno stato da perdere).
- SmartScreen mostrerà l'avviso finché il programma non è firmato (certificato a pagamento): dichiarato in `Benvenuto.txt`, nel LEGGIMI e in `PROVE-WINDOWS.md`. **Decisione per Marco:** acquistare un certificato di firma del codice? Non è nel piano.
- Il collegamento diretto di Windows e Linux resta non provato su hardware vero: qualunque telefono reale può mostrare difetti che nessun test simulato vede.

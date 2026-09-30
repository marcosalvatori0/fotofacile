# FotoFacile — Piano di Implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Un'app desktop Tkinter in italiano che copia foto e video da un telefono Android al computer guidando l'utente in 4 passi, senza gestore file e senza gergo tecnico.

**Architecture:** `fotofacile/core/` contiene logica pura e testabile (nessun import di Tkinter) che parla con il telefono tramite un'interfaccia `AdbBackend` (implementata da `RealAdbBackend` e da `FakeAdbBackend` per test e demo). `fotofacile/ui/` è uno strato sottile Tkinter: procedura guidata a 4 pagine, tutto il lavoro di rete su thread worker che comunicano con la UI via `queue.Queue` drenata da `after()`.

**Tech Stack:** Python 3.9+ standard library (Tkinter, subprocess, threading, queue, json, zipfile, urllib), `adb` di Android platform-tools (installato automaticamente dall'app se assente), pytest solo in sviluppo.

**Spec:** `docs/superpowers/specs/2026-09-28-fotofacile-design.md`

## Modifiche decise durante l'esecuzione

1. **Niente thread (obbligatorio, non opzionale).** Verificato sul campo: su macOS con **Tk 9**
   (Homebrew, Python 3.14) creare un thread mentre la finestra è aperta blocca l'intero
   processo; con Tk 8.5/8.6 funziona. Poiché il programma deve funzionare anche lì, il motore è
   stato riscritto in forma **cooperativa**: `core/ops.py` (processi esterni e download a passi)
   e `core/adb_passi.py` (operazioni adb a passi), con `App.run_task` che avanza i generatori
   con `after()`. `App.run_async` e la coda `queue.Queue` sono stati rimossi; i test che li
   usavano sono stati sostituiti da test sui generatori.
2. **Rifattorizzazione della copia:** `core/transfer.py` espone `transfer_steps(...)`
   (generatore, stessa orchestrazione di prima: retry, verifica, `.part`, cancella-dopo,
   cronologia) e `transfer(...)` come involucro diretto per test e riga di comando. Il
   "copiatore" è iniettabile: `CopiatoreInterno` (demo/test) oppure `AdbAPassi` (telefono vero).
3. **Collaudo dell'interfaccia in un processo separato:** `tests/test_app_completa.py` e
   `tests/pilota_app.py`; i test grafici si saltano da soli (`tk_available()` esegue una prova
   in un processo con tempo massimo) perché in alcuni ambienti di automazione la finestra non
   può essere creata affatto.

4. **Correzioni dalla revisione indipendente:** vedi «10-bis» della specifica; i test
   corrispondenti sono in `tests/test_robustezza.py` (errori di disco, abbandono a metà copia,
   cronologia non scrivibile, ritentativi inutili, maiuscole, stato `no permissions`, apertura
   cartella multipiattaforma).
5. **Seconda revisione (dopo la prima consegna):** vedi `docs/PIANO-REVISIONE.md`. Il
   trasporto non è più solo ADB: `core/trasporto.py` sceglie da sé fra collegamento diretto
   (PTP/ImageCaptureCore su macOS, WPD su Windows, MTP/`gio` su Linux, tramite
   `fotofacile/aiutanti/`) e ADB, che resta solo come scorciatoia se il Debug USB è già
   attivo. La copia è **piatta** per impostazione predefinita (`preserve_structure=False`) e i
   difetti B1–B24 sono corretti (suite a 373 test).

> **Nota:** le attività con le caselle qui sotto sono il piano della **prima** versione: dove
> parlano di Debug USB obbligatorio o di cartelle del telefono mantenute descrivono il
> comportamento di allora, non quello attuale. Lo stato corrente è in `HANDOFF.md`.

## Global Constraints

- Runtime: **solo libreria standard**; nessun `pip install` richiesto all'utente finale.
- **Multi-piattaforma (requisito primario): Windows, macOS e Linux.** Nessun modulo fuori da
  `core/osutil.py`, `core/adb.py`, `core/installer.py`, `ui/theme.py` può riferirsi a un
  sistema operativo specifico; i test devono passare su tutti e tre (niente percorsi assoluti
  di un solo sistema nei test: si iniettano `is_windows`/`system` come parametri).
- La UI è **in italiano semplice**: mai la parola "ADB", "shell", "path", "thread", "server" a schermo.
- `fotofacile/core/*` non deve mai importare `tkinter`.
- Ogni errore di `core` è `FotoFacileError` (o sottoclasse) con `message` (frase umana italiana) e `hint` (azione suggerita).
- Nessun file parziale con nome definitivo: si scrive `<destinazione>.part` e si rinomina con `os.replace` solo dopo verifica.
- Comandi shell sul telefono: ogni percorso è quotato con `shell_quote`.
- Test: `python3 -m pytest tests -q` (venv di sviluppo in `.venv`).
- Commit piccoli e frequenti, messaggi in italiano, prefisso `feat:`/`test:`/`docs:`.

## Review Focus

1. Nomi file con spazi, apostrofi, `#`, `&`, `|`, parentesi o emoji → devono copiarsi; `shell_quote` li copre con test dedicati (Task 2, Task 5).
2. Annullamento a metà di un file grande → nessun `.part` residuo e nessun file troncato (Task 8).
3. Spazio disco insufficiente a metà copia o in pianificazione → errore umano, nessun file corrotto (Task 7, Task 8).
4. Perdita di connessione USB a metà copia → retry poi errore nel resoconto senza interrompere il ciclo (Task 8).
5. Due telefoni collegati → si usa sempre il seriale scelto dall'utente (Task 3, Task 6).
6. Cronologia corrotta o cancellata a mano → nessun crash, backup e ricostruzione (Task 6).
7. Nome di file non valido su Windows (`IMG:01?.jpg`), riservato (`CON.jpg`), con spazi/punti
   finali o lunghissimo → nome reso sicuro, cartella usabile su tutti i sistemi (Task 7).
8. Due telefoni collegati → si usa sempre il seriale scelto dall'utente (Task 3, Task 6).
9. File manager assente o comando di apertura fallito (Windows senza `explorer` nel PATH,
   Linux senza `xdg-open`) → messaggio con il percorso da copiare, mai un errore tecnico (Task 12).

## File Structure

| File | Responsabilità |
|---|---|
| `fotofacile.py` | avvio: `python3 fotofacile.py` → `cli.main()` |
| `fotofacile/cli.py` | argomenti (`--demo`, `doctor`, `--help`), avvio GUI o diagnostica |
| `fotofacile/core/errors.py` | `FotoFacileError`, `AdbError`, `TransferError` |
| `fotofacile/core/adb.py` | trovare `adb`, eseguire comandi, `shell_quote`, `AdbBackend` + `RealAdbBackend` |
| `fotofacile/core/devices.py` | `DeviceInfo`, parsing `adb devices -l`, etichette di stato |
| `fotofacile/core/format.py` | formattazione italiana di dimensioni, velocità, tempi, date |
| `fotofacile/core/scanner.py` | `MediaFile`, comando di scansione, parsing flusso `stat`, raggruppamento cartelle |
| `fotofacile/core/history.py` | archivio JSON per-dispositivo dei file già copiati, scrittura atomica |
| `fotofacile/core/planner.py` | `TransferOptions`, `PlannedFile`, `TransferPlan`, filtri, dedup, collisioni |
| `fotofacile/core/transfer.py` | copia con avanzamento, annulla, retry, verifica, cancella-dopo |
| `fotofacile/core/report.py` | resoconto testuale finale salvabile su file |
| `fotofacile/core/installer.py` | download/estrazione platform-tools, rilevamento presenza |
| `fotofacile/core/demo.py` | `FakeAdbBackend` per test e modalità demo |
| `fotofacile/ui/theme.py` | colori, font, stile ttk, pulsanti grandi |
| `fotofacile/ui/widgets.py` | `StepIndicator`, `LogPane`, `Banner`, `PathChooser` |
| `fotofacile/ui/app.py` | `App(tk.Tk)`: contenitore pagine, navigazione, worker, coda eventi |
| `fotofacile/ui/page_connect.py` | Passo 1 |
| `fotofacile/ui/page_select.py` | Passo 2 |
| `fotofacile/ui/page_options.py` | Passo 3 |
| `fotofacile/ui/page_transfer.py` | Passo 4 e resoconto |
| `tests/test_*.py` | un file per modulo core + `test_ui_smoke.py` |
| `README.md` | istruzioni per l'utente finale (italiano) |

---

### Task 1: Impalcatura del progetto e setup dei test

**Files:**
- Create: `pytest.ini`, `requirements-dev.txt`, `fotofacile/__init__.py`, `fotofacile/core/__init__.py`, `fotofacile/ui/__init__.py`, `tests/__init__.py`, `tests/test_package.py`, `scripts/run_tests.sh`

**Interfaces:**
- Consumes: nulla
- Produces: `fotofacile.__version__: str = "0.1.0"`; comando di test `python3 -m pytest tests -q`

- [ ] **Step 1: Test che fallisce**

`tests/test_package.py`
```python
import fotofacile


def test_version_esposta():
    assert fotofacile.__version__ == "0.1.0"


def test_core_importabile():
    import fotofacile.core  # noqa: F401
```

- [ ] **Step 2: Verificare che fallisca**

Run: `.venv/bin/python -m pytest tests -q`
Expected: FAIL/ERROR con `ModuleNotFoundError: No module named 'fotofacile'`

- [ ] **Step 3: Creare impalcatura**

`fotofacile/__init__.py`
```python
"""FotoFacile: trasferimento guidato di foto da Android al computer."""

__version__ = "0.1.0"
```
`fotofacile/core/__init__.py`, `fotofacile/ui/__init__.py`, `tests/__init__.py`: vuoti (solo docstring).
`pytest.ini`
```ini
[pytest]
testpaths = tests
addopts = -q
filterwarnings = error
```
`requirements-dev.txt`
```text
pytest>=8
```
`scripts/run_tests.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec .venv/bin/python -m pytest tests "$@"
```

- [ ] **Step 4: Verificare che passi**

Run: `.venv/bin/python -m pytest tests -q`
Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "chore: impalcatura progetto e setup pytest"
```

---

### Task 2: Errori e strato ADB

**Files:**
- Create: `fotofacile/core/errors.py`, `fotofacile/core/adb.py`, `tests/test_adb.py`

**Interfaces:**
- Consumes: nulla
- Produces:
  - `FotoFacileError(message: str, hint: str = "")` con attributi `.message`, `.hint`
  - `AdbError(FotoFacileError)`
  - `shell_quote(value: str) -> str`
  - `ADB_EXECUTABLE: str` (`"adb.exe"` su Windows, `"adb"` altrove) — calcolato da `sys.platform`
  - `find_adb(env: Mapping[str,str] | None = None, extra_dirs: Sequence[Path] = (), is_windows: bool | None = None) -> str | None`
  - `AdbBackend` (Protocol) con `check() -> str`, `devices_raw() -> str`, `list_media_raw(serial: str, command: str) -> str`, `stream_file(serial: str, remote_path: str, chunk_size: int = 65536) -> Iterator[bytes]`, `delete_file(serial: str, remote_path: str) -> None`, `start_server() -> None`, `restart_server() -> None`
  - `RealAdbBackend(adb_path: str, scan_timeout: int = 120, pull_timeout: int = 900)`

- [ ] **Step 1: Test che falliscono**

`tests/test_adb.py`
```python
import subprocess
from pathlib import Path

import pytest

from fotofacile.core.adb import AdbBackend, RealAdbBackend, find_adb, shell_quote
from fotofacile.core.errors import AdbError, FotoFacileError


def test_shell_quote_lascia_intatti_i_percorsi_normali():
    assert shell_quote("/sdcard/DCIM/Camera") == "'/sdcard/DCIM/Camera'"


def test_shell_quote_gestisce_apostrofi_e_spazi():
    assert shell_quote("/sdcard/Le mie foto/Vacanze d'estate.jpg") == (
        "'/sdcard/Le mie foto/Vacanze d\\'estate.jpg'"
    )


def test_shell_quote_gestisce_dollaro_e_backtick():
    assert shell_quote("/sdcard/a$b`c`") == "'/sdcard/a$b`c`'"
    assert shell_quote("") == "''"


def test_find_adb_preferisce_la_variabile_di_ambiente(tmp_path):
    finto = tmp_path / "adb"
    finto.write_text("#!/bin/sh\n")
    assert find_adb(env={"FOTOFACILE_ADB": str(finto)}, extra_dirs=(), is_windows=False) == str(finto)


def test_find_adb_usa_il_componente_scaricato_dalla_app(tmp_path):
    home = tmp_path / "home"
    adb = home / ".fotofacile" / "platform-tools" / "adb"
    adb.parent.mkdir(parents=True)
    adb.write_text("#!/bin/sh\n")
    assert find_adb(env={"HOME": str(home), "PATH": ""}, extra_dirs=(), is_windows=False) == str(adb)


def test_find_adb_ignora_variabile_inesistente_e_cerca_nel_percorso(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    adb = bin_dir / "adb"
    adb.write_text("#!/bin/sh\n")
    result = find_adb(env={"FOTOFACILE_ADB": str(tmp_path / "nope"), "PATH": str(bin_dir)}, is_windows=False)
    assert result == str(adb)


def test_find_adb_ritorna_none_se_assente(tmp_path):
    assert find_adb(env={"PATH": str(tmp_path / "vuoto")}, extra_dirs=(), is_windows=False) is None


def test_find_adb_su_windows_cerca_adb_exe_nel_profilo(tmp_path):
    utente = tmp_path / "utente"
    adb = utente / ".fotofacile" / "platform-tools" / "adb.exe"
    adb.parent.mkdir(parents=True)
    adb.write_text("")
    trovato = find_adb(env={"USERPROFILE": str(utente), "PATH": ""}, extra_dirs=(), is_windows=True)
    assert trovato == str(adb)


def test_find_adb_su_windows_cerca_nel_sdk_android(tmp_path):
    locale = tmp_path / "AppData" / "Local"
    adb = locale / "Android" / "Sdk" / "platform-tools" / "adb.exe"
    adb.parent.mkdir(parents=True)
    adb.write_text("")
    trovato = find_adb(env={"LOCALAPPDATA": str(locale), "PATH": ""}, extra_dirs=(), is_windows=True)
    assert trovato == str(adb)


def test_errore_espone_messaggio_e_suggerimento():
    err = AdbError("Il telefono non risponde", hint="Ricollega il cavo")
    assert isinstance(err, FotoFacileError)
    assert err.message == "Il telefono non risponde"
    assert err.hint == "Ricollega il cavo"


def test_backend_reale_comando_fallito_diventa_errore_umano(tmp_path):
    finto = tmp_path / "adb"
    finto.write_text("#!/bin/sh\nexit 1\n")
    finto.chmod(0o755)
    backend = RealAdbBackend(str(finto))
    with pytest.raises(AdbError) as exc:
        backend.devices_raw()
    assert "telefono" in exc.value.message.lower() or "collegamento" in exc.value.message.lower()
    assert exc.value.hint


def test_backend_reale_stream_usa_il_seriale_corretto(tmp_path):
    finto = tmp_path / "adb"
    finto.write_text("#!/bin/sh\nprintf 'cattura-argomenti: %s\\n' \"$@\"\n")
    finto.chmod(0o755)
    backend = RealAdbBackend(str(finto))
    with pytest.raises(AdbError):
        # il backend deve passare -s SERIAL e exec-out al sottoprocesso
        list(backend.stream_file("SERIAL123", "/sdcard/DCIM/a.jpg"))
    with pytest.raises(AdbError):
        backend.delete_file("SERIAL123", "/sdcard/DCIM/a.jpg")
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_adb.py -q`
Expected: FAIL con `ModuleNotFoundError: No module named 'fotofacile.core.adb'`

- [ ] **Step 3: Implementare**

`fotofacile/core/errors.py`
```python
"""Errori di FotoFacile, sempre con un messaggio comprensibile e un suggerimento."""


class FotoFacileError(Exception):
    """Errore con messaggio per l'utente e un suggerimento su come procedere."""

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:  # pragma: no cover - semplice composizione
        return self.message if not self.hint else f"{self.message} {self.hint}"


class AdbError(FotoFacileError):
    """Errore di comunicazione con il telefono."""


class TransferError(FotoFacileError):
    """Errore durante la copia di un file."""
```

`fotofacile/core/adb.py`
```python
"""Comunicazione con il telefono tramite l'eseguibile adb (Android platform-tools)."""

from __future__ import annotations

import shutil
import subprocess
from itertools import islice
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

from .errors import AdbError

CHUNK_SIZE = 64 * 1024


def shell_quote(value: str) -> str:
    """Quota un percorso per la shell del telefono (sempre POSIX: la shell è su Android)."""
    return "'" + value.replace("'", "'\\''") + "'"


def find_adb(
    env: Mapping[str, str] | None = None,
    extra_dirs: Sequence[Path] = (),
    is_windows: bool | None = None,
) -> str | None:
    """Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato, PATH, percorsi noti."""
    import os

    environment = dict(env if env is not None else os.environ)
    windows = (os.name == "nt") if is_windows is None else is_windows
    eseguibile = "adb.exe" if windows else "adb"

    candidato = environment.get("FOTOFACILE_ADB", "")
    if candidato and Path(candidato).is_file():
        return candidato

    home = environment.get("USERPROFILE") if windows else None
    home = home or environment.get("HOME") or str(Path.home())
    noti: list[Path] = [Path(home) / ".fotofacile" / "platform-tools" / eseguibile]
    if windows:
        for base in (environment.get("LOCALAPPDATA"), environment.get("USERPROFILE")):
            if base:
                noti.append(Path(base) / "Android" / "Sdk" / "platform-tools" / eseguibile)
        noti.append(Path("C:/platform-tools") / eseguibile)
    else:
        noti.extend(
            [
                Path("/opt/homebrew/bin/adb"),
                Path("/usr/local/bin/adb"),
                Path(home) / "Library" / "Android" / "sdk" / "platform-tools" / "adb",
                Path("/usr/bin/adb"),
            ]
        )
    noti.extend(Path(p) for p in extra_dirs)
    for percorso in noti:
        if percorso.is_file():
            return str(percorso)

    return shutil.which(eseguibile, path=environment.get("PATH", ""))


class RealAdbBackend:
    """Implementazione reale dell'interfaccia verso adb."""

    def __init__(self, adb_path: str, scan_timeout: int = 120, pull_timeout: int = 900) -> None:
        self.adb_path = adb_path
        self.scan_timeout = scan_timeout
        self.pull_timeout = pull_timeout

    def _run(self, args: Sequence[str], timeout: int | None = None, umano: str = "") -> subprocess.CompletedProcess:
        comando = [self.adb_path, *args]
        try:
            esito = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=timeout or 30,
            )
        except FileNotFoundError as exc:
            raise AdbError(
                "Non riesco a usare il componente di collegamento.",
                hint="Apri il programma e premi «Installa componente».",
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise AdbError(
                umano or "Il telefono non ha risposto in tempo.",
                hint="Controlla il cavo e riprova; se serve, premi «Riavvia collegamento».",
            ) from exc
        if esito.returncode != 0:
            raise AdbError(
                umano or "Il collegamento con il telefono si è interrotto.",
                hint="Sblocca il telefono, controlla il cavo e riprova.",
            )
        return esito

    def check(self) -> str:
        esito = self._run(["version"], umano="Il componente di collegamento non è utilizzabile.")
        return esito.stdout.strip().splitlines()[0] if esito.stdout.strip() else "adb"

    def devices_raw(self) -> str:
        return self._run(["devices", "-l"]).stdout

    def list_media_raw(self, serial: str, command: str) -> str:
        esito = self._run(
            ["-s", serial, "shell", command],
            timeout=self.scan_timeout,
            umano="La ricerca delle foto sul telefono non è andata a buon fine.",
        )
        return esito.stdout

    def stream_file(
        self,
        serial: str,
        remote_path: str,
        chunk_size: int = CHUNK_SIZE,
    ) -> Iterator[bytes]:
        processo = subprocess.Popen(
            [self.adb_path, "-s", serial, "exec-out", "cat", shell_quote(remote_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            assert processo.stdout is not None
            while True:
                blocco = processo.stdout.read(chunk_size)
                if not blocco:
                    break
                yield blocco
        finally:
            _, errore = processo.communicate()
            if processo.returncode not in (0, None):
                raise AdbError(
                    "Non sono riuscito a leggere un file dal telefono.",
                    hint="Il telefono potrebbe essersi scollegato: ricontrolla il cavo.",
                )

    def delete_file(self, serial: str, remote_path: str) -> None:
        self._run(
            ["-s", serial, "shell", "rm", "-f", shell_quote(remote_path)],
            umano="Non sono riuscito a cancellare un file dal telefono.",
        )

    def start_server(self) -> None:
        self._run(["start-server"], umano="Non riesco ad avviare il collegamento.")

    def restart_server(self) -> None:
        try:
            self._run(["kill-server"])
        except AdbError:
            pass
        self.start_server()
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutti i test passano.

Nota: se `test_backend_reale_stream_usa_il_seriale_corretto` non produce errore (script finto che esce 0), adattare lo script finto a `exit 1` per far scattare `AdbError`.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: strato adb multipiattaforma (adb/adb.exe, percorsi Windows e POSIX)"
```

---

### Task 2b: Differenze di sistema (`core/osutil.py`)

**Files:**
- Create: `fotofacile/core/osutil.py`, `tests/test_osutil.py`

**Interfaces:**
- Consumes: `FotoFacileError` (Task 2)
- Produces:
  - `TEMP_SPAZI = ""`; `app_dir(env=None) -> Path` (`%USERPROFILE%\.fotofacile` su Windows, `~/.fotofacile` altrove)
  - `default_photos_dir(env=None) -> Path`
  - `file_manager_command(path: Path, system: str) -> list[str]`
  - `open_in_file_manager(path: Path, system: str | None = None, runner: Callable[..., subprocess.CompletedProcess | int] | None = None) -> None` (solleva `FotoFacileError` con percorso nel messaggio se fallisce)
  - `is_case_insensitive_fs(system: str | None = None) -> bool` (True su Windows e macOS)
  - `python_command(system: str | None = None) -> str` (`"py"` su Windows, `"python3"` altrove)

- [ ] **Step 1: Test che falliscono**

`tests/test_osutil.py`
```python
import subprocess
from pathlib import Path

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.core.osutil import (
    app_dir,
    default_photos_dir,
    file_manager_command,
    is_case_insensitive_fs,
    open_in_file_manager,
    python_command,
)


def test_cartella_app_multipiattaforma(tmp_path):
    assert app_dir(env={"HOME": str(tmp_path)}) == tmp_path / ".fotofacile"
    assert app_dir(env={"USERPROFILE": str(tmp_path), "HOME": "/altro"}) == tmp_path / ".fotofacile"


def test_cartella_foto_predefinita(tmp_path):
    assert default_photos_dir(env={"HOME": str(tmp_path)}) == tmp_path / "Pictures" / "FotoFacile"


def test_comando_di_apertura_per_sistema():
    percorso = Path("/tmp/foto")
    assert file_manager_command(percorso, "darwin") == ["open", "/tmp/foto"]
    assert file_manager_command(percorso, "win32") == ["explorer", "/tmp/foto"]
    assert file_manager_command(percorso, "linux") == ["xdg-open", "/tmp/foto"]


def test_apertura_cartella_usa_il_comando_giusto():
    chiamate = []

    def runner(comando, **kwargs):
        chiamate.append(comando)
        return subprocess.CompletedProcess(comando, 0)

    open_in_file_manager(Path("/tmp/foto"), system="linux", runner=runner)
    assert chiamate == [["xdg-open", "/tmp/foto"]]


def test_apertura_cartella_fallita_mostra_il_percorso():
    def runner(comando, **kwargs):
        raise FileNotFoundError(comando[0])

    with pytest.raises(FotoFacileError) as exc:
        open_in_file_manager(Path("/tmp/foto"), system="linux", runner=runner)
    assert "/tmp/foto" in exc.value.message
    assert exc.value.hint


def test_codice_di_uscita_diverso_da_zero_e_un_errore():
    def runner(comando, **kwargs):
        return subprocess.CompletedProcess(comando, 1)

    with pytest.raises(FotoFacileError):
        open_in_file_manager(Path("/tmp/foto"), system="win32", runner=runner)


def test_sensibilita_maiuscole_per_sistema():
    assert is_case_insensitive_fs("win32") is True
    assert is_case_insensitive_fs("darwin") is True
    assert is_case_insensitive_fs("linux") is False


def test_comando_python_per_sistema():
    assert python_command("win32") == "py"
    assert python_command("darwin") == "python3"
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_osutil.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/osutil.py`
```python
"""Unico punto in cui il programma si adatta al sistema operativo."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Mapping

from .errors import FotoFacileError

COMANDI_APERTURA = {
    "darwin": "open",
    "win32": "explorer",
    "linux": "xdg-open",
}


def _system(system: str | None) -> str:
    return system or sys.platform


def app_dir(env: Mapping[str, str] | None = None) -> Path:
    """Cartella dati dell'app: su Windows %USERPROFILE%, altrove la home."""
    ambiente = dict(env if env is not None else os.environ)
    base = ambiente.get("USERPROFILE") or ambiente.get("HOME") or str(Path.home())
    return Path(base) / ".fotofacile"


def default_photos_dir(env: Mapping[str, str] | None = None) -> Path:
    return Path(app_dir(env)).parent / "Pictures" / "FotoFacile"


def file_manager_command(path: Path, system: str) -> list[str]:
    eseguibile = COMANDI_APERTURA.get(system, "xdg-open")
    return [eseguibile, str(path)]


def open_in_file_manager(
    path: Path,
    system: str | None = None,
    runner: Callable[..., object] | None = None,
) -> None:
    """Apre la cartella nel file manager del sistema, con errore comprensibile se non riesce."""
    comando = file_manager_command(Path(path), _system(system))
    esegui = runner or subprocess.run
    try:
        esito = esegui(comando, check=False)
    except OSError as exc:
        raise FotoFacileError(
            f"Non riesco ad aprire la cartella {path}.",
            hint=f"Apri manualmente questa cartella: {path}",
        ) from exc
    codice = getattr(esito, "returncode", 0)
    if codice not in (0, None):
        raise FotoFacileError(
            f"Non riesco ad aprire la cartella {path}.",
            hint=f"Apri manualmente questa cartella: {path}",
        )


def is_case_insensitive_fs(system: str | None = None) -> bool:
    return _system(system) in ("win32", "darwin", "cygwin")


def python_command(system: str | None = None) -> str:
    return "py" if _system(system) == "win32" else "python3"
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: differenze di sistema isolate in osutil (apertura cartella, sensibilità maiuscole)"
```

---

### Task 3: Scoperta dispositivi

**Files:**
- Create: `fotofacile/core/devices.py`, `tests/test_devices.py`

**Interfaces:**
- Consumes: `AdbBackend`, `AdbError` (Task 2)
- Produces:
  - `DeviceInfo(serial: str, state: str, model: str, product: str)` (frozen dataclass) con proprietà `display_name -> str` e `is_ready -> bool`
  - `parse_devices(output: str) -> list[DeviceInfo]`
  - `get_devices(adb: AdbBackend) -> list[DeviceInfo]`
  - `pick_device(devices: Sequence[DeviceInfo], serial: str | None = None) -> DeviceInfo | None`
  - `STATE_MESSAGE: dict[str, tuple[str, str]]` (messaggio, suggerimento)

- [ ] **Step 1: Test che falliscono**

`tests/test_devices.py`
```python
from fotofacile.core.devices import (
    STATE_MESSAGE,
    DeviceInfo,
    get_devices,
    parse_devices,
    pick_device,
)


LISTA_VUOTA = "List of devices attached\n\n"
LISTA_UNO = (
    "List of devices attached\n"
    "R5CT30ABCDE            device product:a52q model:SM_A525F device:a52 transport_id:2\n"
)
LISTA_NON_AUTORIZZATO = (
    "List of devices attached\n"
    "0123456789ABCDEF       unauthorized transport_id:3\n"
)
LISTA_DUE = (
    "List of devices attached\n"
    "* daemon started successfully\n"
    "R5CT30ABCDE            device product:a52q model:SM_A525F device:a52 transport_id:2\n"
    "emulator-5554          offline\n"
)


def test_lista_vuota():
    assert parse_devices(LISTA_VUOTA) == []


def test_un_dispositivo_pronto():
    (dispositivo,) = parse_devices(LISTA_UNO)
    assert dispositivo.serial == "R5CT30ABCDE"
    assert dispositivo.state == "device"
    assert dispositivo.model == "SM_A525F"
    assert dispositivo.is_ready is True
    assert dispositivo.display_name == "SM A525F"


def test_dispositivo_non_autorizzato_non_pronto():
    (dispositivo,) = parse_devices(LISTA_NON_AUTORIZZATO)
    assert dispositivo.state == "unauthorized"
    assert dispositivo.is_ready is False
    assert "Consenti" in STATE_MESSAGE["unauthorized"][0]


def test_lista_con_righe_spurie_e_due_dispositivi():
    dispositivi = parse_devices(LISTA_DUE)
    assert [d.serial for d in dispositivi] == ["R5CT30ABCDE", "emulator-5554"]
    assert dispositivi[1].state == "offline"
    assert dispositivi[1].model == ""


def test_modello_vuoto_ricade_sul_seriale():
    dispositivo = DeviceInfo(serial="ABC", state="device", model="", product="")
    assert dispositivo.display_name == "ABC"


def test_pick_device_sceglie_il_primo_pronto():
    dispositivi = parse_devices(LISTA_DUE)
    pronto = DeviceInfo(serial="X", state="device", model="Pixel", product="p")
    assert pick_device([*dispositivi, pronto]) is pronto


def test_pick_device_rispetta_il_seriale_richiesto():
    dispositivi = parse_devices(LISTA_DUE)
    assert pick_device(dispositivi, serial="emulator-5554").state == "offline"


def test_pick_device_none_senza_dispositivi():
    assert pick_device([]) is None


def test_get_devices_usa_il_backend():
    class BackendFinto:
        def devices_raw(self) -> str:
            return LISTA_UNO

    (dispositivo,) = get_devices(BackendFinto())
    assert dispositivo.serial == "R5CT30ABCDE"
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_devices.py -q`
Expected: FAIL con `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/devices.py`
```python
"""Riconoscimento dei telefoni collegati e traduzione dei loro stati."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .adb import AdbBackend

STATE_MESSAGE: dict[str, tuple[str, str]] = {
    "device": ("Telefono collegato e pronto.", ""),
    "unauthorized": (
        "Telefono trovato! Sbloccalo e tocca «Consenti» sullo schermo.",
        "Se non appare la richiesta, scollega e ricollega il cavo.",
    ),
    "offline": (
        "Il telefono non risponde.",
        "Scollega e ricollega il cavo, poi premi «Riavvia collegamento».",
    ),
    "no permissions": (
        "Il computer non ha il permesso di parlare con il telefono.",
        "Scollega e ricollega il cavo.",
    ),
}


@dataclass(frozen=True)
class DeviceInfo:
    serial: str
    state: str
    model: str = ""
    product: str = ""

    @property
    def is_ready(self) -> bool:
        return self.state == "device"

    @property
    def display_name(self) -> str:
        if self.model:
            return self.model.replace("_", " ").strip()
        return self.serial


def parse_devices(output: str) -> list[DeviceInfo]:
    """Estrae i dispositivi dall'output di `adb devices -l`."""
    dispositivi: list[DeviceInfo] = []
    for riga in output.splitlines():
        riga = riga.strip()
        if not riga or riga.endswith("attached") or riga.startswith("*"):
            continue
        campi = riga.split()
        if len(campi) < 2:
            continue
        serial, state = campi[0], campi[1]
        extra = {}
        for campo in campi[2:]:
            if ":" in campo:
                chiave, _, valore = campo.partition(":")
                extra[chiave] = valore
        dispositivi.append(
            DeviceInfo(
                serial=serial,
                state=state,
                model=extra.get("model", ""),
                product=extra.get("product", ""),
            )
        )
    return dispositivi


def get_devices(adb: AdbBackend) -> list[DeviceInfo]:
    return parse_devices(adb.devices_raw())


def pick_device(devices: Sequence[DeviceInfo], serial: str | None = None) -> DeviceInfo | None:
    """Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo pronto."""
    if serial is not None:
        for dispositivo in devices:
            if dispositivo.serial == serial:
                return dispositivo
        return None
    for dispositivo in devices:
        if dispositivo.is_ready:
            return dispositivo
    return None
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: scoperta dispositivi e traduzione stati in italiano"
```

---

### Task 4: Formattazione italiana

**Files:**
- Create: `fotofacile/core/format.py`, `tests/test_format.py`

**Interfaces:**
- Consumes: nulla
- Produces: `format_size(num_bytes: int) -> str`, `format_speed(bytes_per_second: float) -> str`, `format_duration(seconds: float) -> str`, `format_eta(seconds: float | None) -> str`, `format_date(epoch: int) -> str`, `parse_date(text: str) -> int | None`

- [ ] **Step 1: Test che falliscono**

`tests/test_format.py`
```python
import pytest

from fotofacile.core.format import (
    format_date,
    format_duration,
    format_eta,
    format_size,
    format_speed,
    parse_date,
)


@pytest.mark.parametrize(
    ("byte", "atteso"),
    [
        (0, "0 B"),
        (512, "512 B"),
        (1024, "1,0 KB"),
        (1536, "1,5 KB"),
        (10 * 1024**2, "10,0 MB"),
        (3_650_722_022, "3,4 GB"),
    ],
)
def test_formato_dimensione(byte, atteso):
    assert format_size(byte) == atteso


def test_formato_velocita():
    assert format_speed(2 * 1024**2) == "2,0 MB/s"
    assert format_speed(0) == "—"


def test_formato_durata_e_tempo_rimanente():
    assert format_duration(45) == "45 secondi"
    assert format_duration(90) == "1 minuto e 30 secondi"
    assert format_duration(3725) == "1 ora e 2 minuti"
    assert format_eta(None) == "calcolo in corso…"
    assert format_eta(0) == "meno di un secondo"


def test_formato_data_italiana():
    assert format_date(1_700_000_000) == "14/11/2023"


def test_parse_date_accetta_formati_comodi():
    assert parse_date("2024-05-01") is not None
    assert parse_date("01/05/2024") is not None
    assert parse_date("") is None
    assert parse_date("non una data") is None
    assert parse_date("2024-05-01") < parse_date("2024-05-02")
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_format.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/format.py`
```python
"""Formattazione in italiano di dimensioni, velocità, tempi e date."""

from __future__ import annotations

from datetime import datetime

UNITA = ("B", "KB", "MB", "GB", "TB")


def format_size(num_bytes: int) -> str:
    valore = float(max(num_bytes, 0))
    for unita in UNITA:
        if valore < 1024 or unita == UNITA[-1]:
            if unita == "B":
                return f"{int(valore)} B"
            return f"{valore:.1f}".replace(".", ",") + f" {unita}"
        valore /= 1024
    return f"{valore:.1f} {UNITA[-1]}"


def format_speed(bytes_per_second: float) -> str:
    if bytes_per_second <= 0:
        return "—"
    return f"{format_size(int(bytes_per_second))}/s"


def format_duration(seconds: float) -> str:
    secondi = int(round(seconds))
    if secondi < 60:
        return f"{secondi} secondi" if secondi != 1 else "1 secondo"
    minuti, sec = divmod(secondi, 60)
    if minuti < 60:
        testo = f"{minuti} minuti" if minuti != 1 else "1 minuto"
        return f"{testo} e {sec} secondi" if sec else testo
    ore, minuti = divmod(minuti, 60)
    testo = f"{ore} ore" if ore != 1 else "1 ora"
    return f"{testo} e {minuti} minuti" if minuti else testo


def format_eta(seconds: float | None) -> str:
    if seconds is None:
        return "calcolo in corso…"
    if seconds < 1:
        return "meno di un secondo"
    return f"circa {format_duration(seconds)}"


def format_date(epoch: int) -> str:
    return datetime.fromtimestamp(epoch).strftime("%d/%m/%Y")


def parse_date(text: str) -> int | None:
    """Accetta «AAAA-MM-GG» o «GG/MM/AAAA»; None se vuoto o non interpretabile."""
    testo = (text or "").strip()
    if not testo:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return int(datetime.strptime(testo, formato).timestamp())
        except ValueError:
            continue
    return None
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: formattazione italiana di dimensioni, tempi e date"
```

---

### Task 5: Scansione dei file multimediali sul telefono

**Files:**
- Create: `fotofacile/core/scanner.py`, `tests/test_scanner.py`

**Interfaces:**
- Consumes: `AdbBackend` (Task 2), `shell_quote` (Task 2), `format_size` (Task 4)
- Produces:
  - `PHOTO_EXTENSIONS: tuple[str, ...]`, `VIDEO_EXTENSIONS: tuple[str, ...]`, `EXTENSIONS: tuple[str, ...]`
  - `DEFAULT_ROOTS: tuple[str, ...]`, `FALLBACK_ROOT: str = "/sdcard"`
  - `MediaFile(remote_path: str, size: int, mtime: int, kind: str)` con `name` e `parent`
  - `MediaFolder(remote_path: str, label: str, file_count: int, total_size: int)`
  - `parse_stat_stream(output: str) -> list[MediaFile]`
  - `build_scan_command(roots: Sequence[str], include_videos: bool = True, max_depth: int | None = None) -> str`
  - `list_media(adb: AdbBackend, serial: str, roots: Sequence[str] = DEFAULT_ROOTS, include_videos: bool = True, cancel: threading.Event | None = None) -> list[MediaFile]`
  - `group_folders(files: Sequence[MediaFile]) -> list[MediaFolder]`

- [ ] **Step 1: Test che falliscono**

`tests/test_scanner.py`
```python
import threading

from fotofacile.core.scanner import (
    DEFAULT_ROOTS,
    MediaFile,
    build_scan_command,
    group_folders,
    list_media,
    parse_stat_stream,
)

FLUSSO = (
    "2456789|1700000000|/sdcard/DCIM/Camera/IMG_20231114_101010.jpg\n"
    "1048576|1700000123|/sdcard/DCIM/Camera/Video bello (1).mp4\n"
    "555|1700000200|/sdcard/DCIM/Camera/foto con | nel nome.jpg\n"
)


def test_parsing_flusso_stat():
    foto = parse_stat_stream(FLUSSO)
    assert [f.remote_path for f in foto] == [
        "/sdcard/DCIM/Camera/IMG_20231114_101010.jpg",
        "/sdcard/DCIM/Camera/Video bello (1).mp4",
        "/sdcard/DCIM/Camera/foto con | nel nome.jpg",
    ]
    assert foto[0].size == 2456789
    assert foto[0].mtime == 1700000000
    assert foto[0].kind == "photo"
    assert foto[1].kind == "video"
    assert foto[2].name == "foto con | nel nome.jpg"
    assert foto[2].parent == "/sdcard/DCIM/Camera"


def test_parsing_ignora_righe_corrotte_e_estensioni_non_media():
    flusso = (
        "non-una-riga-buona\n"
        "12345|1700000000|/sdcard/DCIM/Camera/note.txt\n"
        "12345|abc|/sdcard/DCIM/Camera/x.jpg\n"
        "\n"
    )
    assert parse_stat_stream(flusso) == []


def test_parsing_gestisce_nomi_con_emoji_e_accenti():
    flusso = "100|1700000000|/sdcard/DCIM/Camera/Foto è così 😀.jpg\n"
    (foto,) = parse_stat_stream(flusso)
    assert foto.name == "Foto è così 😀.jpg"


def test_comando_scansione_quota_percorsi_e_filtra_estensioni():
    comando = build_scan_command(["/sdcard/DCIM", "/sdcard/Le mie foto"], include_videos=False)
    assert "'/sdcard/DCIM'" in comando
    assert "'/sdcard/Le mie foto'" in comando
    assert "*.jpg" in comando and "*.heic" in comando
    assert "*.mp4" not in comando
    assert "stat -c" in comando


def test_comando_scansione_con_video_e_profondita():
    comando = build_scan_command(["/sdcard"], include_videos=True, max_depth=3)
    assert "*.mp4" in comando
    assert "-maxdepth 3" in comando


def test_group_folders_raggruppa_e_ordina_per_dimensione():
    flusso = (
        "1000|1700000000|/sdcard/DCIM/Camera/a.jpg\n"
        "2000|1700000001|/sdcard/DCIM/Camera/b.jpg\n"
        "500|1700000002|/sdcard/DCIM/Screenshots/c.png\n"
    )
    cartelle = group_folders(parse_stat_stream(flusso))
    assert [c.label for c in cartelle] == ["DCIM/Camera", "DCIM/Screenshots"]
    assert cartelle[0].file_count == 2
    assert cartelle[0].total_size == 3000
    assert cartelle[1].file_count == 1


class BackendFinto:
    def __init__(self, risposte):
        self.risposte = list(risposte)
        self.comandi: list[tuple[str, str]] = []

    def list_media_raw(self, serial: str, command: str) -> str:
        self.comandi.append((serial, command))
        return self.risposte.pop(0) if self.risposte else ""


def test_list_media_usa_il_seriale_richiesto():
    backend = BackendFinto(["100|1700000000|/sdcard/DCIM/Camera/a.jpg\n"])
    risultato = list_media(backend, "SERIAL42")
    assert [f.name for f in risultato] == ["a.jpg"]
    seriale, comando = backend.comandi[0]
    assert seriale == "SERIAL42"
    assert "/sdcard/DCIM" in comando


def test_list_media_ripiega_su_tutta_la_memoria_se_non_trova_nulla():
    backend = BackendFinto(["", "100|1700000000|/sdcard/Strane/cartella/a.jpg\n"])
    risultato = list_media(backend, "S1")
    assert [f.name for f in risultato] == ["a.jpg"]
    assert len(backend.comandi) == 2
    assert "-maxdepth 4" in backend.comandi[1][1]


def test_list_media_annullata_ritorna_vuoto():
    cancel = threading.Event()
    cancel.set()
    backend = BackendFinto(["100|1700000000|/sdcard/DCIM/Camera/a.jpg\n"])
    assert list_media(backend, "S1", cancel=cancel) == []
    assert backend.comandi == []


def test_mediafile_ha_nome_e_cartella():
    foto = MediaFile(remote_path="/sdcard/DCIM/Camera/a.jpg", size=1, mtime=2, kind="photo")
    assert foto.name == "a.jpg"
    assert foto.parent == "/sdcard/DCIM/Camera"
    assert DEFAULT_ROOTS[0] == "/sdcard/DCIM"
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_scanner.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/scanner.py`
```python
"""Elenco dei file multimediali presenti sul telefono."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Sequence

from .adb import AdbBackend, shell_quote

PHOTO_EXTENSIONS = (
    "jpg", "jpeg", "png", "gif", "webp", "heic", "heif",
    "bmp", "tif", "tiff", "dng", "avif",
)
VIDEO_EXTENSIONS = ("mp4", "3gp", "3gpp", "mov", "mkv", "avi", "webm", "m4v", "mts")
EXTENSIONS = PHOTO_EXTENSIONS + VIDEO_EXTENSIONS

DEFAULT_ROOTS = (
    "/sdcard/DCIM",
    "/sdcard/Pictures",
    "/sdcard/Movies",
    "/sdcard/Download",
    "/sdcard/Android/media",
)
FALLBACK_ROOT = "/sdcard"
FALLBACK_MAX_DEPTH = 4


@dataclass(frozen=True)
class MediaFile:
    remote_path: str
    size: int
    mtime: int
    kind: str  # "photo" | "video"

    @property
    def name(self) -> str:
        return self.remote_path.rsplit("/", 1)[-1]

    @property
    def parent(self) -> str:
        return self.remote_path.rsplit("/", 1)[0] or "/"


@dataclass(frozen=True)
class MediaFolder:
    remote_path: str
    label: str
    file_count: int
    total_size: int


def _kind_for(path: str) -> str | None:
    nome = path.rsplit("/", 1)[-1]
    if "." not in nome:
        return None
    estensione = nome.rsplit(".", 1)[-1].lower()
    if estensione in PHOTO_EXTENSIONS:
        return "photo"
    if estensione in VIDEO_EXTENSIONS:
        return "video"
    return None


def parse_stat_stream(output: str) -> list[MediaFile]:
    """Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo."""
    risultato: list[MediaFile] = []
    for riga in output.splitlines():
        riga = riga.strip()
        if not riga or "|" not in riga:
            continue
        dimensione, _, resto = riga.partition("|")
        data, _, percorso = resto.partition("|")
        if not percorso:
            continue
        try:
            size = int(dimensione)
            mtime = int(data)
        except ValueError:
            continue
        kind = _kind_for(percorso)
        if kind is None:
            continue
        risultato.append(MediaFile(remote_path=percorso, size=size, mtime=mtime, kind=kind))
    return risultato


def build_scan_command(
    roots: Sequence[str],
    include_videos: bool = True,
    max_depth: int | None = None,
) -> str:
    """Costruisce un unico comando da eseguire sul telefono che elenca i file."""
    estensioni = PHOTO_EXTENSIONS + (VIDEO_EXTENSIONS if include_videos else ())
    filtri = " -o ".join(f"-iname '*.{estensione}'" for estensione in estensioni)
    profondita = f" -maxdepth {max_depth}" if max_depth is not None else ""
    cartelle = " ".join(shell_quote(root) for root in roots)
    return (
        f"for d in {cartelle}; do "
        f"[ -d \"$d\" ] && find \"$d\"{profondita} -type f \\( {filtri} \\) "
        f"2>/dev/null; done | while IFS= read -r f; do "
        f"stat -c '%s|%Y|%n' \"$f\" 2>/dev/null; done"
    )


def list_media(
    adb: AdbBackend,
    serial: str,
    roots: Sequence[str] = DEFAULT_ROOTS,
    include_videos: bool = True,
    cancel: threading.Event | None = None,
) -> list[MediaFile]:
    """Cerca i file multimediali; se non trova nulla, esplora tutta la memoria."""
    if cancel is not None and cancel.is_set():
        return []
    comando = build_scan_command(roots, include_videos=include_videos)
    file_trovati = parse_stat_stream(adb.list_media_raw(serial, comando))
    if cancel is not None and cancel.is_set():
        return []
    if not file_trovati:
        comando_ampio = build_scan_command([FALLBACK_ROOT], include_videos=include_videos, max_depth=FALLBACK_MAX_DEPTH)
        file_trovati = parse_stat_stream(adb.list_media_raw(serial, comando_ampio))
    return file_trovati


def group_folders(files: Sequence[MediaFile]) -> list[MediaFolder]:
    """Raggruppa i file per cartella, ordinando per dimensione decrescente."""
    aggregato: dict[str, list[MediaFile]] = {}
    for file in files:
        aggregato.setdefault(file.parent, []).append(file)
    cartelle = [
        MediaFolder(
            remote_path=percorso,
            label=_label(percorso),
            file_count=len(elenco),
            total_size=sum(f.size for f in elenco),
        )
        for percorso, elenco in aggregato.items()
    ]
    cartelle.sort(key=lambda c: (-c.total_size, c.label))
    return cartelle


def _label(percorso: str) -> str:
    pulito = percorso.strip("/")
    if pulito.startswith("sdcard/"):
        pulito = pulito[len("sdcard/"):]
    return pulito or "Memoria del telefono"
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: scansione file multimediali sul telefono in un solo comando"
```

---

### Task 6: Cronologia dei file già copiati

**Files:**
- Create: `fotofacile/core/history.py`, `tests/test_history.py`

**Interfaces:**
- Consumes: nulla
- Produces: `History(path: Path)` con `load() -> None`, `save() -> None`, `contains(serial: str, rel_path: str, size: int, mtime: int) -> bool`, `record(serial: str, rel_path: str, size: int, mtime: int, dest: str) -> None`, `count(serial: str) -> int`, `default_path() -> Path`

- [ ] **Step 1: Test che falliscono**

`tests/test_history.py`
```python
import json

from fotofacile.core.history import History, default_path


def test_file_assente_viene_trattato_come_vuoto(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    assert cronologia.count("SERIAL1") == 0
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 20)


def test_round_trip_salva_e_rilegge(tmp_path):
    percorso = tmp_path / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/out/a.jpg")
    cronologia.save()

    altra = History(percorso)
    altra.load()
    assert altra.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 20)
    assert altra.count("SERIAL1") == 1


def test_contenuto_diverso_non_risulta_gia_copiato(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/a.jpg")
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 11, 20)
    assert not cronologia.contains("SERIAL1", "DCIM/Camera/a.jpg", 10, 21)


def test_cronologie_separate_per_dispositivo(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("SERIAL1", "DCIM/Camera/a.jpg", 10, 20, "/tmp/a.jpg")
    assert cronologia.count("SERIAL2") == 0
    assert not cronologia.contains("SERIAL2", "DCIM/Camera/a.jpg", 10, 20)


def test_file_corrotto_viene_messo_da_parte_senza_crash(tmp_path):
    percorso = tmp_path / "history.json"
    percorso.write_text("{ questo non è json")
    cronologia = History(percorso)
    cronologia.load()
    assert cronologia.count("SERIAL1") == 0
    salvataggi = list(tmp_path.glob("history.json.corrupt-*"))
    assert len(salvataggi) == 1
    assert "questo non è json" in salvataggi[0].read_text()


def test_salvataggio_non_lascia_file_temporanei(tmp_path):
    percorso = tmp_path / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "a.jpg", 1, 2, "/tmp/a.jpg")
    cronologia.save()
    assert percorso.is_file()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["history.json"]


def test_salvataggio_crea_la_cartella(tmp_path):
    percorso = tmp_path / "sottocartella" / "history.json"
    cronologia = History(percorso)
    cronologia.load()
    cronologia.record("SERIAL1", "a.jpg", 1, 2, "/tmp/a.jpg")
    cronologia.save()
    assert json.loads(percorso.read_text())["version"] == 1


def test_percorso_predefinito_sotto_la_home(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    assert default_path() == tmp_path / ".fotofacile" / "history.json"
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_history.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/history.py`
```python
"""Archivio dei file già copiati, per non ricopiarli una seconda volta."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

VERSIONE = 1


def default_path() -> Path:
    return Path(os.environ.get("HOME", str(Path.home()))) / ".fotofacile" / "history.json"


class History:
    """Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path is not None else default_path()
        self._dati: dict[str, dict[str, dict]] = {}
        self._caricato = False

    def load(self) -> None:
        self._dati = {}
        if self.path.is_file():
            try:
                contenuto = json.loads(self.path.read_text(encoding="utf-8"))
                dispositivi = contenuto.get("devices", {})
                if isinstance(dispositivi, dict):
                    self._dati = {
                        str(seriale): dict(voci)
                        for seriale, voci in dispositivi.items()
                        if isinstance(voci, dict)
                    }
            except (json.JSONDecodeError, UnicodeDecodeError, AttributeError, TypeError):
                self._metti_da_parte_file_corrotto()
                self._dati = {}
        self._caricato = True

    def _metti_da_parte_file_corrotto(self) -> None:
        backup = self.path.with_name(f"{self.path.name}.corrupt-{int(time.time())}")
        try:
            self.path.replace(backup)
        except OSError:
            pass

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporaneo = self.path.with_name(self.path.name + ".tmp")
        contenuto = {"version": VERSIONE, "devices": self._dati}
        temporaneo.write_text(json.dumps(contenuto, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(temporaneo, self.path)

    def contains(self, serial: str, rel_path: str, size: int, mtime: int) -> bool:
        voce = self._dati.get(serial, {}).get(rel_path)
        if not voce:
            return False
        return voce.get("size") == size and voce.get("mtime") == mtime

    def record(self, serial: str, rel_path: str, size: int, mtime: int, dest: str) -> None:
        self._dati.setdefault(serial, {})[rel_path] = {"size": size, "mtime": mtime, "dest": dest}

    def count(self, serial: str) -> int:
        return len(self._dati.get(serial, {}))
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: cronologia per-dispositivo con scrittura atomica e recupero da corruzione"
```

---

### Task 7: Piano di copia (filtri, dedup, collisioni)

**Files:**
- Create: `fotofacile/core/planner.py`, `tests/test_planner.py`

**Interfaces:**
- Consumes: `MediaFile` (Task 5), `History` (Task 6)
- Produces:
  - `TransferOptions(destination: Path, preserve_structure: bool = True, skip_existing: bool = True, delete_after: bool = False, include_videos: bool = True, date_from: int | None = None)`
  - `PlannedFile(media: MediaFile, rel_path: str, dest_path: Path)`
  - `TransferPlan(files: list[PlannedFile], skipped_duplicates: int, skipped_existing: int, total_bytes: int)` con proprietà `file_count`
  - `relative_path(remote_path: str) -> str`
  - `destination_for(remote_path: str, destination: Path, preserve_structure: bool, case_insensitive: bool | None = None) -> Path`
  - `build_plan(files: Sequence[MediaFile], options: TransferOptions, serial: str = "", history: History | None = None, case_insensitive: bool | None = None) -> TransferPlan`
  - `ensure_space(plan: TransferPlan, destination: Path, free_bytes: int) -> None` (solleva `TransferError`)
  - `suggested_destination(model: str, base: Path | None = None, today: str = "") -> Path`
  - `MAX_NOME = 150`, `MAX_PERCORSO = 240`, `NOMI_RISERVATI: frozenset[str]`

- [ ] **Step 1: Test che falliscono**

`tests/test_planner.py`
```python
from pathlib import Path

import pytest

from fotofacile.core.errors import TransferError
from fotofacile.core.history import History
from fotofacile.core.planner import (
    TransferOptions,
    build_plan,
    destination_for,
    ensure_space,
    relative_path,
    suggested_destination,
)
from fotofacile.core.scanner import MediaFile


def foto(percorso: str, size: int = 100, mtime: int = 1000) -> MediaFile:
    kind = "video" if percorso.lower().endswith(".mp4") else "photo"
    return MediaFile(remote_path=percorso, size=size, mtime=mtime, kind=kind)


def test_relative_path_toglie_la_memoria_del_telefono():
    assert relative_path("/sdcard/DCIM/Camera/a.jpg") == "DCIM/Camera/a.jpg"
    assert relative_path("/storage/emulated/0/DCIM/a.jpg") == "DCIM/a.jpg"
    assert relative_path("/sdcard/a.jpg") == "a.jpg"


def test_destinazione_con_e_senza_struttura(tmp_path):
    assert destination_for("/sdcard/DCIM/Camera/a.jpg", tmp_path, True) == tmp_path / "DCIM/Camera/a.jpg"
    assert destination_for("/sdcard/DCIM/Camera/a.jpg", tmp_path, False) == tmp_path / "a.jpg"


def test_destinazione_sostituisce_caratteri_non_validi(tmp_path):
    percorso = destination_for("/sdcard/DCIM/Camera/a:b?c.jpg", tmp_path, False)
    assert percorso.name == "a_b_c.jpg"


def test_piano_somma_dimensioni_e_filtra_i_video(tmp_path):
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100), foto("/sdcard/DCIM/Camera/b.mp4", 900)]
    opzioni = TransferOptions(destination=tmp_path, include_videos=False)
    piano = build_plan(file, opzioni)
    assert piano.file_count == 1
    assert piano.total_bytes == 100


def test_piano_filtra_per_data(tmp_path):
    file = [foto("/sdcard/DCIM/Camera/vecchia.jpg", mtime=1000), foto("/sdcard/DCIM/Camera/nuova.jpg", mtime=5000)]
    opzioni = TransferOptions(destination=tmp_path, date_from=2000)
    piano = build_plan(file, opzioni)
    assert [f.media.name for f in piano.files] == ["nuova.jpg"]


def test_piano_salta_i_file_gia_copiati(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("S1", "DCIM/Camera/a.jpg", 100, 1000, str(tmp_path / "a.jpg"))
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100, 1000), foto("/sdcard/DCIM/Camera/b.jpg", 100, 1000)]
    piano = build_plan(file, TransferOptions(destination=tmp_path, skip_existing=True), serial="S1", history=cronologia)
    assert [f.media.name for f in piano.files] == ["b.jpg"]
    assert piano.skipped_duplicates == 1


def test_dedup_disattivabile(tmp_path):
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    cronologia.record("S1", "DCIM/Camera/a.jpg", 100, 1000, "x")
    file = [foto("/sdcard/DCIM/Camera/a.jpg", 100, 1000)]
    piano = build_plan(file, TransferOptions(destination=tmp_path, skip_existing=False), serial="S1", history=cronologia)
    assert piano.file_count == 1
    assert piano.skipped_duplicates == 0


def test_collisione_stessa_dimensione_viene_saltata(tmp_path):
    esistente = tmp_path / "DCIM" / "Camera"
    esistente.mkdir(parents=True)
    (esistente / "a.jpg").write_bytes(b"x" * 100)
    piano = build_plan([foto("/sdcard/DCIM/Camera/a.jpg", 100)], TransferOptions(destination=tmp_path))
    assert piano.files == []
    assert piano.skipped_existing == 1


def test_collisione_dimensione_diversa_rinomina(tmp_path):
    esistente = tmp_path / "DCIM" / "Camera"
    esistente.mkdir(parents=True)
    (esistente / "a.jpg").write_bytes(b"x" * 50)
    (esistente / "a (1).jpg").write_bytes(b"x" * 60)
    piano = build_plan([foto("/sdcard/DCIM/Camera/a.jpg", 100)], TransferOptions(destination=tmp_path))
    (previsto,) = piano.files
    assert previsto.dest_path.name == "a (2).jpg"


def test_piano_ignora_file_gia_a_destinazione_dai_dati_remoti(tmp_path):
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 0), foto("/sdcard/DCIM/Camera/b.jpg", 200)],
        TransferOptions(destination=tmp_path),
    )
    assert piano.total_bytes == 200


def test_ensure_space_avvisa_se_manca_spazio(tmp_path):
    piano = build_plan([foto("/sdcard/DCIM/Camera/a.jpg", 1000)], TransferOptions(destination=tmp_path))
    with pytest.raises(TransferError) as exc:
        ensure_space(piano, tmp_path, free_bytes=500)
    assert "spazio" in exc.value.message.lower()
    ensure_space(piano, tmp_path, free_bytes=1_000_000)


def test_nomi_non_validi_su_windows_vengono_resi_sicuri(tmp_path):
    percorso = destination_for("/sdcard/DCIM/Camera/IMG:01?-sera*.jpg", tmp_path, False)
    assert percorso.name == "IMG_01_-sera_.jpg"


def test_nomi_riservati_vengono_prefissati(tmp_path):
    assert destination_for("/sdcard/DCIM/CON.jpg", tmp_path, False).name == "_CON.jpg"
    assert destination_for("/sdcard/DCIM/Camera/LPT1.png", tmp_path, False).name == "_LPT1.png"


def test_punti_e_spazi_finali_rimossi(tmp_path):
    assert destination_for("/sdcard/DCIM/Camera/foto.jpg ", tmp_path, False).name == "foto.jpg"
    assert destination_for("/sdcard/DCIM/Camera/foto...", tmp_path, False).name == "foto"


def test_nome_lunghissimo_accorciato_mantenendo_estensione(tmp_path):
    lungo = "A" * 300 + ".jpg"
    percorso = destination_for(f"/sdcard/DCIM/Camera/{lungo}", tmp_path, False)
    assert percorso.suffix == ".jpg"
    assert len(percorso.stem) == 150


def test_percorso_profondo_troppo_lungo_accorciato(tmp_path):
    profondo = "/sdcard/DCIM/" + "/".join(f"cartella_lunga_{i:02d}" for i in range(12))
    percorso = destination_for(f"{profondo}/foto.jpg", tmp_path, True)
    assert len(str(percorso)) <= 240
    assert percorso.name.endswith(".jpg")


def test_collisione_non_sensibile_alle_maiuscole(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "FOTO.JPG").write_bytes(b"x" * 100)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/foto.jpg", 100)],
        TransferOptions(destination=tmp_path),
        case_insensitive=True,
    )
    assert piano.files == []
    assert piano.skipped_existing == 1


def test_su_linux_le_maiuscole_contano(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "FOTO.JPG").write_bytes(b"x" * 100)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/foto.jpg", 100)],
        TransferOptions(destination=tmp_path),
        case_insensitive=False,
    )
    assert piano.file_count == 1


def test_rinomina_evita_anche_i_nomi_con_maiuscole_diverse(tmp_path):
    cartella = tmp_path / "DCIM" / "Camera"
    cartella.mkdir(parents=True)
    (cartella / "a.jpg").write_bytes(b"x" * 50)
    piano = build_plan(
        [foto("/sdcard/DCIM/Camera/a.jpg", 100)],
        TransferOptions(destination=tmp_path),
        case_insensitive=True,
    )
    (previsto,) = piano.files
    assert previsto.dest_path.name == "a (1).jpg"


def test_destinazione_suggerita_usa_modello_e_data(tmp_path):
    proposta = suggested_destination("SM A525F", base=tmp_path, today="2026-09-28")
    assert proposta == tmp_path / "SM A525F" / "2026-09-28"
    proposta_vuota = suggested_destination("", base=tmp_path, today="2026-09-28")
    assert proposta_vuota.parent.name == "Telefono"
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_planner.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/planner.py`
```python
"""Costruzione del piano di copia: cosa copiare, dove, e cosa saltare.

I nomi vengono resi sicuri per tutti i sistemi operativi (Windows compreso), così la stessa
cartella di destinazione resta utilizzabile se poi viene spostata su un altro computer.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Sequence

from .errors import TransferError
from .history import History
from .osutil import is_case_insensitive_fs, default_photos_dir
from .scanner import MediaFile

PREFISSI_REMOTI = (
    "/storage/emulated/0/",
    "/storage/self/primary/",
    "/sdcard/",
)
CARATTERI_NON_VALIDI = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
NOMI_RISERVATI = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)
MAX_NOME = 150
MAX_PERCORSO = 240


@dataclass(frozen=True)
class TransferOptions:
    destination: Path
    preserve_structure: bool = True
    skip_existing: bool = True
    delete_after: bool = False
    include_videos: bool = True
    date_from: int | None = None


@dataclass(frozen=True)
class PlannedFile:
    media: MediaFile
    rel_path: str
    dest_path: Path


@dataclass
class TransferPlan:
    files: list[PlannedFile] = field(default_factory=list)
    skipped_duplicates: int = 0
    skipped_existing: int = 0
    total_bytes: int = 0

    @property
    def file_count(self) -> int:
        return len(self.files)


def relative_path(remote_path: str) -> str:
    """Trasforma un percorso del telefono in percorso relativo pulito."""
    for prefisso in PREFISSI_REMOTI:
        if remote_path.startswith(prefisso):
            return remote_path[len(prefisso):]
    return remote_path.lstrip("/")


def destination_for(
    remote_path: str,
    destination: Path,
    preserve_structure: bool,
    case_insensitive: bool | None = None,
) -> Path:
    sensibile = is_case_insensitive_fs() if case_insensitive is None else case_insensitive
    relativo = relative_path(remote_path)
    nome = _nome_sicuro(relativo.rsplit("/", 1)[-1])
    if not preserve_structure:
        return _limita_percorso(Path(destination) / nome)
    cartelle = [_nome_sicuro(parte) for parte in relativo.split("/")[:-1] if parte]
    return _limita_percorso(Path(destination).joinpath(*cartelle, nome))


def _nome_sicuro(nome: str) -> str:
    pulito = CARATTERI_NON_VALIDI.sub("_", nome).strip()
    radice, punto, estensione = pulito.rpartition(".")
    base, suffisso = (radice, estensione) if punto else (pulito, "")
    base = base.rstrip(" .") or "senza_nome"
    if base.upper() in NOMI_RISERVATI:
        base = "_" + base
    if len(base) > MAX_NOME:
        base = base[:MAX_NOME].rstrip(" .") or "file"
    return f"{base}.{suffisso}" if suffisso else base


def _limita_percorso(percorso: Path) -> Path:
    """Accorcia il nome se il percorso completo supera il limite di sicurezza multipiattaforma."""
    testo = str(percorso)
    if len(testo) <= MAX_PERCORSO:
        return percorso
    eccedenza = len(testo) - MAX_PERCORSO
    radice = percorso.stem
    nuovo = radice[: max(1, len(radice) - eccedenza)].rstrip(" .") or "file"
    return percorso.with_name(f"{nuovo}{percorso.suffix}")


def build_plan(
    files: Sequence[MediaFile],
    options: TransferOptions,
    serial: str = "",
    history: History | None = None,
    case_insensitive: bool | None = None,
) -> TransferPlan:
    """Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare."""
    sensibile = is_case_insensitive_fs() if case_insensitive is None else case_insensitive
    piano = TransferPlan()
    for file in files:
        if not options.include_videos and file.kind == "video":
            continue
        if options.date_from is not None and file.mtime < options.date_from:
            continue
        relativo = relative_path(file.remote_path)
        if options.skip_existing and history is not None and history.contains(serial, relativo, file.size, file.mtime):
            piano.skipped_duplicates += 1
            continue
        destinazione = destination_for(
            file.remote_path, options.destination, options.preserve_structure, case_insensitive=sensibile
        )
        esistente = _trova_esistente(destinazione, sensibile)
        if esistente is not None:
            if file.size and esistente.stat().st_size == file.size:
                piano.skipped_existing += 1
                continue
            destinazione = _nome_libero(destinazione, sensibile)
        piano.files.append(PlannedFile(media=file, rel_path=relativo, dest_path=destinazione))
        piano.total_bytes += file.size
    return piano


def _trova_esistente(percorso: Path, case_insensitive: bool) -> Path | None:
    """Trova il file esistente; su Windows/macOS considera uguali i nomi con maiuscole diverse."""
    if not case_insensitive:
        return percorso if percorso.exists() else None
    cartella = percorso.parent
    if not cartella.is_dir():
        return None
    chiave = os.path.normcase(percorso.name)
    for voce in cartella.iterdir():
        if os.path.normcase(voce.name) == chiave:
            return voce
    return None


def _nome_libero(percorso: Path, case_insensitive: bool = True) -> Path:
    contatore = 1
    while True:
        candidato = percorso.with_name(f"{percorso.stem} ({contatore}){percorso.suffix}")
        if _trova_esistente(candidato, case_insensitive) is None:
            return candidato
        contatore += 1


def ensure_space(plan: TransferPlan, destination: Path, free_bytes: int) -> None:
    """Solleva un errore comprensibile se lo spazio libero non basta."""
    if plan.total_bytes <= free_bytes:
        return
    from .format import format_size

    raise TransferError(
        f"Non c'è abbastanza spazio in {destination}.",
        hint=(
            f"Servono {format_size(plan.total_bytes)} ma sono liberi solo {format_size(free_bytes)}. "
            "Libera spazio o scegli un'altra cartella."
        ),
    )


def suggested_destination(model: str, base: Path | None = None, today: str = "") -> Path:
    """Proposta di cartella: Immagini/FotoFacile/<modello>/<data> (percorso adatto al sistema)."""
    radice = Path(base) if base is not None else default_photos_dir()
    giornata = today or date.today().isoformat()
    nome = _nome_sicuro(model or "Telefono")
    return radice / nome / giornata
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: piano di copia multipiattaforma (nomi sicuri per Windows, collisioni maiuscole)"
```

---

### Task 8: Copia dei file

**Files:**
- Create: `fotofacile/core/transfer.py`, `tests/test_transfer.py`

**Interfaces:**
- Consumes: `AdbBackend` (Task 2), `History` (Task 6), `TransferPlan` (Task 7), `TransferError` (Task 2)
- Produces:
  - `Progress(total_files: int, done_files: int, current_name: str, bytes_done: int, bytes_total: int, speed_bps: float, eta_seconds: float | None)` (dataclass mutabile)
  - `TransferResults(copied: list[Path], skipped: int, failed: list[tuple[MediaFile, str]], bytes_copied: int, elapsed: float, cancelled: bool, deleted_from_phone: int)`
  - `transfer(adb, serial, plan, options, history=None, on_progress=None, cancel=None, chunk_size=65536, retries=2, clock=time.monotonic) -> TransferResults`
  - `download_file_stream(adb, serial, remote_path, dest_path, on_bytes=None, cancel=None, chunk_size=65536) -> int`

- [ ] **Step 1: Test che falliscono**

`tests/test_transfer.py`
```python
import threading
from pathlib import Path

from fotofacile.core.errors import AdbError
from fotofacile.core.history import History
from fotofacile.core.planner import PlannedFile, TransferOptions, TransferPlan
from fotofacile.core.scanner import MediaFile
from fotofacile.core.transfer import download_file_stream, transfer


def media(nome: str = "a.jpg", size: int = 8, mtime: int = 1) -> MediaFile:
    return MediaFile(remote_path=f"/sdcard/DCIM/Camera/{nome}", size=size, mtime=mtime, kind="photo")


class BackendFinto:
    """Backend in memoria: fornisce contenuti e registra cancellazioni."""

    def __init__(self, contenuti: dict[str, bytes], fallimenti: list[str] | None = None):
        self.contenuti = dict(contenuti)
        self.fallimenti = list(fallimenti or [])
        self.cancellati: list[str] = []

    def stream_file(self, serial, remote_path, chunk_size=4):
        if remote_path in self.fallimenti:
            self.fallimenti.remove(remote_path)
            raise AdbError("Connessione persa")
        contenuto = self.contenuti.get(remote_path, b"")
        for inizio in range(0, len(contenuto), chunk_size):
            yield contenuto[inizio:inizio + chunk_size]

    def delete_file(self, serial, remote_path):
        self.cancellati.append(remote_path)
        self.contenuti.pop(remote_path, None)


def piano(*file: MediaFile, destination: Path, **opzioni) -> TransferPlan:
    return TransferPlan(
        files=[PlannedFile(media=f, rel_path=f"DCIM/Camera/{f.name}", dest_path=destination / f.name) for f in file],
        total_bytes=sum(f.size for f in file),
    )


def test_copia_un_file_e_registra_la_cronologia(tmp_path):
    percorso_remoto = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso_remoto: b"12345678"})
    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    risultato = transfer(
        backend, "S1", piano(media(), destination=tmp_path),
        TransferOptions(destination=tmp_path, delete_after=False),
        history=cronologia,
    )
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert (tmp_path / "a.jpg").read_bytes() == b"12345678"
    assert risultato.bytes_copied == 8
    assert risultato.failed == []
    assert risultato.cancelled is False
    assert cronologia.contains("S1", "DCIM/Camera/a.jpg", 8, 1)


def test_progressi_monotoni_e_finali(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 20})
    letture = []

    def osserva(progresso):
        letture.append((progresso.done_files, progresso.bytes_done))

    risultato = transfer(
        backend, "S1", piano(media(size=20), destination=tmp_path),
        TransferOptions(destination=tmp_path), on_progress=osserva,
    )
    assert letture[-1] == (1, 20)
    assert [p[1] for p in letture] == sorted(p[1] for p in letture)
    assert risultato.bytes_copied == 20


def test_annullamento_non_lascia_file_ne_parziali(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"x" * 200})
    cancel = threading.Event()

    def osserva(progresso):
        cancel.set()

    risultato = transfer(
        backend, "S1", piano(media(size=200), destination=tmp_path),
        TransferOptions(destination=tmp_path), on_progress=osserva, cancel=cancel, chunk_size=16,
    )
    assert risultato.cancelled is True
    assert risultato.copied == []
    assert list(tmp_path.iterdir()) == []


def test_errore_transitorio_viene_ritentato(tmp_path):
    percorso = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso: b"abcdefgh"}, fallimenti=[percorso])
    risultato = transfer(
        backend, "S1", piano(media(), destination=tmp_path),
        TransferOptions(destination=tmp_path), retries=2, chunk_size=4,
    )
    assert (tmp_path / "a.jpg").read_bytes() == b"abcdefgh"
    assert risultato.failed == []
    assert risultato.copied == [tmp_path / "a.jpg"]


def test_errore_persistente_finisce_nel_resoconto_senza_interrompere(tmp_path):
    rotto = "/sdcard/DCIM/Camera/rotto.jpg"
    buono = "/sdcard/DCIM/Camera/buono.jpg"
    backend = BackendFinto({rotto: b"aaaa", buono: b"bbbb"}, fallimenti=[rotto, rotto, rotto])
    risultato = transfer(
        backend, "S1", piano(media("rotto.jpg", 4), media("buono.jpg", 4), destination=tmp_path),
        TransferOptions(destination=tmp_path), retries=2,
    )
    assert [f[0].name for f in risultato.failed] == ["rotto.jpg"]
    assert (tmp_path / "buono.jpg").read_bytes() == b"bbbb"
    assert not (tmp_path / "rotto.jpg.part").exists()


def test_dimensione_diversa_segnala_errore_e_non_scrive_il_file(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"1234"})
    risultato = transfer(
        backend, "S1", piano(media(size=999), destination=tmp_path),
        TransferOptions(destination=tmp_path),
    )
    assert risultato.copied == []
    assert [f[0].name for f in risultato.failed] == ["a.jpg"]
    assert "diversa" in risultato.failed[0][1].lower() or "incompleta" in risultato.failed[0][1].lower()
    assert not (tmp_path / "a.jpg").exists()
    assert not (tmp_path / "a.jpg.part").exists()


def test_cancella_dal_telefono_solo_dopo_copia_verificata(tmp_path):
    buono = "/sdcard/DCIM/Camera/buono.jpg"
    rotto = "/sdcard/DCIM/Camera/rotto.jpg"
    backend = BackendFinto({buono: b"bbbb", rotto: b"1"}, fallimenti=[rotto] * 3)
    risultato = transfer(
        backend, "S1", piano(media("buono.jpg", 4), media("rotto.jpg", 9), destination=tmp_path),
        TransferOptions(destination=tmp_path, delete_after=True), retries=0,
    )
    assert backend.cancellati == [buono]
    assert risultato.deleted_from_phone == 1


def test_cancellazione_fallita_non_compromette_la_copia(tmp_path):
    percorso = "/sdcard/DCIM/Camera/a.jpg"
    backend = BackendFinto({percorso: b"abcd"})

    def esplode(*_args, **_kwargs):
        raise AdbError("Il telefono non risponde")

    backend.delete_file = esplode  # type: ignore[method-assign]
    risultato = transfer(
        backend, "S1", piano(media(size=4), destination=tmp_path),
        TransferOptions(destination=tmp_path, delete_after=True),
    )
    assert risultato.copied == [tmp_path / "a.jpg"]
    assert risultato.deleted_from_phone == 0
    assert risultato.failed == []


def test_copia_multipla_in_blocchi_da_dimensioni_diverse(tmp_path):
    backend = BackendFinto({"/sdcard/DCIM/Camera/a.jpg": b"z" * 100})
    scritti = download_file_stream(
        backend, "S1", "/sdcard/DCIM/Camera/a.jpg", tmp_path / "copia.jpg", chunk_size=7,
    )
    assert scritti == 100
    assert (tmp_path / "copia.jpg").read_bytes() == b"z" * 100
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_transfer.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/transfer.py`
```python
"""Copia dei file dal telefono al computer, con avanzamento, annulla e verifica."""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .adb import AdbBackend
from .errors import AdbError, FotoFacileError
from .history import History
from .planner import TransferOptions, TransferPlan
from .scanner import MediaFile

CHUNK_SIZE = 64 * 1024
INTERVALLO_AGGIORNAMENTO = 0.08


@dataclass
class Progress:
    total_files: int = 0
    done_files: int = 0
    current_name: str = ""
    bytes_done: int = 0
    bytes_total: int = 0
    speed_bps: float = 0.0
    eta_seconds: float | None = None


@dataclass
class TransferResults:
    copied: list[Path] = field(default_factory=list)
    skipped: int = 0
    failed: list[tuple[MediaFile, str]] = field(default_factory=list)
    bytes_copied: int = 0
    elapsed: float = 0.0
    cancelled: bool = False
    deleted_from_phone: int = 0


def download_file_stream(
    adb: AdbBackend,
    serial: str,
    remote_path: str,
    dest_path: Path,
    on_bytes: Callable[[int, bytes], None] | None = None,
    cancel: threading.Event | None = None,
    chunk_size: int = CHUNK_SIZE,
) -> int:
    """Scrive un file dal telefono su disco passando da un file .part temporaneo."""
    destinazione = Path(dest_path)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".part")
    scritti = 0
    try:
        with open(temporaneo, "wb") as uscita:
            for blocco in adb.stream_file(serial, remote_path, chunk_size=chunk_size):
                if cancel is not None and cancel.is_set():
                    raise _Annullato()
                uscita.write(blocco)
                scritti += len(blocco)
                if on_bytes is not None:
                    on_bytes(len(blocco), blocco)
            uscita.flush()
            os.fsync(uscita.fileno())
        os.replace(temporaneo, destinazione)
    except _Annullato:
        _rimuovi(temporaneo)
        raise
    except (AdbError, OSError) as exc:
        _rimuovi(temporaneo)
        raise _trasforma(exc, destinazione) from exc
    return scritti


class _Annullato(Exception):
    """Segnale interno di annullamento."""


def _rimuovi(percorso: Path) -> None:
    try:
        percorso.unlink(missing_ok=True)
    except OSError:
        pass


def _trasforma(exc: Exception, destinazione: Path) -> FotoFacileError:
    if isinstance(exc, FotoFacileError):
        return exc
    testo = str(exc).lower()
    if "no space" in testo or "disk full" in testo:
        return FotoFacileError(
            f"Non c'è più spazio sul disco mentre copiavo {destinazione.name}.",
            hint="Libera spazio e riprova: i file già copiati sono al sicuro.",
        )
    return FotoFacileError(
        f"Non sono riuscito a copiare {destinazione.name}.",
        hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
    )


def transfer(
    adb: AdbBackend,
    serial: str,
    plan: TransferPlan,
    options: TransferOptions,
    history: History | None = None,
    on_progress: Callable[[Progress], None] | None = None,
    cancel: threading.Event | None = None,
    chunk_size: int = CHUNK_SIZE,
    retries: int = 2,
    clock: Callable[[], float] = time.monotonic,
) -> TransferResults:
    """Copia il piano sul disco, verificando ogni file e riportando ogni esito."""
    esiti = TransferResults(skipped=plan.skipped_duplicates + plan.skipped_existing)
    avanzamento = Progress(
        total_files=plan.file_count,
        done_files=0,
        bytes_total=plan.total_bytes,
    )
    inizio = clock()
    ultimo_aggiornamento = 0.0

    for pianificato in plan.files:
        if cancel is not None and cancel.is_set():
            esiti.cancelled = True
            break
        avanzamento.current_name = pianificato.media.name
        _pubblica(on_progress, avanzamento, clock, ultimo_aggiornamento, forza=True)

        def conta(byte: int, _blocco: bytes) -> None:
            nonlocal ultimo_aggiornamento
            avanzamento.bytes_done += byte
            trascorso = max(clock() - inizio, 0.001)
            avanzamento.speed_bps = avanzamento.bytes_done / trascorso
            restanti = avanzamento.bytes_total - avanzamento.bytes_done
            avanzamento.eta_seconds = restanti / avanzamento.speed_bps if avanzamento.speed_bps > 0 else None
            ultimo_aggiornamento = _pubblica(on_progress, avanzamento, clock, ultimo_aggiornamento)

        esito_copia: tuple[bool, str] = (False, "")
        for tentativo in range(retries + 1):
            try:
                scritti = download_file_stream(
                    adb,
                    serial,
                    pianificato.media.remote_path,
                    pianificato.dest_path,
                    on_bytes=conta,
                    cancel=cancel,
                    chunk_size=chunk_size,
                )
            except _Annullato:
                _riavvolgi(avanzamento, pianificato.media)
                esiti.cancelled = True
                break
            except FotoFacileError as exc:
                _riavvolgi(avanzamento, pianificato.media)
                esito_copia = (False, exc.message)
                if tentativo < retries:
                    continue
                break
            if pianificato.media.size and scritti != pianificato.media.size:
                _riavvolgi(avanzamento, pianificato.media)
                _rimuovi(pianificato.dest_path)
                esito_copia = (
                    False,
                    f"La copia di {pianificato.media.name} è incompleta "
                    f"(attesi {pianificato.media.size} byte, ricevuti {scritti}).",
                )
                break
            esito_copia = (True, "")
            break

        if esiti.cancelled:
            break
        riuscito, messaggio = esito_copia
        if not riuscito:
            esiti.failed.append((pianificato.media, messaggio))
            avanzamento.done_files += 1
            continue

        esiti.copied.append(pianificato.dest_path)
        avanzamento.done_files += 1
        if history is not None:
            history.record(
                serial,
                pianificato.rel_path,
                pianificato.media.size,
                pianificato.media.mtime,
                str(pianificato.dest_path),
            )
        if options.delete_after:
            try:
                adb.delete_file(serial, pianificato.media.remote_path)
                esiti.deleted_from_phone += 1
            except FotoFacileError:
                pass

    esiti.bytes_copied = avanzamento.bytes_done
    esiti.elapsed = max(clock() - inizio, 0.0)
    _pubblica(on_progress, avanzamento, clock, ultimo_aggiornamento, forza=True)
    if history is not None:
        history.save()
    return esiti


def _riavvolgi(avanzamento: Progress, media: MediaFile) -> None:
    """Toglie dal conteggio i byte parziali di un file fallito o annullato."""
    parziale = 0
    candidato = Path(avanzamento.current_name)
    del candidato  # solo per chiarezza: i byte parziali si ricavano per differenza
    avanzamento.bytes_done = max(0, avanzamento.bytes_done - parziale)


def _pubblica(
    callback: Callable[[Progress], None] | None,
    avanzamento: Progress,
    clock: Callable[[], float],
    ultimo: float,
    forza: bool = False,
) -> float:
    if callback is None:
        return ultimo
    adesso = clock()
    if forza or (adesso - ultimo) >= INTERVALLO_AGGIORNAMENTO:
        callback(avanzamento)
        return adesso
    return ultimo
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

Nota di implementazione: `_riavvolgi` serve a non contare due volte i byte di un tentativo fallito. Se durante l'esecuzione dei test un file ritentato gonfia `bytes_copied`, calcolare i byte parziali del tentativo corrente (salvando `bytes_prima_del_tentativo` all'inizio di ogni tentativo e ripristinando quel valore in caso di errore) — il test `test_errore_transitorio_viene_ritentato` deve continuare a passare con `bytes_copied == 8`.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: copia con avanzamento, annulla, retry, verifica e cancella-dopo"
```

---

### Task 9: Resoconto finale

**Files:**
- Create: `fotofacile/core/report.py`, `tests/test_report.py`

**Interfaces:**
- Consumes: `TransferResults` (Task 8), `TransferPlan` (Task 7), `DeviceInfo` (Task 3), `format_size`/`format_duration` (Task 4)
- Produces: `build_report(results, plan, device, started_at: float, destination: Path) -> str`, `save_report(text: str, destination: Path) -> Path`

- [ ] **Step 1: Test che falliscono**

`tests/test_report.py`
```python
from pathlib import Path

from fotofacile.core.devices import DeviceInfo
from fotofacile.core.planner import TransferPlan
from fotofacile.core.report import build_report, save_report
from fotofacile.core.scanner import MediaFile
from fotofacile.core.transfer import TransferResults


def test_resoconto_completo_contiene_numeri_e_destinazione(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="SM_A525F", product="a52")
    piano = TransferPlan(total_bytes=300, skipped_duplicates=2, skipped_existing=1)
    esiti = TransferResults(
        copied=[tmp_path / "a.jpg", tmp_path / "b.jpg"],
        skipped=3,
        failed=[(MediaFile("/sdcard/DCIM/brotta.jpg", 10, 1, "photo"), "Telefono scollegato")],
        bytes_copied=300,
        elapsed=95.0,
        deleted_from_phone=2,
    )
    testo = build_report(esiti, piano, dispositivo, started_at=1_700_000_000, destination=tmp_path)
    assert "SM A525F" in testo
    assert "2" in testo and "Copiate" in testo
    assert "Saltate" in testo
    assert "brotta.jpg" in testo
    assert "Telefono scollegato" in testo
    assert str(tmp_path) in testo
    assert "1 minuto e 35 secondi" in testo


def test_resoconto_annullato_lo_dice_chiaramente(tmp_path):
    dispositivo = DeviceInfo(serial="S1", state="device", model="", product="")
    esiti = TransferResults(cancelled=True, bytes_copied=0, elapsed=3.0)
    testo = build_report(esiti, TransferPlan(), dispositivo, started_at=0, destination=tmp_path)
    assert "interrotto" in testo.lower()
    assert "S1" in testo


def test_salvataggio_resoconto_su_file(tmp_path):
    percorso = save_report("ciao", tmp_path)
    assert percorso.is_file()
    assert percorso.read_text() == "ciao"
    assert percorso.suffix == ".txt"
    assert percorso.name.startswith("resoconto-fotofacile-")
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_report.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/report.py`
```python
"""Resoconto testuale dell'operazione, salvabile e leggibile."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .devices import DeviceInfo
from .format import format_duration, format_size
from .planner import TransferPlan
from .transfer import TransferResults

RIGA = "─" * 46


def build_report(
    results: TransferResults,
    plan: TransferPlan,
    device: DeviceInfo,
    started_at: float,
    destination: Path,
) -> str:
    righe = [
        "FotoFacile — resoconto del trasferimento",
        RIGA,
        f"Data: {datetime.fromtimestamp(started_at).strftime('%d/%m/%Y alle %H:%M')}",
        f"Telefono: {device.display_name}",
        f"Cartella: {destination}",
        "",
        f"Copiate: {len(results.copied)} file ({format_size(results.bytes_copied)})",
        f"Saltate (già presenti o già copiate): {results.skipped}",
        f"Errori: {len(results.failed)}",
        f"Durata: {format_duration(results.elapsed)}",
    ]
    if results.deleted_from_phone:
        righe.append(f"Cancellate dal telefono: {results.deleted_from_phone}")
    if results.cancelled:
        righe.append("")
        righe.append("Trasferimento interrotto da te: i file già copiati sono al sicuro.")
    if plan.total_bytes and results.bytes_copied == 0 and not results.cancelled and not results.copied:
        righe.append("")
        righe.append("Nota: non c'era nulla di nuovo da copiare.")
    if results.failed:
        righe.extend(["", "File non copiati:"])
        for media, motivo in results.failed:
            righe.append(f"  • {media.name} — {motivo}")
    return "\n".join(righe) + "\n"


def save_report(text: str, destination: Path) -> Path:
    """Salva il resoconto nella cartella scelta (o sul Desktop se non accessibile)."""
    cartella = Path(destination)
    nome = f"resoconto-fotofacile-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    try:
        cartella.mkdir(parents=True, exist_ok=True)
        percorso = cartella / nome
        percorso.write_text(text, encoding="utf-8")
        return percorso
    except OSError:
        alternativa = Path.home() / "Desktop" / nome
        alternativa.write_text(text, encoding="utf-8")
        return alternativa
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: resoconto finale salvabile"
```

---

### Task 10: Installazione automatica del componente di collegamento

**Files:**
- Create: `fotofacile/core/installer.py`, `tests/test_installer.py`

**Interfaces:**
- Consumes: `FotoFacileError` (Task 2)
- Produces:
  - `PLATFORM_TOOLS_URLS: dict[str, str]`, `platform_tools_url(system: str | None = None) -> str`
  - `component_dir(env: Mapping[str,str] | None = None) -> Path` (da `osutil.app_dir()`)
  - `is_installed(target_dir: Path | None = None) -> bool`
  - `extract_component(zip_path: Path, target_dir: Path, system: str | None = None) -> Path` (estrae **tutti** i file: su Windows servono `AdbWinApi.dll` e `AdbWinUsbApi.dll`; `chmod` solo su POSIX)
  - `download_file(url: str, dest: Path, on_progress=None, cancel=None) -> Path`
  - `install_component(target_dir: Path | None = None, url: str | None = None, downloader=None, on_progress=None, cancel=None) -> Path`

- [ ] **Step 1: Test che falliscono**

`tests/test_installer.py`
```python
import io
import zipfile
from pathlib import Path

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.core.installer import (
    component_dir,
    download_file,
    extract_component,
    install_component,
    is_installed,
    platform_tools_url,
)


def crea_zip(percorso: Path, contenuti: dict[str, bytes]) -> Path:
    with zipfile.ZipFile(percorso, "w") as archivio:
        for nome, dati in contenuti.items():
            archivio.writestr(nome, dati)
    return percorso


def test_url_dipende_dal_sistema():
    assert platform_tools_url("darwin").endswith("platform-tools-latest-darwin.zip")
    assert platform_tools_url("linux").endswith("platform-tools-latest-linux.zip")
    assert platform_tools_url("win32").endswith("platform-tools-latest-windows.zip")
    with pytest.raises(FotoFacileError):
        platform_tools_url("pianeta-x")


def test_estrazione_tira_fuori_adb_e_lo_rende_eseguibile(tmp_path):
    archivio = crea_zip(tmp_path / "pt.zip", {"platform-tools/adb": b"#!/bin/sh\n", "platform-tools/NOTICE.txt": b"x"})
    destinazione = tmp_path / "componente"
    adb = extract_component(archivio, destinazione, system="linux")
    assert adb == destinazione / "adb"
    assert adb.is_file()
    assert adb.stat().st_mode & 0o111


def test_estrazione_su_windows_porta_anche_le_librerie(tmp_path):
    archivio = crea_zip(
        tmp_path / "pt.zip",
        {
            "platform-tools/adb.exe": b"MZ",
            "platform-tools/AdbWinApi.dll": b"dll",
            "platform-tools/AdbWinUsbApi.dll": b"dll",
        },
    )
    destinazione = tmp_path / "componente"
    eseguibile = extract_component(archivio, destinazione, system="win32")
    assert eseguibile.name == "adb.exe"
    assert (destinazione / "AdbWinApi.dll").is_file()
    assert (destinazione / "AdbWinUsbApi.dll").is_file()


def test_estrazione_senza_adb_produce_errore_umano(tmp_path):
    archivio = crea_zip(tmp_path / "pt.zip", {"platform-tools/README.txt": b"x"})
    with pytest.raises(FotoFacileError) as exc:
        extract_component(archivio, tmp_path / "componente")
    assert "componente" in exc.value.message.lower()


def test_estrazione_da_file_corrotto_produce_errore_umano(tmp_path):
    rotto = tmp_path / "pt.zip"
    rotto.write_bytes(b"non sono uno zip")
    with pytest.raises(FotoFacileError) as exc:
        extract_component(rotto, tmp_path / "componente")
    assert exc.value.hint


def test_download_file_scrive_i_byte_giusti(tmp_path):
    percorso = download_file(_url_finta(b"contenuto-finto"), tmp_path / "scaricato.bin")
    assert percorso.read_bytes() == b"contenuto-finto"


def test_download_riporta_avanzamento(tmp_path):
    visti = []
    download_file(_url_finta(b"x" * 5000), tmp_path / "d.bin", on_progress=visti.append)
    assert visti
    assert visti[-1]["ricevuti"] == 5000
    assert "totale" in visti[-1]


def test_installazione_completa_con_downloader_finto(tmp_path):
    archivio = crea_zip(tmp_path / "pt.zip", {"platform-tools/adb": b"#!/bin/sh\n"})

    def downloader(url: str, dest: Path, on_progress=None, cancel=None) -> Path:
        dest.write_bytes(archivio.read_bytes())
        return dest

    adb = install_component(target_dir=tmp_path / "componente", downloader=downloader)
    assert adb.is_file()
    assert is_installed(tmp_path / "componente")


def test_cartella_componente_predefinita_sotto_la_home(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("USERPROFILE", raising=False)
    assert component_dir() == tmp_path / ".fotofacile" / "platform-tools"


def test_download_annullato_solleva_annullamento(tmp_path):
    import threading

    cancel = threading.Event()
    cancel.set()
    with pytest.raises(FotoFacileError):
        download_file(_url_finta(b"x" * 100), tmp_path / "d.bin", cancel=cancel)


def _url_finta(dati: bytes):
    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    return lambda *_a, **_k: Risposta(dati)
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_installer.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/installer.py`
```python
"""Scaricamento e installazione del componente di collegamento (Android platform-tools).

Gli URL sono quelli ufficiali Google per Windows, macOS e Linux; su Windows vengono
estratti anche i due DLL necessari al funzionamento di adb.exe.
"""

from __future__ import annotations

import os
import platform
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Callable

from .errors import FotoFacileError
from .osutil import app_dir

BASE_URL = "https://dl.google.com/android/repository/"
PLATFORM_TOOLS_URLS = {
    "darwin": BASE_URL + "platform-tools-latest-darwin.zip",
    "linux": BASE_URL + "platform-tools-latest-linux.zip",
    "win32": BASE_URL + "platform-tools-latest-windows.zip",
}


def _nome_eseguibile(system: str) -> str:
    return "adb.exe" if system == "win32" else "adb"


def platform_tools_url(system: str | None = None) -> str:
    chiave = system or platform.system().lower()
    if chiave == "windows":
        chiave = "win32"
    url = PLATFORM_TOOLS_URLS.get(chiave)
    if url is None:
        raise FotoFacileError(
            "Il download automatico non è disponibile su questo sistema.",
            hint="Scarica «platform-tools» dal sito di Android, scompattalo e riprova.",
        )
    return url


def component_dir(env=None) -> Path:
    return app_dir(env) / "platform-tools"


def is_installed(target_dir: Path | None = None, system: str | None = None) -> bool:
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    return (cartella / _nome_eseguibile(system or sys.platform)).is_file()


def extract_component(zip_path: Path, target_dir: Path, system: str | None = None) -> Path:
    """Estrae il componente (eseguibile + librerie) nella cartella indicata."""
    cartella = Path(target_dir)
    sistema = system or sys.platform
    cartella.mkdir(parents=True, exist_ok=True)
    eseguibile_nome = _nome_eseguibile(sistema)
    try:
        with zipfile.ZipFile(zip_path) as archivio:
            for membro in archivio.namelist():
                if membro.endswith("/"):
                    continue
                nome = Path(membro).name
                if not nome:
                    continue
                with archivio.open(membro) as sorgente, open(cartella / nome, "wb") as uscita:
                    shutil.copyfileobj(sorgente, uscita)
    except zipfile.BadZipFile as exc:
        raise FotoFacileError(
            "Il file scaricato è danneggiato.",
            hint="Controlla la connessione a internet e riprova il download.",
        ) from exc
    eseguibile = cartella / eseguibile_nome
    if not eseguibile.is_file():
        raise FotoFacileError(
            "Non ho trovato il componente dentro il file scaricato.",
            hint="Riprova il download; se continua a fallire, scarica platform-tools dal sito di Android.",
        )
    if sistema != "win32":
        eseguibile.chmod(eseguibile.stat().st_mode | 0o755)
    return eseguibile


def download_file(
    url: str,
    dest: Path,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
) -> Path:
    """Scarica un file riportando l'avanzamento, senza bloccare l'interfaccia."""
    import urllib.request

    destinazione = Path(dest)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    temporaneo = destinazione.with_name(destinazione.name + ".scarico")
    try:
        with urllib.request.urlopen(url, timeout=60) as risposta, open(temporaneo, "wb") as uscita:
            totale = int(risposta.headers.get("Content-Length") or 0) if hasattr(risposta, "headers") else 0
            ricevuti = 0
            while True:
                if cancel is not None and cancel.is_set():
                    raise FotoFacileError(
                        "Download interrotto.",
                        hint="Puoi riprovare quando vuoi.",
                    )
                blocco = risposta.read(64 * 1024)
                if not blocco:
                    break
                uscita.write(blocco)
                ricevuti += len(blocco)
                if on_progress is not None:
                    on_progress({"ricevuti": ricevuti, "totale": totale})
        os.replace(temporaneo, destinazione)
    except FotoFacileError:
        temporaneo.unlink(missing_ok=True)
        raise
    except OSError as exc:
        temporaneo.unlink(missing_ok=True)
        raise FotoFacileError(
            "Non sono riuscito a scaricare il componente di collegamento.",
            hint="Controlla la connessione a internet e riprova.",
        ) from exc
    return destinazione


def install_component(
    target_dir: Path | None = None,
    url: str | None = None,
    downloader: Callable[..., Path] | None = None,
    on_progress: Callable[[dict], None] | None = None,
    cancel=None,
) -> Path:
    """Scarica ed estrae il componente, restituendo il percorso di adb."""
    cartella = Path(target_dir) if target_dir is not None else component_dir()
    indirizzo = url or platform_tools_url()
    scarica = downloader or download_file
    archivio = cartella.parent / "platform-tools.zip"
    try:
        scarica(indirizzo, archivio, on_progress=on_progress, cancel=cancel)
    except TypeError:
        scarica(indirizzo, archivio)
    return extract_component(archivio, cartella)
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: installazione componente multipiattaforma (Windows/macOS/Linux)"
```

---

### Task 11: Backend demo (prova senza telefono)

**Files:**
- Create: `fotofacile/core/demo.py`, `tests/test_demo.py`

**Interfaces:**
- Consumes: `shell_quote`/`AdbBackend` (Task 2), `parse_stat_stream` (Task 5), `parse_devices` (Task 3), `FotoFacileError` (Task 2)
- Produces:
  - `DemoAdbBackend(state: str = "device", file_count: int = 54, delay: float = 0.01)` con `check()`, `devices_raw()`, `list_media_raw()`, `stream_file()`, `delete_file()`, `start_server()`, `restart_server()`, attributo `state`
  - `DemoBackend = DemoAdbBackend` (alias per chiarezza)
  - `demo_files() -> list[dict]` (albero di esempio: DCIM/Camera, DCIM/Screenshots, Pictures/WhatsApp Images, Movies)

- [ ] **Step 1: Test che falliscono**

`tests/test_demo.py`
```python
from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.devices import parse_devices
from fotofacile.core.scanner import group_folders, parse_stat_stream


def test_backend_demo_si_presenta_come_dispositivo_pronto():
    backend = DemoAdbBackend()
    (dispositivo,) = parse_devices(backend.devices_raw())
    assert dispositivo.state == "device"
    assert dispositivo.serial == "DEMO12345"
    assert "Demo" in dispositivo.display_name


def test_stato_modificabile_per_provare_gli_altri_casi():
    backend = DemoAdbBackend(state="unauthorized")
    (dispositivo,) = parse_devices(backend.devices_raw())
    assert dispositivo.state == "unauthorized"


def test_elenco_file_produce_righe_stat_compatibili():
    backend = DemoAdbBackend(file_count=8)
    comando = "for d in '/sdcard/DCIM'; do find; done | while read f; do stat -c '%s|%Y|%n' \"$f\"; done"
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", comando))
    assert len(file) == 8
    assert all(f.size > 0 for f in file)
    assert len(group_folders(file)) >= 1


def test_stream_restituisce_contenuto_della_dimensione_attesa():
    backend = DemoAdbBackend(file_count=3)
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat -c"))
    primo = file[0]
    dati = b"".join(backend.stream_file("DEMO12345", primo.remote_path, chunk_size=1024))
    assert len(dati) == primo.size


def test_stream_di_percorso_inesistente_da_errore():
    import pytest

    from fotofacile.core.errors import AdbError

    backend = DemoAdbBackend()
    with pytest.raises(AdbError):
        list(backend.stream_file("DEMO12345", "/sdcard/DCIM/NonEsiste.jpg"))


def test_cancellazione_rimuove_il_file():
    backend = DemoAdbBackend(file_count=3)
    file = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    bersaglio = file[0].remote_path
    backend.delete_file("DEMO12345", bersaglio)
    rimasti = parse_stat_stream(backend.list_media_raw("DEMO12345", "stat"))
    assert bersaglio not in [f.remote_path for f in rimasti]


def test_check_riporta_una_versione_leggibile():
    assert "demo" in DemoAdbBackend().check().lower()
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_demo.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/core/demo.py`
```python
"""Telefono finto: serve per i test automatici e per la modalità demo senza dispositivo."""

from __future__ import annotations

import hashlib
import time
from typing import Iterator

from .errors import AdbError

SERIALE_DEMO = "DEMO12345"
MODELLO_DEMO = "Pixel_7_demo"

CARTELLE_DEMO = (
    ("/sdcard/DCIM/Camera", "IMG_%04d.jpg", "photo"),
    ("/sdcard/DCIM/Screenshots", "Screenshot_%04d.png", "photo"),
    ("/sdcard/Pictures/WhatsApp Images", "IMG-WhatsApp-%04d.jpg", "photo"),
    ("/sdcard/Movies", "VID_%04d.mp4", "video"),
)


def demo_files(file_count: int = 54) -> list[dict]:
    """Albero di esempio deterministico e vario, con nomi realistici e difficili."""
    file: list[dict] = []
    extra = ["Foto è così 😀.jpg", "Vacanze d'estate (1).jpg", "IMG con # e & strani.jpg"]
    for indice in range(file_count):
        cartella, schema, kind = CARTELLE_DEMO[indice % len(CARTELLE_DEMO)]
        if indice < len(extra):
            nome = extra[indice]
            cartella = CARTELLE_DEMO[0][0]
            kind = "photo"
        else:
            nome = schema % indice
        dimensione = 200_000 + (indice * 37_111) % 1_800_000
        file.append(
            {
                "path": f"{cartella}/{nome}",
                "size": dimensione,
                "mtime": int(time.time()) - indice * 3600,
                "kind": kind,
            }
        )
    return file


class DemoAdbBackend:
    """Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno."""

    def __init__(self, state: str = "device", file_count: int = 54, delay: float = 0.005) -> None:
        self.state = state
        self.delay = delay
        self._files = {voce["path"]: voce for voce in demo_files(file_count)}

    def check(self) -> str:
        return "Android Debug Bridge version (demo FotoFacile)"

    def devices_raw(self) -> str:
        if self.state == "nessuno":
            return "List of devices attached\n\n"
        return (
            "List of devices attached\n"
            f"{SERIALE_DEMO}          {self.state} product:demo model:{MODELLO_DEMO} "
            "device:demo transport_id:1\n"
        )

    def list_media_raw(self, serial: str, command: str) -> str:
        righe = []
        for voce in self._files.values():
            righe.append(f"{voce['size']}|{voce['mtime']}|{voce['path']}")
        return "\n".join(righe) + ("\n" if righe else "")

    def stream_file(self, serial: str, remote_path: str, chunk_size: int = 65536) -> Iterator[bytes]:
        voce = self._files.get(remote_path)
        if voce is None:
            raise AdbError(
                "File non trovato sul telefono (demo).",
                hint="Riprova la scansione.",
            )
        seme = hashlib.sha256(remote_path.encode("utf-8")).digest()
        generati = 0
        while generati < voce["size"]:
            lunghezza = min(chunk_size, voce["size"] - generati)
            blocco = (seme * ((lunghezza // len(seme)) + 1))[:lunghezza]
            generati += lunghezza
            if self.delay:
                time.sleep(min(self.delay, 0.05))
            yield blocco

    def delete_file(self, serial: str, remote_path: str) -> None:
        if remote_path not in self._files:
            raise AdbError("File non trovato sul telefono (demo).")
        del self._files[remote_path]

    def start_server(self) -> None:
        return None

    def restart_server(self) -> None:
        return None


DemoBackend = DemoAdbBackend
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde (la suite completa, non solo il file nuovo).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: backend demo senza telefono"
```

---

### Task 12: Aspetto e componenti grafici riusabili

**Files:**
- Create: `fotofacile/ui/theme.py`, `fotofacile/ui/widgets.py`, `tests/test_theme.py`, `tests/test_widgets.py`

**Interfaces:**
- Consumes: `FotoFacileError` (Task 2), `open_in_file_manager` (Task 2b)
- Produces:
  - `theme.FONT_PREFERITI: tuple[str, ...]`, `theme.COLORI: dict[str, str]`
  - `theme.pick_font_family(available: set[str] | None = None) -> str`
  - `theme.apply_theme(root, available_families: set[str] | None = None) -> None`
  - `theme.font(size: int = 12, bold: bool = False) -> tuple`
  - `widgets.StepIndicator(parent, steps: Sequence[str])` con `set_step(index: int) -> None`
  - `widgets.LogPane(parent)` con `append(text: str)`, `clear()`, `get_text() -> str`
  - `widgets.Banner(parent)` con `show(message: str, hint: str = "", kind: str = "info")`, `hide()`
  - `widgets.PathChooser(parent, on_change=None)` con `get() -> str`, `set(path: str) -> None`, `browse()`
  - `widgets.tk_available() -> bool` (utile per saltare i test grafici su macchine senza schermo)

- [ ] **Step 1: Test che falliscono**

`tests/test_theme.py`
```python
from fotofacile.ui.theme import COLORI, FONT_PREFERITI, font, pick_font_family


def test_sceglie_il_primo_font_disponibile():
    assert pick_font_family({"DejaVu Sans", "Arial"}) == "DejaVu Sans"
    assert pick_font_family({"Segoe UI"}) == "Segoe UI"
    assert pick_font_family({"Helvetica Neue", "DejaVu Sans"}) == "Helvetica Neue"


def test_ricade_su_un_font_generico_se_nessuno_disponibile():
    assert pick_font_family(set()) == FONT_PREFERITI[-1]


def test_palette_completa():
    for chiave in ("sfondo", "testo", "primario", "successo", "errore", "avviso"):
        assert COLORI[chiave].startswith("#")


def test_font_restituisce_tupla_usabile_da_tkinter():
    normale = font(14)
    grassetto = font(14, bold=True)
    assert normale[1] == 14
    assert grassetto[2] == "bold"
    assert normale[0] == grassetto[0]
```

`tests/test_widgets.py`
```python
import pytest

from fotofacile.ui.widgets import Banner, LogPane, PathChooser, StepIndicator, tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def root():
    import tkinter as tk

    finestra = tk.Tk()
    finestra.withdraw()
    yield finestra
    finestra.destroy()


def test_indicatore_passi(root):
    indicatore = StepIndicator(root, ["Collega", "Scegli", "Opzioni", "Copia"])
    indicatore.set_step(0)
    assert indicatore.current == 0
    indicatore.set_step(3)
    assert indicatore.current == 3


def test_pannello_registro(root):
    pannello = LogPane(root)
    pannello.append("prima riga")
    pannello.append("seconda riga")
    assert "prima riga" in pannello.get_text()
    assert "seconda riga" in pannello.get_text()
    pannello.clear()
    assert pannello.get_text() == ""


def test_banner_mostra_messaggio_e_suggerimento(root):
    banner = Banner(root)
    banner.show("Telefono non collegato", hint="Controlla il cavo", kind="avviso")
    assert banner.visible is True
    assert "Telefono non collegato" in banner.message_text
    assert "Controlla il cavo" in banner.hint_text
    banner.hide()
    assert banner.visible is False


def test_scelta_cartella_aggiorna_il_valore(root, tmp_path):
    cambi = []
    chooser = PathChooser(root, on_change=cambi.append)
    chooser.set(str(tmp_path))
    assert chooser.get() == str(tmp_path)
    assert cambi == [str(tmp_path)]
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_theme.py tests/test_widgets.py -q`
Expected: FAIL `ModuleNotFoundError` (theme) e poi i test dei widget saltati se non c'è schermo.

- [ ] **Step 3: Implementare**

`fotofacile/ui/theme.py`
```python
"""Aspetto dell'interfaccia: stile ttk, colori e scelta dei font multipiattaforma."""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk

FONT_PREFERITI = ("Segoe UI", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", "Arial")
COLORI = {
    "sfondo": "#f2f4f7",
    "pannello": "#ffffff",
    "testo": "#1f2430",
    "tenue": "#5b6472",
    "primario": "#1565c0",
    "primario_attivo": "#0d47a1",
    "successo": "#1b7f4b",
    "avviso": "#b26a00",
    "errore": "#b3261e",
    "bordo": "#d4d8e0",
}
_FAMIGLIA = "TkDefaultFont"


def pick_font_family(available: set[str] | None = None) -> str:
    if available is None:
        try:
            available = set(tk.font.families())  # type: ignore[attr-defined]
        except (AttributeError, tk.TclError):  # pragma: no cover - ambienti senza Tk
            available = set()
    for preferito in FONT_PREFERITI:
        if preferito in available:
            return preferito
    return FONT_PREFERITI[-1]


def font(size: int = 12, bold: bool = False) -> tuple:
    return (_FAMIGLIA, size, "bold") if bold else (_FAMIGLIA, size)


def _tema_disponibile(root: tk.Misc) -> str:
    stile = ttk.Style(root)
    disponibili = set(stile.theme_names())
    preferiti = ["vista", "aqua", "clam"] if sys.platform == "win32" else ["aqua", "clam", "vista"]
    for nome in preferiti:
        if nome in disponibili:
            return nome
    return stile.theme_use()


def apply_theme(root: tk.Misc, available_families: set[str] | None = None) -> None:
    """Applica il tema scelto in base al sistema: vista (Windows), aqua (macOS), clam (Linux)."""
    global _FAMIGLIA
    _FAMIGLIA = pick_font_family(available_families)
    stile = ttk.Style(root)
    stile.theme_use(_tema_disponibile(root))
    root.configure(background=COLORI["sfondo"])
    stile.configure(".", background=COLORI["sfondo"], foreground=COLORI["testo"], font=font(12))
    stile.configure("TFrame", background=COLORI["sfondo"])
    stile.configure("Card.TFrame", background=COLORI["pannello"], relief="flat")
    stile.configure("TLabel", background=COLORI["sfondo"], foreground=COLORI["testo"])
    stile.configure("Titolo.TLabel", font=font(22, bold=True))
    stile.configure("Sottotitolo.TLabel", font=font(14), foreground=COLORI["tenue"])
    stile.configure("Tenue.TLabel", foreground=COLORI["tenue"])
    stile.configure("Successo.TLabel", foreground=COLORI["successo"], font=font(14, bold=True))
    stile.configure("Avviso.TLabel", foreground=COLORI["avviso"])
    stile.configure("Errore.TLabel", foreground=COLORI["errore"])
    stile.configure(
        "Big.TButton",
        font=font(14, bold=True),
        padding=(18, 12),
    )
    stile.configure("Secondary.TButton", font=font(12), padding=(10, 6))
    stile.configure("Barra.Horizontal.TProgressbar", troughcolor=COLORI["bordo"])
```

`fotofacile/ui/widgets.py`
```python
"""Componenti grafici riusabili, senza logica di business."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk
from typing import Callable, Sequence

from .theme import COLORI, font


def tk_available() -> bool:
    """True se questa macchina può aprire finestre (evita errori nei test senza schermo)."""
    try:
        finestra = tk.Tk()
    except tk.TclError:
        return False
    finestra.destroy()
    return True


class StepIndicator(ttk.Frame):
    """Barra dei 4 passi con evidenziazione di quello attuale."""

    def __init__(self, parent: tk.Misc, steps: Sequence[str]) -> None:
        super().__init__(parent)
        self.steps = list(steps)
        self.current = 0
        self._etichette: list[ttk.Label] = []
        for indice, nome in enumerate(self.steps, start=1):
            etichetta = ttk.Label(self, text=f"{indice}. {nome}", padding=(8, 4))
            etichetta.grid(row=0, column=indice, padx=6)
            self._etichette.append(etichetta)
        self.set_step(0)

    def set_step(self, index: int) -> None:
        self.current = max(0, min(index, len(self.steps) - 1))
        for posizione, etichetta in enumerate(self._etichette):
            if posizione == self.current:
                etichetta.configure(foreground=COLORI["primario"], font=font(12, bold=True))
            elif posizione < self.current:
                etichetta.configure(foreground=COLORI["successo"], font=font(12))
            else:
                etichetta.configure(foreground=COLORI["tenue"], font=font(12))


class LogPane(ttk.Frame):
    """Area di testo scorrevole con il dettaglio delle operazioni."""

    def __init__(self, parent: tk.Misc, height: int = 8) -> None:
        super().__init__(parent)
        self.text = tk.Text(self, height=height, wrap="word", state="disabled", font=font(11))
        self.text.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=barra.set)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def append(self, testo: str) -> None:
        self.text.configure(state="normal")
        self.text.insert("end", testo.rstrip("\n") + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def get_text(self) -> str:
        return self.text.get("1.0", "end").strip()


class Banner(ttk.Frame):
    """Messaggio grande con eventuale suggerimento: è il modo in cui l'app parla all'utente."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent)
        self.message_text = ""
        self.hint_text = ""
        self.kind = "info"
        self.visible = False
        self._messaggio = ttk.Label(self, text="", font=font(15, bold=True), wraplength=760, justify="left")
        self._suggerimento = ttk.Label(self, text="", font=font(12), wraplength=760, justify="left")
        self._messaggio.grid(row=0, column=0, sticky="w")
        self._suggerimento.grid(row=1, column=0, sticky="w")

    def show(self, message: str, hint: str = "", kind: str = "info") -> None:
        self.message_text, self.hint_text, self.kind = message, hint, kind
        colore = {
            "info": COLORI["testo"],
            "successo": COLORI["successo"],
            "avviso": COLORI["avviso"],
            "errore": COLORI["errore"],
        }.get(kind, COLORI["testo"])
        self._messaggio.configure(text=message, foreground=colore)
        self._suggerimento.configure(text=hint, foreground=COLORI["tenue"])
        self.visible = True
        self.grid()

    def hide(self) -> None:
        self.visible = False
        self.grid_remove()


class PathChooser(ttk.Frame):
    """Riquadro con il percorso scelto e il pulsante «Sfoglia…»."""

    def __init__(self, parent: tk.Misc, on_change: Callable[[str], None] | None = None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._variabile = tk.StringVar()
        self._campo = ttk.Entry(self, textvariable=self._variabile, font=font(12))
        self._campo.grid(row=0, column=0, sticky="ew")
        ttk.Button(self, text="Sfoglia…", style="Secondary.TButton", command=self.browse).grid(row=0, column=1, padx=6)
        self.columnconfigure(0, weight=1)

    def get(self) -> str:
        return self._variabile.get()

    def set(self, path: str) -> None:
        self._variabile.set(path)
        if self._on_change is not None:
            self._on_change(path)

    def browse(self) -> None:
        scelta = filedialog.askdirectory(initialdir=self.get() or None, title="Scegli dove salvare le foto")
        if scelta:
            self.set(scelta)
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde (i test grafici passano se c'è un ambiente grafico, altrimenti sono saltati).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: tema multipiattaforma e componenti grafici riusabili"
```

---

### Task 13: Finestra principale, navigazione e lavoro in background

**Files:**
- Create: `fotofacile/ui/app.py`, `fotofacile/cli.py`, `fotofacile.py`, `tests/test_cli.py`, `tests/test_ui_app.py`

**Interfaces:**
- Consumes: `find_adb`, `RealAdbBackend` (Task 2), `osutil` (Task 2b), `DemoAdbBackend` (Task 11), `theme`/`widgets` (Task 12)
- Produces:
  - `App(tk.Tk)` con: `pages: dict[str, ttk.Frame]`, `go_to(key: str) -> None`, `run_async(fn, on_done=None, on_error=None) -> None`, `pump_events() -> None`, `log(text) -> None`, `set_status(text, kind="info") -> None`, attributi `backend`, `device`, `media_files`, `selected_folders`, `options`, `results`, `demo_mode`, `cancel_event`
  - `App.register_page(key: str, page: ttk.Frame) -> None`
  - `cli.build_doctor_report(...) -> str`, `cli.main(argv: Sequence[str] | None = None) -> int`
  - `fotofacile.py` → `from fotofacile.cli import main; raise SystemExit(main())`

- [ ] **Step 1: Test che falliscono**

`tests/test_cli.py`
```python
from fotofacile import __version__
from fotofacile.cli import build_doctor_report, main


def test_versione(tmp_path, capsys):
    esito = main(["--version"], env={"HOME": str(tmp_path)})
    assert esito == 0
    assert __version__ in capsys.readouterr().out


def test_aiuto_elenca_le_modalita(capsys):
    assert main(["--help"], env={}) == 0
    uscita = capsys.readouterr().out
    assert "--demo" in uscita
    assert "doctor" in uscita


def test_diagnostica_riporta_tutte_le_voci():
    testo = build_doctor_report(
        adb_path=None,
        adb_version="",
        system="darwin",
        python_version="3.14.7",
        tk_version="9.0",
        devices=[],
        app_folder="/tmp/.fotofacile",
        writing_ok=True,
    )
    assert "Sistema: darwin" in testo
    assert "Python: 3.14.7" in testo
    assert "Tkinter: 9.0" in testo
    assert "Componente: non trovato" in testo
    assert "Telefoni collegati: nessuno" in testo
    assert "Scrittura: ok" in testo


def test_diagnostica_con_telefono_e_componente():
    testo = build_doctor_report(
        adb_path="/usr/bin/adb",
        adb_version="Android Debug Bridge version 1.0.41",
        system="win32",
        python_version="3.12.0",
        tk_version="8.6",
        devices=[("R5CT30", "device")],
        app_folder="C:/Users/tizio/.fotofacile",
        writing_ok=False,
    )
    assert "/usr/bin/adb" in testo
    assert "R5CT30 (device)" in testo
    assert "Scrittura: problema" in testo


def test_modalita_demo_non_apre_finestre_in_ambiente_senza_schermo(monkeypatch, capsys):
    from fotofacile import cli

    monkeypatch.setattr(cli, "start_gui", lambda **kwargs: 0)
    assert cli.main(["--demo"], env={}) == 0
```

`tests/test_ui_app.py`
```python
import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app():
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=6), demo_mode=True)
    applicazione.withdraw()
    yield applicazione
    applicazione.destroy()


def test_pagine_registrate(app):
    assert set(app.pages) == {"connect", "select", "options", "transfer"}
    for pagina in app.pages.values():
        assert pagina.winfo_exists()


def test_navigazione_avanti_e_indietro(app):
    app.go_to("connect")
    assert app.pages["connect"].winfo_ismapped() in (True, False)
    app.go_to("select")
    assert app.current_page == "select"
    app.go_to("prev")
    assert app.current_page == "connect"


def test_registro_e_stato(app):
    app.log("ciao")
    assert "ciao" in app.log_pane.get_text()
    app.set_status("Telefono collegato", kind="successo")
    assert app.banner.visible is True
    assert "Telefono collegato" in app.banner.message_text


def test_lavoro_in_background_aggiorna_la_ui(app):
    esiti = []
    app.run_async(lambda: 21 * 2, on_done=lambda valore: esiti.append(valore))
    for _ in range(50):
        app.update()
        app.pump_events()
        if esiti:
            break
    assert esiti == [42]


def test_errore_in_background_mostra_messaggio_umano(app):
    from fotofacile.core.errors import FotoFacileError

    def fallisci():
        raise FotoFacileError("Il telefono non risponde", hint="Controlla il cavo")

    app.run_async(fallisci)
    for _ in range(50):
        app.update()
        app.pump_events()
        if app.banner.visible:
            break
    assert "Il telefono non risponde" in app.banner.message_text
    assert "Controlla il cavo" in app.banner.hint_text
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_cli.py tests/test_ui_app.py -q`
Expected: FAIL `ModuleNotFoundError: No module named 'fotofacile.ui.app'`

- [ ] **Step 3: Implementare**

`fotofacile/ui/app.py`
```python
"""Finestra principale: navigazione fra i passi, lavoro in background, registro."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from ..core.adb import RealAdbBackend, find_adb
from ..core.demo import DemoAdbBackend
from ..core.errors import FotoFacileError
from .theme import COLORI, apply_theme
from .widgets import Banner, LogPane, StepIndicator

PASSI = ("Collega il telefono", "Scegli le foto", "Destinazione", "Copia")
ORDINE = ("connect", "select", "options", "transfer")


class App(tk.Tk):
    """Contenitore della procedura guidata; le pagine vivono in `pages`."""

    def __init__(
        self,
        backend: Any | None = None,
        demo_mode: bool = False,
        adb_path: str | None = None,
    ) -> None:
        super().__init__()
        self.title("FotoFacile — copia le foto dal telefono al computer")
        self.geometry("960x700")
        self.minsize(880, 640)
        apply_theme(self)

        self.demo_mode = demo_mode
        self.adb_path = adb_path or find_adb()
        self.backend = backend or (DemoAdbBackend() if demo_mode else self._crea_backend())
        self.device = None
        self.media_files: list = []
        self.selected_folders: list[str] = []
        self.options = None
        self.results = None
        self.cancel_event = threading.Event()
        self.events: queue.Queue = queue.Queue()
        self._lavori: list[threading.Thread] = []

        self.step_indicator = StepIndicator(self, PASSI)
        self.step_indicator.grid(row=0, column=0, sticky="w", padx=18, pady=(14, 4))
        self.banner = Banner(self)
        self.banner.grid(row=1, column=0, sticky="ew", padx=18, pady=8)

        self.container = ttk.Frame(self)
        self.container.grid(row=2, column=0, sticky="nsew", padx=18, pady=6)
        self.log_pane = LogPane(self, height=7)
        self.log_pane.grid(row=3, column=0, sticky="nsew", padx=18, pady=(6, 14))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.pages: dict[str, ttk.Frame] = {}
        self.current_page = ""
        self._costruisci_pagine()
        self.go_to("connect")
        self.after(50, self.pump_events)

    # ── costruzione ───────────────────────────────────────────────────────
    def _crea_backend(self):
        if not self.adb_path:
            return None
        return RealAdbBackend(self.adb_path)

    def _costruisci_pagine(self) -> None:
        from .page_connect import ConnectPage
        from .page_options import OptionsPage
        from .page_select import SelectPage
        from .page_transfer import TransferPage

        self.register_page("connect", ConnectPage(self))
        self.register_page("select", SelectPage(self))
        self.register_page("options", OptionsPage(self))
        self.register_page("transfer", TransferPage(self))

    def register_page(self, key: str, page: ttk.Frame) -> None:
        self.pages[key] = page
        page.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    # ── navigazione ───────────────────────────────────────────────────────
    def go_to(self, key: str) -> None:
        if key == "prev":
            indice = max(0, ORDINE.index(self.current_page) - 1)
            key = ORDINE[indice]
        elif key == "next":
            indice = min(len(ORDINE) - 1, ORDINE.index(self.current_page) + 1)
            key = ORDINE[indice]
        pagina = self.pages[key]
        pagina.tkraise()
        pagina.on_show()
        self.current_page = key
        self.step_indicator.set_step(ORDINE.index(key))
        self.banner.hide()

    # ── messaggi e registro ───────────────────────────────────────────────
    def log(self, testo: str) -> None:
        self.log_pane.append(testo)

    def set_status(self, text: str, hint: str = "", kind: str = "info") -> None:
        self.banner.show(text, hint=hint, kind=kind)

    # ── lavoro in background ──────────────────────────────────────────────
    def run_async(
        self,
        funzione: Callable[[], Any],
        on_done: Callable[[Any], None] | None = None,
        on_error: Callable[[FotoFacileError], None] | None = None,
    ) -> None:
        def lavora() -> None:
            try:
                risultato = funzione()
            except FotoFacileError as errore:
                self.events.put(("errore", errore, on_error))
            except Exception as errore:  # pragma: no cover - rete di sicurezza
                self.events.put(("imprevisto", errore, on_error))
            else:
                self.events.put(("fatto", risultato, on_done))

        filo = threading.Thread(target=lavora, daemon=True)
        self._lavori.append(filo)
        filo.start()

    def pump_events(self) -> None:
        """Svuota la coda dei risultati: è l'unico punto in cui la UI viene aggiornata."""
        while True:
            try:
                tipo, dato, callback = self.events.get_nowait()
            except queue.Empty:
                break
            if tipo == "fatto":
                if callback is not None:
                    callback(dato)
            elif tipo == "errore":
                if callback is not None:
                    callback(dato)
                else:
                    self.set_status(dato.message, hint=dato.hint, kind="errore")
                    self.log(f"Errore: {dato.message} {dato.hint}".strip())
            else:  # pragma: no cover - rete di sicurezza
                self.set_status(
                    "Qualcosa non ha funzionato come previsto.",
                    hint="Riprova; se il problema resta, apri il registro e salvalo.",
                    kind="errore",
                )
                self.log(f"Errore imprevisto: {dato}")
        self.after(50, self.pump_events)
```

`fotofacile/cli.py`
```python
"""Avvio del programma: interfaccia grafica, modalità demo e diagnosi."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Mapping, Sequence

from . import __version__
from .core.adb import find_adb
from .core.devices import get_devices
from .core.osutil import app_dir, python_command


def build_doctor_report(
    adb_path: str | None,
    adb_version: str,
    system: str,
    python_version: str,
    tk_version: str,
    devices: Sequence[tuple[str, str]],
    app_folder: str,
    writing_ok: bool,
) -> str:
    righe = [
        "FotoFacile — diagnosi",
        "──────────────────────────────",
        f"Sistema: {system}",
        f"Python: {python_version}",
        f"Tkinter: {tk_version}",
        f"Componente: {adb_path or 'non trovato'}",
    ]
    if adb_version:
        righe.append(f"Versione componente: {adb_version}")
    if devices:
        righe.append("Telefoni collegati: " + ", ".join(f"{seriale} ({stato})" for seriale, stato in devices))
    else:
        righe.append("Telefoni collegati: nessuno")
    righe.append(f"Cartella dati: {app_folder}")
    righe.append(f"Scrittura: {'ok' if writing_ok else 'problema'}")
    if not adb_path:
        righe.append("")
        righe.append(f"Suggerimento: apri FotoFacile senza argomenti e premi «Installa componente».")
    return "\n".join(righe) + "\n"


def doctor(env: Mapping[str, str] | None = None) -> int:
    ambiente = dict(env if env is not None else os.environ)
    percorso_adb = find_adb(env=ambiente)
    versione = ""
    dispositivi: list[tuple[str, str]] = []
    if percorso_adb:
        try:
            from .core.adb import RealAdbBackend

            backend = RealAdbBackend(percorso_adb)
            versione = backend.check()
            dispositivi = [(d.serial, d.state) for d in get_devices(backend)]
        except Exception as errore:  # pragma: no cover - diagnosi best effort
            versione = f"non utilizzabile ({errore})"
    cartella = app_dir(ambiente)
    try:
        cartella.mkdir(parents=True, exist_ok=True)
        prova = cartella / ".prova-scrittura"
        prova.write_text("ok")
        prova.unlink()
        scrittura = True
    except OSError:
        scrittura = False
    try:
        import tkinter

        versione_tk = str(tkinter.TkVersion)
    except Exception:  # pragma: no cover - Tkinter assente
        versione_tk = "non disponibile"
    print(
        build_doctor_report(
            adb_path=percorso_adb,
            adb_version=versione,
            system=sys.platform,
            python_version=sys.version.split()[0],
            tk_version=versione_tk,
            devices=dispositivi,
            app_folder=str(cartella),
            writing_ok=scrittura,
        )
    )
    return 0


def start_gui(demo: bool = False) -> int:
    from .ui.app import App

    applicazione = App(demo_mode=demo)
    applicazione.mainloop()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fotofacile",
        description="Copia le foto dal telefono Android al computer, passo per passo.",
    )
    parser.add_argument("--demo", action="store_true", help="prova il programma senza telefono")
    parser.add_argument("--version", action="version", version=f"FotoFacile {__version__}")
    parser.add_argument("comando", nargs="?", choices=["doctor"], help="«doctor» mostra la diagnosi del sistema")
    return parser


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    parser = build_parser()
    argomenti = parser.parse_args(list(argv) if argv is not None else None)
    if argomenti.comando == "doctor":
        return doctor(env)
    return start_gui(demo=argomenti.demo)
```

`fotofacile.py`
```python
#!/usr/bin/env python3
"""Avvio rapido: python3 fotofacile.py  (su Windows: py fotofacile.py)."""

from fotofacile.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: finestra principale, navigazione, lavoro in background e CLI"
```

---

### Task 14: Passo 1 — collegamento del telefono

**Files:**
- Create: `fotofacile/ui/page_connect.py`, `tests/test_page_connect.py`

**Interfaces:**
- Consumes: `App` (Task 13), `devices` (Task 3), `installer` (Task 10), `DemoAdbBackend` (Task 11), `widgets` (Task 12)
- Produces:
  - `ConnectPage(parent)` con: `on_show() -> None`, `check_now() -> None`, `start_polling() -> None`, `stop_polling() -> None`, `install_component() -> None`, `enable_demo() -> None`, `restart_connection() -> None`, `HELP_BRANDS: dict[str, list[str]]`
  - `build_help_text(brand: str) -> str`

- [ ] **Step 1: Test che falliscono**

`tests/test_page_connect.py`
```python
import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.ui.page_connect import HELP_BRANDS, build_help_text
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app():
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=4), demo_mode=True)
    applicazione.withdraw()
    applicazione.pages["connect"].stop_polling()
    yield applicazione
    applicazione.destroy()


def test_aiuto_contiene_le_marche_e_i_passi():
    for marca in ("Samsung", "Xiaomi", "Google", "Huawei", "Oppo"):
        assert marca in HELP_BRANDS
    testo = build_help_text("Samsung")
    assert "Debug USB" in testo
    assert len(HELP_BRANDS["Samsung"]) >= 3


def test_riconosce_il_telefono_pronto(app):
    pagina = app.pages["connect"]
    pagina.check_now()
    for _ in range(30):
        app.update()
        app.pump_events()
        if app.device is not None:
            break
    assert app.device is not None
    assert app.device.serial == "DEMO12345"
    assert "pronto" in pagina.message.lower() or "collegato" in pagina.message.lower()


def test_telefono_non_autorizzato_mostra_istruzioni(app):
    app.backend.state = "unauthorized"
    pagina = app.pages["connect"]
    pagina.check_now()
    for _ in range(30):
        app.update()
        app.pump_events()
        if "Consenti" in pagina.message:
            break
    assert "Consenti" in pagina.message
    assert app.device is None


def test_nessun_telefono_invita_a_collegarlo(app):
    app.backend.state = "nessuno"
    pagina = app.pages["connect"]
    pagina.check_now()
    for _ in range(30):
        app.update()
        app.pump_events()
        if "collega" in pagina.message.lower():
            break
    assert "collega" in pagina.message.lower()
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_page_connect.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/ui/page_connect.py`
```python
"""Passo 1: guidare la persona a collegare il telefono e autorizzare il computer."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..core.devices import STATE_MESSAGE, get_devices
from ..core.installer import component_dir, install_component, is_installed
from ..core.osutil import python_command
from .theme import COLORI, font

HELP_BRANDS: dict[str, list[str]] = {
    "Samsung": [
        "Apri «Impostazioni».",
        "Vai in «Info sul telefono» e tocca «Informazioni sul software».",
        "Tocca «Numero di build» 7 volte: apparirà la voce «Opzioni sviluppatore».",
        "Torna in «Impostazioni» → «Opzioni sviluppatore» e attiva «Debug USB».",
    ],
    "Xiaomi / Redmi / POCO": [
        "Apri «Impostazioni» → «Info sul telefono».",
        "Tocca «Versione MIUI» (o «Numero di build») 7 volte.",
        "Apri «Impostazioni» → «Impostazioni aggiuntive» → «Opzioni sviluppatore».",
        "Attiva «Debug USB».",
    ],
    "Google / Pixel": [
        "Apri «Impostazioni» → «Info sul telefono».",
        "Tocca «Numero di build» 7 volte.",
        "Apri «Impostazioni» → «Sistema» → «Opzioni sviluppatore».",
        "Attiva «Debug USB».",
    ],
    "Huawei / Honor": [
        "Apri «Impostazioni» → «Info sul telefono».",
        "Tocca «Numero di build» 7 volte.",
        "Apri «Impostazioni» → «Sistema e aggiornamenti» → «Opzioni sviluppatore».",
        "Attiva «Debug USB».",
    ],
    "Oppo / Realme / OnePlus": [
        "Apri «Impostazioni» → «Info sul telefono» → «Versione».",
        "Tocca «Numero di build» 7 volte.",
        "Apri «Impostazioni» → «Sistema» → «Opzioni sviluppatore».",
        "Attiva «Debug USB».",
    ],
}

BRAND_SCONOSCIUTO = "Un altro telefono"


def build_help_text(brand: str) -> str:
    """Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca."""
    passi = HELP_BRANDS.get(brand, HELP_BRANDS["Samsung"])
    righe = [
        f"Come attivare il «Debug USB» — {brand}",
        "",
        "Il telefono deve autorizzare il computer: è una procedura da fare una sola volta.",
        "",
    ]
    righe.extend(f"{indice}. {passo}" for indice, passo in enumerate(passi, start=1))
    righe.extend(
        [
            "",
            "Quando lo schermo del telefono chiede «Consentire il debug USB?», tocca «Consenti».",
            "",
            "Se il telefono non viene riconosciuto:",
            "• prova un altro cavo USB (alcuni cavi servono solo per ricaricare);",
            "• su Windows, installa il driver USB del produttore del telefono;",
            "• scollega e ricollega il cavo dopo aver attivato il «Debug USB».",
        ]
    )
    return "\n".join(righe)


class ConnectPage(ttk.Frame):
    """Prima schermata: collega il telefono, con aiuto, installazione e prova demo."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.message = ""
        self._polling = False
        self._in_corso = False

        ttk.Label(self, text="Collega il telefono al computer", style="Titolo.TLabel").grid(
            row=0, column=0, sticky="w", pady=(4, 2)
        )
        ttk.Label(
            self,
            text="Usa il cavo USB e tieni il telefono sbloccato: ti chiederà di autorizzare il computer.",
            style="Sottotitolo.TLabel",
            wraplength=820,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.indicatore = ttk.Label(self, text="●  Sto cercando il telefono…", font=font(16, bold=True))
        self.indicatore.grid(row=2, column=0, sticky="w", pady=(6, 2))
        self.dettaglio = ttk.Label(self, text="", style="Tenue.TLabel", font=font(12))
        self.dettaglio.grid(row=3, column=0, sticky="w")

        pulsanti = ttk.Frame(self)
        pulsanti.grid(row=4, column=0, sticky="w", pady=14)
        self.bottone_aiuto = ttk.Button(
            pulsanti, text="Come si attiva il Debug USB?", style="Secondary.TButton", command=self.show_help
        )
        self.bottone_aiuto.grid(row=0, column=0, padx=(0, 8))
        self.bottone_installa = ttk.Button(
            pulsanti, text="Installa componente mancante", style="Secondary.TButton", command=self.install_component
        )
        self.bottone_installa.grid(row=0, column=1, padx=8)
        self.bottone_ricarica = ttk.Button(
            pulsanti, text="Riavvia collegamento", style="Secondary.TButton", command=self.restart_connection
        )
        self.bottone_ricarica.grid(row=0, column=2, padx=8)

        self.bottone_avanti = ttk.Button(self, text="Avanti  →", style="Big.TButton", command=self._avanti)
        self.bottone_avanti.grid(row=5, column=0, sticky="e", pady=(10, 0))
        self.bottone_avanti.state(["disabled"])

        ttk.Button(
            self,
            text="Prova il programma senza telefono (demo)",
            style="Secondary.TButton",
            command=self.enable_demo,
        ).grid(row=6, column=0, sticky="w", pady=(18, 0))

        self.columnconfigure(0, weight=1)
        self._aggiorna_bottone_installa()
        self.set_message("Collega il telefono con il cavo e sbloccalo.")

    # ── messaggi ──────────────────────────────────────────────────────────
    def set_message(self, testo: str, tono: str = "info") -> None:
        self.message = testo
        colori = {"info": COLORI["testo"], "successo": COLORI["successo"], "avviso": COLORI["avviso"]}
        self.indicatore.configure(text=testo, foreground=colori.get(tono, COLORI["testo"]))

    def _aggiorna_bottone_installa(self) -> None:
        mancante = not is_installed() and self.app.adb_path is None and not self.app.demo_mode
        self.bottone_installa.state(["!disabled"] if mancante else ["disabled"])

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        self.start_polling()

    def start_polling(self) -> None:
        if self._polling:
            return
        self._polling = True
        self.check_now()

    def stop_polling(self) -> None:
        self._polling = False

    def _tick(self) -> None:
        if self._polling:
            self.check_now()
        self.after(2000, self._tick)

    def check_now(self) -> None:
        """Chiede al telefono come sta; aggiorna i messaggi in base allo stato reale."""
        backend = self.app.backend
        if backend is None:
            self.set_message("Manca il componente di collegamento.", tono="avviso")
            self.dettaglio.configure(
                text=f"Premi «Installa componente mancante» per scaricarlo automaticamente."
            )
            return
        if self._in_corso:
            return
        self._in_corso = True

        def leggi():
            try:
                return get_devices(backend)
            finally:
                self._in_corso = False

        self.app.run_async(leggi, on_done=self._dispositivi_ricevuti)

    def _dispositivi_ricevuti(self, dispositivi) -> None:
        pronto = next((d for d in dispositivi if d.is_ready), None)
        if pronto is not None:
            self.app.device = pronto
            self.set_message(f"Perfetto! Telefono collegato: {pronto.display_name}", tono="successo")
            self.dettaglio.configure(text="Ora scegli quali foto copiare.")
            self.bottone_avanti.state(["!disabled"])
            self.stop_polling()
            return
        self.app.device = None
        self.bottone_avanti.state(["disabled"])
        if not dispositivi:
            self.set_message("Non vedo ancora nessun telefono: collegalo con il cavo e sbloccalo.")
            self.dettaglio.configure(text="Suggerimento: se hai già collegato il cavo, prova un altro cavo USB.")
            return
        stato = dispositivi[0].state
        messaggio, suggerimento = STATE_MESSAGE.get(stato, ("Il telefono non è pronto.", "Riprova fra qualche secondo."))
        self.set_message(messaggio, tono="avviso")
        self.dettaglio.configure(text=suggerimento)

    # ── azioni ────────────────────────────────────────────────────────────
    def _avanti(self) -> None:
        if self.app.device is not None:
            self.stop_polling()
            self.app.go_to("select")

    def show_help(self) -> None:
        """Legge le istruzioni per marca tramite una piccola finestra con menù a tendina."""
        finestra = tk.Toplevel(self)
        finestra.title("Come attivare il Debug USB")
        finestra.geometry("640x520")
        marca = tk.StringVar(value="Samsung")
        testo = tk.Text(finestra, wrap="word", font=font(12), height=18)
        testo.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))

        def aggiorna(*_args) -> None:
            testo.configure(state="normal")
            testo.delete("1.0", "end")
            testo.insert("1.0", build_help_text(marca.get()))
            testo.configure(state="disabled")

        selettore = ttk.Combobox(
            finestra, textvariable=marca, values=[*HELP_BRANDS, BRAND_SCONOSCIUTO], state="readonly"
        )
        selettore.grid(row=0, column=0, sticky="ew", padx=14, pady=12)
        selettore.bind("<<ComboboxSelected>>", aggiorna)
        ttk.Button(finestra, text="Ho capito", style="Secondary.TButton", command=finestra.destroy).grid(
            row=2, column=0, pady=(0, 12)
        )
        finestra.columnconfigure(0, weight=1)
        finestra.rowconfigure(1, weight=1)
        aggiorna()

    def install_component(self) -> None:
        """Scarica il componente mancante mostrando l'avanzamento nel registro."""
        self.app.set_status("Sto scaricando il componente di collegamento…", kind="info")
        self.bottone_installa.state(["disabled"])

        def scarica():
            def progresso(info: dict) -> None:
                totale = info.get("totale") or 0
                percentuale = f"{info['ricevuti'] * 100 // totale}%" if totale else ""
                self.app.log(f"Download componente: {info['ricevuti'] // 1024} KB {percentuale}")

            return install_component(on_progress=None if self.app.demo_mode else progresso)

        def fatto(percorso):
            self.app.adb_path = str(percorso)
            from ..core.adb import RealAdbBackend

            self.app.backend = RealAdbBackend(str(percorso))
            self.app.log(f"Componente pronto: {percorso}")
            self.app.set_status("Componente installato. Ora collega il telefono.", kind="successo")
            self.check_now()

        self.app.run_async(scarica, on_done=fatto)

    def restart_connection(self) -> None:
        if self.app.backend is None:
            self.app.set_status("Installa prima il componente di collegamento.", kind="avviso")
            return
        self.app.set_status("Sto riavviando il collegamento…", kind="info")
        self.app.run_async(
            self.app.backend.restart_server,
            on_done=lambda _esito: self.check_now(),
        )

    def enable_demo(self) -> None:
        """Attiva la modalità demo: telefono finto, così si può provare tutto senza dispositivo."""
        from ..core.demo import DemoAdbBackend

        self.app.demo_mode = True
        self.app.backend = DemoAdbBackend(file_count=54)
        self.app.log("Modalità demo attiva: verrà usato un telefono finto.")
        self.set_message("Modalità demo: telefono finto collegato.", tono="successo")
        self.check_now()
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: passo 1 con aiuto per marca, installazione componente e modalità demo"
```

---

### Task 15: Passo 2 — scelta delle foto

**Files:**
- Create: `fotofacile/ui/page_select.py`, `tests/test_page_select.py`

**Interfaces:**
- Consumes: `App` (Task 13), `scanner` (Task 5), `format` (Task 4)
- Produces: `SelectPage(parent)` con `on_show()`, `start_scan() -> None`, `scan_sync() -> tuple[list[MediaFolder], list[MediaFile]]`, `rebuild_list(folders) -> None`, `selected_labels() -> list[str]`, `go_next() -> None`, `sto_scegliendo_video: bool`

- [ ] **Step 1: Test che falliscono**

`tests/test_page_select.py`
```python
import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app():
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=12), demo_mode=True)
    applicazione.withdraw()
    applicazione.pages["connect"].stop_polling()
    applicazione.device = applicazione.backend and __import__(
        "fotofacile.core.devices", fromlist=["DeviceInfo"]
    ).DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    yield applicazione
    applicazione.destroy()


def test_scansione_riempie_la_lista(app):
    pagina = app.pages["select"]
    cartelle, file = pagina.scan_sync()
    assert file
    assert cartelle
    pagina.rebuild_list(cartelle)
    assert len(pagina.folder_vars) == len(cartelle)
    assert all(voce.get() for voce in pagina.folder_vars.values())


def test_totale_aggiornato_con_e_senza_video(app):
    pagina = app.pages["select"]
    _cartelle, file = pagina.scan_sync()
    tutti = pagina.total_for(file)
    solo_foto = pagina.total_for([f for f in file if f.kind == "photo"])
    assert tutti[0] >= solo_foto[0]
    assert tutti[1] >= solo_foto[1]


def test_avanti_senza_scansione_blocca_e_spiega(app):
    pagina = app.pages["select"]
    pagina.go_next()
    assert app.current_page == "select"
    assert "scansion" in app.banner.message_text.lower() or "cerca" in app.banner.message_text.lower()


def test_avanti_con_selezione_va_alle_opzioni(app):
    pagina = app.pages["select"]
    pagina.scan_sync()
    pagina.go_next()
    assert app.current_page == "options"
    assert app.media_files
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_page_select.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/ui/page_select.py`
```python
"""Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from ..core.format import format_size, parse_date
from ..core.scanner import DEFAULT_ROOTS, MediaFolder, MediaFile, group_folders, list_media
from .theme import COLORI, font


class SelectPage(ttk.Frame):
    """Elenco delle cartelle con caselle di spunta, filtri e totale scelto."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.folder_vars: dict[str, tk.BooleanVar] = {}
        self._folders: list[MediaFolder] = []
        self._files: list[MediaFile] = []
        self._scan_finito = False
        self.sto_scegliendo_video = tk.BooleanVar(value=True)
        self.data_minima = tk.StringVar(value="")

        ttk.Label(self, text="Scegli cosa copiare", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self,
            text="Le cartelle qui sotto sono state trovate sul telefono. Togli la spunta a quelle che non ti servono.",
            style="Sottotitolo.TLabel",
            wraplength=820,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 8))

        contenitore = ttk.Frame(self)
        contenitore.grid(row=2, column=0, sticky="nsew")
        self.canvas = tk.Canvas(contenitore, highlightthickness=0, background=COLORI["pannello"])
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(contenitore, orient="vertical", command=self.canvas.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=barra.set)
        self.lista = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.lista, anchor="nw")
        contenitore.columnconfigure(0, weight=1)
        contenitore.rowconfigure(0, weight=1)

        opzioni = ttk.Frame(self)
        opzioni.grid(row=3, column=0, sticky="ew", pady=10)
        ttk.Checkbutton(
            opzioni,
            text="Includi anche i video",
            variable=self.sto_scegliendo_video,
            command=self.start_scan,
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(opzioni, text="Solo foto dal giorno (AAAA-MM-GG, vuoto = tutte):").grid(row=0, column=1, padx=(18, 6))
        ttk.Entry(opzioni, textvariable=self.data_minima, width=14).grid(row=0, column=2)
        ttk.Button(opzioni, text="Cerca di nuovo", style="Secondary.TButton", command=self.start_scan).grid(
            row=0, column=3, padx=12
        )

        self.riepilogo = ttk.Label(self, text="", font=font(14, bold=True))
        self.riepilogo.grid(row=4, column=0, sticky="w", pady=(4, 8))

        navigazione = ttk.Frame(self)
        navigazione.grid(row=5, column=0, sticky="ew")
        ttk.Button(navigazione, text="←  Indietro", style="Secondary.TButton", command=lambda: self.app.go_to("prev")).grid(
            row=0, column=0
        )
        self.bottone_avanti = ttk.Button(navigazione, text="Avanti  →", style="Big.TButton", command=self.go_next)
        self.bottone_avanti.grid(row=0, column=1, sticky="e", padx=(12, 0))
        navigazione.columnconfigure(1, weight=1)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self._mostra_messaggio_iniziale()

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        if not self._scan_finito and not self._files:
            self.start_scan()

    def _mostra_messaggio_iniziale(self) -> None:
        self.riepilogo.configure(text="Premi «Cerca di nuovo» per cercare le foto sul telefono.", foreground=COLORI["tenue"])

    # ── scansione ─────────────────────────────────────────────────────────
    def start_scan(self) -> None:
        self.app.set_status("Sto cercando le foto sul telefono… può richiedere un momento.", kind="info")
        self.bottone_avanti.state(["disabled"])
        self.app.run_async(self.scan_sync, on_done=self._scansione_finita)

    def scan_sync(self) -> tuple[list[MediaFolder], list[MediaFile]]:
        """Scansione bloccante (eseguita dal thread di lavoro o direttamente nei test)."""
        dispositivo = self.app.device
        seriale = dispositivo.serial if dispositivo is not None else ""
        self.app.cancel_event = threading.Event()
        file = list_media(
            self.app.backend,
            seriale,
            roots=DEFAULT_ROOTS,
            include_videos=self.sto_scegliendo_video.get(),
        )
        self._files = file
        self._folders = group_folders(file)
        return self._folders, file

    def _scansione_finita(self, risultato: tuple[list[MediaFolder], list[MediaFile]]) -> None:
        cartelle, file = risultato
        self._scan_finito = True
        self.rebuild_list(cartelle)
        if not file:
            self.app.set_status(
                "Non ho trovato foto da copiare.",
                hint="Controlla che il telefono sia sbloccato; su alcuni telefoni le foto sono in «Immagini».",
                kind="avviso",
            )
            return
        quanti, peso = self.selected_total()
        self.app.set_status(f"Trovate {len(file)} foto e video.", hint=f"Selezionati: {quanti} file ({format_size(peso)}).", kind="successo")

    def rebuild_list(self, folders: list[MediaFolder]) -> None:
        for figlio in self.lista.winfo_children():
            figlio.destroy()
        self.folder_vars.clear()
        for indice, cartella in enumerate(folders):
            variabile = tk.BooleanVar(value=True)
            self.folder_vars[cartella.remote_path] = variabile
            ttk.Checkbutton(
                self.lista,
                text=f"{cartella.label}  —  {cartella.file_count} file, {format_size(cartella.total_size)}",
                variable=variabile,
                command=self._aggiorna_totale,
            ).grid(row=indice, column=0, sticky="w", pady=2, padx=4)
        self.lista.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._aggiorna_totale()

    # ── selezione e totali ────────────────────────────────────────────────
    def selected_labels(self) -> list[str]:
        return [percorso for percorso, variabile in self.folder_vars.items() if variabile.get()]

    def selected_files(self) -> list[MediaFile]:
        scelte = set(self.selected_labels())
        data_minima = parse_date(self.data_minima.get())
        risultato = []
        for file in self._files:
            if file.parent not in scelte:
                continue
            if data_minima is not None and file.mtime < data_minima:
                continue
            risultato.append(file)
        return risultato

    def total_for(self, files: list[MediaFile]) -> tuple[int, int]:
        return len(files), sum(f.size for f in files)

    def selected_total(self) -> tuple[int, int]:
        return self.total_for(self.selected_files())

    def _aggiorna_totale(self) -> None:
        quanti, peso = self.selected_total()
        self.riepilogo.configure(
            text=f"Hai scelto {quanti} file — circa {format_size(peso)}.",
            foreground=COLORI["testo"] if quanti else COLORI["avviso"],
        )
        self.bottone_avanti.state(["!disabled"] if quanti else ["disabled"])

    def go_next(self) -> None:
        file = self.selected_files()
        if not file:
            self.app.set_status(
                "Non hai scelto nessuna foto da copiare.",
                hint="Metti la spunta ad almeno una cartella, oppure premi «Cerca di nuovo».",
                kind="avviso",
            )
            return
        self.app.media_files = file
        self.app.selected_folders = self.selected_labels()
        self.app.log(f"Selezionati {len(file)} file da copiare.")
        self.app.go_to("options")
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: passo 2 con elenco cartelle, filtri e totale scelto"
```

---

### Task 16: Passo 3 — destinazione e opzioni

**Files:**
- Create: `fotofacile/ui/page_options.py`, `tests/test_page_options.py`

**Interfaces:**
- Consumes: `App` (Task 13), `planner` (Task 7), `osutil` (Task 2b), `widgets` (Task 12)
- Produces: `SelectPage`-style API: `OptionsPage(parent)` con `on_show()`, `build_options() -> TransferOptions`, `go_next()`, `free_space() -> int`, `video_instructions() -> str`

- [ ] **Step 1: Test che falliscono**

`tests/test_page_options.py`
```python
import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.planner import TransferOptions
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app(tmp_path):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=8), demo_mode=True)
    applicazione.withdraw()
    applicazione.pages["connect"].stop_polling()
    applicazione.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    applicazione.pages["select"].scan_sync()
    applicazione.media_files = applicazione.pages["select"]._files
    yield applicazione, tmp_path
    applicazione.destroy()


def test_proposta_cartella_predefinita(app):
    applicazione, tmp_path = app
    pagina = applicazione.pages["options"]
    pagina.chooser.set(str(tmp_path))
    pagina.on_show()
    opzioni = pagina.build_options()
    assert isinstance(opzioni, TransferOptions)
    assert opzioni.destination == tmp_path
    assert opzioni.preserve_structure is True


def test_avanti_con_spazio_va_al_trasferimento(app):
    applicazione, tmp_path = app
    pagina = applicazione.pages["options"]
    pagina.chooser.set(str(tmp_path))
    pagina.go_next()
    assert applicazione.current_page == "transfer"
    assert applicazione.options is not None


def test_spazio_insufficiente_blocca_con_messaggio(app, monkeypatch):
    applicazione, tmp_path = app
    pagina = applicazione.pages["options"]
    pagina.chooser.set(str(tmp_path))
    monkeypatch.setattr("shutil.disk_usage", lambda _p: (0, 0, 10))
    pagina.go_next()
    assert applicazione.current_page == "options"
    assert "spazio" in applicazione.banner.message_text.lower()


def test_cancella_dopo_copia_richiede_conferma(app):
    applicazione, tmp_path = app
    pagina = applicazione.pages["options"]
    pagina.chooser.set(str(tmp_path))
    pagina.elimina_dopo_copia.set(True)
    pagina.go_next()
    assert applicazione.current_page == "options"
    assert "conferma" in applicazione.banner.message_text.lower() or "sicuro" in applicazione.banner.message_text.lower()
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_page_options.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/ui/page_options.py`
```python
"""Passo 3: dove salvare le foto e come comportarsi con duplicati e telefono."""

from __future__ import annotations

import shutil
import tkinter as tk
from tkinter import ttk

from ..core.format import format_size
from ..core.planner import TransferOptions, build_plan, ensure_space, suggested_destination
from .theme import COLORI, font
from .widgets import PathChooser


class OptionsPage(ttk.Frame):
    """Destinazione, struttura delle cartelle, duplicati e cancellazione dal telefono."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.mantieni_cartelle = tk.BooleanVar(value=True)
        self.salta_gia_copiate = tk.BooleanVar(value=True)
        self.elimina_dopo_copia = tk.BooleanVar(value=False)
        self._conferma_eliminazione = False

        ttk.Label(self, text="Dove vuoi salvare le foto?", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            self,
            text="Va bene la cartella proposta: potrai sempre spostare le foto dopo.",
            style="Sottotitolo.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.chooser = PathChooser(self, on_change=lambda _p: self._aggiorna_spazio())
        self.chooser.grid(row=2, column=0, sticky="ew")

        scelte = ttk.Frame(self)
        scelte.grid(row=3, column=0, sticky="w", pady=12)
        ttk.Checkbutton(
            scelte, text="Mantieni le cartelle come sul telefono (consigliato)", variable=self.mantieni_cartelle
        ).grid(row=0, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte, text="Salta le foto che ho già copiato", variable=self.salta_gia_copiate
        ).grid(row=1, column=0, sticky="w", pady=3)
        ttk.Checkbutton(
            scelte,
            text="Cancella le foto dal telefono dopo averle copiate",
            variable=self.elimina_dopo_copia,
            command=self._eliminazione_cambiata,
        ).grid(row=2, column=0, sticky="w", pady=3)
        self.avviso_eliminazione = ttk.Label(
            scelte,
            text="Attenzione: le foto verranno rimosse dal telefono. Controlla che la copia sia andata bene prima di chiudere il programma.",
            style="Errore.TLabel",
            wraplength=760,
            justify="left",
            font=font(11),
        )

        self.spazio = ttk.Label(self, text="", font=font(13, bold=True))
        self.spazio.grid(row=4, column=0, sticky="w", pady=(6, 0))

        navigazione = ttk.Frame(self)
        navigazione.grid(row=5, column=0, sticky="ew", pady=(16, 0))
        ttk.Button(navigazione, text="←  Indietro", style="Secondary.TButton", command=lambda: self.app.go_to("prev")).grid(
            row=0, column=0
        )
        self.bottone_avanti = ttk.Button(navigazione, text="Copia le foto  →", style="Big.TButton", command=self.go_next)
        self.bottone_avanti.grid(row=0, column=1, padx=(12, 0))
        navigazione.columnconfigure(1, weight=1)

        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=1)

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        if not self.chooser.get():
            modello = self.app.device.display_name if self.app.device is not None else "Telefono"
            self.chooser.set(str(suggested_destination(modello)))
        self.app.set_status(
            "Ultimo passo prima della copia: controlla la cartella e premi «Copia le foto».",
            kind="info",
        )
        self._aggiorna_spazio()

    def _eliminazione_cambiata(self) -> None:
        if self.elimina_dopo_copia.get():
            self.avviso_eliminazione.grid(row=3, column=0, sticky="w")
        else:
            self.avviso_eliminazione.grid_remove()
        self._conferma_eliminazione = False

    # ── opzioni e spazio ──────────────────────────────────────────────────
    def build_options(self) -> TransferOptions:
        return TransferOptions(
            destination=__import__("pathlib").Path(self.chooser.get()),
            preserve_structure=self.mantieni_cartelle.get(),
            skip_existing=self.salta_gia_copiate.get(),
            delete_after=self.elimina_dopo_copia.get(),
            include_videos=True,
        )

    def free_space(self) -> int:
        destinazione = __import__("pathlib").Path(self.chooser.get() or ".")
        while not destinazione.exists() and destinazione != destinazione.parent:
            destinazione = destinazione.parent
        return shutil.disk_usage(destinazione).free

    def _aggiorna_spazio(self) -> None:
        opzioni = self.build_options()
        piano = build_plan(self.app.media_files, opzioni, history=self.app.history())
        libero = self.free_space()
        colore = COLORI["successo"] if piano.total_bytes <= libero else COLORI["errore"]
        self.spazio.configure(
            text=f"Da copiare: {format_size(piano.total_bytes)} — Spazio libero: {format_size(libero)}",
            foreground=colore,
        )

    def go_next(self) -> None:
        opzioni = self.build_options()
        if not str(opzioni.destination).strip():
            self.app.set_status("Scegli una cartella dove salvare le foto.", kind="avviso")
            return
        piano = build_plan(self.app.media_files, opzioni, history=self.app.history())
        try:
            ensure_space(piano, opzioni.destination, self.free_space())
        except Exception as errore:
            messaggio = getattr(errore, "message", str(errore))
            suggerimento = getattr(errore, "hint", "")
            self.app.set_status(messaggio, hint=suggerimento, kind="errore")
            return
        if opzioni.delete_after and not self._conferma_eliminazione:
            self._conferma_eliminazione = True
            self.app.set_status(
                "Conferma la cancellazione dal telefono.",
                hint="Premi di nuovo «Copia le foto» per confermare, oppure togli la spunta alla cancellazione.",
                kind="avviso",
            )
            return
        self.app.options = opzioni
        self.app.log(f"Destinazione scelta: {opzioni.destination}")
        self.app.go_to("transfer")
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: passo 3 con destinazione, opzioni, controllo spazio e conferma cancellazione"
```

---

### Task 17: Passo 4 — copia, avanzamento e resoconto

**Files:**
- Create: `fotofacile/ui/page_transfer.py`, `tests/test_page_transfer.py`

**Interfaces:**
- Consumes: `App` (Task 13), `transfer` (Task 8), `report` (Task 9), `osutil.open_in_file_manager` (Task 2b)
- Produces: `TransferPage(parent)` con `on_show()`, `start_transfer() -> None`, `run_transfer_sync() -> TransferResults`, `update_progress(progress: Progress) -> None`, `show_summary(results) -> None`, `cancel() -> None`, `open_folder() -> None`, `save_report() -> None`

- [ ] **Step 1: Test che falliscono**

`tests/test_page_transfer.py`
```python
import pytest

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.devices import DeviceInfo
from fotofacile.core.planner import TransferOptions, build_plan
from fotofacile.ui.widgets import tk_available

pytestmark = pytest.mark.skipif(not tk_available(), reason="serve un ambiente grafico")


@pytest.fixture
def app(tmp_path):
    from fotofacile.ui.app import App

    applicazione = App(backend=DemoAdbBackend(file_count=6, delay=0.0), demo_mode=True)
    applicazione.withdraw()
    applicazione.pages["connect"].stop_polling()
    applicazione.device = DeviceInfo(serial="DEMO12345", state="device", model="Pixel_7_demo", product="demo")
    cartelle, file = applicazione.pages["select"].scan_sync()
    applicazione.media_files = file
    applicazione.options = TransferOptions(destination=tmp_path)
    yield applicazione, tmp_path
    applicazione.destroy()


def test_copia_completa_e_resoconto(app):
    applicazione, tmp_path = app
    pagina = applicazione.pages["transfer"]
    risultati = pagina.run_transfer_sync()
    assert risultati.cancelled is False
    assert len(risultati.copied) == len(applicazione.media_files)
    for percorso in risultati.copied:
        assert percorso.is_file()
        assert percorso.stat().st_size > 0
    assert applicazione.current_page == "transfer"


def test_seconda_copia_non_ricopia_nulla(app):
    applicazione, _tmp = app
    pagina = applicazione.pages["transfer"]
    pagina.run_transfer_sync()
    piano = build_plan(applicazione.media_files, applicazione.options, history=applicazione.history())
    assert piano.file_count == 0
    assert piano.skipped_duplicates == len(applicazione.media_files)


def test_resoconto_mostra_i_numeri(app):
    applicazione, _tmp = app
    pagina = applicazione.pages["transfer"]
    risultati = pagina.run_transfer_sync()
    pagina.show_summary(risultati)
    assert "Copiate" in pagina.riepilogo_testo() or "copiate" in pagina.riepilogo_testo().lower()
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_page_transfer.py -q`
Expected: FAIL `ModuleNotFoundError`

- [ ] **Step 3: Implementare**

`fotofacile/ui/page_transfer.py`
```python
"""Passo 4: copia con avanzamento, annullamento e resoconto finale."""

from __future__ import annotations

import threading
import time
import tkinter as tk
from tkinter import ttk

from ..core.format import format_eta, format_size, format_speed
from ..core.osutil import open_in_file_manager
from ..core.planner import build_plan
from ..core.report import build_report, save_report
from ..core.transfer import Progress, TransferResults, transfer
from .theme import COLORI, font


class TransferPage(ttk.Frame):
    """Barra di avanzamento, velocità, tempo rimanente e resoconto finale."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.app = parent
        self.results: TransferResults | None = None
        self.report_text = ""
        self.started_at = 0.0

        ttk.Label(self, text="Copia in corso", style="Titolo.TLabel").grid(row=0, column=0, sticky="w")
        self.stato = ttk.Label(self, text="Preparazione…", style="Sottotitolo.TLabel")
        self.stato.grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.barra_totale = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", length=760, maximum=100)
        self.barra_totale.grid(row=2, column=0, sticky="ew")
        self.etichetta_file = ttk.Label(self, text="", style="Tenue.TLabel", font=font(11))
        self.etichetta_file.grid(row=3, column=0, sticky="w", pady=(6, 0))
        self.barra_file = ttk.Progressbar(self, style="Barra.Horizontal.TProgressbar", length=760, maximum=100)
        self.barra_file.grid(row=4, column=0, sticky="ew", pady=(4, 8))

        self.dettagli = ttk.Label(self, text="", font=font(12))
        self.dettagli.grid(row=5, column=0, sticky="w")

        self.riepilogo_frame = ttk.Frame(self)
        self.riepilogo_frame.grid(row=6, column=0, sticky="ew", pady=14)
        self.riepilogo = ttk.Label(self.riepilogo_frame, text="", font=font(15, bold=True), wraplength=780, justify="left")
        self.riepilogo.grid(row=0, column=0, sticky="w")
        self.riepilogo_errori = ttk.Label(
            self.riepilogo_frame, text="", style="Avviso.TLabel", wraplength=780, justify="left", font=font(11)
        )
        self.riepilogo_errori.grid(row=1, column=0, sticky="w")

        pulsanti = ttk.Frame(self)
        pulsanti.grid(row=7, column=0, sticky="ew")
        self.bottone_annulla = ttk.Button(pulsanti, text="Interrompi", style="Secondary.TButton", command=self.cancel)
        self.bottone_annulla.grid(row=0, column=0)
        self.bottone_apri = ttk.Button(
            pulsanti, text="Apri la cartella delle foto", style="Secondary.TButton", command=self.open_folder
        )
        self.bottone_salva = ttk.Button(
            pulsanti, text="Salva resoconto", style="Secondary.TButton", command=self.save_report
        )
        self.bottone_chiudi = ttk.Button(pulsanti, text="Chiudi", style="Big.TButton", command=self.app.destroy)
        for indice, bottone in enumerate((self.bottone_apri, self.bottone_salva), start=1):
            bottone.grid(row=0, column=indice, padx=8)
        self.bottone_chiudi.grid(row=0, column=3, padx=(8, 0))
        pulsanti.columnconfigure(3, weight=1)

        for bottone in (self.bottone_apri, self.bottone_salva, self.bottone_chiudi):
            bottone.state(["disabled"])

        self.columnconfigure(0, weight=1)

    # ── ciclo di vita ─────────────────────────────────────────────────────
    def on_show(self) -> None:
        self.app.set_status("Sto copiando le foto: non scollegare il telefono.", kind="info")
        self.start_transfer()

    def start_transfer(self) -> None:
        self.app.cancel_event = threading.Event()
        self.bottone_annulla.state(["!disabled"])
        self.started_at = time.time()
        self.app.run_async(self.run_transfer_sync, on_done=self._trasferimento_finito)

    def run_transfer_sync(self) -> TransferResults:
        opzioni = self.app.options
        piano = build_plan(self.app.media_files, opzioni, history=self.app.history())
        self.app.log(
            f"Da copiare: {piano.file_count} file ({format_size(piano.total_bytes)}); "
            f"saltati: {piano.skipped_duplicates + piano.skipped_existing}."
        )
        risultato = transfer(
            self.app.backend,
            self.app.device.serial if self.app.device is not None else "",
            piano,
            opzioni,
            history=self.app.history(),
            on_progress=self._progresso_dal_thread,
            cancel=self.app.cancel_event,
        )
        self.results = risultato
        self.last_plan = piano
        return risultato

    def _progresso_dal_thread(self, progresso: Progress) -> None:
        self.app.events.put(("progresso", progresso, None))

    def _trasferimento_finito(self, risultati: TransferResults) -> None:
        self.show_summary(risultati)

    def update_progress(self, progresso: Progress) -> None:
        percentuale = 0.0
        if progresso.bytes_total:
            percentuale = progresso.bytes_done * 100 / progresso.bytes_total
        self.barra_totale.configure(value=percentuale)
        self.barra_file.configure(value=min(percentuale, 100))
        self.etichetta_file.configure(text=f"File in corso: {progresso.current_name or '—'}")
        self.dettagli.configure(
            text=(
                f"{progresso.done_files} di {progresso.total_files} file — "
                f"{format_size(progresso.bytes_done)} di {format_size(progresso.bytes_total)} — "
                f"{format_speed(progresso.speed_bps)} — resta {format_eta(progresso.eta_seconds)}"
            )
        )
        self.stato.configure(text="Sto copiando le foto… non scollegare il telefono.")

    # ── fine copia ────────────────────────────────────────────────────────
    def show_summary(self, risultati: TransferResults) -> None:
        self.barra_totale.configure(value=100 if not risultati.cancelled else self.barra_totale["value"])
        testo = (
            f"Fatto! Ho copiato {len(risultati.copied)} file ({format_size(risultati.bytes_copied)}) "
            f"in {int(risultati.elapsed)} secondi."
        )
        if risultati.skipped:
            testo += f" Ne ho saltati {risultati.skipped} perché erano già presenti."
        if risultati.cancelled:
            testo = f"Trasferimento interrotto: ho copiato {len(risultati.copied)} file. Quelli già copiati sono al sicuro."
        self.riepilogo.configure(text=testo)
        if risultati.failed:
            primi = ", ".join(media.name for media, _motivo in risultati.failed[:5])
            self.riepilogo_errori.configure(text=f"Non copiati ({len(risultati.failed)}): {primi}")
        self.stato.configure(text="Copia conclusa." if not risultati.cancelled else "Copia interrotta.")
        self.report_text = build_report(
            risultati,
            getattr(self, "last_plan", None),
            self.app.device,
            self.started_at,
            self.app.options.destination,
        )
        for bottone in (self.bottone_apri, self.bottone_salva, self.bottone_chiudi):
            bottone.state(["!disabled"])
        self.bottone_annulla.state(["disabled"])
        self.app.log(self.report_text)

    def riepilogo_testo(self) -> str:
        return self.riepilogo.cget("text")

    def cancel(self) -> None:
        self.app.cancel_event.set()
        self.stato.configure(text="Interruzione in corso…")
        self.bottone_annulla.state(["disabled"])

    def open_folder(self) -> None:
        destinazione = self.app.options.destination
        try:
            open_in_file_manager(destinazione)
        except Exception as errore:
            messaggio = getattr(errore, "message", str(errore))
            suggerimento = getattr(errore, "hint", f"Apri manualmente: {destinazione}")
            self.app.set_status(messaggio, hint=suggerimento, kind="avviso")

    def save_report(self) -> None:
        if not self.report_text:
            return
        percorso = save_report(self.report_text, self.app.options.destination)
        self.app.set_status("Resoconto salvato.", hint=f"Lo trovi qui: {percorso}", kind="successo")
```

- [ ] **Step 4: Verificare che passino**

Run: `.venv/bin/python -m pytest tests -q`
Expected: tutto verde.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat: passo 4 con avanzamento, annullamento e resoconto salvabile"
```

---

### Task 18: Controllo multi-piattaforma, documentazione e verifica finale

**Files:**
- Create: `tests/test_multipiattaforma.py`, `tests/test_end_to_end.py`, `README.md`
- Modify: `fotofacile/ui/app.py` (metodo `history()` che restituisce la cronologia caricata)

**Interfaces:**
- Consumes: tutto
- Produces: `App.history() -> History` (cronologia caricata una sola volta e salvata a fine copia); garanzia automatica che nessun modulo fuori da `osutil`/`adb`/`installer`/`theme` contenga riferimenti a un sistema operativo

- [ ] **Step 1: Test che falliscono**

`tests/test_multipiattaforma.py`
```python
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parent.parent / "fotofacile"
AMMESSI = {"core/osutil.py", "core/adb.py", "core/installer.py", "ui/theme.py", "cli.py"}
SPIE = ("sys.platform", "platform.system", "os.name", "win32", "darwin", "xdg-open")


def _moduli():
    for percorso in sorted(RADICE.rglob("*.py")):
        relativo = percorso.relative_to(RADICE).as_posix()
        yield relativo, percorso.read_text(encoding="utf-8")


def test_solo_i_moduli_dedicati_parlano_di_sistemi_operativi():
    colpevoli = []
    for relativo, testo in _moduli():
        if relativo in AMMESSI or relativo.endswith("__init__.py"):
            continue
        for spia in SPIE:
            if spia in testo:
                colpevoli.append(f"{relativo}: {spia}")
    assert colpevoli == []


def test_nessun_percorso_assoluto_di_un_solo_sistema():
    colpevoli = []
    for relativo, testo in _moduli():
        if "/Users/" in testo or "C:\\Users" in testo:
            colpevoli.append(relativo)
    assert colpevoli == []


def test_core_non_importa_tkinter():
    colpevoli = []
    for relativo, testo in _moduli():
        if relativo.startswith("core/") and "tkinter" in testo:
            colpevoli.append(relativo)
    assert colpevoli == []


def test_pytest_finisce_senza_avvisi():
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert True
```

`tests/test_end_to_end.py`
```python
import threading
from pathlib import Path

from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.devices import get_devices, pick_device
from fotofacile.core.history import History
from fotofacile.core.planner import TransferOptions, build_plan
from fotofacile.core.scanner import group_folders, list_media
from fotofacile.core.transfer import transfer


def test_percorso_completo_senza_interfaccia_grafica(tmp_path):
    """Collega → cerca → scegli → copia → ricontrolla: è il flusso dell'app senza GUI."""
    backend = DemoAdbBackend(file_count=20, delay=0.0)
    dispositivo = pick_device(get_devices(backend))
    assert dispositivo is not None and dispositivo.is_ready

    file = list_media(backend, dispositivo.serial)
    assert len(file) == 20
    assert group_folders(file)

    cronologia = History(tmp_path / "history.json")
    cronologia.load()
    opzioni = TransferOptions(destination=tmp_path / "Destinazione", delete_after=True)
    piano = build_plan(file, opzioni, serial=dispositivo.serial, history=cronologia)
    risultati = transfer(backend, dispositivo.serial, piano, opzioni, history=cronologia)

    assert risultati.cancelled is False
    assert len(risultati.copied) == piano.file_count
    for percorso in risultati.copied:
        assert percorso.is_file() and percorso.stat().st_size > 0
    assert risultati.deleted_from_phone == piano.file_count

    seconda = build_plan(
        [f for f in list_media(backend, dispositivo.serial)],
        opzioni,
        serial=dispositivo.serial,
        history=cronologia,
    )
    assert seconda.file_count == 0


def test_copia_interrotta_lascia_il_disco_pulito(tmp_path):
    backend = DemoAdbBackend(file_count=30, delay=0.01)
    file = list_media(backend, "DEMO12345")
    opzioni = TransferOptions(destination=tmp_path)
    piano = build_plan(file, opzioni)
    cancel = threading.Event()
    avvii = {"conteggio": 0}

    def interrompi(progresso):
        avvii["conteggio"] += 1
        if avvii["conteggio"] >= 3:
            cancel.set()

    risultati = transfer(backend, "DEMO12345", piano, opzioni, on_progress=interrompi, cancel=cancel, chunk_size=8192)
    assert risultati.cancelled is True
    assert not list(tmp_path.rglob("*.part"))
    for percorso in tmp_path.rglob("*"):
        if percorso.is_file():
            assert percorso.stat().st_size > 0
```

- [ ] **Step 2: Verificare che falliscano**

Run: `.venv/bin/python -m pytest tests/test_multipiattaforma.py tests/test_end_to_end.py -q`
Expected: FAIL (spie di piattaforma trovate nei moduli UI, `App.history()` non esiste ancora).

- [ ] **Step 3: Implementare**

In `fotofacile/ui/app.py` aggiungere il metodo e l'attributo della cronologia:
```python
    # nel costruttore, dopo self.events = queue.Queue():
    self._history = History()
    self._history.load()

    def history(self):
        """Cronologia caricata una volta sola: evita riletture in ogni pagina."""
        return self._history
```
con `from ..core.history import History` fra gli import.

Se il test `test_solo_i_moduli_dedicati_parlano_di_sistemi_operativi` segnala file UI:
togliere dal codice UI ogni controllo di piattaforma e delegarlo a `core/osutil.py` o `ui/theme.py`.

`README.md` (istruzioni per l'utente finale, in italiano):
```markdown
# FotoFacile

Copia le foto dal telefono Android al computer in pochi clic: niente gestore file, niente
cartelle strane da cercare, niente parole difficili.

## Cosa serve

- Un computer con **Windows 10/11**, **macOS** o **Linux** e **Python 3.9 o più recente**
  (su Windows va bene anche l'installazione da Microsoft Store).
- Il cavo USB del telefono.
- Circa 1 minuto la prima volta per autorizzare il telefono: lo fa il programma, guidandoti.

## Avvio

| Sistema | Comando |
|---|---|
| Windows | `py fotofacile.py` |
| macOS | `python3 fotofacile.py` |
| Linux | `python3 fotofacile.py` |

Il programma non ha bisogno di installare nulla: usa solo componenti già presenti nel computer
(la raccolta di programmi che Python porta con sé).

## La prima volta: autorizza il telefono

1. Collega il telefono con il cavo e **sblocca lo schermo**.
2. Nel programma premi **«Come si attiva il Debug USB?»** e segui i passaggi per la tua marca
   (Samsung, Xiaomi, Google, Huawei, Oppo…). È una procedura da fare **una volta sola**.
3. Quando il telefono chiede *«Consentire il debug USB?»*, tocca **Consenti**.
4. Il programma scrive **«Perfetto! Telefono collegato»**: premi **Avanti**.

Se qualcosa non funziona: prova un altro cavo USB (alcuni ricaricano soltanto), su Windows
installa il driver USB del produttore, oppure premi **«Riavvia collegamento»**.

## Uso quotidiano

1. **Scegli le foto**: spunta le cartelle che vuoi copiare (nella cartella proposta, sul
   computer, verranno mantenute le stesse sottocartelle del telefono).
2. **Destinazione**: va bene quella proposta (Immagini ▸ FotoFacile ▸ nome del telefono ▸ data).
3. **Copia**: vedi quante foto restano, a che velocità e quanto tempo manca. Puoi interrompere
   quando vuoi: le foto già copiate restano, i file mezzi copiati vengono eliminati.
4. Alla fine puoi **aprire la cartella** e **salvare un resoconto** di cosa è stato copiato.

Nota: le foto copiate una volta non vengono copiate di nuovo (l'app tiene un piccolo elenco in
`.fotofacile` dentro la tua cartella utente).

## Se qualcosa non va

| Messaggio | Cosa fare |
|---|---|
| «Non vedo ancora nessun telefono» | Controlla il cavo, sblocca il telefono, prova un'altra porta USB |
| «Sbloccalo e tocca Consenti» | Guarda lo schermo del telefono: c'è una richiesta da approvare |
| «Il telefono non risponde» | Scollega e ricollega il cavo, poi premi «Riavvia collegamento» |
| «Manca il componente di collegamento» | Premi «Installa componente»: il programma lo scarica da solo (serve internet) |
| «Non c'è abbastanza spazio» | Scegli un'altra cartella o libera spazio sul disco |

Diagnosi completa: `py fotofacile.py doctor` (Windows) oppure `python3 fotofacile.py doctor`.

## Prova senza telefono

`python3 fotofacile.py --demo` (su Windows `py fotofacile.py --demo`) simula un telefono con
54 foto di esempio: utile per vedere come funziona.

## Per chi sviluppa

- Test: `.venv/bin/python -m pytest tests -q`
- Codice: `fotofacile/core` (logica, testabile, nessuna dipendenza da Tkinter) e
  `fotofacile/ui` (interfaccia).
- Specifica: `docs/superpowers/specs/2026-09-28-fotofacile-design.md`
- Piano: `docs/superpowers/plans/2026-09-28-fotofacile.md`
```

- [ ] **Step 4: Verifica finale (tutta la suite + diagnosi + avvio demo)**

Run: `.venv/bin/python -m pytest tests -q && .venv/bin/python fotofacile.py doctor && .venv/bin/python -c "import fotofacile.cli as c; print('CLI ok')" && .venv/bin/python -c "
from fotofacile.core.adb import find_adb
print('adb trovato:', find_adb())
"`
Expected: suite verde, diagnosi stampata con tutte le voci, `CLI ok`, `adb trovato: None` (o percorso reale se installato).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "test: garanzia multi-piattaforma, flusso end-to-end e manuale utente"
```

---

## Note di esecuzione

- L'ordine dei task è quello di dipendenza: ogni task presuppone i precedenti già committati.
- Prima di ogni commit: `.venv/bin/python -m pytest tests -q` deve essere verde.
- Su una macchina senza ambiente grafico i test della UI vengono saltati automaticamente
  (`tk_available()`), mentre `tests/test_end_to_end.py` copre comunque l'intero flusso.
- Il collaudo con un telefono vero è manuale: collegare il dispositivo, attivare il Debug USB,
  eseguire `python3 fotofacile.py` e seguire i 4 passi. In assenza di telefono usare `--demo`.

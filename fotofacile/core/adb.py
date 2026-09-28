"""Comunicazione con il telefono tramite l'eseguibile adb (Android platform-tools).

Funziona su Windows (adb.exe), macOS e Linux: la ricerca dell'eseguibile e i percorsi
noti sono gli unici punti dipendenti dal sistema operativo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterator, Mapping, Protocol, Sequence, runtime_checkable

from .errors import AdbError

CHUNK_SIZE = 64 * 1024


@runtime_checkable
class AdbBackend(Protocol):
    """Tutto ciò che il programma sa fare con un telefono.

    Implementata da :class:`RealAdbBackend` (telefono vero) e da
    :class:`fotofacile.core.demo.DemoAdbBackend` (test e modalità demo).
    """

    def check(self) -> str:
        """Restituisce la versione del componente, o solleva AdbError."""

    def devices_raw(self) -> str:
        """Output di ``adb devices -l``."""

    def list_media_raw(self, serial: str, command: str) -> str:
        """Esegue sul telefono il comando di ricerca e restituisce l'output."""

    def stream_file(self, serial: str, remote_path: str, chunk_size: int = CHUNK_SIZE) -> Iterator[bytes]:
        """Legge un file dal telefono a blocchi."""

    def delete_file(self, serial: str, remote_path: str) -> None:
        """Cancella un file dal telefono."""

    def start_server(self) -> None:
        """Avvia il collegamento."""

    def restart_server(self) -> None:
        """Riavvia il collegamento (utile quando il telefono non risponde)."""


def shell_quote(value: str) -> str:
    """Quota un percorso per la shell del telefono (sempre POSIX: la shell gira su Android)."""
    return "'" + value.replace("'", "'\\''") + "'"


def find_adb(
    env: Mapping[str, str] | None = None,
    extra_dirs: Sequence[Path] = (),
    is_windows: bool | None = None,
) -> str | None:
    """Cerca adb (adb.exe su Windows): variabile d'ambiente, componente scaricato, percorsi noti, PATH."""
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
    noti.extend(Path(percorso) for percorso in extra_dirs)
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

    # ── comandi semplici ──────────────────────────────────────────────────
    def _run(
        self,
        args: Sequence[str],
        timeout: float | None = None,
        umano: str = "",
    ) -> subprocess.CompletedProcess:
        comando = [self.adb_path, *args]
        try:
            esito = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=timeout if timeout is not None else 30,
            )
        except FileNotFoundError as errore:
            raise AdbError(
                "Non riesco a usare il componente di collegamento.",
                hint="Apri il programma e premi «Installa componente mancante».",
            ) from errore
        except subprocess.TimeoutExpired as errore:
            raise AdbError(
                umano or "Il telefono non ha risposto in tempo.",
                hint="Controlla il cavo e riprova; se serve, premi «Riavvia collegamento».",
            ) from errore
        if esito.returncode != 0:
            raise AdbError(
                umano or "Il collegamento con il telefono si è interrotto.",
                hint="Sblocca il telefono, controlla il cavo e riprova.",
            )
        return esito

    def check(self) -> str:
        esito = self._run(["version"], umano="Il componente di collegamento non è utilizzabile.")
        prima_riga = esito.stdout.strip().splitlines()
        return prima_riga[0] if prima_riga else "adb"

    def devices_raw(self) -> str:
        return self._run(["devices", "-l"]).stdout

    def list_media_raw(self, serial: str, command: str) -> str:
        esito = self._run(
            ["-s", serial, "shell", command],
            timeout=self.scan_timeout,
            umano="La ricerca delle foto sul telefono non è andata a buon fine.",
        )
        return esito.stdout

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

    # ── lettura di un file ────────────────────────────────────────────────
    def stream_file(
        self,
        serial: str,
        remote_path: str,
        chunk_size: int = CHUNK_SIZE,
    ) -> Iterator[bytes]:
        """Legge un file dal telefono a blocchi (``exec-out`` è binario e sicuro)."""
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
            processo.wait()
            if processo.returncode != 0:
                raise AdbError(
                    "Non sono riuscito a leggere un file dal telefono.",
                    hint="Il telefono potrebbe essersi scollegato: ricontrolla il cavo e riprova.",
                )
        finally:
            if processo.poll() is None:
                processo.kill()
                processo.wait()
            for flusso in (processo.stdout, processo.stderr):
                if flusso is not None:
                    try:
                        flusso.close()
                    except OSError:  # pragma: no cover - chiusura difensiva
                        pass

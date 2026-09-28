"""Operazioni esterne eseguite **a piccoli passi**, senza usare thread.

Perché non i thread: su alcune combinazioni (per esempio macOS con Tk 9) creare un thread
mentre la finestra è aperta blocca il programma. Tenere il lavoro dentro il ciclo della
grafica, avanzando a passi, evita del tutto il problema e rende i test deterministici.

Il comando esterno parte subito; poi il programma lo tiene d'occhio con :meth:`ProcessoEsterno.passo`
chiamata dal ciclo della grafica. L'output lungo viene scritto direttamente su file, così
non si riempie mai il tubo di comunicazione del processo.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generator, Iterator, Sequence

from .errors import FotoFacileError

INTERVALLO_PRECEDENTE = 0.02  # secondi fra un controllo e il successivo
TIMEOUT_PREDEFINITO = 30.0


class Annullato(Exception):
    """Segnale interno: l'utente ha interrotto l'operazione in corso."""


@dataclass
class RisultatoComando:
    returncode: int
    output: str


def esegui_fino_alla_fine(generatore: Iterator[float]):
    """Porta a termine un generatore a passi ignorando le pause (usato da test e CLI)."""
    try:
        while True:
            next(generatore)
    except StopIteration as fine:
        return fine.value


class ProcessoEsterno:
    """Un comando esterno (per esempio adb) seguito senza bloccare la grafica."""

    def __init__(
        self,
        args: Sequence[str],
        timeout: float = TIMEOUT_PREDEFINITO,
        umano: str = "",
        hint: str = "",
        output_file: Path | None = None,
        orologio: Callable[[], float] = time.monotonic,
    ) -> None:
        self.args = [str(argomento) for argomento in args]
        self.timeout = timeout
        self.umano = umano
        self.hint = hint
        self.output_file = Path(output_file) if output_file is not None else None
        self.orologio = orologio
        self.process: subprocess.Popen | None = None
        self._inizio = 0.0
        self._file_errori: Path | None = None

    # ── avvio e avanzamento ───────────────────────────────────────────────
    def avvia(self) -> None:
        if self.process is not None:
            return
        verso_output = None
        descrittore, nome_errori = tempfile.mkstemp(prefix="fotofacile-errori-", suffix=".txt")
        os.close(descrittore)
        self._file_errori = Path(nome_errori)
        verso_errori = open(self._file_errori, "wb")
        if self.output_file is not None:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            verso_output = open(self.output_file, "wb")
        try:
            self.process = subprocess.Popen(
                self.args,
                stdout=verso_output if verso_output is not None else subprocess.PIPE,
                stderr=verso_errori,
                stdin=subprocess.DEVNULL,
            )
        except OSError as errore:
            if verso_output is not None:
                verso_output.close()
            verso_errori.close()
            self._pulisci_flussi()
            raise FotoFacileError(
                self.umano or "Non riesco ad avviare il comando sul computer.",
                hint=self.hint or "Riprova; se serve, apri la diagnosi con «doctor».",
            ) from errore
        finally:
            if verso_output is not None:
                verso_output.close()
            if not verso_errori.closed:
                verso_errori.close()
        self._inizio = self.orologio()

    def passo(self) -> bool:
        """True se il comando è ancora in corso."""
        if self.process is None:
            return False
        return self.process.poll() is None

    def scaduto(self) -> bool:
        return (self.orologio() - self._inizio) > self.timeout

    def termina(self) -> None:
        """Interrompe il comando (usato quando l'utente annulla o allo scadere del tempo)."""
        if self.process is None:
            self._pulisci_flussi()
            return
        if self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except (subprocess.TimeoutExpired, OSError):  # pragma: no cover - difensivo
                try:
                    self.process.kill()
                    self.process.wait(timeout=3)
                except (subprocess.TimeoutExpired, OSError):
                    pass
        self._pulisci_flussi()

    def aspetta(self) -> Generator[float, None, RisultatoComando]:
        """Generatore: cede il controllo alla grafica finché il comando non è finito."""
        if self.process is None:
            self.avvia()
        while self.passo():
            if self.scaduto():
                self.termina()
                raise FotoFacileError(
                    self.umano or "Il telefono non ha risposto in tempo.",
                    hint=self.hint or "Controlla il cavo e riprova; se serve, premi «Riavvia collegamento».",
                )
            yield INTERVALLO_PRECEDENTE
        return self.esito()

    def esito(self) -> RisultatoComando:
        """Output e codice di uscita; solleva un errore comprensibile se è andata male."""
        if self.process is None:
            raise FotoFacileError("Il comando non è mai partito.", hint="Riprova.")
        codice = self.process.returncode if self.process.returncode is not None else self.process.wait()
        output = self._leggi_output()
        errori = self._leggi_errori()
        self._pulisci_flussi()
        if codice != 0:
            raise FotoFacileError(
                self.umano or "Il comando non è riuscito.",
                hint=self.hint or self._primo_errore(errori or output),
            )
        return RisultatoComando(returncode=codice, output=output)

    # ── lettura dell'output ───────────────────────────────────────────────
    def _leggi_output(self) -> str:
        if self.output_file is not None:
            try:
                return self.output_file.read_text(errors="replace")
            except OSError:  # pragma: no cover - difensivo
                return ""
        if self.process is None or self.process.stdout is None:
            return ""
        dati = self.process.stdout.read()
        if isinstance(dati, bytes):
            return dati.decode(errors="replace")
        return dati or ""

    def _leggi_errori(self) -> str:
        if self._file_errori is None or not self._file_errori.exists():
            return ""
        try:
            return self._file_errori.read_text(errors="replace")
        except OSError:  # pragma: no cover - difensivo
            return ""

    def _primo_errore(self, output: str) -> str:
        righe = [riga.strip() for riga in (output or "").splitlines() if riga.strip()]
        if righe:
            return righe[-1]
        return "Riprova; se il problema resta, salva il registro e contattaci."

    def _pulisci_flussi(self) -> None:
        """Chiude i tubi e cancella il file degli errori: nessuna risorsa lasciata aperta."""
        if self.process is not None:
            for flusso in (self.process.stdout, self.process.stderr):
                if flusso is not None and not flusso.closed:
                    try:
                        flusso.close()
                    except OSError:  # pragma: no cover - difensivo
                        pass
        if self._file_errori is not None:
            self._file_errori.unlink(missing_ok=True)
            self._file_errori = None

    def __del__(self) -> None:  # pragma: no cover - pulizia difensiva
        try:
            self.termina()
        except Exception:
            pass


class ScaricatoreAPassi:
    """Scarica un file da internet a piccoli blocchi, senza bloccare la grafica."""

    def __init__(
        self,
        url: str,
        destinazione: Path,
        on_progress: Callable[[dict], None] | None = None,
        annulla=None,
        opener: Callable | None = None,
        blocco: int = 256 * 1024,
        timeout: float = 60.0,
    ) -> None:
        self.url = url
        self.destinazione = Path(destinazione)
        self.on_progress = on_progress
        self.annulla = annulla
        self.opener = opener
        self.blocco = blocco
        self.timeout = timeout

    def scarica(self) -> Generator[float, None, Path]:
        import urllib.request

        apri = self.opener or urllib.request.urlopen
        self.destinazione.parent.mkdir(parents=True, exist_ok=True)
        temporaneo = self.destinazione.with_name(self.destinazione.name + ".scarico")
        try:
            with apri(self.url, timeout=self.timeout) as risposta:
                intestazioni = getattr(risposta, "headers", None)
                totale = int((intestazioni or {}).get("Content-Length") or 0)
                ricevuti = 0
                with open(temporaneo, "wb") as uscita:
                    while True:
                        if self.annulla is not None and self.annulla.is_set():
                            raise FotoFacileError(
                                "Download interrotto.", hint="Puoi riprovare quando vuoi."
                            )
                        blocco = risposta.read(self.blocco)
                        if not blocco:
                            break
                        uscita.write(blocco)
                        ricevuti += len(blocco)
                        if self.on_progress is not None:
                            self.on_progress({"ricevuti": ricevuti, "totale": totale})
                        yield 0.0
            self.destinazione.unlink(missing_ok=True)
            temporaneo.replace(self.destinazione)
        except FotoFacileError:
            temporaneo.unlink(missing_ok=True)
            raise
        except OSError as errore:
            temporaneo.unlink(missing_ok=True)
            raise FotoFacileError(
                "Non sono riuscito a scaricare il componente di collegamento.",
                hint="Controlla la connessione a internet e riprova.",
            ) from errore
        return self.destinazione

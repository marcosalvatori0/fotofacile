"""Operazioni esterne eseguite **a piccoli passi**, senza usare thread.

Perché non i thread: su alcune combinazioni (per esempio macOS con Tk 9) creare un thread
mentre la finestra è aperta blocca il programma. Tenere il lavoro dentro il ciclo della
grafica, avanzando a passi, evita del tutto il problema e rende i test deterministici.

Il comando esterno parte subito; poi il programma lo tiene d'occhio con :meth:`ProcessoEsterno.passo`
chiamata dal ciclo della grafica. L'output **viene sempre scritto su file**, mai letto da un tubo
di comunicazione: così un comando molto loquace non riempie il tubo e non blocca il processo.
"""

from __future__ import annotations

import http.client
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Generator, Iterator, Sequence

from .errors import FotoFacileError
from .osutil import flag_nascosta

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
        leggi_output: bool = True,
        env: dict | None = None,
    ) -> None:
        self.args = [str(argomento) for argomento in args]
        self.timeout = timeout
        self.umano = umano
        self.hint = hint
        self.output_file = Path(output_file) if output_file is not None else None
        self.orologio = orologio
        #: Quando False l'output non viene mai riletto: serve alla copia, dove l'output del
        #: comando *è* il file appena scritto su disco e rileggerlo sprecherebbe memoria e tempo
        #: (un video da 4 GB diventerebbe una stringa da 4 GB in RAM).
        self.leggi_output = leggi_output
        #: Variabili d'ambiente per il figlio (None = eredita quelle del programma).
        self.env = env
        self.process: subprocess.Popen | None = None
        self._inizio = 0.0
        self._file_errori: Path | None = None
        #: File che riceve l'output del comando (mai un tubo: un comando loquace lo riempirebbe
        #: e resterebbe bloccato in scrittura finché qualcuno non lo svuota).
        self._file_output: Path | None = None
        self._output_temporaneo: Path | None = None

    # ── avvio e avanzamento ───────────────────────────────────────────────
    def avvia(self) -> None:
        if self.process is not None:
            return
        self._prepara_file_output()
        try:
            descrittore, nome_errori = tempfile.mkstemp(prefix="fotofacile-errori-", suffix=".txt")
            os.close(descrittore)
        except OSError as errore:
            # Il file di output temporaneo è già stato creato: non deve restare in giro.
            self._pulisci_flussi()
            raise FotoFacileError(
                "Non riesco a preparare il file di appoggio per il comando.",
                hint="Controlla di avere spazio e permessi di scrittura, poi riprova.",
            ) from errore
        self._file_errori = Path(nome_errori)
        verso_errori = None
        verso_output = None
        try:
            verso_errori = open(self._file_errori, "wb")
            verso_output = open(self._file_output, "wb")
            self.process = subprocess.Popen(
                self.args,
                stdout=verso_output,
                stderr=verso_errori,
                stdin=subprocess.DEVNULL,
                creationflags=flag_nascosta(),
                env=self.env,
            )
        except OSError as errore:
            raise FotoFacileError(
                self.umano or "Non riesco ad avviare il comando sul computer.",
                hint=self.hint or "Riprova; se serve, apri la diagnosi con «doctor».",
            ) from errore
        finally:
            # I due file vanno chiusi comunque: il figlio ne ha una copia propria. Se l'apertura
            # di uno dei due fallisce (cartella di destinazione non scrivibile, file bloccato),
            # senza questo `finally` resterebbe aperto e il file temporaneo resterebbe sul disco.
            for flusso in (verso_output, verso_errori):
                if flusso is not None and not flusso.closed:
                    flusso.close()
            if self.process is None:
                self._pulisci_flussi()
        self._inizio = self.orologio()

    def _prepara_file_output(self) -> None:
        """Sceglie dove finisce l'output: il file indicato, oppure uno temporaneo."""
        try:
            if self.output_file is not None:
                self.output_file.parent.mkdir(parents=True, exist_ok=True)
                self._file_output = self.output_file
                return
            descrittore, nome = tempfile.mkstemp(prefix="fotofacile-output-", suffix=".txt")
            os.close(descrittore)
        except OSError as errore:
            raise FotoFacileError(
                "Non riesco a preparare il file di appoggio per il comando.",
                hint="Controlla di avere spazio e permessi di scrittura, poi riprova.",
            ) from errore
        self._file_output = Path(nome)
        self._output_temporaneo = self._file_output

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

    def aspetta(self, leggi_output: bool | None = None) -> Generator[float, None, RisultatoComando]:
        """Generatore: cede il controllo alla grafica finché il comando non è finito.

        Se il generatore viene chiuso (l'utente cambia schermata o chiude la finestra) il
        comando esterno viene **interrotto**: senza questo resterebbe vivo in sottofondo.
        """
        if self.process is None:
            self.avvia()
        if leggi_output is not None:
            self.leggi_output = leggi_output
        try:
            while self.passo():
                if self.scaduto():
                    self.termina()
                    raise FotoFacileError(
                        self.umano or "Il telefono non ha risposto in tempo.",
                        hint=self.hint
                        or "Controlla il cavo e riprova; se serve, premi «Riprova il collegamento».",
                    )
                yield INTERVALLO_PRECEDENTE
            # Il risultato si legge **prima** della pulizia finale: dopo, il file degli
            # errori non esisterebbe più e la spiegazione andrebbe persa.
            esito = self.esito()
        finally:
            self.termina()
        return esito

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
                hint=self._suggerimento(errori or output),
            )
        return RisultatoComando(returncode=codice, output=output)

    # ── lettura dell'output ───────────────────────────────────────────────
    def _leggi_output(self) -> str:
        if not self.leggi_output or self._file_output is None:
            return ""
        try:
            # L'output dei comandi è UTF-8 (adb riporta i nomi dei file come li scrive
            # Android, l'aiutante di Windows scrive JSON UTF-8): con la codifica di sistema,
            # su Windows (cp1252) accenti ed emoji dei nomi diventavano illeggibili.
            return self._file_output.read_text(encoding="utf-8", errors="replace")
        except OSError:  # pragma: no cover - difensivo
            return ""

    def _leggi_errori(self) -> str:
        if self._file_errori is None or not self._file_errori.exists():
            return ""
        try:
            return self._file_errori.read_text(errors="replace")
        except OSError:  # pragma: no cover - difensivo
            return ""

    def _primo_errore(self, output: str) -> str:
        righe = [riga.strip() for riga in (output or "").splitlines() if riga.strip()]
        return righe[-1] if righe else ""

    def _suggerimento(self, output: str) -> str:
        """Unisce il consiglio previsto con quello che ha detto davvero il comando.

        Il testo prodotto dal comando esterno è spesso **la spiegazione più precisa** che
        esista (per esempio «il telefono è bloccato» invece di «controlla il cavo»): buttarlo
        via per far posto al consiglio generico era un peccato.
        """
        dettaglio = self._primo_errore(output)
        if not self.hint:
            return dettaglio or "Riprova; se il problema resta, salva il registro e contattaci."
        if not dettaglio or dettaglio in self.hint or dettaglio == self.umano:
            return self.hint
        return f"{self.hint} (dettaglio: {dettaglio})"

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
        if self._output_temporaneo is not None:
            self._output_temporaneo.unlink(missing_ok=True)
            self._output_temporaneo = None

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
        validatore: Callable[[Path], None] | None = None,
    ) -> None:
        self.url = url
        self.destinazione = Path(destinazione)
        self.on_progress = on_progress
        self.annulla = annulla
        self.opener = opener
        self.blocco = blocco
        self.timeout = timeout
        #: Controllo sul file scaricato **prima** che sostituisca quello buono.
        self.validatore = validatore

    def scarica(self) -> Generator[float, None, Path]:
        import urllib.request

        apri = self.opener or urllib.request.urlopen
        self.destinazione.parent.mkdir(parents=True, exist_ok=True)
        temporaneo = self.destinazione.with_name(self.destinazione.name + ".scarico")
        completato = False
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
            if self.validatore is not None:
                self.validatore(temporaneo)
            temporaneo.replace(self.destinazione)
            completato = True
        except FotoFacileError:
            raise
        except (OSError, http.client.HTTPException) as errore:
            # `HTTPException` non è un OSError: risposta troncata, risposta non HTTP (D22).
            raise FotoFacileError(
                "Non sono riuscito a scaricare il componente di collegamento.",
                hint="Controlla la connessione a internet e riprova.",
            ) from errore
        finally:
            # Vale anche se il download viene abbandonato (chiusura della finestra o cambio
            # idea): il file a metà non deve restare sul disco dell'utente.
            if not completato:
                temporaneo.unlink(missing_ok=True)
        return self.destinazione

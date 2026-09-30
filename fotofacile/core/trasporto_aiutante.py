"""Collegamento diretto al telefono, tramite un programma «aiutante».

Perché un aiutante separato: ogni sistema ha il **suo** modo di parlare con un telefono
collegato via cavo senza Debug USB — ``ImageCaptureCore`` su macOS, ``Shell.Application``
su Windows, ``gio`` su Linux. Nessuno dei tre è ottenibile dalla sola libreria standard di
Python. Invece di scrivere tre programmi diversi, se ne scrive uno per sistema e lo si
pilota sempre allo stesso modo: è un processo separato che risponde a righe JSON.

L'aiutante è **separato dal processo principale** per un motivo preciso: usa un ciclo di
eventi proprio (Cocoa, COM) e mescolarlo con la grafica di Tk della finestra è il modo
sicuro di bloccare tutto. Qui invece è un processo a parte, che si può anche interrompere.

Il dialogo è sempre lo stesso su tutti i sistemi::

    aiutante dispositivi                 → {"dispositivi": [ {...}, ... ]}
    aiutante elenca [--video]            → una riga JSON per file, poi {"fine": true}
    aiutante copia --percorso P          → i byte del file sull'uscita standard
    aiutante cancella --percorso P       → niente sull'uscita, 0 se riuscito

L'uscita standard è quindi sempre «leggibile a macchina»; i messaggi per l'utente vanno
sull'uscita degli errori, che diventa il suggerimento mostrato dall'app.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Callable, Generator, Sequence

from .adb_passi import _controlla_spazio, _dimensione_prevista, _esito_di_copia, percorso_temporaneo
from .devices import DeviceInfo
from .errors import FotoFacileError, traduci_errore_file
from .ops import Annullato, ProcessoEsterno
from .osutil import comando_se_stesso
from .scanner import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS, MediaFile

#: Ogni quanto si guarda se il file a metà è cresciuto.
INTERVALLO = 0.02
#: Quanto si aspetta al massimo che l'aiutante trovi un telefono.
TIMEOUT_DISPOSITIVI = 30.0
#: Quanto si aspetta al massimo per l'elenco completo delle foto.
TIMEOUT_ELENCO = 300.0
#: Quanto si aspetta al massimo per un singolo file (i video lunghi richiedono tempo).
TIMEOUT_COPIA = 1800.0


def comando_aiutante(nome: str) -> list[str]:
    """Come rilanciare **questo stesso programma** in modalità aiutante.

    Funziona sia dal sorgente sia dal programma impacchettato: nel pacchetto non esiste un
    interprete Python separato, quindi si richiama l'eseguibile stesso con un'opzione
    interna (``--aiutante``).
    """
    return comando_se_stesso("--aiutante", nome)


def ambiente_aiutante() -> dict:
    """Variabili d'ambiente per il processo figlio.

    Dal sorgente serve ``PYTHONPATH``: il figlio può essere avviato da una cartella diversa
    da quella del progetto (per esempio se l'utente ha lanciato il programma dal Desktop).
    """
    import os

    ambiente = dict(os.environ)
    if not getattr(sys, "frozen", False):
        from .osutil import cartella_progetto

        radice = str(cartella_progetto())
        esistente = ambiente.get("PYTHONPATH", "")
        if radice not in esistente.split(os.pathsep):
            ambiente["PYTHONPATH"] = f"{radice}{os.pathsep}{esistente}" if esistente else radice
    return ambiente


class TrasportoAiutante:
    """Collegamento diretto: parla con il telefono tramite un programma aiutante.

    Le sottoclassi dicono solo *quale* aiutante usare e *come* si chiama questo modo di
    collegamento; tutto il resto (avvio, attesa, lettura dell'esito, file a metà) è qui.
    """

    nome = "Collegamento diretto"
    spiegazione = "Uso il collegamento normale del telefono: non serve attivare nulla."
    aiutante = ""

    def __init__(self, env=None, intervallo: float = INTERVALLO) -> None:
        self.env = env
        self.intervallo = intervallo
        self._processi: list[ProcessoEsterno] = []

    # ── cose che cambiano da sistema a sistema ────────────────────────────
    def disponibile(self) -> bool:
        """True se su questo computer l'aiutante può funzionare."""
        raise NotImplementedError

    def base(self) -> list[str]:
        """Comando che avvia l'aiutante."""
        return comando_aiutante(self.aiutante)

    # ── aiuti interni ─────────────────────────────────────────────────────
    def _avvia(
        self,
        argomenti: Sequence[str],
        timeout: float,
        umano: str,
        hint: str,
        output_file: Path | None = None,
        leggi_output: bool = False,
    ) -> ProcessoEsterno:
        self._dimentica_finiti()
        processo = ProcessoEsterno(
            [*self.base(), *argomenti],
            timeout=timeout,
            umano=umano,
            hint=hint,
            output_file=output_file,
            leggi_output=leggi_output,
            env=self._ambiente(),
        )
        self._processi.append(processo)
        processo.avvia()
        return processo

    def _ambiente(self) -> dict:
        """Variabili d'ambiente per il processo aiutante."""
        try:
            return ambiente_aiutante()
        except Exception:  # pragma: no cover - difensivo: si usa l'ambiente ereditato
            import os

            return dict(os.environ)

    def _dimentica_finiti(self) -> None:
        """Toglie dall'elenco i processi già terminati.

        Senza questa pulizia l'elenco cresce di un elemento **per ogni file copiato**:
        una copia di 5000 foto terrebbe in memoria 5000 processi conclusi.
        """
        self._processi = [processo for processo in self._processi if processo.passo()]

    def _generatore(
        self,
        argomenti: Sequence[str],
        timeout: float,
        umano: str,
        hint: str,
        output_file: Path | None = None,
        leggi_output: bool = False,
        annulla=None,
    ) -> Generator[float, None, ProcessoEsterno]:
        """Manda avanti un comando dell'aiutante a piccoli passi, annullabile."""
        processo = self._avvia(
            argomenti,
            timeout,
            umano,
            hint,
            output_file=output_file,
            leggi_output=leggi_output,
        )
        try:
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    raise Annullato()
                if processo.scaduto():
                    processo.termina()
                    raise FotoFacileError(
                        umano,
                        hint=hint,
                    )
                yield self.intervallo
        except Annullato:
            processo.termina()
            raise
        except BaseException:
            # Vale anche per un abbandono (la finestra si chiude): il processo non deve
            # restare vivo, altrimenti su Windows il file temporaneo resta bloccato.
            processo.termina()
            raise
        return processo

    def pulisci(self) -> None:
        for processo in self._processi:
            try:
                processo.termina()
            except Exception:  # pulizia difensiva
                continue
        self._processi.clear()

    # ── operazioni ────────────────────────────────────────────────────────
    def dispositivi(self) -> Generator[float, None, list[DeviceInfo]]:
        import os
        import tempfile

        descrittore, nome = tempfile.mkstemp(prefix="fotofacile-dispositivi-", suffix=".json")
        os.close(descrittore)
        percorso = Path(nome)
        try:
            processo = yield from self._generatore(
                ["dispositivi"],
                TIMEOUT_DISPOSITIVI,
                "Non riesco a sentire il telefono.",
                "Controlla il cavo e riprova; se serve, premi «Riavvia collegamento».",
                output_file=percorso,
                leggi_output=True,
            )
            processo.esito()
            return leggi_dispositivi(percorso.read_text(errors="replace"))
        except FotoFacileError:
            raise
        finally:
            percorso.unlink(missing_ok=True)

    def cerca_media(
        self, serial: str, include_videos: bool = True, annulla=None
    ) -> Generator[float, None, list[MediaFile]]:
        import os
        import tempfile

        descrittore, nome = tempfile.mkstemp(prefix="fotofacile-elenco-", suffix=".jsonl")
        os.close(descrittore)
        percorso = Path(nome)
        argomenti = ["elenca", "--seriale", serial]
        if not include_videos:
            argomenti.append("--solo-foto")
        try:
            processo = yield from self._generatore(
                argomenti,
                TIMEOUT_ELENCO,
                "La ricerca delle foto sul telefono non è andata a buon fine.",
                "Sblocca il telefono e riprova: la ricerca si interrompe se lo schermo si blocca.",
                output_file=percorso,
                leggi_output=True,
                annulla=annulla,
            )
            processo.esito()
            return leggi_elenco(percorso.read_text(errors="replace"))
        finally:
            percorso.unlink(missing_ok=True)

    def copia(
        self,
        serial: str,
        remoto: str,
        destinazione: Path,
        on_scritti: Callable[[int], None] | None = None,
        annulla=None,
        remoto_dimensione: int | None = None,
    ) -> Generator[float, None, int]:
        destinazione = Path(destinazione)
        try:
            destinazione.parent.mkdir(parents=True, exist_ok=True)
        except OSError as errore:
            # Un OSError grezzo fermerebbe l'intera copia: `transfer` intercetta solo
            # FotoFacileError (e l'annullamento).
            raise traduci_errore_file(errore, destinazione) from errore
        _controlla_spazio(destinazione, _dimensione_prevista(remoto_dimensione))
        temporaneo = percorso_temporaneo(destinazione)
        scritti = 0
        completato = False
        processo: ProcessoEsterno | None = None
        try:
            processo = self._avvia(
                ["copia", "--seriale", serial, "--percorso", remoto],
                TIMEOUT_COPIA,
                f"Non sono riuscito a copiare {destinazione.name}.",
                "Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
                output_file=temporaneo,
            )
            while processo.passo():
                if annulla is not None and annulla.is_set():
                    raise Annullato()
                if processo.scaduto():
                    raise FotoFacileError(
                        f"La copia di {destinazione.name} è durata troppo tempo.",
                        hint="Riprova: se succede sempre con i video, prova un altro cavo USB.",
                    )
                scritti = _dimensione(temporaneo, scritti, on_scritti)
                yield self.intervallo
            scritti = _dimensione(temporaneo, scritti, on_scritti)
            _esito_di_copia(processo, destinazione)
            _rallenta_scrittura(temporaneo)
            os.replace(temporaneo, destinazione)
            completato = True
        except OSError as errore:
            # Come in `AdbAPassi.copia`: qualunque OSError (file, disco, file di appoggio del
            # comando) diventa una frase comprensibile invece di fermare l'intera copia.
            raise traduci_errore_file(errore, destinazione) from errore
        finally:
            if processo is not None:
                processo.termina()
            if not completato:
                try:
                    temporaneo.unlink(missing_ok=True)
                except OSError:  # pragma: no cover - difensivo
                    pass
        return scritti

    def cancella(self, serial: str, remoto: str) -> Generator[float, None, None]:
        processo = yield from self._generatore(
            ["cancella", "--seriale", serial, "--percorso", remoto],
            120.0,
            "Non sono riuscito a cancellare un file dal telefono.",
            "Il file resta sul telefono: puoi cancellarlo a mano in un secondo momento.",
        )
        try:
            processo.esito()
        finally:
            processo.termina()
        return None

    def riavvia(self) -> Generator[float, None, None]:
        """Non c'è niente da riavviare: il collegamento diretto non ha un servizio.

        Si solleva un errore gentile perché il pulsante «Riavvia collegamento» ha senso solo
        con il Debug USB.
        """
        raise FotoFacileError(
            "Con il collegamento diretto non c'è niente da riavviare.",
            hint="Scollega e ricollega il cavo del telefono, poi aspetta qualche secondo.",
        )
        yield 0.0  # pragma: no cover - rende la funzione un generatore


# ── lettura dell'uscita dell'aiutante ────────────────────────────────────


def leggi_dispositivi(testo: str) -> list[DeviceInfo]:
    """Trasforma l'uscita di «aiutante dispositivi» nell'elenco dei telefoni collegati."""
    testo = (testo or "").strip()
    if not testo:
        return []
    try:
        dati = json.loads(testo)
    except json.JSONDecodeError:
        return []
    voci = dati.get("dispositivi") if isinstance(dati, dict) else None
    if not isinstance(voci, list):
        return []
    risultato: list[DeviceInfo] = []
    for voce in voci:
        if not isinstance(voce, dict):
            continue
        seriale = str(voce.get("seriale") or "").strip()
        if not seriale:
            continue
        risultato.append(
            DeviceInfo(
                serial=seriale,
                state=str(voce.get("stato") or "device"),
                model=str(voce.get("nome") or ""),
                product=str(voce.get("prodotto") or ""),
            )
        )
    return risultato


def leggi_elenco(testo: str) -> list[MediaFile]:
    """Trasforma l'uscita di «aiutante elenca» nell'elenco dei file multimediali.

    Le righe non interpretabili vengono **ignorate**: un file con un nome strano non deve
    mai far fallire l'intera ricerca.
    """
    risultato: list[MediaFile] = []
    for riga in (testo or "").splitlines():
        riga = riga.strip()
        if not riga:
            continue
        try:
            voce = json.loads(riga)
        except json.JSONDecodeError:
            continue
        if not isinstance(voce, dict) or voce.get("fine"):
            continue
        percorso = str(voce.get("percorso") or "").strip()
        if not percorso:
            continue
        try:
            dimensione = int(voce.get("dimensione") or 0)
            data = int(voce.get("data") or 0)
        except (TypeError, ValueError):
            dimensione, data = 0, 0
        genere = str(voce.get("genere") or "").strip().lower()
        if genere not in ("photo", "video"):
            genere = genere_per_estensione(percorso)
        if genere is None:
            continue
        risultato.append(MediaFile(remote_path=percorso, size=dimensione, mtime=data, kind=genere))
    return risultato


def genere_per_estensione(percorso: str) -> str | None:
    """«photo», «video» o ``None`` in base all'estensione del file."""
    nome = percorso.rsplit("/", 1)[-1]
    if "." not in nome:
        return None
    estensione = nome.rsplit(".", 1)[-1].lower()
    if estensione in PHOTO_EXTENSIONS:
        return "photo"
    if estensione in VIDEO_EXTENSIONS:
        return "video"
    return None


def _dimensione(temporaneo: Path, precedente: int, on_scritti: Callable[[int], None] | None) -> int:
    try:
        attuale = temporaneo.stat().st_size
    except OSError:
        return precedente
    if attuale != precedente and on_scritti is not None:
        on_scritti(attuale)
    return attuale


def _rallenta_scrittura(temporaneo: Path) -> None:
    """Assicura che i byte siano davvero sul disco prima di rinominare il file."""
    import os

    try:
        descrittore = os.open(temporaneo, os.O_RDWR)
    except OSError:  # pragma: no cover - difensivo
        return
    try:
        os.fsync(descrittore)
    except OSError:  # pragma: no cover - alcuni file system non lo permettono
        pass
    finally:
        os.close(descrittore)

"""Costruzione del piano di copia: cosa copiare, dove, e cosa saltare.

I nomi dei file vengono resi sicuri per **tutti** i sistemi operativi (Windows compreso),
così la cartella di destinazione resta utilizzabile anche se poi viene copiata su un altro
computer. Le collisioni considerano la sensibilità alle maiuscole del file system.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Sequence

from .errors import TransferError
from .history import History
from .osutil import default_photos_dir, is_case_insensitive_fs
from .scanner import MediaFile

PREFISSI_REMOTI = (
    "/storage/emulated/0/",
    "/storage/self/primary/",
    "/sdcard/",
)
CARATTERI_NON_VALIDI = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
NOMI_RISERVATI = frozenset(
    {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
)
MAX_NOME = 150
MAX_CARTELLA = 40
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
            return remote_path[len(prefisso) :]
    return remote_path.lstrip("/")


def destination_for(
    remote_path: str,
    destination: Path,
    preserve_structure: bool,
    case_insensitive: bool | None = None,
) -> Path:
    """Percorso di destinazione del file, con nomi validi su ogni sistema operativo."""
    relativo = relative_path(remote_path)
    nome = _nome_sicuro(relativo.rsplit("/", 1)[-1])
    if not preserve_structure:
        return _limita_percorso(Path(destination) / nome)
    cartelle = [_nome_sicuro(parte) for parte in relativo.split("/")[:-1] if parte]
    return _limita_percorso(Path(destination).joinpath(*cartelle, nome))


def _nome_sicuro(nome: str) -> str:
    """Rende un nome di file accettabile su Windows, macOS e Linux."""
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
    """Riduce il percorso entro il limite sicuro multipiattaforma.

    Ordine degli interventi: prima i nomi delle cartelle, poi l'eliminazione dei livelli
    più esterni, infine l'accorciamento del nome del file (estensione sempre preservata).
    """
    percorso = _accorcia_cartelle(percorso, MAX_CARTELLA)
    while len(str(percorso)) > MAX_PERCORSO:
        testa = percorso.anchor
        parti = list(percorso.parts[1:] if percorso.is_absolute() else percorso.parts)
        if len(parti) <= 2:
            break
        parti.pop(0)
        percorso = Path(testa).joinpath(*parti) if testa else Path(*parti)
    eccedenza = len(str(percorso)) - MAX_PERCORSO
    if eccedenza <= 0:
        return percorso
    radice = percorso.stem
    nuovo = radice[: max(1, len(radice) - eccedenza)].rstrip(" .") or "file"
    return percorso.with_name(f"{nuovo}{percorso.suffix}")


def _accorcia_cartelle(percorso: Path, limite: int) -> Path:
    parti = percorso.parts
    if len(parti) <= 2:
        return percorso
    testa, *cartelle, nome = parti
    accorciate = [parte[:limite].rstrip(" .") or "_" for parte in cartelle]
    return Path(testa).joinpath(*accorciate, nome)


def build_plan(
    files: Sequence[MediaFile],
    options: TransferOptions,
    serial: str = "",
    history: History | None = None,
    case_insensitive: bool | None = None,
) -> TransferPlan:
    """Applica filtri, deduplica e collisioni producendo l'elenco dei file da copiare."""
    sensibile = is_case_insensitive_fs() if case_insensitive is None else case_insensitive
    esistenza = _Esistenza(sensibile)
    piano = TransferPlan()
    for file in files:
        if not options.include_videos and file.kind == "video":
            continue
        if options.date_from is not None and file.mtime < options.date_from:
            continue
        relativo = relative_path(file.remote_path)
        if (
            options.skip_existing
            and history is not None
            and history.contains(serial, relativo, file.size, file.mtime)
        ):
            piano.skipped_duplicates += 1
            continue
        destinazione = destination_for(
            file.remote_path,
            options.destination,
            options.preserve_structure,
            case_insensitive=sensibile,
        )
        esistente = esistenza.trova(destinazione)
        if esistente is not None:
            # «già presente» vale solo se il nome è identico: se differisce solo per le
            # maiuscole (FOTO.JPG contro foto.jpg) si tratta di un file diverso, e su un
            # disco non sensibile alle maiuscole sovrascriverlo perderebbe una foto.
            uguale = esistente.name == destinazione.name
            if uguale and file.size and _dimensione(esistente) == file.size:
                piano.skipped_existing += 1
                continue
            destinazione = esistenza.nome_libero(destinazione)
        esistenza.registra(destinazione)
        piano.files.append(PlannedFile(media=file, rel_path=relativo, dest_path=destinazione))
        piano.total_bytes += file.size
    return piano


def _dimensione(percorso: Path) -> int:
    """Dimensione di un file esistente; -1 se nel frattempo è sparito."""
    try:
        return percorso.stat().st_size
    except OSError:
        return -1


class _Esistenza:
    """Verifica rapidamente se un nome è già occupato, con o senza distinzione di maiuscole.

    Confronta i nomi direttamente (non delega al file system), così il comportamento è
    identico su Windows, macOS e Linux; tiene una copia dell'elenco di ogni cartella per
    non interrogare il disco una volta per file.
    """

    def __init__(self, case_insensitive: bool) -> None:
        self.case_insensitive = case_insensitive
        self._cache: dict[Path, dict[str, Path]] = {}

    def _chiave(self, nome: str) -> str:
        # Confronto esplicito con casefold: normcase su macOS non cambierebbe nulla.
        return nome.casefold() if self.case_insensitive else nome

    def _indice(self, cartella: Path) -> dict[str, Path]:
        voci = self._cache.get(cartella)
        if voci is None:
            voci = {}
            if cartella.is_dir():
                for voce in cartella.iterdir():
                    voci.setdefault(self._chiave(voce.name), voce)
            self._cache[cartella] = voci
        return voci

    def trova(self, percorso: Path) -> Path | None:
        return self._indice(percorso.parent).get(self._chiave(percorso.name))

    def registra(self, percorso: Path) -> None:
        self._indice(percorso.parent).setdefault(self._chiave(percorso.name), percorso)

    def nome_libero(self, percorso: Path) -> Path:
        contatore = 1
        while True:
            candidato = percorso.with_name(f"{percorso.stem} ({contatore}){percorso.suffix}")
            candidato = _limita_percorso(candidato)
            if self.trova(candidato) is None:
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
            "Libera spazio oppure scegli un'altra cartella."
        ),
    )


def suggested_destination(model: str, base: Path | None = None, today: str = "") -> Path:
    """Proposta di cartella: Immagini/FotoFacile/<modello>/<data>."""
    radice = Path(base) if base is not None else default_photos_dir()
    giornata = today or date.today().isoformat()
    nome = _nome_sicuro(model or "Telefono")
    return radice / nome / giornata

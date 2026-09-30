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
#: Spazio minimo che deve restare per il nome del file, comunque vada.
MIN_NOME = 12
#: Quante volte si prova ad aggiungere « (1)», « (2)»… a un nome già occupato.
MAX_TENTATIVI_NOME = 1000


@dataclass(frozen=True)
class TransferOptions:
    destination: Path
    #: Falso per impostazione predefinita: chi usa il programma vuole le **foto e i video**,
    #: non la copia dell'albero di cartelle del telefono. La struttura si può riattivare.
    preserve_structure: bool = False
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
    """Percorso di destinazione del file, con nomi validi su ogni sistema operativo.

    La cartella scelta dall'utente non viene **mai** riscritta: se il percorso è troppo lungo
    si accorciano solo le cartelle provenienti dal telefono e, se serve, il nome del file.
    """
    radice = Path(destination)
    relativo = relative_path(remote_path)
    nome = _nome_sicuro(relativo.rsplit("/", 1)[-1])
    if not preserve_structure:
        return _limita_percorso(radice / nome, radice)
    cartelle = [_nome_sicuro(parte) for parte in relativo.split("/")[:-1] if parte]
    return _limita_percorso(radice.joinpath(*cartelle, nome), radice)


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


def _limita_percorso(percorso: Path, radice: Path) -> Path:
    """Riduce il percorso entro il limite sicuro multipiattaforma **senza toccare la radice**.

    Ordine degli interventi: prima i nomi delle cartelle, poi l'eliminazione dei livelli
    esterni (quelli che vengono dal telefono, mai la cartella scelta dall'utente), infine
    l'accorciamento del nome del file con l'estensione sempre preservata.
    """
    radice = Path(radice)
    try:
        relativo = percorso.relative_to(radice)
    except ValueError:
        # Fuori dalla radice non sappiamo cosa si può accorciare: meglio non toccare niente.
        return percorso

    parti = [parte for parte in relativo.parts if parte not in ("", ".")]
    if not parti:
        return percorso
    cartelle = [_accorcia_cartella(parte) for parte in parti[:-1]]
    nome = parti[-1]

    # Spazio disponibile per il tratto che possiamo accorciare.
    margine = MAX_PERCORSO - len(str(radice)) - 1
    # Se la sola radice occupa quasi tutto il limite, il file va comunque salvato: si accetta
    # di superare MAX_PERCORSO invece di rifiutare la copia.
    margine = max(margine, MIN_NOME + len(Path(nome).suffix))

    while cartelle and len(str(Path(*cartelle, nome))) > margine:
        cartelle.pop(0)  # i livelli più esterni sono quelli che dicono meno

    if len(str(Path(*cartelle, nome))) > margine:
        # Un carattere in meno: al nome va tolto anche il separatore che lo unisce alle
        # cartelle, altrimenti il percorso finale supera il limite di uno.
        spazio_nome = margine - (len(str(Path(*cartelle))) + 1 if cartelle else 0)
        nome = _accorcia_nome(nome, spazio_nome)
    return radice.joinpath(*cartelle, nome)


def _accorcia_cartella(nome: str) -> str:
    return nome[:MAX_CARTELLA].rstrip(" .") or "_"


def _accorcia_nome(nome: str, limite: int) -> str:
    """Accorcia il nome del file preservando estensione e l'eventuale « (1)» finale."""
    limite = max(int(limite), MIN_NOME)
    if len(nome) <= limite:
        return nome
    percorso = Path(nome)
    suffisso = percorso.suffix
    radice, coda = _radice_e_coda(percorso.stem)
    spazio = limite - len(suffisso) - len(coda)
    if spazio < 1:
        # Non c'è spazio nemmeno per il contatore: si accetta di superare il limite.
        return nome
    return f"{radice[:spazio].rstrip(' .') or 'file'}{coda}{suffisso}"


def _radice_e_coda(gambo: str) -> tuple[str, str]:
    """Separa «foto (3)» in («foto», « (3)»), così il contatore non viene mai tagliato."""
    if gambo.endswith(")"):
        base, parentesi, numero = gambo[:-1].rpartition(" (")
        if base and numero.isdigit() and parentesi:
            return base, f" ({numero})"
    return gambo, ""


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
            destinazione = esistenza.nome_libero(destinazione, options.destination)
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

    def nome_libero(self, percorso: Path, radice: Path) -> Path:
        """Trova un nome non ancora occupato aggiungendo « (1)», « (2)»…

        Il ciclo è **limitato**: se per qualche motivo non si trovasse un nome libero
        (per esempio un accorciamento che cancella il contatore) si solleva un errore
        comprensibile invece di bloccare la finestra per sempre.
        """
        for contatore in range(1, MAX_TENTATIVI_NOME):
            candidato = _limita_percorso(
                percorso.with_name(f"{percorso.stem} ({contatore}){percorso.suffix}"), radice
            )
            if self.trova(candidato) is None:
                return candidato
        raise TransferError(
            f"Troppi file con lo stesso nome in {percorso.parent}.",
            hint="Scegli un'altra cartella di destinazione e riprova.",
        )


def ensure_space(plan: TransferPlan, destination: Path, free_bytes: int | None) -> None:
    """Solleva un errore comprensibile se lo spazio libero non basta.

    ``free_bytes`` a ``None`` significa «non lo so» (per esempio su un disco di rete): in quel
    caso non si blocca nulla, perché un allarme sbagliato è peggio di nessun allarme.
    """
    if free_bytes is None or plan.total_bytes <= free_bytes:
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

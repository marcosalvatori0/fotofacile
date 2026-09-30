"""Elenco dei file multimediali presenti sul telefono.

La ricerca avviene con **un solo comando** eseguito sul dispositivo: si evita così
una connessione per ogni file (che renderebbe la scansione lentissima).
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Sequence

from .adb import AdbBackend, shell_quote

PHOTO_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "heic",
    "heif",
    "bmp",
    "tif",
    "tiff",
    "dng",
    "avif",
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

PREFISSI_MEMORIA = (
    "/storage/emulated/0/",
    "/storage/self/primary/",
    "/sdcard/",
)


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
    """Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo.

    Le righe non interpretabili vengono ignorate (mai far fallire una scansione
    per colpa di un nome strano). Il nome può contenere «|».
    """
    risultato: list[MediaFile] = []
    # Solo «\n», come `read -r` sul telefono: `splitlines()` taglierebbe anche su caratteri
    # che possono stare in un nome (U+2028, U+0085…) e inventerebbe un file (D26).
    for riga in output.split("\n"):
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
    """Costruisce l'unico comando che elenca i file sul telefono."""
    estensioni = PHOTO_EXTENSIONS + (VIDEO_EXTENSIONS if include_videos else ())
    filtri = " -o ".join(f"-iname '*.{estensione}'" for estensione in estensioni)
    profondita = f" -maxdepth {max_depth}" if max_depth is not None else ""
    cartelle = " ".join(shell_quote(root) for root in roots)
    return (
        f"for d in {cartelle}; do "
        f'[ -d "$d" ] && find "$d"{profondita} -type f \\( {filtri} \\) 2>/dev/null; done | '
        'while IFS= read -r f; do stat -c \'%s|%Y|%n\' "$f" 2>/dev/null; done'
    )


def list_media(
    adb: AdbBackend,
    serial: str,
    roots: Sequence[str] = DEFAULT_ROOTS,
    include_videos: bool = True,
    cancel: threading.Event | None = None,
) -> list[MediaFile]:
    """Cerca i file multimediali; se non ne trova, esplora tutta la memoria del telefono."""
    if cancel is not None and cancel.is_set():
        return []
    comando = build_scan_command(roots, include_videos=include_videos)
    trovati = parse_stat_stream(adb.list_media_raw(serial, comando))
    if cancel is not None and cancel.is_set():
        return []
    if not trovati:
        comando_ampio = build_scan_command(
            [FALLBACK_ROOT],
            include_videos=include_videos,
            max_depth=FALLBACK_MAX_DEPTH,
        )
        trovati = parse_stat_stream(adb.list_media_raw(serial, comando_ampio))
    return trovati


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
            total_size=sum(file.size for file in elenco),
        )
        for percorso, elenco in aggregato.items()
    ]
    cartelle.sort(key=lambda cartella: (-cartella.total_size, cartella.label))
    return cartelle


def _label(percorso: str) -> str:
    pulito = percorso
    for prefisso in PREFISSI_MEMORIA:
        if pulito.startswith(prefisso):
            pulito = pulito[len(prefisso) :]
            break
    pulito = pulito.strip("/")
    return pulito or "Memoria del telefono"

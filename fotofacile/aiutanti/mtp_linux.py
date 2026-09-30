"""Aiutante Linux: parla con il telefono tramite MTP usando ``gio``/gvfs.

Sul desktop Linux l'MTP lo sa già leggere il sistema: è lo stesso meccanismo che usa il
gestore file («File»/Nautilus), che si appoggia a ``gio`` e ai montaggi gvfs. Qui non si
reinventa niente: si monta il telefono con ``gio mount`` e poi si legge la cartella FUSE
che gvfs espone in ``$XDG_RUNTIME_DIR/gvfs``. Il montaggio resta vivo anche quando questo
processo esce (è del desktop, non nostro), quindi non si rimonta per ogni foto.

Se ``gio``/gvfs non c'è, si ripiega su ``jmtpfs``, montato in una cartella temporanea.

Uso (dall'esterno non si chiama mai a mano, lo fa :mod:`fotofacile.core.trasporto_aiutante`)::

    python -m fotofacile.aiutanti.mtp_linux dispositivi
    python -m fotofacile.aiutanti.mtp_linux elenca [--seriale S] [--solo-foto]
    python -m fotofacile.aiutanti.mtp_linux copia --seriale S --percorso P
    python -m fotofacile.aiutanti.mtp_linux cancella --seriale S --percorso P
    python -m fotofacile.aiutanti.mtp_linux smonta [--seriale S]   (comando in più,
                                                interno: serve al trasporto per pulire)

L'uscita standard è sempre leggibile a macchina; i messaggi per l'utente vanno sull'uscita
degli errori.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Callable, Iterator, Sequence

#: Le stesse estensioni del collegamento macOS: il contratto è identico su ogni sistema.
from .ptp_mac import ESTENSIONI_FOTO, ESTENSIONI_VIDEO

USCITA_OK = 0
USCITA_ERRORE = 2
USCITA_NESSUN_TELEFONO = 3

#: Quanto si aspetta che il desktop monti il telefono.
TIMEOUT_GIO = 60.0
#: Quanto si aspetta il ripiego jmtpfs.
TIMEOUT_JMTPFS = 60.0
#: Quanto si aspetta per smontare (alla chiusura non si può restare appesi).
TIMEOUT_SMONTA = 30.0
#: Dimensione di un blocco di lettura: compromesso fra velocità e memoria occupata.
BLOCCO = 512 * 1024

#: Riga che apre un blocco di «gio mount -li» («Volume(0): ...» oppure «Mount(0): ...»).
RE_BLOCCO = re.compile(r"^\s*(?:Volume|Mount|Drive)\(\d+\):\s*(.*)$")
#: Un indirizzo MTP dentro l'elenco dei montaggi (activation_root, default_location, ...).
RE_URI_MTP = re.compile(r"mtp://([^/\s\"']+)/?")


class GuaioMtp(Exception):
    """Un guaio raccontabile all'utente, con un suggerimento su come procedere.

    ``ripiego_utile`` dice se vale la pena provare ``jmtpfs``: per un telefono bloccato o
    sparito no, per un problema di gvfs sì.
    """

    #: Codice di uscita del contratto: 2 in generale, 3 per «nessun telefono».
    uscita = USCITA_ERRORE

    def __init__(self, messaggio: str, suggerimento: str = "", ripiego_utile: bool = True) -> None:
        super().__init__(messaggio)
        self.messaggio = messaggio
        self.suggerimento = suggerimento
        self.ripiego_utile = ripiego_utile


class NessunTelefono(GuaioMtp):
    """Nessun telefono collegato, o quello indicato non c'è più."""

    uscita = USCITA_NESSUN_TELEFONO


class ComponenteMancante(GuaioMtp):
    """Su questo computer manca del tutto il supporto MTP del desktop."""


# ── comandi esterni ──────────────────────────────────────────────────────


def _eseguibile(nome: str) -> str | None:
    """Percorso di un programma di sistema, se c'è (separato per poterlo simulare nei test)."""
    return shutil.which(nome)


def _esegui(comando: Sequence[str], timeout: float) -> subprocess.CompletedProcess | None:
    """Esegue un comando del desktop e ne raccoglie l'uscita, senza mai sollevare.

    Restituisce ``None`` se il comando non parte o non finisce in tempo: chi chiama sa
    spiegare il guaio meglio di un'eccezione grezza.
    """
    try:
        return subprocess.run(
            list(comando),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


# ── dove gvfs monta i telefoni ───────────────────────────────────────────


def cartella_gvfs(env=None) -> Path:
    """La cartella dove gvfs crea i montaggi (``$XDG_RUNTIME_DIR/gvfs``)."""
    ambiente = dict(env if env is not None else os.environ)
    base = ambiente.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    return Path(base) / "gvfs"


def _chiave_seriale(seriale: str) -> str:
    """Forma canonica di un seriale gvfs, per confronti e per non contare doppioni.

    ``gio mount -li`` può stampare l'indirizzo così com'è (``mtp://[usb:001,004]/``),
    mentre gvfs chiama la cartella di montaggio con la forma codificata
    (``mtp:host=%5Busb%3A001%2C004%5D``): sono lo stesso telefono e vanno trattati come
    tale. La forma canonica è quella decodificata.
    """
    return urllib.parse.unquote(seriale)


def montaggio_da_seriale(seriale: str, env=None) -> Path | None:
    """La cartella dove gvfs ha montato il telefono indicato, se è montato.

    Il nome della cartella è ``mtp:host=<seriale>``, con il seriale codificato: il
    confronto passa dalla forma canonica, così funziona sia che il seriale arrivi
    codificato sia che arrivi leggibile.
    """
    if not seriale:
        return None
    cartella = cartella_gvfs(env)
    if not cartella.is_dir():
        return None
    chiave = _chiave_seriale(seriale)
    for voce in sorted(cartella.iterdir()):
        if voce.name.startswith("mtp:host=") and _chiave_seriale(voce.name[len("mtp:host=") :]) == chiave:
            if voce.is_dir():
                return voce
    return None


def _nome_leggibile(seriale: str) -> str:
    """Il seriale gvfs è una stringa codificata: per mostrarlo si decodifica."""
    return urllib.parse.unquote(seriale)


def _aggiungi_uri(trovati: list, visti: set, uri: str, nome: str) -> None:
    corrispondenza = RE_URI_MTP.match(uri.strip())
    if corrispondenza is None:
        return
    seriale = corrispondenza.group(1)
    chiave = _chiave_seriale(seriale)
    if chiave in visti:
        return
    visti.add(chiave)
    trovati.append((seriale, nome or _nome_leggibile(seriale)))


def leggi_dispositivi_gio(testo: str) -> list[tuple[str, str]]:
    """Coppie ``(seriale, nome)`` ricavate dall'elenco di ``gio mount -li``.

    Non si dipende dalla forma esatta delle righe (cambia fra versioni di gvfs): si guarda
    il blocco corrente (``Volume(n)``/``Mount(n)``) per il nome e qualunque indirizzo
    ``mtp://`` per il seriale.
    """
    trovati: list[tuple[str, str]] = []
    visti: set[str] = set()
    nome_blocco = ""
    for riga in (testo or "").splitlines():
        corrispondenza = RE_BLOCCO.match(riga)
        if corrispondenza:
            contenuto = corrispondenza.group(1).strip()
            if "->" in contenuto:  # «Mount(0): Nome -> mtp://.../»
                nome_blocco, _, uri = contenuto.partition("->")
                nome_blocco = nome_blocco.strip()
                _aggiungi_uri(trovati, visti, uri, nome_blocco)
            else:  # «Volume(0): Nome», l'indirizzo arriva nelle righe successive
                nome_blocco = contenuto
            continue
        for corrispondenza_uri in RE_URI_MTP.finditer(riga):
            _aggiungi_uri(trovati, visti, corrispondenza_uri.group(0), nome_blocco)
    return trovati


def dispositivi_jmtpfs() -> list[tuple[str, str]]:
    """Coppie ``(seriale, nome)`` ricavate da ``jmtpfs -l`` (ripiego senza gvfs)."""
    esito = _esegui(["jmtpfs", "-l"], timeout=15.0)
    if esito is None or esito.returncode != 0:
        return []
    trovati: list[tuple[str, str]] = []
    for riga in (esito.stdout or "").splitlines():
        riga = riga.strip()
        if not riga:
            continue
        corrispondenza = re.search(r"Device\s+(\d+)", riga)
        if corrispondenza:
            trovati.append((corrispondenza.group(1), riga))
    if not trovati:
        # jmtpfs più vecchi non numerano i dispositivi: si usa la prima riga come nome e un
        # seriale fisso, perché il ripiego monta comunque il primo telefono disponibile.
        righe = [riga.strip() for riga in (esito.stdout or "").splitlines() if riga.strip()]
        if righe:
            trovati.append(("0", righe[0]))
    return trovati


def dispositivi(env=None) -> list[tuple[str, str]]:
    """Telefoni MTP visibili a questo computer, senza montarli.

    Si guardano tre fonti, dalla più diretta alla più di ripiego: le cartelle già montate
    da gvfs, l'elenco dei montaggi di ``gio`` (che vede anche i telefoni non ancora
    montati) e, se non c'è niente, ``jmtpfs``. Lo stesso telefono può comparire in più
    fonti con nomi diversi: si tiene una voce sola, preferendo la forma che ``gio``
    stampa (è quella che ``gio mount`` accetta).
    """
    trovati: dict[str, tuple[str, str]] = {}

    def registra(seriale: str, nome: str, preferisci: bool = False) -> None:
        chiave = _chiave_seriale(seriale)
        presente = trovati.get(chiave)
        if presente is None:
            trovati[chiave] = (seriale, nome or _nome_leggibile(seriale))
        elif preferisci:
            trovati[chiave] = (seriale, nome or presente[1])

    cartella = cartella_gvfs(env)
    if cartella.is_dir():
        for voce in sorted(cartella.iterdir()):
            if voce.name.startswith("mtp:host=") and voce.is_dir():
                seriale = voce.name[len("mtp:host=") :]
                registra(seriale, _nome_leggibile(seriale))
    if _eseguibile("gio"):
        esito = _esegui(["gio", "mount", "-li"], timeout=15.0)
        if esito is not None and esito.returncode == 0:
            for seriale, nome in leggi_dispositivi_gio(esito.stdout):
                registra(seriale, nome, preferisci=True)
    if not trovati and _eseguibile("jmtpfs"):
        for seriale, nome in dispositivi_jmtpfs():
            registra(seriale, nome)
    return [voce for _, voce in sorted(trovati.items())]


# ── montaggio e smontaggio ───────────────────────────────────────────────


def _spiega_montaggio(esito: subprocess.CompletedProcess | None) -> GuaioMtp:
    """Traduce l'errore di ``gio mount`` in una frase utile, riconoscendo i casi tipici."""
    dettaglio = ""
    if esito is not None:
        dettaglio = f"{esito.stderr or ''} {esito.stdout or ''}"
    testo = dettaglio.lower()
    if "lock" in testo or "blocc" in testo or "busy" in testo:
        return GuaioMtp(
            "Il telefono è bloccato: non posso leggere i file finché lo schermo resta spento.",
            "Sblocca il telefono e rispondi «Consenti» alla richiesta di accesso ai dati, poi riprova.",
            ripiego_utile=False,
        )
    if "no such" in testo or "not found" in testo or "no device" in testo or "non esiste" in testo:
        return NessunTelefono(
            "Non trovo più il telefono che stavo usando.",
            "Scollega e ricollega il cavo, poi riprova.",
        )
    if "permission" in testo or "denied" in testo or "not authorized" in testo:
        return GuaioMtp(
            "Il computer non ha il permesso di leggere il telefono.",
            "Sblocca il telefono e accetta la richiesta di accesso ai dati; se resta uguale, "
            "scollega e ricollega il cavo.",
            ripiego_utile=False,
        )
    if esito is None:
        return GuaioMtp(
            "Il collegamento al telefono non ha risposto in tempo.",
            "Sblocca il telefono e riprova; se serve, scollega e ricollega il cavo.",
        )
    return GuaioMtp(
        "Non riesco a collegarmi al telefono tramite il desktop.",
        "Sblocca il telefono e accetta «Consenti accesso ai dati del dispositivo», poi riprova. "
        "Se non basta, installa o aggiorna il supporto MTP del desktop (pacchetto "
        "«gvfs-backends» su Debian/Ubuntu, «gvfs-mtp» su Fedora/Arch).",
    )


def _file_stato() -> Path:
    """Il file dove si ricordano i montaggi jmtpfs fra un comando e l'altro."""
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    cartella = Path(base) / "fotofacile"
    cartella.mkdir(parents=True, exist_ok=True)
    return cartella / "mtp-jmtpfs.json"


def _stato_jmtpfs() -> dict:
    try:
        dati = json.loads(_file_stato().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dati if isinstance(dati, dict) else {}


def _scrivi_stato_jmtpfs(stato: dict) -> None:
    try:
        _file_stato().write_text(json.dumps(stato), encoding="utf-8")
    except OSError:  # pragma: no cover - la memoria dei montaggi è solo un'ottimizzazione
        pass


def _cartella_nostra(percorso: Path) -> bool:
    """True solo per le cartelle temporanee che crea questo aiutante.

    Il file di stato è un semplice file di testo: se fosse rovinato, senza questo
    controllo una voce sbagliata farebbe cancellare una cartella qualunque del computer.
    """
    if not percorso.name.startswith("fotofacile-mtp-"):
        return False
    try:
        radice = Path(tempfile.gettempdir()).resolve()
        risolto = percorso.resolve()
    except OSError:  # pragma: no cover - difensivo
        return False
    return radice in risolto.parents


def _smonta_percorso(percorso: Path) -> None:
    """Smonta una cartella jmtpfs e la rimuove, **senza mai toccare i file del telefono**.

    La cartella viene rimossa solo quando non è più un montaggio: se lo smontaggio non
    riuscisse, ``rmtree`` cancellerebbe i file del telefono passando dal montaggio. E
    viene rimossa solo se è davvero una delle nostre cartelle temporanee: una voce
    sbagliata nel file di stato non deve poter cancellare una cartella dell'utente.
    """
    for comando in (["fusermount", "-u", str(percorso)], ["umount", str(percorso)]):
        # _esegui restituisce None anche quando il programma non esiste: si prova il
        # successivo senza controlli in più.
        esito = _esegui(comando, timeout=TIMEOUT_SMONTA)
        if esito is not None and esito.returncode == 0:
            break
    try:
        ancora_montato = os.path.ismount(percorso)
    except OSError:  # pragma: no cover - difensivo
        ancora_montato = False
    if not ancora_montato and _cartella_nostra(percorso):
        shutil.rmtree(percorso, ignore_errors=True)


def _punto_jmtpfs(seriale: str) -> Path | None:
    """La cartella jmtpfs già montata per quel telefono, se è ancora valida."""
    punto = _stato_jmtpfs().get(seriale)
    if not punto:
        return None
    percorso = Path(punto)
    if percorso.is_dir() and os.path.ismount(percorso):
        return percorso
    # Montaggio rimasto appeso (telefono scollegato senza smontare): si pulisce.
    _smonta_percorso(percorso)
    return None


def _monta_jmtpfs(seriale: str) -> Path:
    """Monta il telefono con jmtpfs (ripiego quando gvfs non c'è).

    jmtpfs non sa scegliere fra più telefoni: monta il primo che trova. Per non copiare o
    cancellare file sul telefono sbagliato, con più di un telefono collegato ci si ferma
    e si chiede di installare il supporto MTP del desktop.
    """
    percorso = _punto_jmtpfs(seriale)
    if percorso is not None:
        return percorso
    elenco = dispositivi_jmtpfs()
    if len(elenco) > 1:
        raise GuaioMtp(
            "Ci sono più telefoni collegati e il ripiego jmtpfs non sa quale scegliere.",
            "Installa il supporto MTP del desktop (pacchetto «gvfs-backends» su "
            "Debian/Ubuntu, «gvfs-mtp» su Fedora/Arch) e riprova.",
            ripiego_utile=False,
        )
    # Con un telefono solo, un montaggio jmtpfs già vivo è per forza lo stesso: lo si
    # riusa (gio e jmtpfs possono chiamarlo con nomi diversi) invece di montarne un secondo.
    stato = _stato_jmtpfs()
    for altro in list(stato):
        if altro == seriale:
            continue
        percorso = _punto_jmtpfs(altro)
        if percorso is not None:
            stato[seriale] = str(percorso)
            _scrivi_stato_jmtpfs(stato)
            return percorso
    punto = Path(tempfile.mkdtemp(prefix="fotofacile-mtp-"))
    try:
        esito = _esegui(["jmtpfs", str(punto)], timeout=TIMEOUT_JMTPFS)
    except BaseException:
        # Interrotto mentre montava (annullo, chiusura): la cartella non deve restare.
        _smonta_percorso(punto)
        raise
    if esito is None or esito.returncode != 0 or not os.path.ismount(punto):
        _smonta_percorso(punto)  # smonta (se serve) e rimuove solo se non è più montato
        dettaglio = ""
        if esito is not None:
            dettaglio = (esito.stderr or "").strip()
        raise GuaioMtp(
            "Il telefono non si è lasciato montare (jmtpfs).",
            "Sblocca il telefono e accetta la richiesta di accesso ai dati, poi riprova."
            + (f" Dettaglio: {dettaglio}" if dettaglio else ""),
        )
    stato[seriale] = str(punto)
    _scrivi_stato_jmtpfs(stato)
    return punto


def _monta(seriale: str, env=None) -> Path:
    """La cartella del telefono montato, montandolo se non lo è ancora.

    Prima si usa il meccanismo del desktop (``gio``/gvfs): è quello che conosce le
    autorizzazioni e parla la lingua del telefono. Solo se non c'è, o se è lui a essere
    rotto, si ripiega su ``jmtpfs``.
    """
    if not seriale:
        trovati = dispositivi(env)
        if not trovati:
            raise NessunTelefono("Non vedo nessun telefono collegato.")
        seriale = trovati[0][0]
    punto = montaggio_da_seriale(seriale, env)
    if punto is not None:
        return punto

    guaio_gio: GuaioMtp | None = None
    if _eseguibile("gio"):
        esito = _esegui(["gio", "mount", f"mtp://{seriale}/"], timeout=TIMEOUT_GIO)
        punto = montaggio_da_seriale(seriale, env)
        if punto is not None:
            return punto
        guaio_gio = _spiega_montaggio(esito)
        if not guaio_gio.ripiego_utile:
            raise guaio_gio

    if _eseguibile("jmtpfs"):
        try:
            return _monta_jmtpfs(seriale)
        except GuaioMtp:
            if guaio_gio is not None:
                raise guaio_gio
            raise

    if guaio_gio is not None:
        raise guaio_gio
    raise ComponenteMancante(
        "Su questo computer manca il componente per leggere il telefono (gio/gvfs).",
        "Installa il supporto MTP del desktop (pacchetto «gvfs-backends» su Debian/Ubuntu, "
        "«gvfs-mtp» su Fedora/Arch) e riprova.",
    )


def smonta(seriale: str, env=None) -> None:
    """Smonta il telefono indicato, sia da gvfs sia da jmtpfs (se è montato)."""
    punto = montaggio_da_seriale(seriale, env)
    if punto is not None and _eseguibile("gio"):
        # gvfs può volere il nome nella forma in cui lo stampa o in quella codificata
        # della cartella: si provano entrambe finché la cartella non sparisce.
        forme = [seriale, punto.name[len("mtp:host=") :]]
        try:
            forme.append(urllib.parse.unquote(forme[1]))
        except Exception:  # pragma: no cover - difensivo
            pass
        for forma in dict.fromkeys(forme):
            _esegui(["gio", "mount", "-u", f"mtp://{forma}/"], timeout=TIMEOUT_SMONTA)
            if montaggio_da_seriale(seriale, env) is None:
                break
    stato = _stato_jmtpfs()
    if seriale in stato:
        percorso = Path(stato.pop(seriale))
        _smonta_percorso(percorso)
        _scrivi_stato_jmtpfs(stato)


# ── percorsi e contenuto ─────────────────────────────────────────────────


def percorso_di_filesystem(punto: Path, percorso: str) -> Path:
    """Il file vero dentro il montaggio, dal percorso opaco del contratto.

    Il percorso arriva da ``elenca`` (o da un comando precedente) e non va mai
    interpretato come un percorso assoluto del computer: si scende sempre dentro il
    montaggio. I pezzi ``.`` e ``..`` vengono rifiutati: non hanno senso sul telefono e
    servirebbero solo a uscire dal montaggio.
    """
    parti = [parte for parte in percorso.split("/") if parte]
    for parte in parti:
        if parte in (".", ".."):
            raise GuaioMtp("Percorso del telefono non valido.", "Ripeti la ricerca delle foto.")
    return Path(punto).joinpath(*parti)


def cammina(radice: Path) -> Iterator[tuple[str, os.stat_result]]:
    """Percorre il telefono montato restituendo ``(percorso, informazioni)`` per ogni file.

    Una cartella che non si riesce a leggere viene saltata con una nota sull'uscita degli
    errori: un permesso mancante o un file che sparisce non devono far fallire l'intero
    elenco.
    """

    def scendi(cartella: Path, prefisso: str) -> Iterator[tuple[str, os.stat_result]]:
        try:
            voci = list(os.scandir(cartella))
        except OSError as errore:
            if not prefisso:
                # La radice che non si legge è un guaio, non una cartella da saltare: un
                # «0 foto» tranquillo farebbe credere che sul telefono non c'è niente.
                raise GuaioMtp(
                    "Non riesco a leggere il contenuto del telefono.",
                    "Sblocca il telefono e accetta la richiesta di accesso ai dati, poi riprova.",
                ) from errore
            sys.stderr.write(f"Salto la cartella {prefisso}: {errore}\n")
            return
        for voce in voci:
            percorso = f"{prefisso}/{voce.name}"
            try:
                if voce.is_dir(follow_symlinks=False):
                    yield from scendi(Path(voce.path), percorso)
                    continue
                info = voce.stat(follow_symlinks=False)
            except OSError as errore:
                sys.stderr.write(f"Salto {percorso}: {errore}\n")
                continue
            yield percorso, info

    yield from scendi(Path(radice), "")


def genere_per_estensione(percorso: str) -> str | None:
    """«photo», «video» o ``None`` in base all'estensione del file."""
    nome = percorso.rsplit("/", 1)[-1]
    if "." not in nome:
        return None
    estensione = nome.rsplit(".", 1)[-1].lower()
    if estensione in ESTENSIONI_FOTO:
        return "photo"
    if estensione in ESTENSIONI_VIDEO:
        return "video"
    return None


# ── comandi del contratto ────────────────────────────────────────────────


def _stampa_riga(dati: dict) -> None:
    # Solo ASCII («\u00e0» invece di «à»): la riga si legge uguale qualunque sia la
    # codifica di sistema di questo processo.
    sys.stdout.write(json.dumps(dati) + "\n")
    sys.stdout.flush()


def _valore(argomenti: Sequence[str], chiave: str, predefinito: str = "") -> str:
    elenco = list(argomenti)
    if chiave in elenco:
        posizione = elenco.index(chiave)
        if posizione + 1 < len(elenco):
            return elenco[posizione + 1]
    return predefinito


def comando_dispositivi(_argomenti: Sequence[str]) -> int:
    trovati = dispositivi()
    if not trovati:
        raise NessunTelefono(
            "Non vedo nessun telefono collegato.",
            "Collega il telefono con il cavo, sbloccalo e accetta la richiesta di accesso ai dati.",
        )
    _stampa_riga(
        {
            "dispositivi": [
                {"seriale": seriale, "nome": nome, "stato": "device", "prodotto": ""}
                for seriale, nome in trovati
            ]
        }
    )
    return USCITA_OK


def _nota_se_vuoto(punto: Path) -> None:
    """Un telefono montato ma vuoto è quasi sempre bloccato: dirlo, senza fallire."""
    try:
        voci = list(os.scandir(punto))
    except OSError:
        return
    if not voci:
        sys.stderr.write(
            "Il telefono risulta montato ma vuoto: sbloccalo e accetta la richiesta di "
            "accesso ai dati, poi riprova.\n"
        )


def comando_elenca(argomenti: Sequence[str]) -> int:
    voluto = _valore(argomenti, "--seriale")
    solo_foto = "--solo-foto" in argomenti
    punto = _monta(voluto)
    _nota_se_vuoto(punto)
    conteggio = 0
    for percorso, info in cammina(punto):
        genere = genere_per_estensione(percorso)
        if genere is None or (solo_foto and genere == "video"):
            continue
        _stampa_riga(
            {
                "percorso": percorso,
                "dimensione": int(info.st_size),
                "data": int(info.st_mtime),
                "genere": genere,
            }
        )
        conteggio += 1
    _stampa_riga({"fine": True, "conteggio": conteggio})
    return USCITA_OK


def comando_copia(argomenti: Sequence[str]) -> int:
    percorso = _valore(argomenti, "--percorso")
    if not percorso:
        raise GuaioMtp("Manca il file da copiare (--percorso).")
    punto = _monta(_valore(argomenti, "--seriale"))
    file = percorso_di_filesystem(punto, percorso)
    if not file.is_file():
        raise GuaioMtp(
            f"Sul telefono non trovo più il file {percorso}.",
            "Ripeti la ricerca delle foto e riprova.",
        )
    uscita = sys.stdout.buffer
    try:
        with open(file, "rb") as sorgente:
            for blocco in iter(lambda: sorgente.read(BLOCCO), b""):
                uscita.write(blocco)
                # L'avanzamento deve essere visibile mentre il file cresce: il programma
                # principale guarda la dimensione del file «.part» per la barra.
                uscita.flush()
    except OSError as errore:
        raise GuaioMtp(
            f"Non sono riuscito a leggere il file dal telefono: {errore}",
            "Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
        ) from errore
    return USCITA_OK


def comando_cancella(argomenti: Sequence[str]) -> int:
    percorso = _valore(argomenti, "--percorso")
    if not percorso:
        raise GuaioMtp("Manca il file da cancellare (--percorso).")
    punto = _monta(_valore(argomenti, "--seriale"))
    file = percorso_di_filesystem(punto, percorso)
    if not file.exists():
        raise GuaioMtp(
            f"Sul telefono non trovo più il file {percorso}.",
            "Forse è già stato cancellato: riprova l'elenco delle foto.",
        )
    try:
        file.unlink()
    except OSError as errore:
        raise GuaioMtp(
            f"Non sono riuscito a cancellare il file dal telefono: {errore}",
            "Il file resta sul telefono: puoi cancellarlo dalla Galleria, oppure attivare "
            "il Debug USB per cancellarlo da qui.",
        ) from errore
    return USCITA_OK


def comando_smonta(argomenti: Sequence[str]) -> int:
    """Comando interno in più rispetto al contratto: smonta i telefoni montati.

    Serve al trasporto per pulire alla chiusura del programma: non c'è una persona a cui
    chiedere niente, quindi qualunque errore viene ignorato.
    """
    voluto = _valore(argomenti, "--seriale")
    if voluto:
        seriali = [voluto]
    else:
        seriali = [seriale for seriale, _ in dispositivi()] + list(_stato_jmtpfs())
    for seriale in dict.fromkeys(seriali):
        try:
            smonta(seriale)
        except Exception:  # pulizia difensiva: non deve mai fermare la chiusura
            continue
    return USCITA_OK


COMANDI: dict[str, Callable[[Sequence[str]], int]] = {
    "dispositivi": comando_dispositivi,
    "elenca": comando_elenca,
    "copia": comando_copia,
    "cancella": comando_cancella,
    "smonta": comando_smonta,
}


def main(argv: Sequence[str] | None = None) -> int:
    argomenti = list(sys.argv[1:] if argv is None else argv)
    if not argomenti:
        sys.stderr.write("Serve un comando: dispositivi, elenca, copia, cancella.\n")
        return USCITA_ERRORE
    comando, resto = argomenti[0], argomenti[1:]
    funzione = COMANDI.get(comando)
    if funzione is None:
        sys.stderr.write(f"Comando sconosciuto: {comando}\n")
        return USCITA_ERRORE
    try:
        return funzione(resto)
    except GuaioMtp as guaio:
        # L'ultima riga finisce nel suggerimento mostrato dall'app: prima il motivo,
        # poi cosa fare.
        sys.stderr.write(f"{guaio.messaggio}\n")
        if guaio.suggerimento:
            sys.stderr.write(f"{guaio.suggerimento}\n")
        return guaio.uscita
    except Exception as errore:  # qualunque guaio va raccontato, non nascosto
        sys.stderr.write(f"{type(errore).__name__}: {errore}\n")
        return USCITA_ERRORE


if __name__ == "__main__":  # pragma: no cover - avvio diretto
    raise SystemExit(main())

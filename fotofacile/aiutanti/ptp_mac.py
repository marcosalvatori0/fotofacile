"""Aiutante macOS: parla con il telefono tramite il componente di sistema ImageCaptureCore.

Perché serve: macOS **non** sa leggere i telefoni Android come dischi (non ha il supporto
MTP), ma ogni telefono Android si presenta anche come «fotocamera» (PTP): è lo stesso
meccanismo che usa l'applicazione «Acquisizione immagini» di macOS. ImageCaptureCore è il
componente di sistema che lo rende disponibile, e PyObjC lo espone a Python.

Perché un processo separato: ImageCaptureCore ha bisogno di un ciclo di eventi Cocoa tutto
suo. Mescolarlo con la grafica di Tk della finestra principale blocca tutto. Qui è un
programma a parte, che il programma principale avvia, tiene d'occhio e può interrompere.

Uso (dall'esterno non si chiama mai a mano, lo fa :mod:`fotofacile.core.trasporto_aiutante`)::

    python -m fotofacile.aiutanti.ptp_mac dispositivi
    python -m fotofacile.aiutanti.ptp_mac elenca [--seriale S] [--solo-foto]
    python -m fotofacile.aiutanti.ptp_mac copia --percorso P
    python -m fotofacile.aiutanti.ptp_mac cancella --percorso P

L'uscita standard è sempre leggibile a macchina; i messaggi per l'utente vanno sull'uscita
degli errori.
"""

from __future__ import annotations

import json
import sys
import time
from typing import Callable, Iterator, Sequence

#: Quanto si aspetta che compaia un telefono.
ATTESA_DISPOSITIVO = 6.0
#: Quanto si aspetta per aprire la «conversazione» con il telefono.
ATTESA_SESSIONE = 15.0
#: Quanto si aspetta per l'elenco completo.
ATTESA_ELENCO = 120.0
#: Quanto si aspetta per un blocco di dati.
ATTESA_LETTURA = 120.0
#: Dimensione di un blocco di lettura: compromesso fra velocità e memoria occupata.
BLOCCO = 512 * 1024
#: Passo del ciclo di eventi: abbastanza corto da restare reattivi, abbastanza lungo da
#: non consumare il processore.
PASSO_CICLO = 0.05

USCITA_OK = 0
USCITA_ERRORE = 2
USCITA_NESSUN_TELEFONO = 3

ESTENSIONI_FOTO = (
    "jpg", "jpeg", "png", "gif", "webp", "heic", "heif", "bmp", "tif", "tiff", "dng", "avif",
)
ESTENSIONI_VIDEO = ("mp4", "3gp", "3gpp", "mov", "mkv", "avi", "webm", "m4v", "mts")


class AiutanteNonDisponibile(Exception):
    """PyObjC o ImageCaptureCore non ci sono: il collegamento diretto non è utilizzabile."""


class NessunTelefono(Exception):
    """Nessun telefono collegato riconosciuto come fotocamera."""


def _componenti():
    """Importa PyObjC e ImageCaptureCore, spiegando con calma se mancano."""
    try:
        import objc
        from Foundation import NSDate, NSObject, NSRunLoop, NSURL
        import ImageCaptureCore as ic
    except ImportError as errore:  # pragma: no cover - dipende dall'installazione
        raise AiutanteNonDisponibile(
            "Manca il componente di sistema per leggere il telefono (pyobjc)."
        ) from errore
    return objc, NSDate, NSObject, NSRunLoop, NSURL, ic


def sistema_disponibile() -> bool:
    """True se questo aiutante può funzionare su questo computer."""
    try:
        _componenti()
    except AiutanteNonDisponibile:
        return False
    return True


# ── ciclo di eventi e attese ─────────────────────────────────────────────


def _pompa(finche: Callable[[], bool], timeout: float) -> bool:
    """Fa girare il ciclo di eventi Cocoa finché la condizione non è vera o scade il tempo.

    ImageCaptureCore risponde **sempre** in modo asincrono: senza far girare il ciclo di
    eventi le risposte non arrivano mai.
    """
    _, NSDate, _, NSRunLoop, _, _ = _componenti()
    ciclo = NSRunLoop.currentRunLoop()
    scadenza = time.monotonic() + timeout
    while not finche() and time.monotonic() < scadenza:
        ciclo.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(PASSO_CICLO))
    return bool(finche())


class _Attesa:
    """Raccoglitore del risultato di una chiamata asincrona.

    ImageCaptureCore non restituisce mai un valore: consegna il risultato a una funzione
    («gestore di completamento») chiamata più tardi. Questa classe è il posto dove quel
    risultato viene messo da parte mentre si fa girare il ciclo di eventi.

    I due metodi corrispondono alle due forme usate dal componente: alcune chiamate
    rispondono solo con un eventuale errore, altre con ``(dati, errore)``. Distinguerle è
    importante: senza, l'errore verrebbe scambiato per i dati e viceversa.
    """

    def __init__(self) -> None:
        self.fatto = False
        self.valore: object = None
        self.errore: object = None

    def solo_errore(self, errore=None) -> None:
        """Risposta del tipo ``(errore)``."""
        self.fatto = True
        self.errore = errore

    def dati_ed_errore(self, dati=None, errore=None) -> None:
        """Risposta del tipo ``(dati, errore)``."""
        self.fatto = True
        self.valore = dati
        self.errore = errore

    def attendi(self, timeout: float) -> "_Attesa":
        _pompa(lambda: self.fatto, timeout)
        return self


# ── telefoni collegati ───────────────────────────────────────────────────


def trova_telefoni(timeout: float = ATTESA_DISPOSITIVO) -> list:
    """Elenca i telefoni che macOS riconosce come fotocamera."""
    objc, _, NSObject, _, _, ic = _componenti()

    class Raccoglitore(NSObject):
        def init(self):
            self = objc.super(Raccoglitore, self).init()
            if self is None:  # pragma: no cover - difensivo
                return None
            self.trovati = []
            return self

        def deviceBrowser_didAddDevice_moreComing_(self, _browser, device, _more):
            if device not in self.trovati:
                self.trovati.append(device)

        def deviceBrowser_didRemoveDevice_moreComing_(self, _browser, device, _more):
            if device in self.trovati:
                self.trovati.remove(device)

    browser = ic.ICDeviceBrowser.alloc().init()
    raccoglitore = Raccoglitore.alloc().init()
    browser.setDelegate_(raccoglitore)
    browser.setBrowsedDeviceTypeMask_(ic.ICDeviceTypeMaskCamera | ic.ICDeviceLocationTypeMaskLocal)
    browser.start()
    try:
        _pompa(lambda: bool(raccoglitore.trovati), timeout)
        return list(raccoglitore.trovati)
    finally:
        try:
            browser.stop()
        except Exception:  # pragma: no cover - difensivo
            pass


def apri_sessione(device, timeout: float = ATTESA_SESSIONE) -> None:
    """Apre la «conversazione» con il telefono, necessaria prima di qualunque lettura."""
    attesa = _Attesa()
    device.requestOpenSessionWithOptions_completion_(None, attesa.solo_errore)
    attesa.attendi(timeout)
    if attesa.errore is not None:
        raise OSError(f"Non riesco ad aprire il collegamento con il telefono: {attesa.errore}")


def chiudi_sessione(device) -> None:
    """Chiude la conversazione: è gentile e libera il telefono per altre applicazioni."""
    try:
        attesa = _Attesa()
        device.requestCloseSessionWithOptions_completion_(None, attesa.solo_errore)
        attesa.attendi(2.0)
    except Exception:  # pragma: no cover - la chiusura non deve mai bloccare
        pass


def enumera(device, timeout: float = ATTESA_ELENCO) -> None:
    """Chiede al telefono l'elenco completo del contenuto."""
    attesa = _Attesa()
    try:
        device.requestEnumerateContentWithOptions_completion_(None, attesa.solo_errore)
    except Exception:  # pragma: no cover - versioni senza questa funzione
        # Senza questa chiamata `contents()` funziona lo stesso, solo più lentamente.
        return
    attesa.attendi(timeout)


def seriale(device) -> str:
    """Identificativo stabile del telefono: non cambia fra un collegamento e l'altro."""
    for attributo in ("serialNumber", "UUIDString", "name"):
        try:
            valore = getattr(device, attributo)()
        except Exception:  # pragma: no cover - attributo assente
            continue
        if valore:
            return str(valore)
    return "telefono"


def nome(device) -> str:
    try:
        return str(device.name() or "")
    except Exception:  # pragma: no cover - difensivo
        return ""


def _e_cartella(voce, ic) -> bool:
    try:
        return bool(voce.isKindOfClass_(ic.ICCameraFolder))
    except Exception:  # pragma: no cover - difensivo
        return False


def cammina(device, ic) -> Iterator[tuple[object, str]]:
    """Percorre tutto il contenuto del telefono restituendo coppie ``(file, percorso)``."""

    def scendi(nodo, prefisso: str, visti: set) -> Iterator[tuple[object, str]]:
        try:
            voci = list(nodo.contents() or [])
        except Exception:  # pragma: no cover - cartella illeggibile
            return
        for voce in voci:
            chiave = id(voce)
            if chiave in visti:  # difesa contro elenchi che si ripetono
                continue
            visti.add(chiave)
            try:
                etichetta = str(voce.name() or "")
            except Exception:  # pragma: no cover - difensivo
                continue
            percorso = f"{prefisso}/{etichetta}" if prefisso else f"/{etichetta}"
            if _e_cartella(voce, ic):
                yield from scendi(voce, percorso, visti)
            else:
                yield voce, percorso

    yield from scendi(device, "", set())


def genere_per_nome(percorso: str) -> str | None:
    """«photo», «video» o ``None`` in base all'estensione del file."""
    nome_file = percorso.rsplit("/", 1)[-1]
    if "." not in nome_file:
        return None
    estensione = nome_file.rsplit(".", 1)[-1].lower()
    if estensione in ESTENSIONI_FOTO:
        return "photo"
    if estensione in ESTENSIONI_VIDEO:
        return "video"
    return None


def voce_json(file, percorso: str, seriale_telefono: str = "") -> dict:
    """Descrizione di un file, nella forma che il programma principale si aspetta."""
    return {
        "percorso": percorso,
        "dimensione": _dimensione_di(file),
        "data": _data_di(file),
        "genere": genere_per_nome(percorso),
        "seriale": seriale_telefono,
    }


def _dimensione_di(file) -> int:
    try:
        return int(file.fileSize())
    except Exception:  # pragma: no cover - difensivo
        return 0


def _data_di(file) -> int:
    for attributo in ("creationDate", "modificationDate", "fileCreationDate"):
        try:
            valore = getattr(file, attributo)()
        except Exception:  # pragma: no cover - attributo assente
            continue
        if valore is not None:
            try:
                return int(valore.timeIntervalSince1970())
            except Exception:  # pragma: no cover - difensivo
                continue
    return 0


# ── lettura dei byte di un file ──────────────────────────────────────────


def leggi_file(
    file, scrivi: Callable[[bytes], None], dimensione: int, timeout: float = ATTESA_LETTURA
) -> int:
    """Consegna a ``scrivi`` i byte di un file del telefono, a blocchi.

    Si prova prima la lettura diretta a blocchi: non serve spazio su disco e non si scrive
    due volte (un video da 4 GB non viene mai copiato in una cartella temporanea). Se il
    telefono non la supporta si ripiega sullo scaricamento classico.
    """
    try:
        return _leggi_a_blocchi(file, scrivi, dimensione, timeout)
    except _LetturaNonDisponibile:
        return _leggi_scaricando(file, scrivi)


class _LetturaNonDisponibile(Exception):
    """Il telefono non sa consegnare i byte a blocchi: si usa l'altro metodo."""


def _leggi_a_blocchi(
    file, scrivi: Callable[[bytes], None], dimensione: int, timeout: float
) -> int:
    letti = 0
    while letti < dimensione:
        richiesti = min(BLOCCO, dimensione - letti)
        attesa = _Attesa()
        try:
            file.requestReadDataAtOffset_length_completion_(letti, richiesti, attesa.dati_ed_errore)
        except Exception as errore:
            if letti == 0:
                raise _LetturaNonDisponibile(str(errore)) from errore
            break
        attesa.attendi(timeout)
        if attesa.errore is not None:
            if letti == 0:
                raise _LetturaNonDisponibile(str(attesa.errore)) from attesa.errore
            break
        if attesa.valore is None:
            break
        dati = bytes(attesa.valore)
        if not dati:
            break
        scrivi(dati)
        letti += len(dati)
    return letti


def _leggi_scaricando(file, scrivi: Callable[[bytes], None]) -> int:
    """Ripiego: si fa consegnare il file in una cartella temporanea e poi lo si ricopia."""
    import os
    import tempfile

    _, _, _, _, NSURL, _ = _componenti()
    try:
        device = file.device()
    except Exception as errore:  # pragma: no cover - difensivo
        raise OSError("Il telefono non è più disponibile.") from errore
    if device is None:
        raise OSError("Il telefono non è più disponibile.")
    nome_file = str(file.name() or "file")
    with tempfile.TemporaryDirectory(prefix="fotofacile-ptp-") as cartella:
        attesa = _Attesa()
        opzioni = {
            "ICDownloadsDirectoryURL": NSURL.fileURLWithPath_(cartella),
            "ICSaveAsFilename": nome_file,
            "ICOverwrite": True,
        }
        try:
            file.requestDownloadWithOptions_completion_(opzioni, attesa.solo_errore)
        except Exception as errore:
            raise OSError(
                "Questo telefono non mi lascia leggere i file in nessuno dei due modi."
            ) from errore
        attesa.attendi(ATTESA_LETTURA)
        if attesa.errore is not None:
            raise OSError(f"Il telefono non ha consegnato il file: {attesa.errore}")
        candidati = [nome for nome in sorted(os.listdir(cartella)) if not nome.startswith(".")]
        if not candidati:
            raise OSError("Il telefono non ha consegnato il file.")
        percorso = os.path.join(cartella, candidati[0])
        totale = 0
        with open(percorso, "rb") as sorgente:
            for blocco in iter(lambda: sorgente.read(BLOCCO), b""):
                scrivi(blocco)
                totale += len(blocco)
        return totale


# ── comandi ──────────────────────────────────────────────────────────────


def _stampa_riga(dati: dict) -> None:
    sys.stdout.write(json.dumps(dati, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _valore(argomenti: Sequence[str], chiave: str, predefinito: str = "") -> str:
    elenco = list(argomenti)
    if chiave in elenco:
        posizione = elenco.index(chiave)
        if posizione + 1 < len(elenco):
            return elenco[posizione + 1]
    return predefinito


def _apri_telefono(voluto: str = ""):
    """Trova il telefono (quello indicato o il primo) e apre la sessione."""
    telefoni = trova_telefoni()
    if not telefoni:
        raise NessunTelefono("Non vedo nessun telefono collegato.")
    scelto = telefoni[0]
    if voluto:
        for telefono in telefoni:
            if seriale(telefono) == voluto:
                scelto = telefono
                break
    apri_sessione(scelto)
    return scelto


def trova_file(telefono, percorso: str, ic):
    """Il file del telefono che corrisponde al percorso indicato."""
    enumera(telefono)
    for file, cammino in cammina(telefono, ic):
        if cammino == percorso:
            return file
    return None


def comando_dispositivi(_argomenti: Sequence[str]) -> int:
    telefoni = trova_telefoni()
    _stampa_riga(
        {
            "dispositivi": [
                {"seriale": seriale(t), "nome": nome(t), "stato": "device", "prodotto": ""}
                for t in telefoni
            ]
        }
    )
    return USCITA_OK


def comando_elenca(argomenti: Sequence[str]) -> int:
    _, _, _, _, _, ic = _componenti()
    voluto = _valore(argomenti, "--seriale")
    solo_foto = "--solo-foto" in argomenti
    telefono = _apri_telefono(voluto)
    try:
        enumera(telefono)
        identificativo = seriale(telefono)
        conteggio = 0
        for file, percorso in cammina(telefono, ic):
            genere = genere_per_nome(percorso)
            if genere is None or (solo_foto and genere == "video"):
                continue
            _stampa_riga(voce_json(file, percorso, identificativo))
            conteggio += 1
        _stampa_riga({"fine": True, "conteggio": conteggio})
    finally:
        chiudi_sessione(telefono)
    return USCITA_OK


def comando_copia(argomenti: Sequence[str]) -> int:
    _, _, _, _, _, ic = _componenti()
    percorso = _valore(argomenti, "--percorso")
    if not percorso:
        raise ValueError("Manca il file da copiare (--percorso).")
    telefono = _apri_telefono(_valore(argomenti, "--seriale"))
    try:
        trovato = trova_file(telefono, percorso, ic)
        if trovato is None:
            raise OSError(f"Sul telefono non trovo più il file {percorso}.")
        dimensione = _dimensione_di(trovato)
        if dimensione <= 0:
            # Senza una dimensione credibile non si può verificare che la copia sia completa:
            # meglio fermarsi che consegnare un file vuoto (e magari cancellare l'originale).
            raise OSError(
                f"Il telefono non dice quanto è grande {percorso}: non me la sento di copiarlo."
            )
        uscita = sys.stdout.buffer

        def scrivi(blocco: bytes) -> None:
            uscita.write(blocco)

        scritti = leggi_file(trovato, scrivi, dimensione)
        uscita.flush()
        if scritti != dimensione:
            raise OSError(
                f"Il file è arrivato incompleto ({scritti} byte su {dimensione})."
            )
    finally:
        chiudi_sessione(telefono)
    return USCITA_OK


def comando_cancella(argomenti: Sequence[str]) -> int:
    _, _, _, _, _, ic = _componenti()
    percorso = _valore(argomenti, "--percorso")
    if not percorso:
        raise ValueError("Manca il file da cancellare (--percorso).")
    telefono = _apri_telefono(_valore(argomenti, "--seriale"))
    try:
        trovato = trova_file(telefono, percorso, ic)
        if trovato is None:
            raise OSError(f"Sul telefono non trovo più il file {percorso}.")
        attesa = _Attesa()
        telefono.requestDeleteFiles_deleteFailed_completion_([trovato], None, attesa.dati_ed_errore)
        attesa.attendi(ATTESA_SESSIONE)
        if attesa.errore is not None:
            raise OSError(f"Non sono riuscito a cancellare il file: {attesa.errore}")
    finally:
        chiudi_sessione(telefono)
    return USCITA_OK


COMANDI: dict[str, Callable[[Sequence[str]], int]] = {
    "dispositivi": comando_dispositivi,
    "elenca": comando_elenca,
    "copia": comando_copia,
    "cancella": comando_cancella,
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
    except NessunTelefono as errore:
        sys.stderr.write(f"{errore}\n")
        return USCITA_NESSUN_TELEFONO
    except AiutanteNonDisponibile as errore:
        sys.stderr.write(f"{errore}\n")
        return USCITA_ERRORE
    except Exception as errore:  # qualunque guaio va raccontato, non nascosto
        sys.stderr.write(f"{type(errore).__name__}: {errore}\n")
        return USCITA_ERRORE


if __name__ == "__main__":  # pragma: no cover - avvio diretto
    raise SystemExit(main())

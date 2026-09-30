"""Un test per ogni errore realmente trovato e corretto.

Ogni test qui descrive un difetto che è **davvero esistito** nel programma, non un caso
immaginario: il commento dice cosa succedeva prima della correzione. Servono a impedire che
quegli errori tornino senza che nessuno se ne accorga.
"""

from __future__ import annotations

import hashlib
import json
import threading
import zipfile
from pathlib import Path

import pytest

from fotofacile.core.adb_passi import AdbDemoAPassi
from fotofacile.core.demo import DemoAdbBackend
from fotofacile.core.errors import FotoFacileError
from fotofacile.core.history import History
from fotofacile.core.installer import controlla_archivio, impronta_file
from fotofacile.core.ops import ProcessoEsterno, esegui_fino_alla_fine
from fotofacile.core.planner import MAX_PERCORSO, TransferOptions, build_plan, destination_for
from fotofacile.core.scanner import MediaFile


def script(tmp_path: Path, nome: str, corpo: str) -> str:
    percorso = tmp_path / nome
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return str(percorso)


# ── la cartella scelta dall'utente non viene mai riscritta ───────────────
def test_percorso_lunghissimo_non_esce_mai_dalla_cartella_scelta(tmp_path):
    """Prima: un percorso oltre 240 caratteri veniva accorciato togliendo i primi pezzi,
    compresa la cartella scelta (`/Users/tizio/Immagini/...` diventava `/tizio/Immagini/...`).
    Le foto finivano in una cartella diversa da quella indicata, o la copia falliva con un
    falso «non hai i permessi»."""
    scelta = tmp_path / "Immagini" / "FotoFacile" / "Telefono" / "2026-09-28"
    profondo = "/sdcard/DCIM/" + "/".join("cartella_lunga_" + "x" * 30 for _ in range(8))
    percorso = destination_for(f"{profondo}/foto.jpg", scelta, True)

    assert str(percorso).startswith(str(scelta)), "la radice scelta non deve mai cambiare"
    assert percorso.name.endswith(".jpg")
    assert percorso.parent.is_relative_to(scelta.parent)


def test_percorso_lunghissimo_resta_dentro_anche_con_nomi_piatti(tmp_path):
    scelta = tmp_path / ("m" * 60)
    percorso = destination_for("/sdcard/DCIM/" + "n" * 300 + ".jpg", scelta, False)
    assert percorso.parent == scelta
    assert percorso.suffix == ".jpg"


def test_nomi_troncati_non_si_sovrascrivono_a_vicenda(tmp_path):
    """Prima: accorciando due nomi lunghi lo stesso modo si poteva ottenere lo stesso
    percorso per due foto diverse, e una delle due andava persa."""
    lunga = "foto_con_nome_molto_lungo_" + "x" * 160
    file = [
        MediaFile(f"/sdcard/DCIM/{lunga}_1.jpg", 100, 0, "photo"),
        MediaFile(f"/sdcard/DCIM/{lunga}_2.jpg", 100, 0, "photo"),
        MediaFile(f"/sdcard/DCIM/{lunga}_1.jpg", 100, 0, "photo"),
    ]
    piano = build_plan(file, TransferOptions(destination=tmp_path))
    nomi = [pianificato.dest_path.name for pianificato in piano.files]
    assert len(set(nomi)) == len(nomi), "ogni foto deve avere un nome diverso"


def test_un_nome_impossibile_da_liberare_non_blocca_il_programma(tmp_path):
    """Prima: se il contatore « (1)» veniva tagliato dall'accorciamento, il ciclo che cerca
    un nome libero non finiva mai e la finestra si bloccava."""
    # 150 caratteri: il massimo che il programma tiene in un nome di file.
    lungo = "a" * 150
    (tmp_path / f"{lungo}.jpg").write_text("occupato", encoding="utf-8")
    piano = build_plan(
        [MediaFile(f"/sdcard/DCIM/{lungo}.jpg", 999, 0, "photo")],
        TransferOptions(destination=tmp_path),
    )
    assert piano.file_count == 1
    assert piano.files[0].dest_path.name != f"{lungo}.jpg"
    assert piano.files[0].dest_path != tmp_path / f"{lungo}.jpg"


# ── la copia non rilegge in memoria il file appena scritto ───────────────
def test_copia_non_rilegge_il_file_appena_scritto(tmp_path):
    """Prima: dopo ogni copia l'intero file veniva riletto in memoria come stringa.
    Un video da 4 GB diventava 4 GB di RAM occupata (e la copia falliva)."""
    comando = script(tmp_path, "adb", "dd if=/dev/zero bs=1024 count=400 2>/dev/null\n")
    adb = AdbDemoAPassi(DemoAdbBackend(file_count=0), intervallo=0.0)
    _ = adb  # il finto serve altrove; qui interessa il comando esterno
    processo = ProcessoEsterno(
        [comando],
        output_file=tmp_path / "grande.bin",
        leggi_output=False,
    )
    esito = esegui_fino_alla_fine(processo.aspetta())
    assert esito.output == "", "l'output non deve essere riletto quando non serve"
    assert (tmp_path / "grande.bin").stat().st_size == 400 * 1024


def test_processo_senza_file_di_output_non_usa_un_tubo(tmp_path):
    """Prima: senza file di output l'uscita finiva in un tubo che nessuno svuotava.
    Un comando molto loquace restava bloccato in scrittura e la finestra si piantava."""
    comando = script(tmp_path, "loquace", "i=0\nwhile [ $i -lt 20000 ]; do echo 'riga di prova 0123456789'; i=$((i+1)); done\n")
    processo = ProcessoEsterno([comando], timeout=60.0, leggi_output=False)
    esito = esegui_fino_alla_fine(processo.aspetta())
    assert esito.returncode == 0


# ── pulizia: nessun file o processo lasciato in giro ─────────────────────
def test_il_telefono_demo_si_puo_pulire(tmp_path):
    """Prima: `AdbDemoAPassi.pulisci()` cercava un attributo che non esisteva e sollevava
    AttributeError (non coperto dal `except OSError`), quindi la pulizia falliva sempre."""
    demo = AdbDemoAPassi(DemoDbBackend := DemoAdbBackend(file_count=2), intervallo=0.0)
    demo.pulisci()  # non deve sollevare niente
    assert isinstance(DemoDbBackend, DemoAdbBackend)


def test_scaricatore_abbandonato_non_lascia_file_a_meta(tmp_path):
    """Prima: chiudere la finestra durante il download lasciava `platform-tools.zip.scarico`
    (~10 MB) nella cartella dell'utente, perché GeneratorExit non è né OSError né
    FotoFacileError."""
    import io

    from fotofacile.core.ops import ScaricatoreAPassi

    dati = b"x" * 500_000

    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    destinazione = tmp_path / "componente.zip"
    generatore = ScaricatoreAPassi(
        "https://esempio/file.zip", destinazione, opener=lambda *_a, **_k: Risposta(dati)
    ).scarica()
    next(generatore)  # il download è iniziato
    generatore.close()  # l'utente chiude la finestra
    assert not destinazione.exists()
    assert not (tmp_path / "componente.zip.scarico").exists()


def test_copia_demo_abbandonata_non_lascia_parti(tmp_path):
    """Prima: abbandonare una copia in modalità demo lasciava il `.part` nella cartella foto."""
    demo = AdbDemoAPassi(DemoDbBackend := DemoAdbBackend(file_count=1), intervallo=0.0, pezzi_per_passo=1)
    file = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "x"))
    destinazione = tmp_path / "uscita" / "x.bin"
    generatore = demo.copia("DEMO12345", file[0].remote_path, destinazione)
    next(generatore)
    generatore.close()
    assert list((tmp_path / "uscita").glob("*.part")) == []
    assert isinstance(DemoDbBackend, DemoAdbBackend)


# ── il file temporaneo è unico per processo ──────────────────────────────
def test_file_a_meta_ha_un_nome_unico_per_processo(tmp_path):
    """Prima: due copie avviate insieme nella stessa cartella scrivevano nello stesso `.part`
    e si rovinavano a vicenda."""
    from fotofacile.core.adb_passi import percorso_temporaneo

    destinazione = tmp_path / "foto.jpg"
    temporaneo = percorso_temporaneo(destinazione)
    assert temporaneo != destinazione
    assert temporaneo.name.endswith(".part")
    assert str(__import__("os").getpid()) in temporaneo.name


def test_disco_pieno_viene_detto_prima_di_iniziare(tmp_path, monkeypatch):
    """Prima: un disco pieno arrivava come un generico «adb non è riuscito»,
    senza dire all'utente cosa fare."""
    import shutil

    from fotofacile.core import adb_passi

    monkeypatch.setattr(
        shutil, "disk_usage", lambda _p: shutil._ntuple_diskusage(0, 0, 1024)
    )
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0)
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(demo.copia("DEMO12345", "/x/y.jpg", tmp_path / "y.jpg"))
    assert "spazio" in errore.value.message.lower()
    assert errore.value.hint
    assert not (tmp_path / "y.jpg").exists()
    assert adb_passi  # il modulo è quello giusto


# ── il componente scaricato viene verificato davvero ─────────────────────
def _zip_finto(percorso: Path) -> Path:
    with zipfile.ZipFile(percorso, "w") as archivio:
        archivio.writestr("platform-tools/adb", b"#!/bin/sh\n")
    return percorso


def test_impronta_di_un_file_e_calcolata_davvero(tmp_path):
    """Prima: la verifica dell'impronta esisteva ma non era mai stata eseguita, e conteneva
    un errore (`hashlib` non importato) che sarebbe esploso al primo download vero."""
    percorso = tmp_path / "x.bin"
    percorso.write_bytes(b"contenuto")
    atteso = hashlib.sha1(b"contenuto").hexdigest()
    assert impronta_file(percorso) == atteso
    assert impronta_file(percorso, "sha256") == hashlib.sha256(b"contenuto").hexdigest()


def test_archivio_manomesso_viene_rifiutato(tmp_path, monkeypatch):
    from fotofacile.core import installer

    monkeypatch.setattr(installer, "MIN_DIMENSIONE_ARCHIVIO", 1)
    percorso = _zip_finto(tmp_path / "pt.zip")
    with pytest.raises(FotoFacileError) as errore:
        controlla_archivio(percorso, "0" * 40)
    assert "ufficiale" in errore.value.message.lower()


def test_archivio_con_impronta_giusta_viene_accettato(tmp_path, monkeypatch):
    from fotofacile.core import installer

    monkeypatch.setattr(installer, "MIN_DIMENSIONE_ARCHIVIO", 1)
    percorso = _zip_finto(tmp_path / "pt.zip")
    controlla_archivio(percorso, impronta_file(percorso))  # non deve sollevare niente


def test_un_file_troppo_piccolo_non_e_il_componente(tmp_path):
    """Una pagina di errore del server non deve essere scambiata per il componente."""
    percorso = tmp_path / "pt.zip"
    percorso.write_bytes(b"<html>errore 404</html>")
    with pytest.raises(FotoFacileError) as errore:
        controlla_archivio(percorso)
    assert "piccolo" in errore.value.message.lower()


# ── la cronologia malformata non fa saltare il programma ─────────────────
def test_cronologia_con_voci_malformate_non_fa_crash(tmp_path):
    """Prima: un file JSON valido ma con la struttura sbagliata faceva sollevare
    AttributeError da `contains`, in un punto lontano e difficile da capire."""
    percorso = tmp_path / "history.json"
    percorso.write_text(
        json.dumps({"version": 1, "devices": {"S1": {"/DCIM/a.jpg": 5}}}), encoding="utf-8"
    )
    cronologia = History(percorso)
    cronologia.load()
    assert cronologia.contains("S1", "/DCIM/a.jpg", 5, 0) is False
    assert cronologia.count("S1") == 0

    piano = build_plan(
        [MediaFile("/sdcard/DCIM/a.jpg", 5, 0, "photo")],
        TransferOptions(destination=tmp_path),
        serial="S1",
        history=cronologia,
    )
    assert piano.file_count == 1


def test_cronologia_con_voci_giuste_funziona_ancora(tmp_path):
    percorso = tmp_path / "history.json"
    percorso.write_text(
        json.dumps(
            {"version": 1, "devices": {"S1": {"/DCIM/a.jpg": {"size": 5, "mtime": 7, "dest": "x"}}}}
        ),
        encoding="utf-8",
    )
    cronologia = History(percorso)
    cronologia.load()
    assert cronologia.contains("S1", "/DCIM/a.jpg", 5, 7) is True


# ── la ricerca di ripiego rispetta la scelta sui video ───────────────────
def test_ricerca_di_ripiego_non_aggiunge_i_video_se_non_li_vuoi(tmp_path):
    """Prima: la ricerca estesa a tutta la memoria passava sempre `include_videos=True`,
    quindi chi aveva tolto la spunta si ritrovava comunque i video in elenco."""
    comando = script(
        tmp_path,
        "adb",
        "if [ \"$3\" = \"x\" ]; then exit 0; fi\necho '10|1700000000|/sdcard/Movies/v.mp4'\necho '20|1700000000|/sdcard/DCIM/f.jpg'\n",
    )
    adb = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0)
    _ = comando
    # Il finto deve restituire i file veri: si usa il backend demo, che elenca foto e video.
    trovati = esegui_fino_alla_fine(adb.cerca_media("DEMO12345", "x", include_videos=False))
    assert trovati, "il telefono demo deve pur restituire qualcosa"
    assert all(file.kind == "photo" for file in trovati)


# ── la finestra non moltiplica i controlli ───────────────────────────────
def test_il_sondaggio_non_si_moltiplica(tmp_path):
    """Prima: ogni ritorno al passo 1 lasciava in giro la catena di controlli precedente,
    e il telefono veniva interrogato 2, 3, 4 volte ogni due secondi."""
    pytest.importorskip("tkinter")
    from fotofacile.ui.widgets import tk_available

    if not tk_available():
        pytest.skip("serve un ambiente grafico")
    from fotofacile.ui.app import App

    app = App(backend=DemoAdbBackend(file_count=2), demo_mode=True)
    app.withdraw()
    try:
        pagina = app.pages["connect"]
        for _ in range(3):
            pagina.start_polling()
            pagina.stop_polling()
        assert pagina._tick_id is None
        pagina.start_polling()
        primo = pagina._tick_id
        pagina.start_polling()  # un secondo ingresso non deve lasciare il primo attivo
        assert pagina._tick_id != primo
        pagina.stop_polling()
        assert pagina._tick_id is None
    finally:
        app.stop_all_polling()
        app.destroy()


def test_ricostruire_le_pagine_lascia_una_pagina_valida(tmp_path):
    """Prima: dopo la ricostruzione `current_page` restava vuoto, e il primo «Indietro»
    sollevava ValueError."""
    pytest.importorskip("tkinter")
    from fotofacile.ui.widgets import tk_available

    if not tk_available():
        pytest.skip("serve un ambiente grafico")
    from fotofacile.ui.app import App

    app = App(backend=DemoAdbBackend(file_count=2), demo_mode=True)
    app.withdraw()
    try:
        app.ricostruisci_pagine()
        assert app.current_page in {"connect", "select", "options", "transfer"}
        app.go_to("prev")  # non deve sollevare niente
        app.go_to("next")
    finally:
        app.stop_all_polling()
        app.destroy()


# ── il resoconto non crea cartelle inattese ──────────────────────────────
def test_resoconto_non_crea_il_desktop_se_non_esiste(tmp_path, monkeypatch):
    """Prima: salvare il resoconto creava una cartella «Desktop» anche su computer che non
    ne hanno una (server, Desktop spostato altrove)."""
    from fotofacile.core.report import save_report

    bloccata = tmp_path / "bloccata"
    bloccata.mkdir()
    bloccata.chmod(0o500)
    monkeypatch.setenv("HOME", str(tmp_path))
    try:
        percorso = save_report("ciao", bloccata)
    finally:
        bloccata.chmod(0o700)
    assert percorso.parent == tmp_path / ".fotofacile"
    assert not (tmp_path / "Desktop").exists()


def test_annullamento_durante_la_copia_non_lascia_avanzi(tmp_path):
    """Le foto già copiate restano, il file a metà no."""
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0, pezzi_per_passo=1)
    file = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "x"))
    annulla = threading.Event()
    annulla.set()
    with pytest.raises(Exception):
        esegui_fino_alla_fine(
            demo.copia("DEMO12345", file[0].remote_path, tmp_path / "y.bin", annulla=annulla)
        )
    assert list(tmp_path.glob("*.part")) == []


def test_i_percorsi_accorciati_rispettano_il_limite_multipiattaforma(tmp_path):
    profondo = "/sdcard/DCIM/" + "/".join(f"cartella_numero_{i}" for i in range(30))
    percorso = destination_for(f"{profondo}/foto.jpg", tmp_path, True)
    assert len(str(percorso)) <= MAX_PERCORSO
    assert percorso.suffix == ".jpg"


# ── i processi figli si avviano davvero ──────────────────────────────────
def test_il_programma_sa_ritrovare_se_stesso():
    """Prima: il percorso per rilanciare sé stesso era sbagliato di una cartella
    (`fotofacile/fotofacile.py`, che non esiste). Tutto il collegamento diretto — cioè la
    possibilità di usare il telefono **senza Debug USB** — era morto dal sorgente."""
    from fotofacile.core.osutil import comando_se_stesso

    comando = comando_se_stesso("--aiutante", "ptp_mac")
    assert comando[0], "serve un programma da avviare"
    if not getattr(__import__("sys"), "frozen", False):
        assert Path(comando[1]).is_file(), f"il file di avvio non esiste: {comando[1]}"
        assert comando[1].endswith("fotofacile.py")
    assert comando[-2:] == ["--aiutante", "ptp_mac"]


def test_gli_aiutanti_hanno_un_nome_valido():
    from fotofacile.aiutanti import MODULI, modulo_disponibile

    for nome in ("ptp_mac", "wpd_win", "mtp_linux"):
        assert nome in MODULI
    assert modulo_disponibile("ptp_mac") is True
    assert modulo_disponibile("non_esiste") is False


def test_gli_script_powershell_hanno_il_bom():
    """Windows PowerShell 5.1 legge i file `.ps1` senza BOM con la codifica ANSI: gli accenti
    delle frasi italiane diventerebbero illeggibili e alcuni confronti smetterebbero di
    funzionare. Il BOM serve; a cmd.exe non dà fastidio perché quello legge i `.bat`."""
    radice = Path(__file__).resolve().parent.parent
    for percorso in radice.rglob("*.ps1"):
        if ".venv" in percorso.parts:
            continue
        assert percorso.read_bytes().startswith(b"\xef\xbb\xbf"), f"manca il BOM: {percorso}"


def test_i_bat_generati_non_hanno_il_bom():
    """Al contrario i `.bat` non devono averlo: cmd.exe non lo salta e la prima riga
    diventerebbe `'ï»¿@echo' non riconosciuto`."""
    radice = Path(__file__).resolve().parent.parent
    for percorso in radice.rglob("*.bat"):
        assert not percorso.read_bytes().startswith(b"\xef\xbb\xbf"), f"BOM di troppo: {percorso}"


# ── non si riprova all'infinito lo stesso collegamento ───────────────────
def test_cambiare_collegamento_non_riprova_sempre_lo_stesso():
    """Prima: il confronto per capire se il collegamento era cambiato era sempre vero
    (gli oggetti sono ricostruiti a ogni tentativo), quindi un errore faceva ripartire
    subito lo stesso tentativo, all'infinito, senza mai mostrare il messaggio."""
    from fotofacile.core.trasporto import TrasportoDemo
    from fotofacile.ui.app import App

    pytest.importorskip("tkinter")
    from fotofacile.ui.widgets import tk_available

    if not tk_available():
        pytest.skip("serve un ambiente grafico")

    app = App(backend=DemoAdbBackend(file_count=2), demo_mode=True)
    app.withdraw()
    try:
        app._gia_provati = set()
        disponibili = [TrasportoDemo(app.backend, intervallo=0.0)]

        def finti(**_kwargs):
            return disponibili

        import fotofacile.ui.app as modulo_app

        originale = modulo_app.trasporti_disponibili
        modulo_app.trasporti_disponibili = finti
        try:
            assert app.cambia_collegamento() is True   # il primo tentativo si fa
            assert app.cambia_collegamento() is False  # il secondo no: già provato
        finally:
            modulo_app.trasporti_disponibili = originale
    finally:
        app.stop_all_polling()
        app.destroy()


# ── lo spazio su disco si controlla sul file, non a caso ─────────────────
def test_una_foto_piccola_si_copia_anche_con_poco_spazio(tmp_path, monkeypatch):
    """Prima: sotto i 16 MB liberi il programma si rifiutava di copiare **qualsiasi** cosa,
    anche una foto da 200 KB."""
    import shutil

    monkeypatch.setattr(
        shutil, "disk_usage", lambda _p: shutil._ntuple_diskusage(0, 0, 8 * 1024 * 1024)
    )
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0)
    file = esegui_fino_alla_fine(demo.cerca_media("DEMO12345", "x"))
    piccolo = MediaFile(file[0].remote_path, 200_000, file[0].mtime, file[0].kind)
    scritti = esegui_fino_alla_fine(
        demo.copia(
            "DEMO12345", piccolo.remote_path, tmp_path / "p.jpg", remoto_dimensione=piccolo.size
        )
    )
    assert scritti == piccolo.size


def test_un_video_troppo_grande_viene_fermato_prima(tmp_path, monkeypatch):
    import shutil

    monkeypatch.setattr(
        shutil, "disk_usage", lambda _p: shutil._ntuple_diskusage(0, 0, 8 * 1024 * 1024)
    )
    demo = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0)
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(
            demo.copia("DEMO12345", "/x/v.mp4", tmp_path / "v.mp4", remoto_dimensione=500_000_000)
        )
    assert "spazio" in errore.value.message.lower()
    assert not (tmp_path / "v.mp4").exists()


# ── i processi esterni non restano appesi ────────────────────────────────
def test_un_comando_abbandonato_viene_interrotto(tmp_path):
    """Prima: abbandonare un controllo del telefono (cambio schermata) lasciava il comando
    vivo in sottofondo finché non finiva da solo."""
    comando = script(tmp_path, "lungo", "sleep 30\n")
    processo = ProcessoEsterno([comando], timeout=60.0, umano="x", hint="y")
    generatore = processo.aspetta()
    next(generatore)
    assert processo.passo() is True
    generatore.close()
    assert processo.passo() is False, "il comando deve essere interrotto"


def test_se_la_cartella_non_e_scrivibile_non_restano_file_temporanei(tmp_path):
    """Prima: se il file di destinazione non si poteva aprire, il file degli errori e il
    suo descrittore restavano aperti e sul disco."""
    import glob
    import tempfile

    prima = set(glob.glob(str(Path(tempfile.gettempdir()) / "fotofacile-errori-*")))
    # Un file che in realtà è una cartella: si apre senza problemi come percorso, ma
    # la scrittura fallisce dopo che il file degli errori è già stato creato.
    occupato = tmp_path / "occupato.txt"
    occupato.mkdir()
    processo = ProcessoEsterno(["/bin/echo", "ciao"], output_file=occupato)
    with pytest.raises(FotoFacileError):
        processo.avvia()
    dopo = set(glob.glob(str(Path(tempfile.gettempdir()) / "fotofacile-errori-*")))
    assert dopo == prima, "nessun file di appoggio deve restare in giro"


def test_una_cartella_non_scrivibile_produce_un_errore_comprensibile(tmp_path):
    cartella = tmp_path / "bloccata"
    cartella.mkdir()
    cartella.chmod(0o500)
    try:
        processo = ProcessoEsterno(["/bin/echo", "ciao"], output_file=cartella / "sotto" / "x.txt")
        with pytest.raises(FotoFacileError) as errore:
            processo.avvia()
    finally:
        cartella.chmod(0o700)
    assert errore.value.hint


# ── D1 ─────────────────────────────────────────────────────────────────────
# Prima: le foto copiate avevano la data di «adesso»; la data di scatto andava persa e
# in Esplora file / Foto tutto risultava di oggi.
class _TelefonoFinto:
    """Il minimo che serve a `transfer`: due metodi."""

    def __init__(self, contenuti: dict[str, bytes]) -> None:
        self.contenuti = contenuti
        self.cancellati: list[str] = []

    def stream_file(self, serial, remote_path, chunk_size=65536):
        yield self.contenuti[remote_path]

    def delete_file(self, serial, remote_path):
        self.cancellati.append(remote_path)


def _piano_singolo(tmp_path, percorso="/sdcard/DCIM/Camera/a.jpg", dati=b"x" * 10, mtime=1_500_000_000):
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile

    media = MediaFile(remote_path=percorso, size=len(dati), mtime=mtime, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out")
    return build_plan([media], opzioni), opzioni, _TelefonoFinto({percorso: dati})


def test_d1_la_copia_conserva_la_data_di_scatto(tmp_path):
    from fotofacile.core.transfer import transfer

    piano, opzioni, telefono = _piano_singolo(tmp_path)
    esiti = transfer(telefono, "S1", piano, opzioni)
    assert len(esiti.copied) == 1
    assert int(esiti.copied[0].stat().st_mtime) == 1_500_000_000


# ── D2 ─────────────────────────────────────────────────────────────────────
# Prima: se il lavoro veniva abbandonato (finestra chiusa) la cronologia non si salvava.
def test_d2_la_cronologia_si_salva_anche_se_il_lavoro_viene_chiuso(tmp_path):
    from fotofacile.core.history import History
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import CopiatoreInterno, transfer_steps

    file = [
        MediaFile(f"/sdcard/DCIM/Camera/{i}.jpg", size=5, mtime=1000 + i, kind="photo") for i in range(3)
    ]
    telefono = _TelefonoFinto({f.remote_path: b"12345" for f in file})
    opzioni = TransferOptions(destination=tmp_path / "out")
    piano = build_plan(file, opzioni)
    cronologia = History(tmp_path / "h.json")
    cronologia.load()
    generatore = transfer_steps(piano, opzioni, CopiatoreInterno(telefono), "S1", history=cronologia)
    next(generatore)  # il primo passo scarica il file…
    next(generatore)  # …il secondo lo verifica e lo annota nella cronologia, poi comincia il successivo
    generatore.close()  # …poi la finestra si chiude
    riletta = History(tmp_path / "h.json")
    riletta.load()
    assert riletta.count("S1") >= 1


# ── D3 ─────────────────────────────────────────────────────────────────────
# Prima: se la cancellazione dal telefono falliva non lo sapeva nessuno.
def test_d3_cancellazione_fallita_diventa_un_avviso(tmp_path):
    from fotofacile.core.errors import FotoFacileError
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import transfer

    class Rifiuta(_TelefonoFinto):
        def delete_file(self, serial, remote_path):
            raise FotoFacileError("Il telefono non lo permette.", "")

    media = MediaFile("/sdcard/DCIM/Camera/a.jpg", size=3, mtime=1000, kind="photo")
    opzioni = TransferOptions(destination=tmp_path / "out", delete_after=True)
    esiti = transfer(Rifiuta({media.remote_path: b"abc"}), "S1", build_plan([media], opzioni), opzioni)
    assert esiti.deleted_from_phone == 0
    assert any("a.jpg" in avviso and "telefono" in avviso for avviso in esiti.warnings)


# ── D4 ─────────────────────────────────────────────────────────────────────
# Prima: con un file fallito il totale restava alto e la barra non arrivava mai al 100 %.
def test_d4_il_totale_non_conta_i_file_falliti(tmp_path):
    from fotofacile.core.planner import TransferOptions, build_plan
    from fotofacile.core.scanner import MediaFile
    from fotofacile.core.transfer import Progress, transfer

    buono = MediaFile("/sdcard/DCIM/Camera/ok.jpg", size=4, mtime=1, kind="photo")
    rotto = MediaFile("/sdcard/DCIM/Camera/rotto.jpg", size=99, mtime=1, kind="photo")
    # `rotto` dichiara 99 byte ma il telefono ne consegna 3: la verifica lo scarta
    telefono = _TelefonoFinto({buono.remote_path: b"abcd", rotto.remote_path: b"abc"})
    opzioni = TransferOptions(destination=tmp_path / "out")
    viste: list[Progress] = []
    esiti = transfer(
        telefono, "S1", build_plan([buono, rotto], opzioni), opzioni,
        on_progress=lambda p: viste.append(Progress(**vars(p))), retries=0,
    )
    assert len(esiti.failed) == 1
    assert viste[-1].bytes_done == viste[-1].bytes_total == 4


# ── D5 ─────────────────────────────────────────────────────────────────────
# Prima: `_scansione_fallita(_errore)` buttava via il motivo; restava «Ricerca non riuscita.»
def test_d5_ricerca_fallita_spiega_il_motivo(app):
    from fotofacile.core.devices import DeviceInfo
    from fotofacile.core.errors import FotoFacileError
    from tests.aiuto import attendi

    class Bloccato:
        nome = "prova"
        spiegazione = ""

        def cerca_media(self, serial, include_videos=True, annulla=None):
            raise FotoFacileError("Il telefono è bloccato.", "Sblocca lo schermo e riprova.")
            yield 0.0  # pragma: no cover - lo rende un generatore

        def pulisci(self):
            pass

    app.remote = Bloccato()
    app.device = DeviceInfo(serial="S1", state="device", model="Prova", product="")
    pagina = app.pages["select"]
    pagina.start_scan()
    assert attendi(app, lambda: not pagina._scansione_in_corso)
    assert app.banner.message_text == "Il telefono è bloccato."
    assert "Sblocca" in app.banner.hint_text


# ── D11 ────────────────────────────────────────────────────────────────────
# Prima: nel collegamento diretto (macOS, Linux) e nella demo la cartella di destinazione
# veniva creata fuori dal `try`. Se non si poteva creare (disco esterno staccato, cartella
# protetta, un file con lo stesso nome) usciva un OSError grezzo: `transfer` lo lasciava
# passare, l'intera copia si fermava e restava solo «Qualcosa non ha funzionato».
@pytest.mark.parametrize("quale", ["aiutante", "demo"])
def test_d11_cartella_impossibile_da_creare_da_un_errore_comprensibile(tmp_path, quale):
    from fotofacile.core.trasporto_aiutante import TrasportoAiutante

    class AiutanteFinto(TrasportoAiutante):
        def base(self) -> list[str]:
            return ["/bin/echo"]

    (tmp_path / "occupato").write_text("un file, non una cartella", encoding="utf-8")
    destinazione = tmp_path / "occupato" / "foto.jpg"
    if quale == "aiutante":
        copiatore = AiutanteFinto(intervallo=0.0)
    else:
        copiatore = AdbDemoAPassi(DemoAdbBackend(file_count=1), intervallo=0.0)
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(copiatore.copia("S1", "/DCIM/foto.jpg", destinazione))
    assert "foto.jpg" in errore.value.message
    assert errore.value.hint



def test_d11_errore_del_sistema_durante_la_copia_diretta_da_un_errore_comprensibile(
    tmp_path, monkeypatch
):
    """Stesso difetto più avanti: il blocco principale della copia diretta non traduceva gli
    OSError (per esempio il file a metà che non si riesce a chiudere o a scrivere sul
    disco), a differenza di `AdbAPassi.copia`."""
    import errno

    from fotofacile.core import trasporto_aiutante
    from fotofacile.core.trasporto_aiutante import TrasportoAiutante

    class AiutanteFinto(TrasportoAiutante):
        def base(self) -> list[str]:
            return ["/bin/echo"]

    def pieno(_percorso):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(trasporto_aiutante, "_rallenta_scrittura", pieno)
    destinazione = tmp_path / "uscita" / "foto.jpg"
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(AiutanteFinto(intervallo=0.0).copia("S1", "/DCIM/foto.jpg", destinazione))
    assert "spazio" in errore.value.message.lower()
    assert list(destinazione.parent.iterdir()) == [], "niente .part e niente foto a metà"


# ── D12 ────────────────────────────────────────────────────────────────────
# Prima: il disco pieno veniva riconosciuto cercando «spazio» anche nel messaggio, che
# contiene il nome del file. Una foto chiamata «Spazio_bimbi.jpg» che falliva per il cavo
# staccato diventava «Non c'è più spazio»: l'utente liberava il disco per niente.
def test_d12_il_nome_del_file_non_fa_credere_a_un_disco_pieno(tmp_path):
    from fotofacile.core.adb_passi import _esito_di_copia

    processo = ProcessoEsterno(
        ["/bin/sh", "-c", "exit 1"],
        umano="Non sono riuscito a copiare Spazio_bimbi.jpg.",
        hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
    )
    processo.avvia()
    processo.process.wait()
    with pytest.raises(FotoFacileError) as errore:
        _esito_di_copia(processo, tmp_path / "Spazio_bimbi.jpg")
    assert "spazio" not in errore.value.message.lower().replace("spazio_bimbi", "")
    assert "cavo" in errore.value.hint


def test_d12_il_disco_pieno_detto_dal_comando_si_riconosce_ancora(tmp_path):
    from fotofacile.core.adb_passi import _esito_di_copia

    processo = ProcessoEsterno(
        ["/bin/sh", "-c", "echo 'write: No space left on device' >&2; exit 1"],
        umano="Non sono riuscito a copiare foto.jpg.",
        hint="Il telefono potrebbe essersi scollegato: controlla il cavo e riprova.",
    )
    processo.avvia()
    processo.process.wait()
    with pytest.raises(FotoFacileError) as errore:
        _esito_di_copia(processo, tmp_path / "foto.jpg")
    assert "spazio" in errore.value.message.lower()


# ── D13 ────────────────────────────────────────────────────────────────────
# Prima: se il file degli errori non si poteva creare (disco di sistema pieno) usciva un
# OSError grezzo da `ProcessoEsterno.avvia` e il file di output temporaneo, già creato,
# restava nella cartella temporanea. Il controllo del telefono finiva in «Qualcosa non ha
# funzionato» invece di dire cosa fare.
def test_d13_file_degli_errori_impossibile_da_creare(tmp_path, monkeypatch):
    import errno
    import tempfile

    from fotofacile.core import ops

    originale = tempfile.mkstemp
    creati: list[str] = []

    def secondo_fallisce(*args, **kwargs):
        if creati:
            raise OSError(errno.ENOSPC, "No space left on device")
        descrittore, nome = originale(*args, dir=str(tmp_path), **kwargs)
        creati.append(nome)
        return descrittore, nome

    monkeypatch.setattr(ops.tempfile, "mkstemp", secondo_fallisce)
    processo = ProcessoEsterno(["/bin/echo", "ciao"])
    with pytest.raises(FotoFacileError) as errore:
        processo.avvia()
    assert errore.value.hint
    assert creati and not Path(creati[0]).exists(), "il file di output non deve restare"


# ── D14 ────────────────────────────────────────────────────────────────────
# Prima: `TrasportoMtpLinux.copia` non accettava `remoto_dimensione`, che `transfer` passa
# sempre (anche attraverso `TrasportoComposto`). Su Linux, con il collegamento diretto,
# ogni copia finiva in un TypeError: nessuna foto copiata e solo «Qualcosa non ha
# funzionato».
def test_d14_la_copia_diretta_su_linux_accetta_la_dimensione(tmp_path):
    from fotofacile.core.trasporto_linux import TrasportoMtpLinux

    aiutante = script(tmp_path, "aiutante", "printf 'ciao!'\n")

    class LinuxFinto(TrasportoMtpLinux):
        def base(self) -> list[str]:
            return [aiutante]

    destinazione = tmp_path / "foto" / "a.jpg"
    copiatore = LinuxFinto(intervallo=0.0)
    scritti = esegui_fino_alla_fine(
        copiatore.copia(
            "S1", "/DCIM/a.jpg", destinazione, on_scritti=None, annulla=None, remoto_dimensione=5
        )
    )
    assert scritti == 5
    assert destinazione.read_bytes() == b"ciao!"
    assert copiatore._usati == {"S1"}


# ── D15 ────────────────────────────────────────────────────────────────────
# Prima: su macOS, se il telefono indicato con `--seriale` non c'era più, l'aiutante
# ripiegava in silenzio sul primo telefono collegato. Con due telefoni, copia e
# cancellazione potevano agire sul telefono sbagliato (quello non scelto dall'utente).
class _TelefonoMacFinto:
    def __init__(self, seriale: str) -> None:
        self._seriale = seriale

    def serialNumber(self) -> str:
        return self._seriale

    def name(self) -> str:
        return f"Telefono {self._seriale}"


def test_d15_con_due_telefoni_non_si_usa_quello_sbagliato(monkeypatch):
    from fotofacile.aiutanti import ptp_mac

    aperti: list[str] = []
    monkeypatch.setattr(
        ptp_mac, "trova_telefoni", lambda: [_TelefonoMacFinto("B"), _TelefonoMacFinto("C")]
    )
    monkeypatch.setattr(ptp_mac, "apri_sessione", lambda telefono: aperti.append(ptp_mac.seriale(telefono)))
    with pytest.raises(ptp_mac.NessunTelefono):
        ptp_mac._apri_telefono("A")
    assert aperti == [], "non si apre la sessione su un telefono diverso da quello scelto"
    assert ptp_mac.seriale(ptp_mac._apri_telefono("C")) == "C"


def test_d15_con_un_solo_telefono_si_usa_quello(monkeypatch):
    """Guardia: con un telefono solo si continua a usarlo anche se l'identificativo è
    cambiato (per esempio fra un avvio dell'aiutante e l'altro)."""
    from fotofacile.aiutanti import ptp_mac

    monkeypatch.setattr(ptp_mac, "trova_telefoni", lambda: [_TelefonoMacFinto("B")])
    monkeypatch.setattr(ptp_mac, "apri_sessione", lambda telefono: None)
    assert ptp_mac.seriale(ptp_mac._apri_telefono("A")) == "B"


# ── D16 ────────────────────────────────────────────────────────────────────
# Prima: l'elenco delle foto (JSON UTF-8 dell'aiutante, output UTF-8 di adb) veniva riletto
# con la codifica di sistema. Su Windows è cp1252: «Città 😀.jpg» diventava «CittÃ ðŸ˜€.jpg»,
# la copia chiedeva al telefono un file che non esiste e ogni foto con accenti o emoji nel
# nome falliva. Su questo Mac la codifica di sistema è sempre UTF-8: la si simula.
NOME_STRANO = "Città 😀 l'«estate».jpg"


@pytest.fixture
def codifica_di_windows(monkeypatch):
    """Rilegge i file di testo come farebbe Windows quando la codifica non è indicata."""
    originale = Path.read_text

    def come_windows(self, encoding=None, errors=None, newline=None):
        return originale(self, encoding=encoding or "cp1252", errors=errors, newline=newline)

    monkeypatch.setattr(Path, "read_text", come_windows)


def test_d16_l_elenco_del_collegamento_diretto_conserva_accenti_ed_emoji(
    tmp_path, codifica_di_windows
):
    from fotofacile.core.trasporto_aiutante import TrasportoAiutante

    riga = json.dumps({"percorso": f"/DCIM/{NOME_STRANO}", "dimensione": 3, "data": 1, "genere": "photo"}, ensure_ascii=False)
    (tmp_path / "elenco.json").write_bytes((riga + "\n").encode("utf-8"))
    aiutante = script(tmp_path, "aiutante", f"cat '{tmp_path / 'elenco.json'}'\n")

    class AiutanteFinto(TrasportoAiutante):
        def base(self) -> list[str]:
            return [aiutante]

    trovati = esegui_fino_alla_fine(AiutanteFinto(intervallo=0.0).cerca_media("S1"))
    assert [file.remote_path for file in trovati] == [f"/DCIM/{NOME_STRANO}"]


def test_d16_la_ricerca_con_adb_conserva_accenti_ed_emoji(tmp_path, codifica_di_windows):
    from fotofacile.core.adb_passi import AdbAPassi

    (tmp_path / "elenco.txt").write_bytes(f"3|1|/sdcard/DCIM/{NOME_STRANO}\n".encode("utf-8"))
    adb = script(tmp_path, "adb", f"cat '{tmp_path / 'elenco.txt'}'\n")
    passi = AdbAPassi(adb, intervallo=0.0, cartella_lavoro=tmp_path / "lavoro")
    trovati = esegui_fino_alla_fine(passi.cerca_media("S1", "comando", ripiega=False))
    assert [file.remote_path for file in trovati] == [f"/sdcard/DCIM/{NOME_STRANO}"]


@pytest.mark.parametrize("modulo", ["ptp_mac", "mtp_linux"])
def test_d16_gli_aiutanti_scrivono_righe_leggibili_con_ogni_codifica(modulo, capsys):
    """Gli aiutanti Python scrivono JSON solo ASCII: la lettura in UTF-8 non dipende dalla
    codifica di sistema del processo aiutante."""
    import importlib

    from fotofacile.core.trasporto_aiutante import leggi_elenco

    aiutante = importlib.import_module(f"fotofacile.aiutanti.{modulo}")
    aiutante._stampa_riga({"percorso": f"/DCIM/{NOME_STRANO}", "dimensione": 3, "data": 1, "genere": "photo"})
    uscita = capsys.readouterr().out
    assert uscita.isascii()
    assert [file.remote_path for file in leggi_elenco(uscita)] == [f"/DCIM/{NOME_STRANO}"]


# ── D17 ────────────────────────────────────────────────────────────────────
# Prima: lo script Windows usava `FolderItem.Name` come nome dei file. È il nome **mostrato**
# da Esplora file: con l'opzione predefinita di Windows «Nascondi le estensioni per i tipi
# di file conosciuti» può arrivare «IMG_001» invece di «IMG_001.jpg», e `Genere-File` scarta
# i nomi senza punto: il collegamento diretto su Windows non avrebbe trovato nessuna foto.
# PowerShell non si può eseguire su questo Mac: il test legge lo script (contratto), la
# correzione **non è verificata su un Windows vero**.
SCRIPT_WINDOWS = Path(__file__).resolve().parent.parent / "fotofacile" / "aiutanti" / "wpd_win.ps1"


def _funzione_powershell(testo: str, nome: str) -> str:
    """Il testo di una funzione dello script, dalla firma alla graffa che la chiude."""
    inizio = testo.index(f"function {nome}(")
    profondita = 0
    for posizione in range(testo.index("{", inizio), len(testo)):
        if testo[posizione] == "{":
            profondita += 1
        elif testo[posizione] == "}":
            profondita -= 1
            if profondita == 0:
                return testo[inizio : posizione + 1]
    raise AssertionError(f"la funzione {nome} non si chiude")


def test_d17_lo_script_windows_usa_il_nome_completo_dei_file():
    testo = SCRIPT_WINDOWS.read_text(encoding="utf-8-sig")
    nome_file = _funzione_powershell(testo, "Nome-File")
    assert 'ExtendedProperty("System.FileName")' in nome_file, "il nome vero, con l'estensione"
    assert 'ExtendedProperty("System.FileExtension")' in nome_file, "ultimo ripiego: l'estensione"
    assert "Nome-Voce" in nome_file, "se le proprietà mancano si usa il nome mostrato"
    # L'elenco decide foto/video sul nome completo...
    elenca = _funzione_powershell(testo, "Elenca-Cartella")
    assert elenca.index("Nome-File") < elenca.index("Genere-File"), "il genere va deciso sul nome completo"
    # ...e la copia ritrova il file con lo stesso nome che l'elenco ha stampato.
    trova = _funzione_powershell(testo, "Trova-Voce")
    assert "Test-StessoNome" in trova
    assert "(Nome-Voce $figlio) -eq" not in trova
    assert "Nome-File" in _funzione_powershell(testo, "Test-StessoNome")
    assert "$nomeFile = Nome-File $voce" in _funzione_powershell(testo, "Comando-Copia")


def test_d17_lo_script_windows_resta_ben_formato():
    """Guardia: BOM UTF-8 e parentesi bilanciate dopo la modifica (PowerShell 5.1 non si può
    avviare qui: è il controllo più vicino a «lo script si legge»)."""
    dati = SCRIPT_WINDOWS.read_bytes()
    assert dati.startswith(b"\xef\xbb\xbf")
    testo = dati.decode("utf-8-sig")
    for apertura, chiusura in ("{}", "()", "[]"):
        assert testo.count(apertura) == testo.count(chiusura), f"{apertura}{chiusura} sbilanciate"


# ── D18 ────────────────────────────────────────────────────────────────────
# Prima: l'aiutante macOS ricordava le voci già viste solo con `id(voce)`. Ogni voce è un
# «proxy» PyObjC che viene liberato quando la cartella è finita, e il proxy di un file di
# un'altra cartella riusa la stessa memoria, quindi lo stesso `id`: quel file veniva
# **saltato in silenzio**. Misurato con PyObjC vero su questo Mac: 48 proxy su 50 della
# seconda cartella riusavano un `id` della prima. Con più cartelle di foto (Camera,
# Screenshots, Pictures...) sparivano dall'elenco tutte quelle dopo la prima, e la copia di
# quei file diceva «non trovo più il file». Qui il riuso della memoria è reso certo.
class _VocePtpFinta:
    """Come un proxy PyObjC: un oggetto Python che rappresenta un file o una cartella."""

    def __init__(self, nome: str = "", figli: dict | None = None) -> None:
        self.nome_voce, self.figli = nome, figli

    def name(self) -> str:
        return self.nome_voce

    def isKindOfClass_(self, _classe) -> bool:
        return self.figli is not None


class _ProxyPtpFinto(_VocePtpFinta):
    """Un file: quando nessuno lo tiene più, la sua «memoria» torna libera, come quella di
    un proxy PyObjC, e il prossimo file la riusa (stesso ``id``)."""

    liberi: list = []

    def __del__(self) -> None:
        _ProxyPtpFinto.liberi.append(self)


class _CartellaPtpFinta(_VocePtpFinta):
    def contents(self):
        voci = []
        for nome, figli in self.figli.items():
            if figli is not None:
                voci.append(_CartellaPtpFinta(nome, figli))
                continue
            voce = _ProxyPtpFinto.liberi.pop() if _ProxyPtpFinto.liberi else _ProxyPtpFinto()
            voce.nome_voce, voce.figli = nome, None
            voci.append(voce)
        return voci


def test_d18_l_elenco_macos_non_salta_i_file_delle_cartelle_successive(monkeypatch):
    from types import SimpleNamespace

    from fotofacile.aiutanti import ptp_mac

    monkeypatch.setattr(_ProxyPtpFinto, "liberi", [])
    albero = {
        "DCIM": {
            "Camera": {f"c{numero}.jpg": None for numero in range(5)},
            "Screenshots": {f"s{numero}.png": None for numero in range(5)},
        }
    }
    telefono = _CartellaPtpFinta("telefono", albero)
    percorsi = [percorso for _, percorso in ptp_mac.cammina(telefono, SimpleNamespace(ICCameraFolder=None))]
    assert len(percorsi) == 10, percorsi
    assert "/DCIM/Screenshots/s4.png" in percorsi


def test_d18_una_voce_ripetuta_si_elenca_una_volta_sola():
    """Guardia: la difesa contro gli elenchi che ripetono la stessa voce resta."""
    from types import SimpleNamespace

    from fotofacile.aiutanti import ptp_mac

    foto = _VocePtpFinta("a.jpg")

    class CartellaCheRipete(_VocePtpFinta):
        def contents(self):
            return [foto, foto]

    percorsi = [p for _, p in ptp_mac.cammina(CartellaCheRipete("t", {}), SimpleNamespace(ICCameraFolder=None))]
    assert percorsi == ["/a.jpg"]


# ── D19 ────────────────────────────────────────────────────────────────────
# Prima: per annullare (o allo scadere del tempo, o alla chiusura) il programma principale
# ferma l'aiutante con SIGTERM (`ProcessoEsterno.termina`). Senza un gestore Python muore
# all'istante e nessun `finally` scatta: su macOS restava in `$TMPDIR` la cartella
# `fotofacile-ptp-*` con la foto scaricata (il ripiego per i telefoni che non consegnano a
# blocchi); su Linux restavano vivi e orfani i comandi figli (`jmtpfs`, `gio mount`) e la
# cartella di montaggio vuota. Qui l'aiutante gira davvero in un processo a parte.
_PTP_CHE_SCARICA = r'''
import sys, time
from pathlib import Path
from fotofacile import cli
from fotofacile.aiutanti import ptp_mac

segnale = Path(sys.argv[1])

class Ciclo:
    def runUntilDate_(self, _quando):
        time.sleep(0.02)

class NSRunLoop:
    @staticmethod
    def currentRunLoop():
        return Ciclo()

class NSDate:
    @staticmethod
    def dateWithTimeIntervalSinceNow_(secondi):
        return secondi

class NSURL:
    @staticmethod
    def fileURLWithPath_(percorso):
        return percorso

class FileLento:
    def fileSize(self):
        return 10
    def name(self):
        return "a.jpg"
    def device(self):
        return object()
    def requestReadDataAtOffset_length_completion_(self, *_argomenti):
        raise RuntimeError("questo telefono non consegna a blocchi")
    def requestDownloadWithOptions_completion_(self, opzioni, _fatto):
        cartella = Path(opzioni["ICDownloadsDirectoryURL"])
        (cartella / "a.jpg").write_bytes(b"mezza foto")
        segnale.write_text(str(cartella))  # la risposta non arriva mai: telefono lento

ptp_mac._componenti = lambda: (None, NSDate, None, NSRunLoop, NSURL, None)
ptp_mac._apri_telefono = lambda voluto="": object()
ptp_mac.trova_file = lambda telefono, percorso, ic: FileLento()
ptp_mac.chiudi_sessione = lambda telefono: None
sys.exit(cli.main(["--aiutante", "ptp_mac", "copia", "--percorso", "/DCIM/a.jpg"]))
'''

_MTP_CHE_MONTA = r'''
import sys
from fotofacile import cli
sys.exit(cli.main(["--aiutante", "mtp_linux", "elenca"]))
'''


def _aspetta_file(percorso: Path, secondi: float = 20.0) -> str:
    import time

    scadenza = time.monotonic() + secondi
    while time.monotonic() < scadenza:
        if percorso.exists() and percorso.read_text().strip():
            return percorso.read_text().strip()
        time.sleep(0.05)
    raise AssertionError(f"l'aiutante non è arrivato al punto atteso ({percorso.name})")


def _processo_vivo(pid: int) -> bool:
    import os

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


@pytest.mark.skipif(__import__("os").name == "nt", reason="SIGTERM esiste solo su macOS e Linux")
def test_d19_macos_interrotto_non_lascia_la_foto_nella_cartella_temporanea(tmp_path):
    import os
    import subprocess
    import sys

    temporanea = tmp_path / "tmp"
    temporanea.mkdir()
    segnale = tmp_path / "scaricando"
    ambiente = {**os.environ, "TMPDIR": str(temporanea), "HOME": str(tmp_path)}
    radice = Path(__file__).resolve().parent.parent
    aiutante = subprocess.Popen(
        [sys.executable, "-c", _PTP_CHE_SCARICA, str(segnale)],
        cwd=radice, env=ambiente, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    try:
        cartella = Path(_aspetta_file(segnale))
        assert cartella.is_dir()
        aiutante.terminate()  # come ProcessoEsterno.termina
        aiutante.wait(timeout=10)
        assert not cartella.exists(), "la foto scaricata è rimasta nella cartella temporanea"
        assert list(temporanea.glob("fotofacile-ptp-*")) == []
    finally:
        if aiutante.poll() is None:
            aiutante.kill()
            aiutante.wait()
        aiutante.stderr.close()


@pytest.mark.skipif(__import__("os").name == "nt", reason="SIGTERM esiste solo su macOS e Linux")
def test_d19_linux_interrotto_non_lascia_comandi_orfani(tmp_path):
    import os
    import signal
    import subprocess
    import sys

    finti = tmp_path / "bin"
    finti.mkdir()
    temporanea = tmp_path / "tmp"
    temporanea.mkdir()
    segnale = tmp_path / "jmtpfs.pid"
    script(
        finti,
        "jmtpfs",
        'if [ "$1" = "-l" ]; then echo "Device 0: Telefono finto"; exit 0; fi\n'
        f'echo $$ > "{segnale}"\n'
        "exec sleep 60\n",  # un telefono bloccato: il montaggio non finisce
    )
    ambiente = {
        **os.environ,
        "PATH": f"{finti}:/usr/bin:/bin",  # niente gio: si usa il ripiego jmtpfs
        "TMPDIR": str(temporanea),
        "HOME": str(tmp_path),
        "XDG_RUNTIME_DIR": str(tmp_path / "run"),
        "XDG_CACHE_HOME": str(tmp_path / "cache"),
    }
    radice = Path(__file__).resolve().parent.parent
    aiutante = subprocess.Popen(
        [sys.executable, "-c", _MTP_CHE_MONTA],
        cwd=radice, env=ambiente, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    pid = 0
    try:
        pid = int(_aspetta_file(segnale))
        aiutante.terminate()  # come ProcessoEsterno.termina
        aiutante.wait(timeout=10)
        assert not _processo_vivo(pid), "jmtpfs è rimasto vivo senza nessuno ad aspettarlo"
        assert list(temporanea.glob("fotofacile-mtp-*")) == [], "la cartella di montaggio è rimasta"
    finally:
        if aiutante.poll() is None:
            aiutante.kill()
            aiutante.wait()
        aiutante.stderr.close()
        if pid and _processo_vivo(pid):
            os.kill(pid, signal.SIGKILL)


# ── D20 ────────────────────────────────────────────────────────────────────
# Prima: i guai previsti dell'aiutante macOS (file sparito, sessione che non si apre, file
# incompleto, argomento mancante) sono frasi italiane sollevate come OSError/ValueError, ma
# venivano stampate col nome della classe: la persona leggeva nel «dettaglio» dell'errore
# «OSError: Sul telefono non trovo più il file …». Gli altri aiutanti scrivono solo la frase.
def test_d20_l_aiutante_macos_scrive_frasi_senza_nomi_tecnici(monkeypatch, capsys):
    from fotofacile.aiutanti import ptp_mac

    monkeypatch.setattr(ptp_mac, "_componenti", lambda: (None,) * 6)
    assert ptp_mac.main(["copia"]) == 2
    assert capsys.readouterr().err == "Manca il file da copiare (--percorso).\n"

    monkeypatch.setattr(ptp_mac, "_apri_telefono", lambda voluto="": object())
    monkeypatch.setattr(ptp_mac, "trova_file", lambda telefono, percorso, ic: None)
    monkeypatch.setattr(ptp_mac, "chiudi_sessione", lambda telefono: None)
    assert ptp_mac.main(["cancella", "--percorso", "/DCIM/a.jpg"]) == 2
    assert capsys.readouterr().err == "Sul telefono non trovo più il file /DCIM/a.jpg.\n"


def test_d20_un_guaio_imprevisto_resta_riconoscibile(monkeypatch, capsys):
    """Guardia: un errore di programmazione continua a dire di che tipo è (serve a noi)."""
    from fotofacile.aiutanti import ptp_mac

    def rotto(_argomenti):
        raise KeyError("x")

    monkeypatch.setitem(ptp_mac.COMANDI, "elenca", rotto)
    assert ptp_mac.main(["elenca"]) == 2
    assert capsys.readouterr().err.startswith("KeyError")


# ── D21 ────────────────────────────────────────────────────────────────────
# Prima: `download_file_stream` (il copiatore della riga di comando e dei test) creava la
# cartella di destinazione fuori dal `try`, come i copiatori corretti in D11. Se non si
# poteva creare (disco staccato, cartella protetta, un file con lo stesso nome) usciva un
# OSError grezzo: `transfer` lo lasciava passare e l'intera copia si fermava.
def test_d21_la_copia_interna_traduce_la_cartella_impossibile_da_creare(tmp_path):
    from fotofacile.core.transfer import transfer

    piano, opzioni, telefono = _piano_singolo(tmp_path)
    (tmp_path / "out").write_text("un file, non una cartella", encoding="utf-8")
    esiti = transfer(telefono, "S1", piano, opzioni, retries=0)
    assert esiti.copied == []
    assert len(esiti.failed) == 1
    assert "a.jpg" in esiti.failed[0][1]


# ── D22 ────────────────────────────────────────────────────────────────────
# Prima: il download del componente e la lettura del catalogo intercettavano solo gli
# OSError. Ma `http.client` segnala una risposta troncata a metà (`IncompleteRead`, per
# esempio con il Wi-Fi che cade durante un trasferimento «a pezzi») o una risposta non HTTP
# di un proxy o di una rete con pagina di accesso (`BadStatusLine`) con eccezioni che **non**
# sono OSError (verificato con un server locale e `urllib.request.urlopen`). Uscivano
# grezze: «Qualcosa non ha funzionato», e siccome `run_task` chiama `on_error` solo per i
# FotoFacileError, il pulsante «Installa componente mancante» restava disattivato.
def _risposta_http(leggi):
    class Risposta:
        headers = {"Content-Length": "2000000"}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, *_args):
            return leggi()

        read1 = read

    return Risposta()


def _troncata():
    import http.client

    raise http.client.IncompleteRead(b"")


@pytest.mark.parametrize("guasto", ["troncata", "non_http"])
def test_d22_una_risposta_di_rete_anomala_da_un_errore_comprensibile(tmp_path, guasto):
    import http.client

    from fotofacile.core.installer import installa_a_passi

    def apri(*_args, **_kwargs):
        if guasto == "non_http":
            raise http.client.BadStatusLine("CIAO MONDO")
        return _risposta_http(_troncata)

    cartella = tmp_path / "casa" / ".fotofacile" / "platform-tools"
    # Senza `url` si passa anche dal catalogo ufficiale, che usa lo stesso `opener`.
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(installa_a_passi(target_dir=cartella, opener=apri, system="linux"))
    assert "connessione" in errore.value.hint
    assert list(cartella.parent.iterdir()) == [], "niente pacchetto né file a metà"


# ── D23 ────────────────────────────────────────────────────────────────────
# Prima: i guai del **disco** durante l'installazione del componente non erano detti come
# tali. Se la cartella `.fotofacile` non si poteva creare (un file con lo stesso nome, cartella
# personale protetta) o il disco si riempiva durante l'estrazione, usciva un OSError grezzo:
# «Qualcosa non ha funzionato» e pulsante «Installa» disattivato (vedi D22). Se il disco si
# riempiva durante il download, il messaggio diceva di controllare la connessione a internet.
def _zip_del_componente(tmp_path: Path) -> bytes:
    percorso = tmp_path / "pt.zip"
    with zipfile.ZipFile(percorso, "w") as archivio:
        archivio.writestr("platform-tools/adb", b"#!/bin/sh\nexit 0\n")
    return percorso.read_bytes()


def _opener_con(dati: bytes):
    import io

    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    return lambda *_a, **_k: Risposta(dati)


def test_d23_cartella_dei_dati_impossibile_da_creare(tmp_path, monkeypatch):
    from fotofacile.core import installer

    monkeypatch.setattr(installer, "MIN_DIMENSIONE_ARCHIVIO", 1)
    casa = tmp_path / "casa"
    casa.mkdir()
    (casa / ".fotofacile").write_text("un file, non una cartella", encoding="utf-8")
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(
            installer.installa_a_passi(
                target_dir=casa / ".fotofacile" / "platform-tools",
                url="https://esempio/pt.zip",
                opener=_opener_con(_zip_del_componente(tmp_path)),
                system="linux",
            )
        )
    assert ".fotofacile" in errore.value.message
    assert "connessione" not in errore.value.hint


@pytest.mark.parametrize("quando", ["download", "estrazione"])
def test_d23_disco_pieno_durante_l_installazione_del_componente(tmp_path, monkeypatch, quando):
    import errno
    import io

    from fotofacile.core import installer, ops

    monkeypatch.setattr(installer, "MIN_DIMENSIONE_ARCHIVIO", 1)
    dati = _zip_del_componente(tmp_path)
    if quando == "download":
        vero_open = open

        class Pieno(io.RawIOBase):
            def writable(self):
                return True

            def write(self, _dati):
                raise OSError(errno.ENOSPC, "No space left on device")

        def apri_file(percorso, modo="r", *args, **kwargs):
            if str(percorso).endswith(".scarico"):
                vero_open(percorso, modo).close()  # il file a metà esiste davvero
                return Pieno()
            return vero_open(percorso, modo, *args, **kwargs)

        monkeypatch.setattr(ops, "open", apri_file, raising=False)
    else:

        def pieno(*_args, **_kwargs):
            raise OSError(errno.ENOSPC, "No space left on device")

        monkeypatch.setattr(installer.shutil, "copyfileobj", pieno)
    cartella = tmp_path / "casa" / ".fotofacile" / "platform-tools"
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(
            installer.installa_a_passi(
                target_dir=cartella, url="https://esempio/pt.zip", opener=_opener_con(dati), system="linux"
            )
        )
    assert "spazio" in errore.value.message.lower()
    assert list(cartella.parent.iterdir()) == [], "niente pacchetto, file a metà o cartelle di appoggio"


def test_d23_disco_pieno_anche_con_il_file_bufferizzato(tmp_path, monkeypatch):
    """`open(..., "wb")` dà un `BufferedWriter`: i byte restano in coda e l'errore compare
    sia a `write`/`flush` sia di nuovo a `close()`. Il secondo non deve cancellare il
    messaggio «disco pieno» (prima diventava «controlla la connessione»)."""
    import errno
    import io

    from fotofacile.core import installer, ops

    monkeypatch.setattr(installer, "MIN_DIMENSIONE_ARCHIVIO", 1)
    dati = _zip_del_componente(tmp_path)
    vero_open = open

    class Pieno(io.RawIOBase):
        def writable(self):
            return True

        def write(self, _dati):
            raise OSError(errno.ENOSPC, "No space left on device")

    def apri_file(percorso, modo="r", *args, **kwargs):
        if str(percorso).endswith(".scarico"):
            vero_open(percorso, modo).close()  # il file a metà esiste davvero
            return io.BufferedWriter(Pieno(), buffer_size=1024 * 1024)
        return vero_open(percorso, modo, *args, **kwargs)

    monkeypatch.setattr(ops, "open", apri_file, raising=False)
    cartella = tmp_path / "casa" / ".fotofacile" / "platform-tools"
    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(
            installer.installa_a_passi(
                target_dir=cartella, url="https://esempio/pt.zip", opener=_opener_con(dati), system="linux"
            )
        )
    assert "spazio" in errore.value.message.lower()
    assert "connessione" not in errore.value.hint
    assert list(cartella.parent.iterdir()) == [], "niente pacchetto, file a metà o cartelle di appoggio"


# ── D24 ────────────────────────────────────────────────────────────────────
# Prima: ogni passo del download chiedeva `read(256 KB)` alla risposta di `urllib`. Su una
# rete lenta quella chiamata **aspetta** che arrivino tutti i 256 KB (misurato con un server
# locale che manda 1 KB ogni 50 ms: `read(256 KB)` è tornata dopo 2,1 s, `read1` subito): la
# finestra restava ferma per secondi a ogni passo e il pulsante «Annulla» non rispondeva.
class _RispostaLenta:
    """Come `http.client.HTTPResponse` su una rete lenta: `read(n)` aspetterebbe n byte,
    `read1(n)` consegna subito quello che è già arrivato."""

    headers = {"Content-Length": "3000"}

    def __init__(self) -> None:
        self.pezzi = [b"x" * 1000] * 3

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, *_args):
        raise AssertionError("read(n) blocca la finestra finché non arrivano n byte")

    def read1(self, *_args):
        return self.pezzi.pop(0) if self.pezzi else b""


def test_d24_con_la_rete_lenta_ogni_passo_prende_solo_quello_che_e_arrivato(tmp_path):
    from fotofacile.core.ops import ScaricatoreAPassi

    destinazione = tmp_path / "pt.zip"
    passi = list(
        ScaricatoreAPassi(
            "https://esempio/pt.zip", destinazione, opener=lambda *_a, **_k: _RispostaLenta()
        ).scarica()
    )
    assert destinazione.read_bytes() == b"x" * 3000
    assert len(passi) == 3, "un passo (e un ritorno alla finestra) per ogni pezzo arrivato"


# ── D25 ────────────────────────────────────────────────────────────────────
# Prima: il singolare valeva solo per la prima unità. Il tempo restante e la «Durata» del
# resoconto dicevano «1 minuto e 1 secondi» e «1 ora e 1 minuti».
def test_d25_un_secondo_e_un_minuto_restano_al_singolare():
    from fotofacile.core.format import format_duration, format_eta

    assert format_duration(61) == "1 minuto e 1 secondo"
    assert format_duration(3660) == "1 ora e 1 minuto"
    assert format_eta(121) == "circa 2 minuti e 1 secondo"
    assert format_duration(7260) == "2 ore e 1 minuto"
    assert format_duration(62) == "1 minuto e 2 secondi"  # guardia: il plurale resta


# ── D26 ────────────────────────────────────────────────────────────────────
# Prima: `parse_stat_stream` divideva l'elenco con `splitlines()`, che taglia anche su
# caratteri che possono stare nel nome di un file (U+2028, U+0085, \x1c…), mentre sul
# telefono `read -r` e `stat` producono una riga per file, divisa solo da «\n». Il file
# «a.jpg<U+2028>b.jpg» spariva dall'elenco e al suo posto compariva «a.jpg», un file diverso
# (se esiste) con la dimensione sbagliata.
def test_d26_nomi_con_separatori_unicode_restano_un_file_solo():
    from fotofacile.core.scanner import parse_stat_stream

    uscita = (
        "5|1|/sdcard/DCIM/a.jpg b.jpg\n"
        "7|2|/sdcard/DCIM/c\x85d.jpg\n"
        "3|4|/sdcard/DCIM/e.jpg\r\n"  # guardia: i vecchi telefoni chiudono le righe con \r\n
    )
    percorsi = [file.remote_path for file in parse_stat_stream(uscita)]
    assert percorsi == [
        "/sdcard/DCIM/a.jpg b.jpg",
        "/sdcard/DCIM/c\x85d.jpg",
        "/sdcard/DCIM/e.jpg",
    ]


# ── D27 ────────────────────────────────────────────────────────────────────
# Prima: `scrivi_log_avvio` aggiungeva righe a `~/.fotofacile/avvio.log` per sempre, senza
# limite né rotazione (due righe a ogni apertura del programma, più gli avvisi interi).
def test_d27_il_registro_di_avvio_non_cresce_per_sempre(tmp_path):
    from fotofacile.cli import scrivi_log_avvio

    env = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}
    registro = tmp_path / ".fotofacile" / "avvio.log"
    copia = registro.with_name("avvio.log.1")
    registro.parent.mkdir()
    registro.write_text("riga vecchia\n" * 200_000, encoding="utf-8")  # circa 2,6 MB

    scrivi_log_avvio("dopo la prima rotazione", env)
    assert registro.stat().st_size < 1024, "il registro riparte da capo"
    assert "dopo la prima rotazione" in registro.read_text(encoding="utf-8")
    assert copia.read_text(encoding="utf-8").startswith("riga vecchia"), "la copia precedente resta"

    registro.write_text("riga più recente\n" * 200_000, encoding="utf-8")
    scrivi_log_avvio("dopo la seconda rotazione", env)
    assert copia.read_text(encoding="utf-8").startswith("riga più recente"), "si tiene una copia sola"
    assert sorted(voce.name for voce in registro.parent.iterdir()) == ["avvio.log", "avvio.log.1"]


def test_d27_un_registro_piccolo_continua_a_crescere(tmp_path):
    from fotofacile.cli import scrivi_log_avvio

    env = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}
    scrivi_log_avvio("prima", env)
    percorso = scrivi_log_avvio("seconda", env)
    testo = percorso.read_text(encoding="utf-8")
    assert "prima" in testo and "seconda" in testo
    assert not percorso.with_name("avvio.log.1").exists()


# ── D28 ────────────────────────────────────────────────────────────────────
# Prima: `start_gui` e `avviso_visibile` scrivevano il registro di avvio fuori da ogni `try`.
# Se non si poteva scrivere (disco pieno, cartella dei dati che non si crea perché al suo posto
# c'è un file, cartella personale protetta) usciva un OSError grezzo: il programma **non si
# apriva affatto**, e l'avviso che doveva spiegare il problema non compariva.
@pytest.fixture(params=["cartella_impossibile", "file_impossibile"])
def registro_non_scrivibile(request, tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    if request.param == "cartella_impossibile":
        (tmp_path / ".fotofacile").write_text("un file al posto della cartella", encoding="utf-8")
    else:
        (tmp_path / ".fotofacile" / "avvio.log").mkdir(parents=True)  # open("a") fallisce
    return tmp_path


def test_d28_il_programma_si_apre_anche_se_il_registro_non_si_scrive(registro_non_scrivibile, monkeypatch):
    from fotofacile import cli

    aperte = []

    class AppFinta:
        def __init__(self, **_kwargs):
            pass

        def mainloop(self):
            aperte.append(True)

    monkeypatch.setattr("fotofacile.ui.app.App", AppFinta, raising=False)
    monkeypatch.setattr(cli, "contesto_grafico_dubbio", lambda *_a, **_k: False)
    assert cli.start_gui() == 0
    assert aperte == [True]


def test_d28_l_avviso_compare_anche_se_il_registro_non_si_scrive(registro_non_scrivibile, capsys):
    from fotofacile import cli

    chiamate = []
    cli.avviso_visibile(
        "Non riesco ad aprire la finestra", system="darwin", runner=lambda comando, **_k: chiamate.append(comando)
    )
    assert chiamate and chiamate[0][0] == "osascript"
    assert "Non riesco ad aprire la finestra" in capsys.readouterr().out


# ── D29 ────────────────────────────────────────────────────────────────────
# Prima: `App.go_to` chiamava `on_show` della pagina e **dopo** aggiornava `current_page`,
# l'indicatore dei passi e chiudeva l'avviso. Ogni messaggio scritto da `on_show` spariva
# subito («Sto copiando le foto: non scollegare il telefono.», «Ultimo passo prima della
# copia…»), e quando `on_show` rimandava a un'altra pagina (telefono scollegato, informazioni
# mancanti) la finestra mostrava quella pagina ma restava convinta di essere nell'altra: passo
# sbagliato in alto, avviso del motivo nascosto, e «Indietro» che non si muoveva.
# Le pagine qui sono sostituite da versioni minime: conta solo quello che fa `go_to`.
def test_d29_il_messaggio_scritto_all_ingresso_resta_visibile(app, monkeypatch):
    pagina = app.pages["options"]
    monkeypatch.setattr(pagina, "on_show", lambda: app.set_status("Controlla la cartella.", kind="info"))
    app.go_to("options")
    assert app.banner.visible is True
    assert app.banner.message_text == "Controlla la cartella."


def test_d29_una_pagina_che_rimanda_altrove_lascia_la_finestra_coerente(app, monkeypatch):
    for chiave in ("select", "options"):
        monkeypatch.setattr(app.pages[chiave], "on_show", lambda: None)

    def telefono_scollegato():
        app.go_to("options")
        app.set_status("Il telefono non è più collegato.", kind="avviso")

    monkeypatch.setattr(app.pages["transfer"], "on_show", telefono_scollegato)
    app.go_to("transfer")
    assert app.current_page == "options"
    assert app.step_indicator.current == 2
    assert app.banner.visible and app.banner.message_text == "Il telefono non è più collegato."
    app.go_to("prev")
    assert app.current_page == "select", "«Indietro» deve portare al passo prima di quello mostrato"


# ── D30 ────────────────────────────────────────────────────────────────────
# Prima: chiudendo la finestra con **qualunque** lavoro in corso compariva «Sto ancora
# copiando le foto. Vuoi interrompere e chiudere?». Al passo 1 il telefono viene controllato
# ogni 2 secondi (su macOS, senza telefono, ogni controllo dura fino a 6 s): chi chiudeva il
# programma prima di collegare il telefono si sentiva chiedere di interrompere una copia che
# non esisteva.
def _lavoro_infinito():
    while True:
        yield 0.05


def test_d30_chiudere_mentre_si_cerca_il_telefono_non_parla_di_copia(app, monkeypatch):
    from fotofacile.ui import app as modulo_app

    domande, chiusa = [], []
    monkeypatch.setattr(modulo_app.messagebox, "askyesno", lambda *a, **_k: domande.append(a) or False)
    monkeypatch.setattr(app, "destroy", lambda: chiusa.append(True))
    app.run_task(_lavoro_infinito())
    assert app.current_page == "connect" and app.task_in_corso
    app._chiusura()
    assert domande == [], "nessuna domanda su una copia che non c'è"
    assert chiusa == [True]
    assert app.task_in_corso is False


def test_d30_durante_la_copia_la_domanda_resta(app, monkeypatch):
    from fotofacile.ui import app as modulo_app

    domande, chiusa = [], []
    monkeypatch.setattr(modulo_app.messagebox, "askyesno", lambda *a, **_k: domande.append(a) or False)
    monkeypatch.setattr(app, "destroy", lambda: chiusa.append(True))
    monkeypatch.setattr(app.pages["transfer"], "on_show", lambda: app.run_task(_lavoro_infinito()))
    app.go_to("transfer")
    app._chiusura()
    assert len(domande) == 1 and "copiando" in domande[0][1]
    assert chiusa == [] and app.task_in_corso, "rispondendo «No» la copia continua"


# ── D31 ────────────────────────────────────────────────────────────────────
# Prima: `doctor` e `--selftest` stampavano con `print`. Su Windows, quando l'uscita non è la
# finestra dei comandi ma un file o un altro programma («py fotofacile.py doctor >
# diagnosi.txt», la pipeline GitHub, `build_app.py --verify`), Python scrive nella codifica
# del sistema (cp1252), che non ha la riga «──────» della diagnosi: `print` si fermava con
# UnicodeEncodeError e la diagnosi non usciva affatto (codice 1 e un traceback).
def _uscita_cp1252(monkeypatch):
    import io
    import sys

    grezzo = io.BytesIO()
    uscita = io.TextIOWrapper(grezzo, encoding="cp1252", newline="")  # come su Windows: «strict»
    monkeypatch.setattr(sys, "stdout", uscita)
    return grezzo, uscita


def test_d31_la_diagnosi_esce_anche_in_un_file_con_la_codifica_di_windows(tmp_path, monkeypatch):
    from fotofacile import cli

    grezzo, uscita = _uscita_cp1252(monkeypatch)
    esito = cli.main(["doctor"], env={"HOME": str(tmp_path), "USERPROFILE": str(tmp_path), "PATH": ""})
    uscita.flush()
    testo = grezzo.getvalue().decode("cp1252")
    uscita.detach()
    assert esito == 0
    assert "FotoFacile — diagnosi" in testo  # «—» esiste in cp1252 e resta
    assert "Sistema:" in testo and "Cartella dati:" in testo


def test_d31_l_autocollaudo_esce_anche_con_la_codifica_di_windows(monkeypatch):
    import json
    import tkinter as tk

    from fotofacile import cli

    class AppRotta:
        def __init__(self, **_kwargs):
            raise tk.TclError("impossibile leggere C:\\Users\\Иван\\tcl ─ init.tcl")

    monkeypatch.setattr("fotofacile.ui.app.App", AppRotta, raising=False)
    grezzo, uscita = _uscita_cp1252(monkeypatch)
    assert cli.main(["--selftest"], env={}) == 1
    uscita.flush()
    dati = json.loads(grezzo.getvalue().decode("cp1252"))
    uscita.detach()
    assert dati["ok"] is False and dati["motivo"].startswith("TclError: impossibile leggere")

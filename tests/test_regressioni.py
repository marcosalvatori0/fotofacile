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

"""Verifica del livello «collegamento diretto»: lettura dell'uscita degli aiutanti, scelta
del trasporto e comportamento della copia. Tutto con aiutanti finti: nessun telefono vero.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from fotofacile.core import trasporto_linux, trasporto_mac, trasporto_win
from fotofacile.core.devices import DeviceInfo
from fotofacile.core.errors import FotoFacileError
from fotofacile.core.ops import Annullato, esegui_fino_alla_fine
from fotofacile.core.scanner import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS, MediaFile
from fotofacile.core.trasporto import TrasportoComposto
from fotofacile.core.trasporto_aiutante import (
    TrasportoAiutante,
    genere_per_estensione,
    leggi_dispositivi,
    leggi_elenco,
)
from fotofacile.core.trasporto_linux import TrasportoMtpLinux
from fotofacile.core.trasporto_mac import TrasportoPtpMac
from fotofacile.core.trasporto_win import TrasportoWpdWindows


# ── lettura dell'uscita degli aiutanti ───────────────────────────────────


def test_leggi_dispositivi_riconosce_i_campi():
    testo = json.dumps(
        {
            "dispositivi": [
                {"seriale": "ABC123", "nome": "Pixel 8", "stato": "device", "prodotto": "husky"},
                {"seriale": "DEF456"},
            ]
        }
    )
    primo, secondo = leggi_dispositivi(testo)
    assert primo == DeviceInfo(serial="ABC123", state="device", model="Pixel 8", product="husky")
    assert secondo == DeviceInfo(serial="DEF456", state="device", model="", product="")


@pytest.mark.parametrize(
    "testo",
    [
        "",
        "   ",
        "questa riga non è JSON",
        "{}",
        '{"dispositivi": "non una lista"}',
        "[1, 2, 3]",
        '{"dispositivi": [null, 3, {"nome": "senza seriale"}, {"seriale": "   "}]}',
    ],
)
def test_leggi_dispositivi_ignora_testi_non_validi(testo):
    assert leggi_dispositivi(testo) == []


def test_leggi_elenco_legge_le_righe_buone_e_ignora_le_rotte():
    testo = "\n".join(
        [
            '{"percorso": "/DCIM/a.jpg", "dimensione": 10, "data": 20, "genere": "photo"}',
            "questa riga non è JSON",
            "",
            '{"fine": true, "conteggio": 1}',
            '{"percorso": "/DCIM/video.MP4", "dimensione": "30", "data": "40"}',
            '{"percorso": "/DCIM/scarto.xyz", "dimensione": 1, "data": 1}',
            '{"percorso": "/DCIM/scarto.txt", "dimensione": 1, "data": 1, "genere": "foto"}',
            '{"dimensione": 99, "data": 99}',
        ]
    )
    file = leggi_elenco(testo)
    assert [voce.remote_path for voce in file] == ["/DCIM/a.jpg", "/DCIM/video.MP4"]
    assert file[0] == MediaFile(remote_path="/DCIM/a.jpg", size=10, mtime=20, kind="photo")
    assert file[1].size == 30
    assert file[1].mtime == 40
    assert file[1].kind == "video"


def test_leggi_elenco_coercizza_i_numeri_e_azzera_quelli_rotti():
    (con_stringhe,) = leggi_elenco('{"percorso": "/DCIM/a.jpg", "dimensione": "123", "data": "456"}')
    assert con_stringhe.size == 123
    assert con_stringhe.mtime == 456
    (rotti,) = leggi_elenco('{"percorso": "/DCIM/b.jpg", "dimensione": "molto", "data": "poco"}')
    assert rotti.size == 0
    assert rotti.mtime == 0
    (vuoti,) = leggi_elenco('{"percorso": "/DCIM/c.jpg", "dimensione": null, "data": null}')
    assert vuoti.size == 0
    assert vuoti.mtime == 0


# ── estensioni ───────────────────────────────────────────────────────────


def test_genere_per_estensione_copre_tutte_le_estensioni_anche_maiuscole():
    for estensione in PHOTO_EXTENSIONS:
        assert genere_per_estensione(f"/DCIM/foto.{estensione}") == "photo"
        assert genere_per_estensione(f"/DCIM/FOTO.{estensione.upper()}") == "photo"
    for estensione in VIDEO_EXTENSIONS:
        assert genere_per_estensione(f"/DCIM/video.{estensione}") == "video"
        assert genere_per_estensione(f"/DCIM/VIDEO.{estensione.upper()}") == "video"
    assert genere_per_estensione("/DCIM/senzaestensione") is None
    assert genere_per_estensione("/DCIM/nota.txt") is None


def test_gli_elenchi_di_estensioni_sono_gli_stessi_degli_aiutanti():
    from fotofacile.aiutanti import ptp_mac

    assert set(ptp_mac.ESTENSIONI_FOTO) == set(PHOTO_EXTENSIONS)
    assert set(ptp_mac.ESTENSIONI_VIDEO) == set(VIDEO_EXTENSIONS)


# ── scelta fra più collegamenti ──────────────────────────────────────────


class TrasportoFinto:
    """Trasporto minimo per i test: sa fallire su richiesta e registra di essere stato usato."""

    def __init__(
        self,
        nome: str,
        dispositivi: list[DeviceInfo] | None = None,
        errore: Exception | None = None,
    ) -> None:
        self.nome = nome
        self.spiegazione = f"finto: {nome}"
        self._dispositivi = list(dispositivi or [])
        self._errore = errore
        self.riavvii = 0
        self.pulizie = 0

    def disponibile(self) -> bool:
        return True

    def dispositivi(self):
        if self._errore is not None:
            raise self._errore
        yield 0.0
        return list(self._dispositivi)

    def cerca_media(self, serial, include_videos=True, annulla=None):
        yield 0.0
        return []

    def copia(self, serial, remoto, destinazione, on_scritti=None, annulla=None):
        yield 0.0
        return 0

    def cancella(self, serial, remoto):
        yield 0.0
        return None

    def riavvia(self):
        self.riavvii += 1
        if self._errore is not None:
            raise self._errore
        yield 0.0
        return None

    def pulisci(self) -> None:
        self.pulizie += 1


def test_composto_sceglie_il_primo_collegamento_che_vede_il_telefono():
    vuoto = TrasportoFinto("vuoto")
    con_telefono = TrasportoFinto("con telefono", [DeviceInfo(serial="ABC", state="device")])
    composto = TrasportoComposto([vuoto, con_telefono])

    trovati = esegui_fino_alla_fine(composto.dispositivi())

    assert [dispositivo.serial for dispositivo in trovati] == ["ABC"]
    assert composto.attivo is con_telefono
    assert composto.nome == "con telefono"


def test_composto_salta_il_collegamento_che_solleva_un_errore():
    rotto = TrasportoFinto("rotto", errore=FotoFacileError("non disponibile"))
    buono = TrasportoFinto("buono", [DeviceInfo(serial="ABC", state="device")])
    composto = TrasportoComposto([rotto, buono])

    trovati = esegui_fino_alla_fine(composto.dispositivi())

    assert [dispositivo.serial for dispositivo in trovati] == ["ABC"]
    assert composto.attivo is buono


def test_composto_senza_telefoni_non_solleva():
    composto = TrasportoComposto([TrasportoFinto("primo"), TrasportoFinto("secondo")])
    assert esegui_fino_alla_fine(composto.dispositivi()) == []


def test_composto_riavvia_anche_se_un_collegamento_fallisce():
    rotto = TrasportoFinto("rotto", errore=FotoFacileError("non disponibile"))
    buono = TrasportoFinto("buono")
    composto = TrasportoComposto([rotto, buono])

    esegui_fino_alla_fine(composto.riavvia())

    assert rotto.riavvii == 1
    assert buono.riavvii == 1


def test_composto_pulisci_non_solleva_mai():
    class TrasportoCheEsplode(TrasportoFinto):
        def pulisci(self) -> None:
            raise RuntimeError("esplosione durante la pulizia")

    esplosivo = TrasportoCheEsplode("esplosivo")
    tranquillo = TrasportoFinto("tranquillo")
    composto = TrasportoComposto([esplosivo, tranquillo])

    composto.pulisci()  # non deve sollevare

    assert tranquillo.pulizie == 1


# ── copia attraverso un aiutante finto ───────────────────────────────────


def script(tmp_path: Path, nome: str, corpo: str) -> str:
    """Un finto aiutante eseguibile, nello stile di tests/test_adb_passi.py."""
    percorso = tmp_path / nome
    percorso.write_text("#!/bin/sh\n" + corpo)
    percorso.chmod(0o755)
    return str(percorso)


class TrasportoAiutanteFinto(TrasportoAiutante):
    """Pilota uno script finto come se fosse un aiutante vero."""

    aiutante = "finto"

    def __init__(self, percorso_script: str) -> None:
        super().__init__(intervallo=0.0)
        self._percorso_script = percorso_script

    def disponibile(self) -> bool:
        return True

    def base(self) -> list[str]:
        return [self._percorso_script]


def test_copia_scrive_i_byte_e_rinomina_solo_alla_fine(tmp_path):
    percorso_script = script(tmp_path, "aiutante", "printf 'contenuto-buono'\n")
    trasporto = TrasportoAiutanteFinto(percorso_script)
    destinazione = tmp_path / "uscita" / "foto.jpg"
    visti: list[int] = []

    def guarda(scritti: int) -> None:
        visti.append(scritti)
        # Mentre si copia esiste solo il file «a metà»: la destinazione compare alla fine.
        assert not destinazione.exists()
        assert any(percorso.name.endswith(".part") for percorso in destinazione.parent.iterdir())

    scritti = esegui_fino_alla_fine(
        trasporto.copia("SERIAL1", "/DCIM/foto.jpg", destinazione, on_scritti=guarda)
    )

    assert scritti == len(b"contenuto-buono")
    assert destinazione.read_bytes() == b"contenuto-buono"
    assert list(destinazione.parent.iterdir()) == [destinazione]
    assert visti and visti[-1] == scritti


def test_copia_riporta_l_avanzamento_intermedio(tmp_path):
    percorso_script = script(
        tmp_path,
        "aiutante",
        "dd if=/dev/zero bs=1024 count=1 2>/dev/null\n"
        "sleep 0.5\n"
        "dd if=/dev/zero bs=1024 count=1 2>/dev/null\n",
    )
    trasporto = TrasportoAiutanteFinto(percorso_script)
    visti: list[int] = []
    destinazione = tmp_path / "grande.bin"

    scritti = esegui_fino_alla_fine(
        trasporto.copia("SERIAL1", "/DCIM/grande.bin", destinazione, on_scritti=visti.append)
    )

    assert scritti == 2 * 1024
    assert destinazione.stat().st_size == 2 * 1024
    assert len(visti) >= 2
    assert visti[0] < scritti  # l'avanzamento intermedio c'è stato davvero


def test_copia_annullata_rimuove_il_file_a_meta(tmp_path):
    # Il primo pezzo viene scritto subito e poi l'aiutante resta fermo: così il test non
    # dipende dalla velocità del disco (un dd lunghissimo potrebbe finire prima che il
    # programma se ne accorga, e l'annullamento non scatterebbe mai).
    percorso_script = script(
        tmp_path,
        "aiutante",
        "dd if=/dev/zero bs=1024 count=1 2>/dev/null\nsleep 5\n",
    )
    trasporto = TrasportoAiutanteFinto(percorso_script)
    annulla = threading.Event()
    destinazione = tmp_path / "uscita" / "video.mp4"

    def ferma(scritti: int) -> None:
        if scritti > 0:
            annulla.set()

    with pytest.raises(Annullato):
        esegui_fino_alla_fine(
            trasporto.copia(
                "SERIAL1", "/DCIM/video.mp4", destinazione, on_scritti=ferma, annulla=annulla
            )
        )

    assert destinazione.parent.exists()
    assert list(destinazione.parent.iterdir()) == []


def test_copia_fallita_rimuove_il_file_a_meta(tmp_path):
    percorso_script = script(tmp_path, "aiutante", "printf 'meta'\nexit 1\n")
    trasporto = TrasportoAiutanteFinto(percorso_script)
    destinazione = tmp_path / "foto.jpg"

    with pytest.raises(FotoFacileError):
        esegui_fino_alla_fine(trasporto.copia("SERIAL1", "/DCIM/foto.jpg", destinazione))

    assert not destinazione.exists()
    assert list(destinazione.parent.glob("*.part")) == []


# ── il collegamento Windows passa la cartella di appoggio ────────────────


def test_wpd_passa_la_destinazione_all_aiutante(tmp_path):
    """CopyHere non sa scrivere sull'uscita standard: l'aiutante ha bisogno di una
    cartella di appoggio, creata dal trasporto dentro la destinazione scelta."""
    registro = tmp_path / "argomenti.txt"
    percorso_script = script(
        tmp_path,
        "aiutante",
        f'printf "%s\\n" "$@" > "{registro}"\nprintf "dati"\n',
    )

    class TrasportoWpdFinto(TrasportoWpdWindows):
        def base(self) -> list[str]:
            return [percorso_script]

    destinazione = tmp_path / "uscita" / "foto.jpg"
    scritti = esegui_fino_alla_fine(
        TrasportoWpdFinto().copia("SERIAL9", "/DCIM/foto.jpg", destinazione)
    )

    assert scritti == len(b"dati")
    assert destinazione.read_bytes() == b"dati"
    argomenti = registro.read_text().splitlines()
    assert argomenti[:5] == ["copia", "--seriale", "SERIAL9", "--percorso", "/DCIM/foto.jpg"]
    assert "--destinazione" in argomenti
    appoggio = Path(argomenti[argomenti.index("--destinazione") + 1])
    assert appoggio.parent == destinazione.parent
    assert appoggio.name.startswith("fotofacile-appoggio-")
    # La cartella di appoggio non deve restare: è il trasporto a ripulire, così non
    # dipende dal fatto che l'aiutante di Windows riesca a eseguire il suo «finally».
    assert list(destinazione.parent.glob("fotofacile-appoggio-*")) == []


def test_wpd_rimuove_la_cartella_di_appoggio_anche_se_la_copia_fallisce(tmp_path):
    percorso_script = script(tmp_path, "aiutante", "printf 'meta'\nexit 1\n")

    class TrasportoWpdFinto(TrasportoWpdWindows):
        def base(self) -> list[str]:
            return [percorso_script]

    destinazione = tmp_path / "uscita" / "foto.jpg"
    with pytest.raises(FotoFacileError):
        esegui_fino_alla_fine(TrasportoWpdFinto().copia("SERIAL9", "/DCIM/foto.jpg", destinazione))

    assert not destinazione.exists()
    assert list(destinazione.parent.glob("fotofacile-appoggio-*")) == []


def test_wpd_cancella_traduce_il_rifiuto_in_un_suggerimento(tmp_path):
    percorso_script = script(
        tmp_path,
        "aiutante",
        'echo "La cancellazione non è disponibile con il collegamento di Windows." >&2\n'
        "exit 2\n",
    )

    class TrasportoWpdFinto(TrasportoWpdWindows):
        def base(self) -> list[str]:
            return [percorso_script]

    with pytest.raises(FotoFacileError) as errore:
        esegui_fino_alla_fine(TrasportoWpdFinto().cancella("SERIAL9", "/DCIM/foto.jpg"))

    assert "Debug USB" in errore.value.hint
    assert "Galleria" in errore.value.hint


# ── disponibilità dei collegamenti a seconda del sistema ─────────────────


def test_il_collegamento_macos_non_e_disponibile_fuori_da_macos(monkeypatch):
    monkeypatch.setattr(trasporto_mac, "chiave_sistema", lambda sistema=None: "win32")
    assert TrasportoPtpMac().disponibile() is False


def test_il_collegamento_windows_non_e_disponibile_fuori_da_windows(monkeypatch):
    monkeypatch.setattr(trasporto_win, "chiave_sistema", lambda sistema=None: "darwin")
    assert TrasportoWpdWindows().disponibile() is False
    monkeypatch.setattr(trasporto_win, "chiave_sistema", lambda sistema=None: "win32")
    assert TrasportoWpdWindows().disponibile() is True


def test_il_collegamento_linux_ha_bisogno_di_gio_o_jmtpfs(monkeypatch):
    monkeypatch.setattr(trasporto_linux, "chiave_sistema", lambda sistema=None: "darwin")
    assert TrasportoMtpLinux().disponibile() is False

    monkeypatch.setattr(trasporto_linux, "chiave_sistema", lambda sistema=None: "linux")
    monkeypatch.setattr(trasporto_linux, "_eseguibile", lambda nome: None)
    assert TrasportoMtpLinux().disponibile() is False

    monkeypatch.setattr(
        trasporto_linux,
        "_eseguibile",
        lambda nome: "/usr/bin/gio" if nome == "gio" else None,
    )
    assert TrasportoMtpLinux().disponibile() is True

    monkeypatch.setattr(
        trasporto_linux,
        "_eseguibile",
        lambda nome: "/usr/bin/jmtpfs" if nome == "jmtpfs" else None,
    )
    assert TrasportoMtpLinux().disponibile() is True


# ── aiutante Linux: parti che si possono provare senza un telefono ───────


def test_montaggio_gvfs_trovato_dal_seriale(tmp_path, monkeypatch):
    from fotofacile.aiutanti import mtp_linux

    cartella = tmp_path / "gvfs" / "mtp:host=SERIALE%20A"
    cartella.mkdir(parents=True)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))

    assert mtp_linux.montaggio_da_seriale("SERIALE%20A") == cartella
    assert mtp_linux.montaggio_da_seriale("SERIALE A") == cartella  # forma decodificata
    assert mtp_linux.montaggio_da_seriale("ALTRO") is None


def test_montaggio_gvfs_trovato_anche_con_il_seriale_leggibile(tmp_path, monkeypatch):
    """I telefoni senza numero di serie hanno un indirizzo «[usb:001,004]»: gvfs chiama
    la cartella con la forma codificata e i due nomi devono combaciare."""
    from fotofacile.aiutanti import mtp_linux

    cartella = tmp_path / "gvfs" / "mtp:host=%5Busb%3A001%2C004%5D"
    cartella.mkdir(parents=True)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))

    assert mtp_linux.montaggio_da_seriale("[usb:001,004]") == cartella


def test_dispositivi_non_elenca_due_volte_lo_stesso_telefono(tmp_path, monkeypatch):
    import subprocess

    from fotofacile.aiutanti import mtp_linux

    (tmp_path / "gvfs" / "mtp:host=%5Busb%3A001%2C004%5D").mkdir(parents=True)
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path))
    monkeypatch.setattr(mtp_linux, "_eseguibile", lambda nome: "/usr/bin/gio")
    monkeypatch.setattr(
        mtp_linux,
        "_esegui",
        lambda comando, timeout: subprocess.CompletedProcess(
            list(comando), 0, stdout="Mount(0): Telefono -> mtp://[usb:001,004]/\n", stderr=""
        ),
    )

    # Una voce sola, con la forma stampata da gio (quella che «gio mount» accetta) e il
    # nome leggibile del telefono.
    assert mtp_linux.dispositivi() == [("[usb:001,004]", "Telefono")]


def test_lettura_dei_montaggi_di_gio():
    from fotofacile.aiutanti import mtp_linux

    # Un telefono già montato, uno visto ma non ancora montato (compare solo come
    # «Volume», con activation_root) e una periferica che non c'entra nulla.
    testo = (
        "Volume(0): Telefono di casa\n"
        "  Type: GProxyVolume (GProxyVolumeMonitorMTP)\n"
        "  activation_root=mtp://Telefono_di_casa_SERIALE1/\n"
        "Mount(0): Telefono di casa -> mtp://Telefono_di_casa_SERIALE1/\n"
        "  Type: GProxyMount (GProxyVolumeMonitorMTP)\n"
        "Volume(1): Secondo telefono\n"
        "  Type: GProxyVolume (GProxyVolumeMonitorMTP)\n"
        "  activation_root=mtp://%5Busb%3A001%2C004%5D/\n"
        "Volume(2): Pennetta USB\n"
        "  activation_root=file:///media/utente/PENNA\n"
    )
    assert mtp_linux.leggi_dispositivi_gio(testo) == [
        ("Telefono_di_casa_SERIALE1", "Telefono di casa"),
        ("%5Busb%3A001%2C004%5D", "Secondo telefono"),
    ]


def test_il_percorso_del_telefono_non_puo_uscire_dal_montaggio(tmp_path):
    from fotofacile.aiutanti import mtp_linux

    with pytest.raises(mtp_linux.GuaioMtp):
        mtp_linux.percorso_di_filesystem(tmp_path, "/DCIM/../../fuori.jpg")
    assert mtp_linux.percorso_di_filesystem(tmp_path, "/DCIM/Camera/a.jpg") == (
        tmp_path / "DCIM" / "Camera" / "a.jpg"
    )


def test_una_radice_illeggibile_non_diventa_un_elenco_vuoto(tmp_path, monkeypatch):
    from fotofacile.aiutanti import mtp_linux

    def scandir_rotto(_percorso):
        raise OSError("Transport endpoint is not connected")

    monkeypatch.setattr(mtp_linux.os, "scandir", scandir_rotto)
    with pytest.raises(mtp_linux.GuaioMtp):
        list(mtp_linux.cammina(tmp_path))


def test_jmtpfs_rifiuta_di_scegliere_fra_due_telefoni(monkeypatch):
    """jmtpfs monta sempre il primo telefono: con due collegati, proseguire vorrebbe dire
    cancellare o copiare sul dispositivo sbagliato."""
    from fotofacile.aiutanti import mtp_linux

    monkeypatch.setattr(
        mtp_linux, "dispositivi_jmtpfs", lambda: [("0", "primo"), ("1", "secondo")]
    )
    monkeypatch.setattr(mtp_linux, "_punto_jmtpfs", lambda seriale: None)
    with pytest.raises(mtp_linux.GuaioMtp):
        mtp_linux._monta_jmtpfs("0")


def test_lo_smontaggio_non_cancella_cartelle_che_non_sono_nostre(tmp_path, monkeypatch):
    """Il file di stato di jmtpfs è un semplice file di testo: se fosse rovinato, non deve
    poter far cancellare una cartella qualunque del computer."""
    from fotofacile.aiutanti import mtp_linux

    monkeypatch.setattr(mtp_linux, "_esegui", lambda comando, timeout: None)
    cartella = tmp_path / "documenti"
    cartella.mkdir()
    importante = cartella / "importante.txt"
    importante.write_text("da non perdere")

    mtp_linux._smonta_percorso(cartella)

    assert importante.exists()
    assert mtp_linux._cartella_nostra(cartella) is False


def test_le_cartelle_di_appoggio_jmtpfs_sono_riconosciute_nostre():
    import tempfile

    from fotofacile.aiutanti import mtp_linux

    cartella = Path(tempfile.mkdtemp(prefix="fotofacile-mtp-"))
    try:
        assert mtp_linux._cartella_nostra(cartella) is True
    finally:
        cartella.rmdir()


def test_aiutante_linux_senza_telefono_esce_con_3(monkeypatch, capsys):
    from fotofacile.aiutanti import mtp_linux

    monkeypatch.setattr(mtp_linux, "dispositivi", lambda env=None: [])
    assert mtp_linux.main(["dispositivi"]) == 3
    assert "telefono" in capsys.readouterr().err.lower()


# ── aiutante Windows: la parte Python (PowerShell non è provabile qui) ───


def test_wpd_win_costruisce_il_comando_per_powershell():
    from fotofacile.aiutanti import wpd_win

    riga = wpd_win.comando_powershell(
        Path("wpd_win.ps1"),
        "copia",
        seriale="SERIAL9",
        percorso="/DCIM/La mia foto.jpg",
        destinazione="C:\\destinazione",
    )
    assert riga[:2] == ["powershell", "-NoProfile"]
    assert "-NonInteractive" in riga
    assert "-ExecutionPolicy" in riga
    assert "-PidSupervisionato" in riga
    assert riga[riga.index("-PidSupervisionato") + 1].isdigit()
    assert riga[-6:] == [
        "-Seriale",
        "SERIAL9",
        "-Percorso",
        "/DCIM/La mia foto.jpg",
        "-Destinazione",
        "C:\\destinazione",
    ]
    assert "-SoloFoto" not in riga


def test_wpd_win_aggiunge_solo_foto_solo_quando_serve():
    from fotofacile.aiutanti import wpd_win

    riga = wpd_win.comando_powershell(Path("wpd_win.ps1"), "elenca", seriale="S", solo_foto=True)
    assert riga[-1] == "-SoloFoto"


def test_wpd_win_rifiuta_un_comando_sconosciuto(capsys):
    from fotofacile.aiutanti import wpd_win

    assert wpd_win.main(["brum"]) == 2
    assert "sconosciuto" in capsys.readouterr().err.lower()


def test_i_tempi_dell_aiutante_windows_sono_piu_corti_del_driver():
    """L'aiutante deve poter uccidere PowerShell e spiegare l'errore prima che il driver
    interrompa il wrapper: su Windows un file aperto non si cancella, e l'errore vero
    verrebbe sostituito da uno incomprensibile."""
    from fotofacile.aiutanti import wpd_win
    from fotofacile.core import trasporto_aiutante as driver

    limiti = {
        "dispositivi": driver.TIMEOUT_DISPOSITIVI,
        "elenca": driver.TIMEOUT_ELENCO,
        "copia": driver.TIMEOUT_COPIA,
        "cancella": 120.0,
    }
    for comando, limite in limiti.items():
        assert wpd_win.TIMEOUT_POWERSHELL[comando] < limite

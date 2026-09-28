import io
import threading
import zipfile
from pathlib import Path

import pytest

from fotofacile.core.errors import FotoFacileError
from fotofacile.core.installer import (
    component_dir,
    download_file,
    extract_component,
    install_component,
    is_installed,
    platform_tools_url,
)


def crea_zip(percorso: Path, contenuti: dict[str, bytes]) -> Path:
    with zipfile.ZipFile(percorso, "w") as archivio:
        for nome, dati in contenuti.items():
            archivio.writestr(nome, dati)
    return percorso


def risposta_finta(dati: bytes):
    class Risposta(io.BytesIO):
        headers = {"Content-Length": str(len(dati))}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    return lambda *_a, **_k: Risposta(dati)


def test_url_dipende_dal_sistema():
    assert platform_tools_url("darwin").endswith("platform-tools-latest-darwin.zip")
    assert platform_tools_url("linux").endswith("platform-tools-latest-linux.zip")
    assert platform_tools_url("win32").endswith("platform-tools-latest-windows.zip")
    assert platform_tools_url("windows").endswith("platform-tools-latest-windows.zip")
    assert platform_tools_url("darwin").startswith("https://dl.google.com/")


def test_url_su_sistema_sconosciuto_produce_errore_umano():
    with pytest.raises(FotoFacileError) as errore:
        platform_tools_url("pianeta-x")
    assert errore.value.hint


def test_estrazione_tira_fuori_adb_e_lo_rende_eseguibile(tmp_path):
    archivio = crea_zip(
        tmp_path / "pt.zip",
        {"platform-tools/adb": b"#!/bin/sh\n", "platform-tools/NOTICE.txt": b"x"},
    )
    destinazione = tmp_path / "componente"
    adb = extract_component(archivio, destinazione, system="linux")
    assert adb == destinazione / "adb"
    assert adb.is_file()
    assert adb.stat().st_mode & 0o111
    assert (destinazione / "NOTICE.txt").is_file()


def test_estrazione_su_windows_porta_anche_le_librerie(tmp_path):
    archivio = crea_zip(
        tmp_path / "pt.zip",
        {
            "platform-tools/adb.exe": b"MZ",
            "platform-tools/AdbWinApi.dll": b"dll",
            "platform-tools/AdbWinUsbApi.dll": b"dll",
        },
    )
    eseguibile = extract_component(archivio, tmp_path / "componente", system="win32")
    assert eseguibile.name == "adb.exe"
    assert (eseguibile.parent / "AdbWinApi.dll").is_file()
    assert (eseguibile.parent / "AdbWinUsbApi.dll").is_file()


def test_estrazione_senza_eseguibile_produce_errore_umano(tmp_path):
    archivio = crea_zip(tmp_path / "pt.zip", {"platform-tools/README.txt": b"x"})
    with pytest.raises(FotoFacileError) as errore:
        extract_component(archivio, tmp_path / "componente", system="linux")
    assert "componente" in errore.value.message.lower()
    assert errore.value.hint


def test_estrazione_da_file_corrotto_produce_errore_umano(tmp_path):
    rotto = tmp_path / "pt.zip"
    rotto.write_bytes(b"non sono uno zip")
    with pytest.raises(FotoFacileError) as errore:
        extract_component(rotto, tmp_path / "componente", system="linux")
    assert "danneggiato" in errore.value.message.lower()
    assert errore.value.hint


def test_download_file_scrive_i_byte_giusti(tmp_path):
    percorso = download_file(
        "https://esempio/finto.bin",
        tmp_path / "scaricato.bin",
        opener=risposta_finta(b"contenuto-finto"),
    )
    assert percorso.read_bytes() == b"contenuto-finto"
    assert not (tmp_path / "scaricato.bin.scarico").exists()


def test_download_riporta_avanzamento(tmp_path):
    visti = []
    download_file(
        "https://esempio/grande.bin",
        tmp_path / "d.bin",
        on_progress=visti.append,
        opener=risposta_finta(b"x" * 5000),
    )
    assert visti
    assert visti[-1]["ricevuti"] == 5000
    assert visti[-1]["totale"] == 5000


def test_download_annullato_non_lascia_file(tmp_path):
    cancel = threading.Event()
    cancel.set()
    with pytest.raises(FotoFacileError) as errore:
        download_file(
            "https://esempio/grande.bin",
            tmp_path / "d.bin",
            cancel=cancel,
            opener=risposta_finta(b"x" * 5000),
        )
    assert "interrotto" in errore.value.message.lower()
    assert list(tmp_path.iterdir()) == []


def test_download_senza_rete_spiega_cosa_fare(tmp_path):
    def opener(*_a, **_k):
        raise OSError("network unreachable")

    with pytest.raises(FotoFacileError) as errore:
        download_file("https://esempio/x.zip", tmp_path / "x.zip", opener=opener)
    assert "internet" in errore.value.hint.lower()
    assert list(tmp_path.iterdir()) == []


def test_installazione_completa_con_downloader_finto(tmp_path):
    archivio = crea_zip(tmp_path / "pt.zip", {"platform-tools/adb": b"#!/bin/sh\n"})

    def downloader(url: str, dest: Path, **_kwargs) -> Path:
        assert url.startswith("https://")
        dest.write_bytes(archivio.read_bytes())
        return dest

    adb = install_component(target_dir=tmp_path / "componente", downloader=downloader, system="linux")
    assert adb.is_file()
    assert is_installed(tmp_path / "componente", system="linux")


def test_componente_installato_ma_assente_risulta_non_installato(tmp_path):
    assert is_installed(tmp_path / "vuota", system="linux") is False


def test_cartella_componente_predefinita_sotto_la_cartella_utente(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("USERPROFILE", raising=False)
    assert component_dir() == tmp_path / ".fotofacile" / "platform-tools"


def test_cartella_componente_su_windows(monkeypatch, tmp_path):
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    assert component_dir() == tmp_path / ".fotofacile" / "platform-tools"

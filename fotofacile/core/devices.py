"""Riconoscimento dei telefoni collegati e traduzione dei loro stati in italiano."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .adb import AdbBackend

STATE_MESSAGE: dict[str, tuple[str, str]] = {
    "device": ("Telefono collegato e pronto.", ""),
    "unauthorized": (
        "Telefono trovato! Sbloccalo e tocca «Consenti» sullo schermo.",
        "Se non appare la richiesta, scollega e ricollega il cavo.",
    ),
    "offline": (
        "Il telefono non risponde.",
        "Scollega e ricollega il cavo, poi premi «Riavvia collegamento».",
    ),
    "no permissions": (
        "Il computer non ha il permesso di parlare con il telefono.",
        "Scollega e ricollega il cavo; se serve, installa il driver USB del produttore.",
    ),
    "bootloader": (
        "Il telefono è in modalità avvio.",
        "Riavvia il telefono normalmente e ricollegalo.",
    ),
}


@dataclass(frozen=True)
class DeviceInfo:
    serial: str
    state: str
    model: str = ""
    product: str = ""

    @property
    def is_ready(self) -> bool:
        return self.state == "device"

    @property
    def display_name(self) -> str:
        if self.model:
            return self.model.replace("_", " ").strip()
        return self.serial


def parse_devices(output: str) -> list[DeviceInfo]:
    """Estrae i dispositivi dall'output di ``adb devices -l``."""
    dispositivi: list[DeviceInfo] = []
    for riga in output.splitlines():
        riga = riga.strip()
        if not riga or riga.endswith("attached") or riga.startswith("*"):
            continue
        campi = riga.split()
        if len(campi) < 2:
            continue
        serial, state = campi[0], campi[1]
        if state == "no" and len(campi) > 2 and campi[2].startswith("permissions"):
            state = "no permissions"  # riga tipica di Linux quando mancano i permessi udev
        extra: dict[str, str] = {}
        for campo in campi[2:]:
            if ":" in campo:
                chiave, _, valore = campo.partition(":")
                extra[chiave] = valore
        dispositivi.append(
            DeviceInfo(
                serial=serial,
                state=state,
                model=extra.get("model", ""),
                product=extra.get("product", ""),
            )
        )
    return dispositivi


def get_devices(adb: AdbBackend) -> list[DeviceInfo]:
    return parse_devices(adb.devices_raw())


def pick_device(devices: Sequence[DeviceInfo], serial: str | None = None) -> DeviceInfo | None:
    """Sceglie il dispositivo da usare: il seriale indicato, altrimenti il primo pronto."""
    if serial is not None:
        for dispositivo in devices:
            if dispositivo.serial == serial:
                return dispositivo
        return None
    for dispositivo in devices:
        if dispositivo.is_ready:
            return dispositivo
    return None

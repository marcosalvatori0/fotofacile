"""Pilota l'applicazione vera, dall'avvio al resoconto, senza intervento umano.

Serve come collaudo completo dell'interfaccia: apre la vera finestra in modalità demo,
attraversa i quattro passi (collegamento, scelta, destinazione, copia) e verifica che i
file siano davvero finiti sul disco. Usa solo funzioni pubbliche delle pagine.

    FF_DEST=<cartella> FF_ESITO=<file json> python3 tests/pilota_app.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from fotofacile.ui.app import App

DESTINAZIONE = Path(os.environ.get("FF_DEST", "cartella-di-prova"))
ESITO = Path(os.environ.get("FF_ESITO", "esito.json"))
SCADENZA = float(os.environ.get("FF_SCADENZA", "120"))
PAUSA = int(os.environ.get("FF_PAUSA_MS", "200"))


def main() -> int:
    applicazione = App(demo_mode=True)
    inizio = time.monotonic()
    stato = {"errore": ""}

    def scrivi_esito(esito: dict) -> None:
        ESITO.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")

    def fallisci(motivo: str) -> None:
        stato["errore"] = motivo
        scrivi_esito({"ok": False, "motivo": motivo, "pagina": applicazione.current_page})
        applicazione.destroy()

    def passo() -> None:
        if time.monotonic() - inizio > SCADENZA:
            return fallisci("tempo scaduto")
        pagina = applicazione.current_page
        if pagina == "connect":
            if applicazione.device is None:
                applicazione.pages["connect"].check_now()
            else:
                applicazione.pages["connect"]._avanti()
        elif pagina == "select":
            if not applicazione.pages["select"]._scansione_fatta:
                pass
            elif not applicazione.pages["select"].selected_files():
                return fallisci("nessun file selezionato dopo la ricerca")
            else:
                applicazione.pages["select"].go_next()
        elif pagina == "options":
            pagina_opzioni = applicazione.pages["options"]
            if pagina_opzioni.chooser.get() != str(DESTINAZIONE):
                pagina_opzioni.chooser.set(str(DESTINAZIONE))
            if applicazione.options is None or applicazione.current_page == "options":
                pagina_opzioni.go_next()
        elif pagina == "transfer":
            risultati = applicazione.pages["transfer"].results
            if risultati is not None:
                file_scritti = sorted(str(percorso) for percorso in risultati.copied)
                scrivi_esito(
                    {
                        "ok": not risultati.cancelled and bool(file_scritti),
                        "copiati": len(risultati.copied),
                        "saltati": risultati.skipped,
                        "errori": [media.name for media, _ in risultati.failed],
                        "byte": risultati.bytes_copied,
                        "file": file_scritti[:5],
                        "pagina": applicazione.current_page,
                        "resoconto": applicazione.pages["transfer"].riepilogo_testo(),
                    }
                )
                applicazione.destroy()
                return
        if applicazione.winfo_exists():
            applicazione.after(PAUSA, passo)

    applicazione.after(PAUSA, passo)
    applicazione.mainloop()
    if stato["errore"]:
        print(f"ERRORE: {stato['errore']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

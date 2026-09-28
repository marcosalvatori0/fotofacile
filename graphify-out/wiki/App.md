# App

> God node · 42 connections · `fotofacile/ui/app.py`

**Community:** [Metodi della finestra App](Metodi_della_finestra_App.md)

## Connections by Relation

### calls
- main() `EXTRACTED`
- start_gui() `EXTRACTED`

### contains
- app.py `EXTRACTED`

### imports
- cli.py `EXTRACTED`
- conftest.py `EXTRACTED`
- pilota_app.py `EXTRACTED`

### method
- .__init__() `EXTRACTED`
- ._costruisci_pagine() `EXTRACTED`
- .attiva_demo() `EXTRACTED`
- .log() `EXTRACTED`
- ._esegui_callback() `EXTRACTED`
- .usa_telefono_vero() `EXTRACTED`
- .ricostruisci_pagine() `EXTRACTED`
- .run_task() `EXTRACTED`
- .annulla_task() `EXTRACTED`
- ._chiusura() `EXTRACTED`
- ._usa_backend() `EXTRACTED`
- ._usa_adb() `EXTRACTED`
- .stop_all_polling() `EXTRACTED`
- .register_page() `EXTRACTED`
- .set_status() `EXTRACTED`
- .history() `EXTRACTED`
- ._pulisci_ambiente() `EXTRACTED`
- .go_to() `EXTRACTED`
- .pump_events() `EXTRACTED`
- .component_mancante() `EXTRACTED`
- *…and 1 more `method` connection(s) not listed (lowest-degree first to go)*

### rationale_for
- Contenitore della procedura guidata: crea le pagine e coordina il lavoro. `EXTRACTED`

### uses
- [FotoFacileError](FotoFacileError.md) `INFERRED`
- [AdbAPassi](AdbAPassi.md) `INFERRED`
- [DemoAdbBackend](DemoAdbBackend.md) `INFERRED`
- [History](History.md) `INFERRED`
- RealAdbBackend `INFERRED`
- AdbDemoAPassi `INFERRED`
- ConnectPage `INFERRED`
- TransferPage `INFERRED`
- SelectPage `INFERRED`
- OptionsPage `INFERRED`
- Banner `INFERRED`
- LogPane `INFERRED`
- StepIndicator `INFERRED`
- finestra_condivisa() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
# Test della finestra

> 27 nodes · cohesion 0.08

## Key Concepts

- **test_ui_app.py** (24 connections) — `tests/test_ui_app.py`
- **azzera()** (8 connections) — `tests/conftest.py`
- **test_un_task_abbandonato_si_ferma_subito()** (4 connections) — `tests/test_ui_app.py`
- **app()** (3 connections) — `tests/test_ui_app.py`
- **test_errore_nella_callback_non_ferma_il_programma()** (3 connections) — `tests/test_ui_app.py`
- **test_task_con_errore_imprevisto_non_chiude_il_programma()** (3 connections) — `tests/test_ui_app.py`
- **test_task_eseguito_a_passi_senza_thread()** (3 connections) — `tests/test_ui_app.py`
- **test_un_task_abbandonato_chiude_il_generatore()** (3 connections) — `tests/test_ui_app.py`
- **test_la_finestra_resta_reattiva_durante_un_task_lungo()** (2 connections) — `tests/test_ui_app.py`
- **test_modalita_demo_attivabile_e_disattivabile()** (2 connections) — `tests/test_ui_app.py`
- **Riporta la finestra allo stato iniziale (Passo 1, telefono demo pronto).** (1 connections) — `tests/conftest.py`
- **fixture** (1 connections)
- **Se l'utente cambia idea, il lavoro in corso deve fermarsi davvero.** (1 connections) — `tests/test_ui_app.py`
- **test_chiusura_ferma_i_sondaggi()** (1 connections) — `tests/test_ui_app.py`
- **test_cronologia_caricata_una_volta()** (1 connections) — `tests/test_ui_app.py`
- **callback_rotta()** (1 connections) — `tests/test_ui_app.py`
- **lavoro()** (1 connections) — `tests/test_ui_app.py`
- **test_indicatore_passi_segue_la_pagina()** (1 connections) — `tests/test_ui_app.py`
- **lavoro()** (1 connections) — `tests/test_ui_app.py`
- **test_navigazione_avanti_indietro()** (1 connections) — `tests/test_ui_app.py`
- **test_navigazione_non_esce_dai_limiti()** (1 connections) — `tests/test_ui_app.py`
- **test_pagine_registrate()** (1 connections) — `tests/test_ui_app.py`
- **test_registro_e_stato()** (1 connections) — `tests/test_ui_app.py`
- **lavoro()** (1 connections) — `tests/test_ui_app.py`
- **lavoro()** (1 connections) — `tests/test_ui_app.py`
- *... and 2 more nodes in this community*

## Relationships

- [Aiuto Debug USB e appoggi test](Aiuto_Debug_USB_e_appoggi_test.md) (6 shared connections)
- [Componenti grafici riusabili](Componenti_grafici_riusabili.md) (4 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (3 shared connections)
- [Telefono demo](Telefono_demo.md) (2 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (1 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (1 shared connections)
- [Appoggi per i test grafici](Appoggi_per_i_test_grafici.md) (1 shared connections)

## Source Files

- `tests/conftest.py`
- `tests/test_ui_app.py`

## Audit Trail

- EXTRACTED: 44 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
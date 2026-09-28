# Interfaccia AdbBackend

> 74 nodes · cohesion 0.07

## Key Concepts

- **TransferOptions** (46 connections) — `fotofacile/core/planner.py`
- **test_transfer.py** (37 connections) — `tests/test_transfer.py`
- **transfer()** (32 connections) — `fotofacile/core/transfer.py`
- **transfer.py** (30 connections) — `fotofacile/core/transfer.py`
- **BackendFinto** (26 connections) — `tests/test_transfer.py`
- **piano()** (23 connections) — `tests/test_transfer.py`
- **AdbBackend** (21 connections) — `fotofacile/core/adb.py`
- **media()** (19 connections) — `tests/test_transfer.py`
- **Annullato** (18 connections) — `fotofacile/core/ops.py`
- **transfer_steps()** (18 connections) — `fotofacile/core/transfer.py`
- **download_file_stream()** (12 connections) — `fotofacile/core/transfer.py`
- **test_cancellazione_fallita_non_compromette_la_copia()** (8 connections) — `tests/test_transfer.py`
- **CopiatoreInterno** (7 connections) — `fotofacile/core/transfer.py`
- **Progress** (7 connections) — `fotofacile/core/transfer.py`
- **test_copia_un_file_e_registra_la_cronologia()** (7 connections) — `tests/test_transfer.py`
- **test_disco_pieno_produce_messaggio_comprensibile()** (7 connections) — `tests/test_transfer.py`
- **test_errori_di_tipo_fotofacile_non_vengono_riconfezionati()** (7 connections) — `tests/test_transfer.py`
- **test_progressi_monotoni_e_finali()** (7 connections) — `tests/test_transfer.py`
- **test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream()** (6 connections) — `tests/test_transfer.py`
- **test_annullamento_prima_di_iniziare_non_copia_nulla()** (6 connections) — `tests/test_transfer.py`
- **test_cancella_dal_telefono_solo_dopo_copia_verificata()** (6 connections) — `tests/test_transfer.py`
- **test_dimensione_diversa_segnala_errore_e_non_scrive_il_file()** (6 connections) — `tests/test_transfer.py`
- **test_dimensione_sconosciuta_non_blocca_la_copia()** (6 connections) — `tests/test_transfer.py`
- **test_elapsed_riflette_l_orologio()** (6 connections) — `tests/test_transfer.py`
- **test_errore_di_rete_usa_il_messaggio_dell_errore()** (6 connections) — `tests/test_transfer.py`
- *... and 49 more nodes in this community*

## Relationships

- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (19 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (16 shared connections)
- [Piano di copia e percorsi](Piano_di_copia_e_percorsi.md) (14 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (7 shared connections)
- [Telefono demo](Telefono_demo.md) (7 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (6 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (6 shared connections)
- [Avvio, CLI e diagnosi](Avvio,_CLI_e_diagnosi.md) (4 shared connections)
- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (4 shared connections)
- [Ricerca dei file sul telefono](Ricerca_dei_file_sul_telefono.md) (3 shared connections)
- [Copia a blocchi dal telefono](Copia_a_blocchi_dal_telefono.md) (3 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (3 shared connections)

## Source Files

- `fotofacile/core/adb.py`
- `fotofacile/core/ops.py`
- `fotofacile/core/planner.py`
- `fotofacile/core/transfer.py`
- `tests/test_transfer.py`

## Audit Trail

- EXTRACTED: 259 (89%)
- INFERRED: 31 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
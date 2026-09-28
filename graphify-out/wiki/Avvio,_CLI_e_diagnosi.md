# Avvio, CLI e diagnosi

> 72 nodes · cohesion 0.05

## Key Concepts

- **test_adb.py** (30 connections) — `tests/test_adb.py`
- **RealAdbBackend** (27 connections) — `fotofacile/core/adb.py`
- **cli.py** (17 connections) — `fotofacile/cli.py`
- **find_adb()** (16 connections) — `fotofacile/core/adb.py`
- **adb.py** (15 connections) — `fotofacile/core/adb.py`
- **shell_quote()** (15 connections) — `fotofacile/core/adb.py`
- **main()** (12 connections) — `fotofacile/cli.py`
- **test_cli.py** (12 connections) — `tests/test_cli.py`
- **_script_adb()** (10 connections) — `tests/test_adb.py`
- **._run()** (9 connections) — `fotofacile/core/adb.py`
- **doctor()** (8 connections) — `fotofacile/cli.py`
- **build_doctor_report()** (6 connections) — `fotofacile/cli.py`
- **start_gui()** (4 connections) — `fotofacile/cli.py`
- **.stream_file()** (4 connections) — `fotofacile/core/adb.py`
- **fotofacile/__init__.py** (4 connections) — `fotofacile/__init__.py`
- **test_comando_fallito_produce_errore_umano()** (4 connections) — `tests/test_adb.py`
- **test_scansione_lenta_supera_il_tempo_massimo()** (4 connections) — `tests/test_adb.py`
- **test_stream_interrotto_produce_errore_umano()** (4 connections) — `tests/test_adb.py`
- **fotofacile.py** (3 connections) — `fotofacile.py`
- **build_parser()** (3 connections) — `fotofacile/cli.py`
- **.delete_file()** (3 connections) — `fotofacile/core/adb.py`
- **.restart_server()** (3 connections) — `fotofacile/core/adb.py`
- **.start_server()** (3 connections) — `fotofacile/core/adb.py`
- **test_cancellazione_usa_rm_con_seriale_e_percorso_quotato()** (3 connections) — `tests/test_adb.py`
- **test_check_riporta_la_prima_riga_della_versione()** (3 connections) — `tests/test_adb.py`
- *... and 47 more nodes in this community*

## Relationships

- [Telefono demo](Telefono_demo.md) (12 shared connections)
- [Metodi della finestra App](Metodi_della_finestra_App.md) (6 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (6 shared connections)
- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (4 shared connections)
- [Differenze di sistema (osutil)](Differenze_di_sistema_osutil.md) (3 shared connections)
- [Ricerca dei file sul telefono](Ricerca_dei_file_sul_telefono.md) (3 shared connections)
- [Finestra e schermata opzioni](Finestra_e_schermata_opzioni.md) (3 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (3 shared connections)
- [Copia a blocchi dal telefono](Copia_a_blocchi_dal_telefono.md) (2 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (2 shared connections)

## Source Files

- `fotofacile.py`
- `fotofacile/__init__.py`
- `fotofacile/cli.py`
- `fotofacile/core/adb.py`
- `tests/test_adb.py`
- `tests/test_cli.py`
- `tests/test_package.py`

## Audit Trail

- EXTRACTED: 166 (95%)
- INFERRED: 8 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
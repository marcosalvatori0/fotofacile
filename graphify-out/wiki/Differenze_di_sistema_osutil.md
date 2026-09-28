# Differenze di sistema (osutil)

> 35 nodes · cohesion 0.10

## Key Concepts

- **test_osutil.py** (18 connections) — `tests/test_osutil.py`
- **osutil.py** (17 connections) — `fotofacile/core/osutil.py`
- **open_in_file_manager()** (15 connections) — `fotofacile/core/osutil.py`
- **app_dir()** (13 connections) — `fotofacile/core/osutil.py`
- **default_photos_dir()** (8 connections) — `fotofacile/core/osutil.py`
- **is_case_insensitive_fs()** (7 connections) — `fotofacile/core/osutil.py`
- **file_manager_command()** (6 connections) — `fotofacile/core/osutil.py`
- **python_command()** (5 connections) — `fotofacile/core/osutil.py`
- **test_apertura_cartella_senza_file_manager_mostra_il_percorso()** (5 connections) — `tests/test_osutil.py`
- **test_codice_di_uscita_diverso_da_zero_e_un_errore_su_linux()** (5 connections) — `tests/test_osutil.py`
- **Path** (4 connections)
- **_system()** (4 connections) — `fotofacile/core/osutil.py`
- **test_apertura_cartella_su_linux_usa_processo_leggero()** (4 connections) — `tests/test_robustezza.py`
- **test_apertura_cartella_usa_il_comando_giusto()** (3 connections) — `tests/test_osutil.py`
- **runner()** (3 connections) — `tests/test_osutil.py`
- **test_apertura_cartella_su_windows_non_boccia_explorer()** (3 connections) — `tests/test_robustezza.py`
- **.open_folder()** (2 connections) — `fotofacile/ui/page_transfer.py`
- **test_cartella_app_multipiattaforma()** (2 connections) — `tests/test_osutil.py`
- **test_cartella_app_senza_variabili_ambientali()** (2 connections) — `tests/test_osutil.py`
- **test_cartella_foto_predefinita()** (2 connections) — `tests/test_osutil.py`
- **test_comando_di_apertura_per_sistema()** (2 connections) — `tests/test_osutil.py`
- **test_comando_python_per_sistema()** (2 connections) — `tests/test_osutil.py`
- **test_sensibilita_maiuscole_per_sistema()** (2 connections) — `tests/test_osutil.py`
- **Unico punto in cui il programma si adatta al sistema operativo.** (1 connections) — `fotofacile/core/osutil.py`
- **Cartella dati dell'app: su Windows %USERPROFILE%, altrove la cartella personale.** (1 connections) — `fotofacile/core/osutil.py`
- *... and 10 more nodes in this community*

## Relationships

- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (5 shared connections)
- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (4 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (4 shared connections)
- [Avvio, CLI e diagnosi](Avvio,_CLI_e_diagnosi.md) (3 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (3 shared connections)
- [Installazione del componente](Installazione_del_componente.md) (3 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (3 shared connections)
- [Telefono demo](Telefono_demo.md) (2 shared connections)
- [Piano di copia e percorsi](Piano_di_copia_e_percorsi.md) (1 shared connections)

## Source Files

- `fotofacile/core/osutil.py`
- `fotofacile/ui/page_transfer.py`
- `tests/test_osutil.py`
- `tests/test_robustezza.py`

## Audit Trail

- EXTRACTED: 80 (92%)
- INFERRED: 7 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
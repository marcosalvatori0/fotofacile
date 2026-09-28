# Telefono vero a passi (AdbAPassi)

> 23 nodes · cohesion 0.23

## Key Concepts

- **AdbAPassi** (41 connections) — `fotofacile/core/adb_passi.py`
- **esegui_fino_alla_fine()** (41 connections) — `fotofacile/core/ops.py`
- **test_adb_passi.py** (26 connections) — `tests/test_adb_passi.py`
- **script()** (13 connections) — `tests/test_adb_passi.py`
- **test_copia_annullata_non_lascia_file()** (6 connections) — `tests/test_adb_passi.py`
- **test_cancellazione_usa_il_percorso_quotato()** (5 connections) — `tests/test_adb_passi.py`
- **test_cerca_media_legge_l_output_anche_se_e_lungo()** (5 connections) — `tests/test_adb_passi.py`
- **test_copia_fallita_rimuove_il_file_parziale()** (5 connections) — `tests/test_adb_passi.py`
- **test_errore_sui_dispositivi_produce_messaggio_umano()** (5 connections) — `tests/test_adb_passi.py`
- **test_scansione_annullabile()** (5 connections) — `tests/test_robustezza.py`
- **test_cerca_media_passa_il_seriale_giusto()** (4 connections) — `tests/test_adb_passi.py`
- **test_copia_di_un_file_grande_riporta_avanzamento_intermedio()** (4 connections) — `tests/test_adb_passi.py`
- **test_copia_un_file_e_rinomina_solo_alla_fine()** (4 connections) — `tests/test_adb_passi.py`
- **test_file_temporanei_non_si_accumulano()** (4 connections) — `tests/test_adb_passi.py`
- **test_legge_i_dispositivi_collegati()** (4 connections) — `tests/test_adb_passi.py`
- **test_riavvio_ignora_gli_errori_di_chiusura()** (4 connections) — `tests/test_adb_passi.py`
- **test_scansione_ripiega_su_tutta_la_memoria_se_non_trova_nulla()** (4 connections) — `tests/test_robustezza.py`
- **.pulisci()** (2 connections) — `fotofacile/core/adb_passi.py`
- **Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione.** (1 connections) — `fotofacile/core/adb_passi.py`
- **Rimuove la cartella di appoggio usata per gli elenchi temporanei.** (1 connections) — `fotofacile/core/adb_passi.py`
- **Porta a termine un generatore a passi ignorando le pause (usato da test e CLI).** (1 connections) — `fotofacile/core/ops.py`
- **Path** (1 connections)
- **ferma()** (1 connections) — `tests/test_adb_passi.py`

## Relationships

- [Copia a blocchi dal telefono](Copia_a_blocchi_dal_telefono.md) (11 shared connections)
- [Processi esterni a passi](Processi_esterni_a_passi.md) (10 shared connections)
- [Test copia reale](Test_copia_reale.md) (7 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (7 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (6 shared connections)
- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (6 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (5 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (5 shared connections)
- [Ricerca dei file sul telefono](Ricerca_dei_file_sul_telefono.md) (4 shared connections)
- [Download a blocchi del componente](Download_a_blocchi_del_componente.md) (3 shared connections)
- [Avvio, CLI e diagnosi](Avvio,_CLI_e_diagnosi.md) (3 shared connections)
- [Metodi della finestra App](Metodi_della_finestra_App.md) (2 shared connections)

## Source Files

- `fotofacile/core/adb_passi.py`
- `fotofacile/core/ops.py`
- `tests/test_adb_passi.py`
- `tests/test_robustezza.py`

## Audit Trail

- EXTRACTED: 119 (92%)
- INFERRED: 11 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
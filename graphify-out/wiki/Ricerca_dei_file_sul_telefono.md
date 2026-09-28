# Ricerca dei file sul telefono

> 25 nodes · cohesion 0.14

## Key Concepts

- **scanner.py** (24 connections) — `fotofacile/core/scanner.py`
- **parse_stat_stream()** (23 connections) — `fotofacile/core/scanner.py`
- **test_scanner.py** (18 connections) — `tests/test_scanner.py`
- **group_folders()** (14 connections) — `fotofacile/core/scanner.py`
- **build_scan_command()** (11 connections) — `fotofacile/core/scanner.py`
- **page_select.py** (11 connections) — `fotofacile/ui/page_select.py`
- **test_elenco_file_produce_righe_stat_compatibili()** (4 connections) — `tests/test_demo.py`
- **test_cancellazione_rimuove_il_file()** (3 connections) — `tests/test_demo.py`
- **test_stream_e_deterministico()** (3 connections) — `tests/test_demo.py`
- **test_etichetta_della_cartella_toglie_la_memoria_del_telefono()** (3 connections) — `tests/test_scanner.py`
- **test_group_folders_raggruppa_e_ordina_per_dimensione()** (3 connections) — `tests/test_scanner.py`
- **_kind_for()** (2 connections) — `fotofacile/core/scanner.py`
- **_label()** (2 connections) — `fotofacile/core/scanner.py`
- **MediaFolder** (2 connections) — `fotofacile/core/scanner.py`
- **test_comando_scansione_con_video_e_profondita()** (2 connections) — `tests/test_scanner.py`
- **test_comando_scansione_quota_percorsi_e_filtra_estensioni()** (2 connections) — `tests/test_scanner.py`
- **test_mediafile_ha_nome_e_cartella()** (2 connections) — `tests/test_scanner.py`
- **test_parsing_flusso_stat()** (2 connections) — `tests/test_scanner.py`
- **test_parsing_gestisce_nomi_con_emoji_accenti_e_maiuscole()** (2 connections) — `tests/test_scanner.py`
- **test_parsing_ignora_righe_corrotte_e_estensioni_non_media()** (2 connections) — `tests/test_scanner.py`
- **Elenco dei file multimediali presenti sul telefono. La ricerca avviene con **un…** (1 connections) — `fotofacile/core/scanner.py`
- **Costruisce l'unico comando che elenca i file sul telefono.** (1 connections) — `fotofacile/core/scanner.py`
- **Raggruppa i file per cartella, ordinando per dimensione decrescente.** (1 connections) — `fotofacile/core/scanner.py`
- **Interpreta l'output «dimensione|data|percorso» prodotto sul dispositivo. Le…** (1 connections) — `fotofacile/core/scanner.py`
- **Passo 2: mostrare le cartelle trovate sul telefono e far scegliere cosa copiare.** (1 connections) — `fotofacile/ui/page_select.py`

## Relationships

- [Telefono demo](Telefono_demo.md) (11 shared connections)
- [Test della ricerca file](Test_della_ricerca_file.md) (8 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (7 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (7 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (4 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (4 shared connections)
- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (3 shared connections)
- [Avvio, CLI e diagnosi](Avvio,_CLI_e_diagnosi.md) (3 shared connections)
- [Passo 2: scelta delle foto](Passo_2-_scelta_delle_foto.md) (3 shared connections)
- [Copia a blocchi dal telefono](Copia_a_blocchi_dal_telefono.md) (2 shared connections)
- [Finestra e schermata opzioni](Finestra_e_schermata_opzioni.md) (2 shared connections)
- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (1 shared connections)

## Source Files

- `fotofacile/core/scanner.py`
- `fotofacile/ui/page_select.py`
- `tests/test_demo.py`
- `tests/test_scanner.py`

## Audit Trail

- EXTRACTED: 98 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
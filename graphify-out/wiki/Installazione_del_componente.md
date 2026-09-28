# Installazione del componente

> 49 nodes · cohesion 0.08

## Key Concepts

- **test_installer.py** (25 connections) — `tests/test_installer.py`
- **installer.py** (18 connections) — `fotofacile/core/installer.py`
- **extract_component()** (13 connections) — `fotofacile/core/installer.py`
- **installa_a_passi()** (12 connections) — `fotofacile/core/installer.py`
- **component_dir()** (10 connections) — `fotofacile/core/installer.py`
- **page_connect.py** (10 connections) — `fotofacile/ui/page_connect.py`
- **download_file()** (9 connections) — `fotofacile/core/installer.py`
- **platform_tools_url()** (9 connections) — `fotofacile/core/installer.py`
- **install_component()** (8 connections) — `fotofacile/core/installer.py`
- **is_installed()** (8 connections) — `fotofacile/core/installer.py`
- **Path** (6 connections)
- **crea_zip()** (6 connections) — `tests/test_installer.py`
- **test_installazione_a_passi_annullabile()** (6 connections) — `tests/test_installer_passi.py`
- **risposta_finta()** (6 connections) — `tests/test_installer.py`
- **_risposta()** (5 connections) — `tests/test_installer_passi.py`
- **test_installazione_a_passi_scarica_ed_estrae()** (5 connections) — `tests/test_installer_passi.py`
- **test_installazione_completa_con_downloader_finto()** (5 connections) — `tests/test_installer.py`
- **_chiave_sistema()** (4 connections) — `fotofacile/core/installer.py`
- **_nome_eseguibile()** (4 connections) — `fotofacile/core/installer.py`
- **_zip()** (4 connections) — `tests/test_installer_passi.py`
- **test_download_annullato_non_lascia_file()** (4 connections) — `tests/test_installer.py`
- **test_download_senza_rete_spiega_cosa_fare()** (4 connections) — `tests/test_installer.py`
- **test_estrazione_senza_eseguibile_produce_errore_umano()** (4 connections) — `tests/test_installer.py`
- **test_download_file_scrive_i_byte_giusti()** (3 connections) — `tests/test_installer.py`
- **test_download_riporta_avanzamento()** (3 connections) — `tests/test_installer.py`
- *... and 24 more nodes in this community*

## Relationships

- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (11 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (6 shared connections)
- [Differenze di sistema (osutil)](Differenze_di_sistema_osutil.md) (3 shared connections)
- [Download a blocchi del componente](Download_a_blocchi_del_componente.md) (2 shared connections)
- [Telefono demo](Telefono_demo.md) (2 shared connections)
- [Passo 1: collegamento](Passo_1-_collegamento.md) (2 shared connections)
- [Finestra e schermata opzioni](Finestra_e_schermata_opzioni.md) (2 shared connections)
- [Aiuto Debug USB e appoggi test](Aiuto_Debug_USB_e_appoggi_test.md) (2 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (2 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (1 shared connections)

## Source Files

- `fotofacile/core/installer.py`
- `fotofacile/ui/page_connect.py`
- `tests/test_installer.py`
- `tests/test_installer_passi.py`

## Audit Trail

- EXTRACTED: 122 (94%)
- INFERRED: 8 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
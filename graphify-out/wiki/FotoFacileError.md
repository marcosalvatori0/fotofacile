# FotoFacileError

> God node · 70 connections · `fotofacile/core/errors.py`

**Community:** [Errori con messaggio umano](Errori_con_messaggio_umano.md)

## Connections by Relation

### calls
- open_in_file_manager() `EXTRACTED`
- extract_component() `EXTRACTED`
- .copia() `EXTRACTED`
- save_report() `EXTRACTED`
- test_errore_di_permesso_non_viene_ritentato() `EXTRACTED`
- ._esegui_ricerca() `EXTRACTED`
- download_file() `EXTRACTED`
- platform_tools_url() `EXTRACTED`
- .aspetta() `EXTRACTED`
- .esito() `EXTRACTED`
- traduci_errore_file() `EXTRACTED`
- test_errori_di_tipo_fotofacile_non_vengono_riconfezionati() `EXTRACTED`
- .copia() `EXTRACTED`
- .avvia() `EXTRACTED`
- test_task_con_callback_di_errore_personalizzato() `EXTRACTED`
- test_task_con_errore_mostra_il_messaggio_umano() `EXTRACTED`
- .scarica() `EXTRACTED`
- copia() `EXTRACTED`
- lavoro() `EXTRACTED`
- lavoro() `EXTRACTED`

### contains
- errors.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- test_transfer.py `EXTRACTED`
- transfer.py `EXTRACTED`
- test_adb.py `EXTRACTED`
- test_adb_passi.py `EXTRACTED`
- app.py `EXTRACTED`
- test_installer.py `EXTRACTED`
- test_ui_app.py `EXTRACTED`
- adb_passi.py `EXTRACTED`
- test_installer_passi.py `EXTRACTED`
- installer.py `EXTRACTED`
- test_osutil.py `EXTRACTED`
- osutil.py `EXTRACTED`
- report.py `EXTRACTED`
- test_ops.py `EXTRACTED`
- ops.py `EXTRACTED`

### inherits
- AdbError `EXTRACTED`
- TransferError `EXTRACTED`
- Exception `EXTRACTED`

### method
- .__init__() `EXTRACTED`
- .__str__() `EXTRACTED`

### rationale_for
- Errore con messaggio per l'utente e un suggerimento su come procedere. `EXTRACTED`

### references
- .run_task() `EXTRACTED`

### uses
- [App](App.md) `INFERRED`
- [AdbAPassi](AdbAPassi.md) `INFERRED`
- ProcessoEsterno `INFERRED`
- AdbDemoAPassi `INFERRED`
- transfer_steps() `INFERRED`
- download_file_stream() `INFERRED`
- ScaricatoreAPassi `INFERRED`
- test_scaricatore_annullabile() `INFERRED`
- test_installazione_a_passi_annullabile() `INFERRED`
- test_copia_reale_con_errore_di_disco_non_lascia_part() `INFERRED`
- test_copia_reale_con_permesso_negato_spiega_come_rimediare() `INFERRED`
- test_copia_fallita_rimuove_il_file_parziale() `INFERRED`
- test_errore_sui_dispositivi_produce_messaggio_umano() `INFERRED`
- test_processo_che_non_risponde_scade_e_viene_interrotto() `INFERRED`
- test_processo_fallito_produce_errore_umano() `INFERRED`
- test_scaricatore_senza_rete_spiega_cosa_controllare() `INFERRED`
- test_apertura_cartella_senza_file_manager_mostra_il_percorso() `INFERRED`
- test_codice_di_uscita_diverso_da_zero_e_un_errore_su_linux() `INFERRED`
- test_download_annullato_non_lascia_file() `INFERRED`
- test_download_senza_rete_spiega_cosa_fare() `INFERRED`
- *…and 6 more `uses` connection(s) not listed (lowest-degree first to go)*

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
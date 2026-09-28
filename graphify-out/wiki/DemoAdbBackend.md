# DemoAdbBackend

> God node · 39 connections · `fotofacile/core/demo.py`

**Community:** [Telefono demo](Telefono_demo.md)

## Connections by Relation

### calls
- test_cronologia_non_scrivibile_non_perde_le_foto_copiate() `EXTRACTED`
- azzera() `EXTRACTED`
- .attiva_demo() `EXTRACTED`
- test_demo_a_passi_annullabile_senza_residui() `EXTRACTED`
- test_demo_a_passi_cancella_e_riavvia() `EXTRACTED`
- test_elenco_file_produce_righe_stat_compatibili() `EXTRACTED`
- test_demo_a_passi_elenca_e_copia() `EXTRACTED`
- test_demo_a_passi_riporta_avanzamento_a_pezzi() `EXTRACTED`
- test_backend_demo_si_presenta_come_dispositivo_pronto() `EXTRACTED`
- test_cancellazione_di_percorso_inesistente_da_errore() `EXTRACTED`
- test_cancellazione_rimuove_il_file() `EXTRACTED`
- test_demo_ha_sia_foto_sia_video() `EXTRACTED`
- test_stato_modificabile_per_provare_gli_altri_casi() `EXTRACTED`
- test_stato_nessuno_telefono() `EXTRACTED`
- test_stream_di_percorso_inesistente_da_errore() `EXTRACTED`
- test_stream_e_deterministico() `EXTRACTED`
- test_stream_restituisce_il_contenuto_della_dimensione_attesa() `EXTRACTED`
- .__init__() `EXTRACTED`
- test_check_riporta_una_versione_leggibile_e_riavvio_non_fa_nulla() `EXTRACTED`

### contains
- demo.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- app.py `EXTRACTED`
- adb_passi.py `EXTRACTED`
- test_demo.py `EXTRACTED`
- test_installer_passi.py `EXTRACTED`
- conftest.py `EXTRACTED`

### method
- .delete_file() `EXTRACTED`
- .__init__() `EXTRACTED`
- .stream_file() `EXTRACTED`
- .start_server() `EXTRACTED`
- .restart_server() `EXTRACTED`
- .check() `EXTRACTED`
- .devices_raw() `EXTRACTED`
- .list_media_raw() `EXTRACTED`

### rationale_for
- Implementazione finta di AdbBackend: nessun telefono, nessun processo esterno. `EXTRACTED`

### uses
- [App](App.md) `INFERRED`
- AdbDemoAPassi `INFERRED`
- AdbError `INFERRED`
- finestra_condivisa() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
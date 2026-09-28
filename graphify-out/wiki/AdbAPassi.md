# AdbAPassi

> God node · 41 connections · `fotofacile/core/adb_passi.py`

**Community:** [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md)

## Connections by Relation

### calls
- test_copia_annullata_non_lascia_file() `EXTRACTED`
- test_copia_reale_con_errore_di_disco_non_lascia_part() `EXTRACTED`
- test_copia_reale_con_permesso_negato_spiega_come_rimediare() `EXTRACTED`
- ._usa_adb() `EXTRACTED`
- test_cancellazione_usa_il_percorso_quotato() `EXTRACTED`
- test_cerca_media_legge_l_output_anche_se_e_lungo() `EXTRACTED`
- test_copia_fallita_rimuove_il_file_parziale() `EXTRACTED`
- test_errore_sui_dispositivi_produce_messaggio_umano() `EXTRACTED`
- test_scansione_annullabile() `EXTRACTED`
- test_cerca_media_passa_il_seriale_giusto() `EXTRACTED`
- test_copia_di_un_file_grande_riporta_avanzamento_intermedio() `EXTRACTED`
- test_copia_un_file_e_rinomina_solo_alla_fine() `EXTRACTED`
- test_file_temporanei_non_si_accumulano() `EXTRACTED`
- test_legge_i_dispositivi_collegati() `EXTRACTED`
- test_riavvio_ignora_gli_errori_di_chiusura() `EXTRACTED`
- test_copia_reale_abbandonata_non_lascia_nulla() `EXTRACTED`
- test_scansione_ripiega_su_tutta_la_memoria_se_non_trova_nulla() `EXTRACTED`

### contains
- adb_passi.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- test_adb_passi.py `EXTRACTED`
- app.py `EXTRACTED`

### method
- .copia() `EXTRACTED`
- ._esegui_ricerca() `EXTRACTED`
- ._processo() `EXTRACTED`
- .cerca_media() `EXTRACTED`
- .dispositivi() `EXTRACTED`
- ._rallenta_scrittura() `EXTRACTED`
- .cancella() `EXTRACTED`
- ._dimensione() `EXTRACTED`
- .riavvia() `EXTRACTED`
- ._file_temporaneo() `EXTRACTED`
- .__init__() `EXTRACTED`
- .pulisci() `EXTRACTED`
- ._ripulisci() `EXTRACTED`

### rationale_for
- Telefono vero, comandato a passi: dispositivi, ricerca, copia e cancellazione. `EXTRACTED`

### uses
- [FotoFacileError](FotoFacileError.md) `INFERRED`
- [App](App.md) `INFERRED`
- [DeviceInfo](DeviceInfo.md) `INFERRED`
- [MediaFile](MediaFile.md) `INFERRED`
- ProcessoEsterno `INFERRED`
- Annullato `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
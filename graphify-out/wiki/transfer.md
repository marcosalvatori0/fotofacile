# transfer()

> God node · 32 connections · `fotofacile/core/transfer.py`

**Community:** [Interfaccia AdbBackend](Interfaccia_AdbBackend.md)

## Connections by Relation

### calls
- [esegui_fino_alla_fine()](esegui_fino_alla_fine.md) `EXTRACTED`
- transfer_steps() `EXTRACTED`
- test_cronologia_non_scrivibile_non_perde_le_foto_copiate() `EXTRACTED`
- test_cancellazione_fallita_non_compromette_la_copia() `EXTRACTED`
- CopiatoreInterno `EXTRACTED`
- test_copia_un_file_e_registra_la_cronologia() `EXTRACTED`
- test_disco_pieno_produce_messaggio_comprensibile() `EXTRACTED`
- test_errori_di_tipo_fotofacile_non_vengono_riconfezionati() `EXTRACTED`
- test_progressi_monotoni_e_finali() `EXTRACTED`
- test_annullamento_a_meta_file_non_lascia_residui_e_chiude_lo_stream() `EXTRACTED`
- test_annullamento_prima_di_iniziare_non_copia_nulla() `EXTRACTED`
- test_cancella_dal_telefono_solo_dopo_copia_verificata() `EXTRACTED`
- test_dimensione_diversa_segnala_errore_e_non_scrive_il_file() `EXTRACTED`
- test_dimensione_sconosciuta_non_blocca_la_copia() `EXTRACTED`
- test_elapsed_riflette_l_orologio() `EXTRACTED`
- test_errore_di_rete_usa_il_messaggio_dell_errore() `EXTRACTED`
- test_errore_persistente_finisce_nel_resoconto_senza_interrompere() `EXTRACTED`
- test_errore_transitorio_viene_ritentato() `EXTRACTED`
- test_permesso_negato_produce_messaggio_comprensibile() `EXTRACTED`
- test_progressi_riportano_velocita_e_tempo_rimanente() `EXTRACTED`
- *…and 2 more `calls` connection(s) not listed (lowest-degree first to go)*

### contains
- transfer.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- test_transfer.py `EXTRACTED`

### rationale_for
- Copia il piano e restituisce il resoconto (modo diretto, senza passi). `EXTRACTED`

### references
- TransferResults `EXTRACTED`
- Progress `EXTRACTED`

### uses
- [TransferOptions](TransferOptions.md) `INFERRED`
- [History](History.md) `INFERRED`
- TransferPlan `INFERRED`
- AdbBackend `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
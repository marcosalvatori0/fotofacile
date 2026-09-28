# TransferOptions

> God node · 46 connections · `fotofacile/core/planner.py`

**Community:** [Interfaccia AdbBackend](Interfaccia_AdbBackend.md)

## Connections by Relation

### calls
- test_errore_di_permesso_non_viene_ritentato() `EXTRACTED`
- test_cronologia_non_scrivibile_non_perde_le_foto_copiate() `EXTRACTED`
- test_cancellazione_fallita_non_compromette_la_copia() `EXTRACTED`
- test_copia_un_file_e_registra_la_cronologia() `EXTRACTED`
- test_disco_pieno_produce_messaggio_comprensibile() `EXTRACTED`
- test_errori_di_tipo_fotofacile_non_vengono_riconfezionati() `EXTRACTED`
- test_progressi_monotoni_e_finali() `EXTRACTED`
- test_ensure_space_avvisa_se_manca_spazio() `EXTRACTED`
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
- test_senza_cronologia_la_copia_funziona_comunque() `EXTRACTED`
- *…and 13 more `calls` connection(s) not listed (lowest-degree first to go)*

### contains
- planner.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- test_transfer.py `EXTRACTED`
- test_planner.py `EXTRACTED`
- transfer.py `EXTRACTED`
- test_page_options.py `EXTRACTED`
- page_options.py `EXTRACTED`

### references
- build_plan() `EXTRACTED`
- .build_options() `EXTRACTED`

### uses
- [transfer()](transfer.md) `INFERRED`
- transfer_steps() `INFERRED`
- OptionsPage `INFERRED`
- test_proposta_cartella_e_opzioni() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
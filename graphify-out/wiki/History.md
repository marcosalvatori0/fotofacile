# History

> God node · 36 connections · `fotofacile/core/history.py`

**Community:** [Cronologia dei file copiati](Cronologia_dei_file_copiati.md)

## Connections by Relation

### calls
- test_cronologia_non_scrivibile_non_perde_le_foto_copiate() `EXTRACTED`
- azzera() `EXTRACTED`
- test_copia_un_file_e_registra_la_cronologia() `EXTRACTED`
- test_dedup_non_attiva_quando_disattivata() `EXTRACTED`
- test_piano_salta_i_file_gia_copiati() `EXTRACTED`
- test_contenuto_diverso_non_risulta_gia_copiato() `EXTRACTED`
- test_cronologie_separate_per_dispositivo() `EXTRACTED`
- test_file_assente_viene_trattato_come_vuoto() `EXTRACTED`
- test_file_con_struttura_inattesa_non_fa_esplodere_nulla() `EXTRACTED`
- test_file_corrotto_viene_messo_da_parte_senza_crash() `EXTRACTED`
- test_round_trip_salva_e_rilegge() `EXTRACTED`
- test_salvataggio_crea_la_cartella_e_scrive_la_versione() `EXTRACTED`
- test_salvataggio_non_lascia_file_temporanei() `EXTRACTED`
- test_cronologia_non_leggibile_non_impedisce_l_avvio() `EXTRACTED`

### contains
- history.py `EXTRACTED`

### imports
- test_robustezza.py `EXTRACTED`
- test_transfer.py `EXTRACTED`
- test_planner.py `EXTRACTED`
- planner.py `EXTRACTED`
- transfer.py `EXTRACTED`
- app.py `EXTRACTED`
- conftest.py `EXTRACTED`
- test_history.py `EXTRACTED`

### method
- .__init__() `EXTRACTED`
- .load() `EXTRACTED`
- ._metti_da_parte_file_corrotto() `EXTRACTED`
- .contains() `EXTRACTED`
- .save() `EXTRACTED`
- .record() `EXTRACTED`
- .count() `EXTRACTED`

### rationale_for
- Cronologia per-dispositivo: percorso relativo → dimensione, data, destinazione. `EXTRACTED`

### references
- .history() `EXTRACTED`

### uses
- [App](App.md) `INFERRED`
- [transfer()](transfer.md) `INFERRED`
- build_plan() `INFERRED`
- transfer_steps() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
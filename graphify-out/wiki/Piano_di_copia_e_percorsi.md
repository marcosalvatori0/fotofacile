# Piano di copia e percorsi

> 29 nodes · cohesion 0.16

## Key Concepts

- **test_planner.py** (36 connections) — `tests/test_planner.py`
- **build_plan()** (31 connections) — `fotofacile/core/planner.py`
- **destination_for()** (15 connections) — `fotofacile/core/planner.py`
- **foto()** (14 connections) — `tests/test_planner.py`
- **relative_path()** (6 connections) — `fotofacile/core/planner.py`
- **test_ensure_space_avvisa_se_manca_spazio()** (6 connections) — `tests/test_planner.py`
- **test_dedup_non_attiva_quando_disattivata()** (5 connections) — `tests/test_planner.py`
- **test_nome_con_maiuscole_diverse_e_un_file_diverso()** (5 connections) — `tests/test_planner.py`
- **test_piano_salta_i_file_gia_copiati()** (5 connections) — `tests/test_planner.py`
- **test_collisione_dimensione_diversa_rinomina()** (4 connections) — `tests/test_planner.py`
- **test_collisione_stessa_dimensione_viene_saltata()** (4 connections) — `tests/test_planner.py`
- **test_piano_filtra_per_data()** (4 connections) — `tests/test_planner.py`
- **test_piano_ignora_i_file_senza_dimensione_nel_totale()** (4 connections) — `tests/test_planner.py`
- **test_piano_non_modifica_i_file_di_input()** (4 connections) — `tests/test_planner.py`
- **test_piano_somma_dimensioni_e_filtra_i_video()** (4 connections) — `tests/test_planner.py`
- **test_rinomina_evita_anche_i_nomi_con_maiuscole_diverse()** (4 connections) — `tests/test_planner.py`
- **test_su_linux_le_maiuscole_contano()** (4 connections) — `tests/test_planner.py`
- **test_destinazione_con_e_senza_struttura()** (2 connections) — `tests/test_planner.py`
- **test_nome_lunghissimo_accorciato_mantenendo_estensione()** (2 connections) — `tests/test_planner.py`
- **test_nome_vuoto_o_solo_caratteri_strani()** (2 connections) — `tests/test_planner.py`
- **test_nomi_non_validi_su_windows_vengono_resi_sicuri()** (2 connections) — `tests/test_planner.py`
- **test_nomi_riservati_vengono_prefissati()** (2 connections) — `tests/test_planner.py`
- **test_percorso_profondo_troppo_lungo_accorciato()** (2 connections) — `tests/test_planner.py`
- **test_punti_e_spazi_finali_rimossi()** (2 connections) — `tests/test_planner.py`
- **test_relative_path_toglie_la_memoria_del_telefono()** (2 connections) — `tests/test_planner.py`
- *... and 4 more nodes in this community*

## Relationships

- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (14 shared connections)
- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (14 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (7 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (5 shared connections)
- [Collisioni di nomi](Collisioni_di_nomi.md) (3 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (3 shared connections)
- [Differenze di sistema (osutil)](Differenze_di_sistema_osutil.md) (1 shared connections)
- [Ricerca dei file sul telefono](Ricerca_dei_file_sul_telefono.md) (1 shared connections)
- [Telefono demo](Telefono_demo.md) (1 shared connections)

## Source Files

- `fotofacile/core/planner.py`
- `tests/test_planner.py`

## Audit Trail

- EXTRACTED: 109 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
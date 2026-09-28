# Test copia reale

> 8 nodes · cohesion 0.25

## Key Concepts

- **script()** (7 connections) — `tests/test_robustezza.py`
- **test_copia_reale_con_errore_di_disco_non_lascia_part()** (6 connections) — `tests/test_robustezza.py`
- **test_copia_reale_con_permesso_negato_spiega_come_rimediare()** (6 connections) — `tests/test_robustezza.py`
- **test_copia_reale_abbandonata_non_lascia_nulla()** (4 connections) — `tests/test_robustezza.py`
- **Path** (1 connections)
- **Se l'utente chiude la finestra a metà copia, il file parziale deve sparire.** (1 connections) — `tests/test_robustezza.py`
- **replace_rotto()** (1 connections) — `tests/test_robustezza.py`
- **open_negato()** (1 connections) — `tests/test_robustezza.py`

## Relationships

- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (7 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (4 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (2 shared connections)

## Source Files

- `tests/test_robustezza.py`

## Audit Trail

- EXTRACTED: 16 (80%)
- INFERRED: 4 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
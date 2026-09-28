# Processi esterni a passi

> 31 nodes · cohesion 0.12

## Key Concepts

- **ProcessoEsterno** (28 connections) — `fotofacile/core/ops.py`
- **test_ops.py** (17 connections) — `tests/test_ops.py`
- **ops.py** (14 connections) — `fotofacile/core/ops.py`
- **.aspetta()** (9 connections) — `fotofacile/core/ops.py`
- **.esito()** (9 connections) — `fotofacile/core/ops.py`
- **script()** (8 connections) — `tests/test_ops.py`
- **._pulisci_flussi()** (5 connections) — `fotofacile/core/ops.py`
- **.termina()** (5 connections) — `fotofacile/core/ops.py`
- **test_processo_che_non_risponde_scade_e_viene_interrotto()** (5 connections) — `tests/test_ops.py`
- **test_processo_fallito_produce_errore_umano()** (5 connections) — `tests/test_ops.py`
- **.avvia()** (4 connections) — `fotofacile/core/ops.py`
- **test_comando_inesistente_produce_errore_umano()** (4 connections) — `tests/test_ops.py`
- **test_output_grande_va_su_file_per_non_intasare_il_collegamento()** (4 connections) — `tests/test_ops.py`
- **test_processo_breve_riporta_output_e_codice()** (4 connections) — `tests/test_ops.py`
- **test_processo_lungo_non_blocca_chi_lo_guida()** (4 connections) — `tests/test_ops.py`
- **.passo()** (3 connections) — `fotofacile/core/ops.py`
- **RisultatoComando** (3 connections) — `fotofacile/core/ops.py`
- **test_processo_interrotto_a_mano_non_lascia_processi_appesi()** (3 connections) — `tests/test_ops.py`
- **.__del__()** (2 connections) — `fotofacile/core/ops.py`
- **._leggi_errori()** (2 connections) — `fotofacile/core/ops.py`
- **._leggi_output()** (2 connections) — `fotofacile/core/ops.py`
- **._primo_errore()** (2 connections) — `fotofacile/core/ops.py`
- **.scaduto()** (2 connections) — `fotofacile/core/ops.py`
- **Operazioni esterne eseguite **a piccoli passi**, senza usare thread. Perché non…** (1 connections) — `fotofacile/core/ops.py`
- **True se il comando è ancora in corso.** (1 connections) — `fotofacile/core/ops.py`
- *... and 6 more nodes in this community*

## Relationships

- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (10 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (10 shared connections)
- [Download a blocchi del componente](Download_a_blocchi_del_componente.md) (6 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (2 shared connections)
- [Telefono demo](Telefono_demo.md) (2 shared connections)
- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (2 shared connections)
- [Modelli dati e casi difficili](Modelli_dati_e_casi_difficili.md) (2 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (1 shared connections)
- [Copia a blocchi dal telefono](Copia_a_blocchi_dal_telefono.md) (1 shared connections)

## Source Files

- `fotofacile/core/ops.py`
- `tests/test_ops.py`

## Audit Trail

- EXTRACTED: 89 (95%)
- INFERRED: 5 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
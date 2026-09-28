# Modelli dati e casi difficili

> 12 nodes · cohesion 0.23

## Key Concepts

- **test_robustezza.py** (42 connections) — `tests/test_robustezza.py`
- **MediaFile** (33 connections) — `fotofacile/core/scanner.py`
- **test_errore_di_permesso_non_viene_ritentato()** (10 connections) — `tests/test_robustezza.py`
- **test_cronologia_non_scrivibile_non_perde_le_foto_copiate()** (9 connections) — `tests/test_robustezza.py`
- **PlannedFile** (7 connections) — `fotofacile/core/planner.py`
- **test_nome_con_maiuscole_diverse_non_viene_scambiato_per_lo_stesso_file()** (4 connections) — `tests/test_robustezza.py`
- **test_cronologia_non_leggibile_non_impedisce_l_avvio()** (2 connections) — `tests/test_robustezza.py`
- **.name()** (1 connections) — `fotofacile/core/scanner.py`
- **.parent()** (1 connections) — `fotofacile/core/scanner.py`
- **Test dei casi "fuori dal percorso felice": errori di disco, chiusura a metà,…** (1 connections) — `tests/test_robustezza.py`
- **salva_rotto()** (1 connections) — `tests/test_robustezza.py`
- **cancella()** (1 connections) — `tests/test_robustezza.py`

## Relationships

- [Interfaccia AdbBackend](Interfaccia_AdbBackend.md) (16 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (10 shared connections)
- [Piano di copia e percorsi](Piano_di_copia_e_percorsi.md) (7 shared connections)
- [Ricerca dei file sul telefono](Ricerca_dei_file_sul_telefono.md) (7 shared connections)
- [Telefono vero a passi (AdbAPassi)](Telefono_vero_a_passi_AdbAPassi.md) (7 shared connections)
- [Telefono finto a passi](Telefono_finto_a_passi.md) (4 shared connections)
- [Telefono demo](Telefono_demo.md) (4 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (4 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (4 shared connections)
- [Differenze di sistema (osutil)](Differenze_di_sistema_osutil.md) (4 shared connections)
- [Test copia reale](Test_copia_reale.md) (4 shared connections)
- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (3 shared connections)

## Source Files

- `fotofacile/core/planner.py`
- `fotofacile/core/scanner.py`
- `tests/test_robustezza.py`

## Audit Trail

- EXTRACTED: 89 (92%)
- INFERRED: 8 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
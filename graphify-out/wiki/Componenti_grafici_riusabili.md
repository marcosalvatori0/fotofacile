# Componenti grafici riusabili

> 20 nodes · cohesion 0.14

## Key Concepts

- **widgets.py** (19 connections) — `fotofacile/ui/widgets.py`
- **conftest.py** (15 connections) — `tests/conftest.py`
- **tk_available()** (14 connections) — `fotofacile/ui/widgets.py`
- **finestra_condivisa()** (5 connections) — `tests/conftest.py`
- **test_app_completa.py** (5 connections) — `tests/test_app_completa.py`
- **app()** (4 connections) — `tests/conftest.py`
- **fixture** (4 connections)
- **casa_temporanea()** (3 connections) — `tests/conftest.py`
- **root()** (3 connections) — `tests/conftest.py`
- **_prova_finestra()** (2 connections) — `fotofacile/ui/widgets.py`
- **test_app_non_si_avvia_senza_finestra_ma_spiega_il_problema()** (2 connections) — `tests/test_app_completa.py`
- **Componenti grafici riusabili: nessuna logica di business, solo presentazione.** (1 connections) — `fotofacile/ui/widgets.py`
- **True se questa macchina riesce davvero ad aprire una finestra. La verifica…** (1 connections) — `fotofacile/ui/widgets.py`
- **Impostazioni comuni dei test. Su macOS creare e distruggere più finestre Tk…** (1 connections) — `tests/conftest.py`
- **La finestra condivisa, azzerata prima e dopo ogni test.** (1 connections) — `tests/conftest.py`
- **Contenitore usa e getta per i test dei singoli componenti grafici. È una…** (1 connections) — `tests/conftest.py`
- **Cartella utente finta: i test non devono mai toccare i file reali dell'utente.** (1 connections) — `tests/conftest.py`
- **Collaudo completo dell'applicazione vera (avvio → copia → resoconto). Il…** (1 connections) — `tests/test_app_completa.py`
- **Diagnostica utile: se la finestra non è disponibile, la diagnosi lo dice.** (1 connections) — `tests/test_app_completa.py`
- **test_app_completa_la_copia_in_modalita_demo()** (1 connections) — `tests/test_app_completa.py`

## Relationships

- [Finestra e schermata opzioni](Finestra_e_schermata_opzioni.md) (11 shared connections)
- [Test della finestra](Test_della_finestra.md) (4 shared connections)
- [Telefono demo](Telefono_demo.md) (3 shared connections)
- [Errori di copia e nomi sicuri](Errori_di_copia_e_nomi_sicuri.md) (2 shared connections)
- [Aiuto Debug USB e appoggi test](Aiuto_Debug_USB_e_appoggi_test.md) (2 shared connections)
- [Test della schermata opzioni](Test_della_schermata_opzioni.md) (2 shared connections)
- [Appoggi per i test grafici](Appoggi_per_i_test_grafici.md) (2 shared connections)
- [Test del trasferimento (Passo 4)](Test_del_trasferimento_Passo_4.md) (2 shared connections)
- [Cronologia dei file copiati](Cronologia_dei_file_copiati.md) (2 shared connections)
- [Metodi della finestra App](Metodi_della_finestra_App.md) (2 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (1 shared connections)

## Source Files

- `fotofacile/ui/widgets.py`
- `tests/conftest.py`
- `tests/test_app_completa.py`

## Audit Trail

- EXTRACTED: 57 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
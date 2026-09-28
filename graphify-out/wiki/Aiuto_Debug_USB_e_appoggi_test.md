# Aiuto Debug USB e appoggi test

> 17 nodes · cohesion 0.18

## Key Concepts

- **attendi()** (30 connections) — `tests/aiuto.py`
- **test_page_connect.py** (20 connections) — `tests/test_page_connect.py`
- **build_help_text()** (6 connections) — `fotofacile/ui/page_connect.py`
- **test_aiuto_contiene_le_marche_e_i_passi()** (2 connections) — `tests/test_page_connect.py`
- **test_aiuto_per_marca_sconosciuta_non_lascia_vuoti()** (2 connections) — `tests/test_page_connect.py`
- **test_avanti_funziona_solo_con_telefono_pronto()** (2 connections) — `tests/test_page_connect.py`
- **test_modalita_demo_attivabile_dal_passo_1()** (2 connections) — `tests/test_page_connect.py`
- **test_nessun_telefono_invita_a_collegarlo()** (2 connections) — `tests/test_page_connect.py`
- **test_riavvio_collegamento_richiama_il_backend()** (2 connections) — `tests/test_page_connect.py`
- **test_riavvio_senza_componente_avvisa()** (2 connections) — `tests/test_page_connect.py`
- **test_riconosce_il_telefono_pronto()** (2 connections) — `tests/test_page_connect.py`
- **test_senza_componente_lo_dice_e_propone_installazione()** (2 connections) — `tests/test_page_connect.py`
- **test_telefono_non_autorizzato_mostra_istruzioni()** (2 connections) — `tests/test_page_connect.py`
- **Istruzioni in italiano per attivare il «Debug USB», personalizzate per marca.** (1 connections) — `fotofacile/ui/page_connect.py`
- **Fa girare il ciclo della grafica finché la condizione non è vera (o scade).** (1 connections) — `tests/aiuto.py`
- **test_con_componente_presente_il_pulsante_installazione_e_spento()** (1 connections) — `tests/test_page_connect.py`
- **test_sondaggio_attivo_al_primo_ingresso()** (1 connections) — `tests/test_page_connect.py`

## Relationships

- [Test del trasferimento (Passo 4)](Test_del_trasferimento_Passo_4.md) (6 shared connections)
- [Test della finestra](Test_della_finestra.md) (6 shared connections)
- [Test della schermata opzioni](Test_della_schermata_opzioni.md) (4 shared connections)
- [Appoggi per i test grafici](Appoggi_per_i_test_grafici.md) (4 shared connections)
- [adb a passi: operazioni](adb_a_passi-_operazioni.md) (3 shared connections)
- [Installazione del componente](Installazione_del_componente.md) (2 shared connections)
- [Errori con messaggio umano](Errori_con_messaggio_umano.md) (2 shared connections)
- [Componenti grafici riusabili](Componenti_grafici_riusabili.md) (2 shared connections)
- [Passo 1: collegamento](Passo_1-_collegamento.md) (1 shared connections)

## Source Files

- `fotofacile/ui/page_connect.py`
- `tests/aiuto.py`
- `tests/test_page_connect.py`

## Audit Trail

- EXTRACTED: 55 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*
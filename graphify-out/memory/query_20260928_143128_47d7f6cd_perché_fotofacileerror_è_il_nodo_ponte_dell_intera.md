---
type: "query"
date: "2026-09-28T14:31:28.557644+00:00"
question: "perché FotoFacileError è il nodo ponte dell'intera architettura?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["FotoFacileError", "App", "AdbAPassi", "ProcessoEsterno", "transfer", "ConnectPage", "Banner"]
---

# Q: perché FotoFacileError è il nodo ponte dell'intera architettura?

## Answer

Query espansa dal vocabolario del grafo: [error errore errori hint messaggio traduci adb app gui copia copiatore trasferimento]. Traversata BFS: 633 nodi a profondità 2. FotoFacileError (fotofacile/core/errors.py:8) ha grado 70 e attraversa 20 comunità (test_installer.py 10, FotoFacileError 9, ProcessoEsterno 8, ScaricatoreAPassi 4, adb_passi.py 4, AdbAPassi 4, test_robustezza.py 4, .copia 3, open_in_file_manager 3, TransferOptions 3, transfer.py 3, test_adb.py 3, +8). Relazioni: uses 26, calls 20, imports 16, inherits 3; fiducia 44 EXTRACTED / 26 INFERRED. Percorsi a 2 salti (EXTRACTED): FotoFacileError <-imports- app.py -imports-> ConnectPage; FotoFacileError <-imports- transfer.py -contains-> transfer(). Meccanismo: ogni strato (ProcessoEsterno ops.py:93, AdbAPassi.copia adb_passi.py:144, traduci_errore_file errors.py:33, installer.py:16) converte il proprio errore tecnico in FotoFacileError(message,hint); App.run_task (ui/app.py:183) è l'unico punto che lo trasforma nel Banner (ui/widgets.py:104), e i test (test_robustezza.py:14) fissano il contratto. Conclusione: il nodo più connesso non è la classe grande App ma la piccola eccezione condivisa: è la cucitura architetturale che rende possibile 'mai mostrare un errore tecnico'. Rischio: un errore sollevato senza hint peggiora l'esperienza ovunque.

## Outcome

- Signal: useful

## Source Nodes

- FotoFacileError
- App
- AdbAPassi
- ProcessoEsterno
- transfer
- ConnectPage
- Banner
# FotoFacile

Copia le foto dal telefono Android al computer in pochi clic: niente gestore file, niente
cartelle difficili da trovare, niente parole tecniche.

Funziona su **Windows**, **macOS** e **Linux** e non richiede di installare nulla di strano:
usa solo programmi già presenti nel computer (il linguaggio **Python** con la sua grafica).

## Cosa serve

- Un computer con **Python 3.9 o più recente** (su Windows va bene anche la versione del
  Microsoft Store; su Linux serve il pacchetto della grafica, per esempio `python3-tk`).
- Il cavo USB del telefono.
- Un minuto la prima volta, per autorizzare il telefono: lo fa il programma guidandoti.

## Avvio

| Sistema | Comando |
|---|---|
| Windows | `py fotofacile.py` |
| macOS | `python3 fotofacile.py` |
| Linux | `python3 fotofacile.py` |

Si apre una finestra con quattro passi. Premi **Avanti** per andare avanti e **Indietro** per
tornare: non si perde nulla, e le foto già copiate non vengono copiate di nuovo.

## La prima volta: autorizza il telefono

1. Collega il telefono con il cavo e **sblocca lo schermo**.
2. Nella prima schermata premi **«Come si attiva il Debug USB?»** e segui i passaggi della tua
   marca (Samsung, Xiaomi, Google, Huawei, Oppo…). È una procedura da fare **una volta sola**.
3. Quando il telefono chiede *«Consentire il debug USB?»*, tocca **Consenti**.
4. Il programma scrive **«Perfetto! Telefono collegato»**: premi **Avanti**.

Se il collegamento non riesce, prova un altro cavo USB (alcuni servono solo per ricaricare),
un'altra porta del computer, oppure premi **«Riavvia collegamento»**. Su Windows a volte serve
il driver USB del produttore del telefono.

Non hai un telefono a portata di mano? Premi **«Prova il programma senza telefono (demo)»**:
viene usato un telefono finto e puoi vedere tutta la procedura.

## Uso quotidiano

1. **Scegli le foto**: metti o togli la spunta alle cartelle trovate sul telefono (Camera,
   Screenshot, WhatsApp…). Puoi includere o escludere i video e copiare solo le foto più
   recenti di una certa data.
2. **Destinazione**: va bene la cartella proposta (per esempio *Immagini → FotoFacile → nome
   del telefono → data*). Le sottocartelle del telefono vengono mantenute.
3. **Copia**: vedi quante foto restano, a che velocità e quanto tempo manca. Puoi interrompere
   quando vuoi: le foto già copiate restano al sicuro e i file mezzi copiati vengono eliminati.
4. Alla fine puoi **aprire la cartella delle foto** e **salvare un resoconto** di quello che è
   stato copiato.

## Se qualcosa non va

| Messaggio | Cosa fare |
|---|---|
| «Non vedo ancora nessun telefono» | Controlla il cavo, sblocca lo schermo, prova un'altra porta USB |
| «Sbloccalo e tocca Consenti» | Guarda lo schermo del telefono: c'è una richiesta da approvare |
| «Il telefono non risponde» | Scollega e ricollega il cavo, poi premi «Riavvia collegamento» |
| «Manca il componente di collegamento» | Premi «Installa componente mancante» (serve internet) |
| «Non c'è abbastanza spazio» | Scegli un'altra cartella o libera spazio sul disco |
| «Non riesco ad aprire la finestra» | Su Linux installa «python3-tk»; poi esegui la diagnosi sotto |

Diagnosi completa del computer e del collegamento:

```
python3 fotofacile.py doctor      (Windows: py fotofacile.py doctor)
```

## Se il programma non si apre

1. **Modo più semplice**: doppio clic su **`Avvia FotoFacile.command`** nella cartella del
   progetto (si apre una finestra nera del Terminale: è normale, serve ad avviare il programma).
   In alternativa, doppio clic su **`dist/FotoFacile.app`**.
2. Se compare un avviso di macOS («sviluppatore non verificato»): **clic destro sull'app → Apri**
   (solo la prima volta; il pacchetto non è firmato).
3. Se non succede nulla, guarda il file **`~/.fotofacile/avvio.log`**: contiene la data e il
   motivo dell'ultimo tentativo.
4. Verifica la grafica con:
   ```
   python3 fotofacile.py --selftest      # apre e chiude la finestra, stampa l'esito
   python3 fotofacile.py doctor          # diagnosi completa del computer
   ```
   Se `--selftest` risponde `{"ok": true, ...}` la finestra funziona: il problema è solo il modo
   in cui il programma viene avviato (per esempio da una sessione non grafica).

Il programma **si adatta da solo alla modalità chiara o scura** del sistema (su macOS lo rileva
con `defaults read -g AppleInterfaceStyle`): prima, in modalità scura, il testo risultava scuro su
fondo scuro e la finestra sembrava vuota.

## Creare il pacchetto da regalare (build)

Per dare il programma a qualcuno che **non ha Python** si crea un pacchetto che contiene tutto:

```
python3 scripts/build_app.py            # crea dist/FotoFacile.app e l'archivio .zip
python3 scripts/build_app.py --verify   # crea e verifica subito il pacchetto
```

| Sistema | Cosa viene creato | Come si apre |
|---|---|---|
| macOS | `dist/FotoFacile.app` (+ `.zip` da condividere) | doppio clic; la prima volta **clic destro → Apri** (il pacchetto non è firmato) |
| qualsiasi | `Avvia FotoFacile.command` | doppio clic: avvia la versione da sorgente (serve Python) |
| Windows | `dist/FotoFacile/FotoFacile.exe` | doppio clic (si può zippare la cartella `dist/FotoFacile`) |
| Linux | `dist/FotoFacile/FotoFacile` | `./dist/FotoFacile/FotoFacile` |

Il pacchetto pesa circa 25–55 MB, non richiede installazioni e si comporta come la versione da
sorgente (compreso il download automatico del componente di collegamento). Per verificare un
pacchetto: `FotoFacile.app/Contents/MacOS/FotoFacile --selftest` (apre e chiude la finestra e
stampa l'esito), oppure `... doctor` per la diagnosi. L'icona è generata da
`python3 scripts/make_icon.py` (nessuna libreria esterna).

## Installer pronti da scaricare (GitHub)

Ogni versione pubblicata ha gli installer costruiti automaticamente su computer veri:

**https://github.com/marcosalvatori0/fotofacile/releases/latest**

| File | A cosa serve |
|---|---|
| `FotoFacile-Setup-<versione>.exe` | installer Windows: copia il programma, crea i collegamenti sul Desktop e nel menu Start, registra la disinstallazione in Impostazioni → App |
| `FotoFacile-portable.zip` | Windows senza installare nulla: si scompatta e si usa |
| `FotoFacile-<versione>.dmg` | installer macOS: si apre e si trascina l'app in Applicazioni |

Gli installer li costruisce la pipeline in `.github/workflows/build-installers.yml` (runner macOS e Windows) e prima di pubblicarli esegue l'autocollaudo del programma.

## Cartella pronta per Windows

`python3 scripts/crea_pacchetto_windows.py` crea sulla Scrivania la cartella
**«FotoFacile per Windows»**, con dentro il programma completo, due file da doppio clic e le
istruzioni (`LEGGIMI - Windows.txt`):

| File | Cosa fa |
|---|---|
| `Avvia FotoFacile.bat` | fa partire il programma subito; se Python manca lo installa (winget) o spiega come fare |
| `Crea l'eseguibile per Windows.bat` | crea `dist\FotoFacile\FotoFacile.exe` con PyInstaller e lo verifica subito con l'autocollaudo |

**Perché una cartella e non un `.exe` già pronto:** un eseguibile Windows si può creare e
collaudare **solo su Windows** (PyInstaller non compila da un sistema per un altro). Un `.exe`
prodotto su macOS non sarebbe verificabile, quindi non è stato incluso: la cartella permette di
ottenerlo con un doppio clic, e di usare il programma anche senza creare nulla.

## Collaudo automatico (per chi vuole verificare)

```
# 1. controllo completo di tutta la logica (nessuna finestra richiesta)
python3 -m pytest tests -q

# 2. collaudo della vera finestra: attraversa i quattro passi in modalità demo
#    e verifica che i file finiscano davvero sul disco
FF_DEST="$HOME/Desktop/CollaudoFotoFacile" FF_ESITO="/tmp/esito-fotofacile.json" python3 tests/pilota_app.py
```

Il secondo comando apre la finestra vera, la guida da solo e scrive l'esito in
`esito-fotofacile.json`: è il modo più rapido per essere sicuri che sul *tuo* computer la
procedura completa funzioni.

## Per chi sviluppa

- `fotofacile/core/` — logica pura e testabile (nessuna dipendenza dalla grafica):
  collegamento al telefono, ricerca delle foto, piano di copia, copia, cronologia, resoconto.
- `fotofacile/ui/` — interfaccia Tkinter: quattro schermate, nessuna logica di business.
- **Scelta importante:** il programma **non usa thread**. Le operazioni lunghe sono
  generatori che avanzano a piccoli passi dentro il ciclo della grafica
  (`fotofacile/core/ops.py`, `fotofacile/core/adb_passi.py`). Così l'interfaccia resta
  reattiva anche su combinazioni in cui la grafica non è sicura con i thread
  (per esempio macOS con Tk 9).
- Specifica: `docs/superpowers/specs/2026-09-28-fotofacile-design.md`
- Piano di lavoro: `docs/superpowers/plans/2026-09-28-fotofacile.md`
- Dipendenze: nessuna per l'uso; `pytest` solo per lo sviluppo (`requirements-dev.txt`).

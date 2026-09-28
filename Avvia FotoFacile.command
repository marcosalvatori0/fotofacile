#!/bin/bash
# Avvia FotoFacile (doppio clic). Chiudendo questa finestra il programma si chiude.
cd "$(dirname "$0")" || exit 1
echo "Avvio di FotoFacile…"
python3 fotofacile.py "$@"
codice=$?
if [ $codice -ne 0 ]; then
  echo "Il programma è uscito con codice $codice. Diagnosi:"
  python3 fotofacile.py doctor
fi
echo "Puoi chiudere questa finestra."

#!/bin/bash

# 1 - Effettua uno screenshot di una selezione
# Usa scrot per fare uno screenshot dell'area selezionata e salvalo in una cartella temporanea
TEMP_SCREENSHOT="/tmp/screenshot_temp.png"
grim -g "$(slurp)" "$TEMP_SCREENSHOT"
if [ $? -ne 0 ]; then
    echo "grim non è riuscito a fare lo screenshot. Uscita..."
    exit 1
fi
# 1a - Rimozione dello sfondo usando GraphicsMagick
# Supponiamo che lo sfondo sia bianco, puoi cambiare "white" con altri colori, se necessario
gm convert "$TEMP_SCREENSHOT" -fuzz 50% -transparent white "$TEMP_SCREENSHOT"

# 2 - Usa rofi per richiedere un nome per lo screenshot
FILENAME=$(zenity --entry --text="Inserisci il nome dello screenshot")

# Verifica che l'utente abbia inserito un nome
if [ -z "$FILENAME" ]; then
    echo "Nessun nome fornito, uscita."
    exit 1
fi

# Aggiungi estensione al file
FILENAME="${FILENAME}.png"

# 3 - Inserisce lo screenshot dentro una cartella specifica
DESTINATION_DIR="$HOME/current_course/figures"  # Puoi cambiare la cartella di destinazione
mkdir -p "$DESTINATION_DIR"
mv "$TEMP_SCREENSHOT" "$DESTINATION_DIR/$FILENAME"

# 4 - Copia nella clipboard il nome completo del file (con estensione)
LATEX_BLOCK="\\\begin{figure}[H]\n\\centering\n\\includegraphics[scale=.5]{$FILENAME}\n\\\end{figure}"



printf "$LATEX_BLOCK" | wl-copy

# Conferma operazione completata
notify-send "Screenshot salvato come $FILENAME e copiato nella clipboard."


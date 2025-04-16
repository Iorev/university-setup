import os
import subprocess
import sys
from pathlib import Path
from unilib.rofi import rofi

# Funzione per rinominare il file
def rename_file(file_path):
    print("Sto rinominando il file")
    if str(file_path).endswith('.mp4'):
        if str(file_path).startswith('done-'):
            new_name = str(file_path)[5:]  # Rimuovi 'done-' dalla parte iniziale
            os.rename(file_path, new_name)
            print(f"File rinominato in: {new_name}")
        else:
            new_name = f"done-{os.path.basename(file_path)}"
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
            print(f"File rinominato in: {new_name}")
    else:
        print("Rinominazione non applicabile: non è un file mp4.")

# Imposta il percorso di default
default_folder_path = "/home/lorev/current_course/"

# Gestisci il percorso passato come argomento
if len(sys.argv) > 1 and sys.argv[1].startswith("/home/lorev/current_course/"):
    folder_path = sys.argv[1]
else:
    folder_path = os.path.join(default_folder_path, sys.argv[1] if len(sys.argv) > 1 else '')

# Mostra il percorso
print(f"Percorso della cartella: {folder_path}")

# Trova i file nel percorso specificato
files = []
for file in Path(folder_path).rglob('*'):
    if file.is_file() and not any(file.suffix == ext for ext in ['.aux', '.log', '.latexmain', '.out', '.toc', '.fdb_latexmk', '.fls', '.gz', '.nav', '.sty', '.snm']):
        if not file.match('*/lec_[0-9][0-9].tex'):
            files.append(file)

files.sort()

# Se non ci sono file trovati
if not files:
    print("Nessun file trovato nel percorso specificato.")
    sys.exit(1)

# Crea una lista di nomi di file per rofi

file_names = [file.name for file in files]

# Usa rofi per selezionare un file
key, index, selected_file_name = rofi('Scegli un file', file_names,[
    '-kb-custom-1','Ctrl+y',
    '-auto-select',
])

# Verifica se è stato selezionato un file
if not selected_file_name:
    print("Nessun file selezionato.")
    sys.exit(1)

# Trova il percorso completo del file selezionato
selected_file = None
for file in files:
    if file.name == selected_file_name:
        selected_file = file
        break

# Verifica se il file selezionato è stato trovato
if selected_file is None:
    print("File selezionato non trovato.")
    sys.exit(1)

# Se è stato premuto Ctrl+y
if key == 1:
    rename_file(selected_file)
    sys.exit(0)

# Esegui l'applicazione appropriata in base al tipo di file
if selected_file.suffix == '.pdf':
    subprocess.run(['zathura', str(selected_file)])
elif selected_file.suffix == '.mp4':
    subprocess.run(['vlc', str(selected_file)])
else:
    subprocess.run(['kitty', 'nvim', str(selected_file)])

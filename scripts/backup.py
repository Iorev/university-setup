#!/usr/bin/python3
import shutil
from pathlib import Path
from courses import Courses

# Specifica qui il percorso di destinazione
DESTINATION_DIR = '/home/lorev/Dropbox/PdfDocs/'
#DESTINATION_DIR.mkdir(parents=True, exist_ok=True)  # Crea la directory se non esiste

for course in Courses():
    lectures = course.lectures
    #print(f'{course.name}')
    # Compila il master e controlla il risultato
    #if lectures.compile_master() == 0:  # Se la compilazione ha successo
    output_pdf = course.path / 'master.pdf'  # Modifica se il nome del file è diverso
    if output_pdf.exists():
        #print(f'{output_pdf}')
        dst = DESTINATION_DIR + course.name +'.pdf'
        shutil.copyfile(output_pdf, Path(dst).expanduser())
        print(f'File copiato in {dst}')
    else:
        print(f'Il file {output_pdf} non esiste.')
    #else:
        #print(f'Compilazione fallita per il corso {course.name}.')


#!/usr/bin/python3
import shutil
from pathlib import Path
from courses import Courses
# Specifica qui il percorso di destinazione
DESTINATION_DIR = '/home/lorev/ownCloud/appunti pdf/'
#DESTINATION_DIR.mkdir(parents=True, exist_ok=True)  # Crea la directory se non esiste

for course in Courses():
    lectures = course.lectures
    r = lectures.parse_range_string('all')
    lectures.update_lectures_in_master(r)
    print(f'compilo una volta {course.name}')
    lectures.compile_master()
    print(f'compilo una seconda volta {course.name}')
    lectures.compile_master()
    output_pdf = course.path / 'master.pdf'  
    if output_pdf.exists():
        print(f'Il file {output_pdf} esiste, eseguo il caricamento')
        dst = DESTINATION_DIR + course.name +'.pdf'
        shutil.copyfile(output_pdf, Path(dst).expanduser())
        print(f'File copiato in {dst}')
    else:
        print(f'Il file {output_pdf} non esiste.')
    #else:
        #print(f'Compilazione fallita per il corso {course.name}.')


#!/usr/bin/python3
import shutil
from pathlib import Path
from courses import Courses
import subprocess
DESTINATION_DIR = '/home/lorev/ownCloud/appunti pdf/'
DST_FILES_DIR = '/home/lorev/ownCloud/polimi/'
try:
    for course in Courses():
        NTFY_TITLE = f'{course.name}'
        NTFY_SUBTITLE = 'backup effettuato!'
        try:
            if course.name == "PF2CFU":
                print("Compilo PF2CFU")
                output_pdf = course.path / 'Presentazione2cfu/main.pdf'
                result = subprocess.run(
                    ['pdflatex', '-f', '-interaction=nonstopmode',str(course.path) + '/Presentazione2cfu/main.tex'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=(str(course.lectures.root))
                )
                print(f"RETURN CODE = {result.returncode}")
                
            else:
                lectures = course.lectures
                r = lectures.parse_range_string('all')
                lectures.update_lectures_in_master(r)
                print(f'compilo una volta {course.name}')
                lectures.compile_master()
                print(f'compilo una seconda volta {course.name}')
                lectures.compile_master()
                output_pdf = course.path / 'master.pdf'
            if output_pdf.exists():
                print(f'✅Il file {output_pdf} esiste')
                dst = DESTINATION_DIR + course.name +'.pdf'
                shutil.copyfile(output_pdf, Path(dst).expanduser())
                subprocess.run(['dunstify',"✅" + NTFY_TITLE,NTFY_SUBTITLE])
            else:
                subprocess.run(['dunstify',"-b","-u","critical","-t"," 10000","❌" +NTFY_TITLE,"backup failed, file doesn't exists"])
                print(f'❌Il file {output_pdf} non esiste.')
            #else:
                #print(f'Compilazione fallita per il corso {course.name}.')
    
        except Exception as e:
                subprocess.run(['dunstify',"-b","-u","critical","-t","10000","❌"+NTFY_TITLE,f"backup failed! {e}"])
    
except Exception as e:
                subprocess.run(['dunstify',"-b", "-u","critical","-t","10000","❌"+"ERROR!!!",f"backup failed! {e}"])

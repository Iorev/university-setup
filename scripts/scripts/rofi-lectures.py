#!/usr/bin/python3
from unilib.courses import Courses
from unilib.rofi import rofi
from unilib.utils import generate_short_title, MAX_LEN

lectures = Courses().current.lectures

sorted_lectures = sorted(lectures, key=lambda l: -l.number)

options = [
    "{number: >2}. <b>{title: <{fill}}</b> <span size='smaller'>{date}</span>".format(
    #"{number: >2}. <b>{title: <{fill}}</b> <span size='smaller'>{date}  ({week})</span>".format(
        fill=MAX_LEN,
        number=lecture.number,
        title=generate_short_title(lecture.title),
        date=lecture.date.strftime('%a %d %b'),
        #week=lecture.week
    )
    for lecture in sorted_lectures
]

key, index, selected = rofi('Select lecture', options, [
    '-lines', 5,
    '-no-auto-select',
    '-markup-rows',
    '-kb-row-down', 'Down',
    '-kb-custom-1', 'Ctrl+n'
])

if key == 0:
    sorted_lectures[index].edit()
elif key == 1:
    new_lecture = lectures.new_lecture()
    new_lecture.edit()

from config import *
from PyQt5.QtWidgets import QLabel

run([
    ('Basic label', label('Hello world!')),
    ('Basic label2', label('Hello world!')),
    ('Label with attr', m('label', '<b>Bold and indent</b>', {'indent': 20})),
    ('Nested label', m('label', 'parent', m('label', '      child'))),

    ('tag type', m(QLabel, 'Hello world!'))
])

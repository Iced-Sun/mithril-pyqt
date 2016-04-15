from config import *
from PyQt5.QtWidgets import QLabel

run([
    ('Label', label('Hello world!')),
    ('Label with attr', m('label', '<b>Bold and indent</b>', {'indent': 20})),
    ('Nested label', m('label', 'parent', m('label', 'child', {'indent': 60}))),

    ('tag type', m(QLabel, 'Hello world!'))
])

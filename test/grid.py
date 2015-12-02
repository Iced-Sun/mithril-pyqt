from config import *

## TODO span and optional arguments support
run([
    ('G41', m('widget', [
        {
            'layout': 'grid',
        },
        label('1'),
        label('2'),
        label('3'),
        label('4'),
    ])),

    ('G22', m('widget', [
        {
            'layout': 'grid',
            'columns': 2
        },
        label('1'), label('2'),
        label('3'), label('4'),
    ])),

    ('G33', m('widget', [
        {
            'layout': 'grid',
            'columns': 3,
        },
        label('1'), None,       label('3'),
        None,       label('5'), None,
        label('7'), None,       label('9')
    ])),

    ('G+nest', m('widget', [
        {
            'layout': 'grid',
            'columns': 2
        },
        [label('1-1'), label('1-2')],
        (label('2-1'), label('2-2')),
        label('3'),
        label('4'),
    ])),
])


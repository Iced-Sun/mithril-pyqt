from config import *

run([(
    'G41', m('widget', [
        {'container': 'grid',},
        label('1'),
        label('2'),
        label('3'),
        label('4'),
    ])),

    ('G22', m('widget', [
        {
            'container': 'grid',
            'columns': 2
        },
        label('1'), label('2'),
        label('3'), label('4'),
    ])),

    ('G33', m('widget', [
        {
            'container': 'grid',
            'columns': 3,
        },
        label('1'), None,       label('3'),
        None,       label('5'), None,
        label('7'), None,       label('9')
    ])),

    ('G+nest', m('widget', [
        {
            'container': 'grid',
            'columns': 2
        },
        [label('1'), label('1')], (label('2'), label('2')),
        label('3'),               label('4'),
    ])),

    ('G+nest(args)', m('widget', [
        {
            'container': 'grid',
            'columns': 3
        },

        m.add([label('1'), label('1')], 1, 2),  None,       label('3'),
        m.add((label('4'), label('4')), 2, 1),  label('5'), label('6'),
        None,                                   label('8'), label('9')
    ])),

    ('G33+args', m('widget', [
        {
            'container': 'grid',
            'columns': 3
        },

        m.add(label('1'), 2, 2), None,                  label('3'),
        None,                    None,                  label('6'),
        label('7'),              m.add(label('8'),1,2), None
    ])),
])


from config import *

from PyQt5.QtCore import Qt

run([
    ('H', m('Widget', [label('1'), label('2'), label('3')])),
    ('H+item', m('Widget', [label('1'), 'stretch', label('2'), label('3')])),
    ('H+item(arg)', m('Widget', ['stretch', label('1'), {'spacing': 80}, label('2'), label('3')])),

    #('H+item/attrs', m('Widget', [{'spacing': 20,}])),                # ambiguous: setSpacing or addSpacing?
    ('H+de-ambiguous item', m('Widget', [{}, {'spacing': 20,}])),             # addSpacing
    ('H+de-ambiguous attr', m('Widget', [{'layout': True, 'spacing': 20,}])), # setSpacing

    ('H+full-demo', m('Widget', [ # [] denotes a HBox by default
        {
            'layout': 'v_box',    # but use VBox instead
            'spacing': 20,        # setSpacing
        },

        label('1'),               # item begin
        label('2'),
        {'spacing': 60},          # addSpacing
        label('3')
    ])),

    ('H+widget', m('Widget', [
        {'widget': (label('1'), 0, Qt.AlignLeft)}, # positional arguments

        {
            'widget': label('2'),                  # positional arguments
            'alignment': Qt.AlignJustify           # keyword arguments
        },

        {
            'widget': (label('3'),0),              # positional arguments
            'alignment': Qt.AlignRight             # keyword arguments
        },
    ])),

    ('H', m('Widget', [label('1'), label('2'), label('3')])),
    ('V', m('Widget', (label('1'), label('2'), label('3')))),
    ('HH', m('Widget', [
        [label('1'), label('2'), label('3')],
        [label('4'), label('5'), label('6')],
    ])),
    ('HV', m('Widget', [
        (label('1'), label('2'), label('3')),
        (label('4'), label('5'), label('6')),
    ])),
    ('VH', m('Widget', (
        [label('1'), label('2'), label('3')],
        [label('4'), label('5'), label('6')],
    ))),
    ('VV', m('Widget', (
        (label('1'), label('2'), label('3')),
        (label('4'), label('5'), label('6')),
    ))),
])


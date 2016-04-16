from config import *

from PyQt5.QtCore import Qt
run([
    ## fundamental support
    ('No layout', m('widget', [{'container': None}, label('1'), label('  2')])),
    ('H', m('Widget', [label('1'), label('2'), label('3')])),
    ('H+attr', m('Widget', [{'container': True, 'spacing': 30}, label('1'), label('2')])),

    ## nested layout
    ('H', m('widget', [label('1'), label('2'), label('3')])),
    ('V', m('widget', (label('1'), label('2'), label('3')))),
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

    ## adder
    ('H+item', m('widget', [label('1'), 'stretch', label('2'), label('3')])),
    ('H+item(arg)', m('Widget', ['stretch', label('1'), m.add('spacing', 80), label('2'), label('3')])),

    ('H+full', m('Widget', [ # [] denotes a HBox by default
        {
            'container': 'v_box',    # but use VBox instead
            'spacing': 20,        # setSpacing
        },

        label('1'),               # item begin
        label('2'),
        m.add('spacing', 60),
        label('3')
    ])),

    ('H+widget(args)', m('Widget', [
        m.add(label('1'), 0, Qt.AlignLeft),
        m.add(label('2'), alignment=Qt.AlignJustify),
        label('3')
    ])),
])

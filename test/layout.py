from config import *

run([
    ('H', m('Widget', [label('1'), label('2'), label('3')])),
    ('H+item', m('Widget', [label('1'), 'stretch', label('2'), label('3')])),
    ('H+item(arg)', m('Widget', ['stretch', label('1'), ('spacing', 80), label('2'), label('3')])),
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
    ### grid layout??
])

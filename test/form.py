from config import *
run([
    ('Form', m('widget', [
        {
            'layout': 'form'
        },

        label('1'),               # addWidget
        m.add('row', label('1')), # addRow

        m.add('row', 'Name',       m('line_edit')),
        m.add('row', label('Age'), m('spin_box')),
        m.add('row', 'HBox',       [m('line_edit'), m('line_edit')]),
        m.add('row', 'VBox',       (m('line_edit'), m('line_edit'))),
        m.add('row', 'HVBox',      [(m('line_edit'), m('line_edit')), (m('line_edit'), m('line_edit'))]),
    ])),
])


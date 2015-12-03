from config import *

run([
    ('Form', m('widget', [
        {
            'layout': 'form'
        },

        label('1'),
        m.add('row', 'Name',       m('line_edit')),
        m.add('row', label('Age'), m('spin_box')),
        m.add('row', 'VBox',       (m('line_edit'), m('line_edit'))),
        m.add('row', 'HBox',       [m('line_edit'), m('line_edit')]),
        m.add('row', m('text_edit'))
    ])),
])

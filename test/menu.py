from config import *

run([
    ('widget+action', m('widget', m('action', 'Action'))),

    ('widget+menu+action', m('widget', m('menu', 'Menu', m('action', 'Action')))),
    ('widget+[menu+action]', m('widget', [m('menu', 'Menu', m('action', 'Action'))])),
    ('widget+menubar+action', m('widget', m('menu_bar', m('action', 'Action')))),
    ('widget+menubar+menu+action', m('widget', m('menu_bar', m('menu', m('action', 'Action'))))),
    
    ('widget+[menubar+menu+action]', m('widget', [
        m('menu_bar', m('menu', 'Menu', m('action', 'Action'))), label('1'), label('2')
    ])),
    ('widget+[].setMenuBar', m('widget', [
        {
            'container': 'grid',
            'columns': 2,
            'menu_bar': m('menu_bar', m('menu', 'Menu', m('action', 'Action'))),
        },
        label('1'), label('2'), label('3'), label('4')
    ])),

    ('widget+[].setMenuBar(adders)', m('widget', [
        {
            'menu_bar': m('menu_bar', m('menu', 'Menu', [
                m('action', 'Auto A'),
                m('action', 'Auto B'),
                'separator',
                m.add('action', 'Adder C'),
                m.add('action', 'Adder D'),
                m.add('section', 'Section'),
                m('action', 'Auto E'),
                m('action', 'Auto F'),
            ])),
        },
    ])),

    ('widget+[].setMenuBar(nested menu)', m('widget', [
        {
            'menu_bar': m('menu_bar', m('menu', 'Menu', [
                m('action', 'Auto Action'),
                m('menu',   'Auto Menu', m('action', 'Auto Action')),
                m('menu',   'Auto Menu', [m('action', 'Auto Action'), m('action', 'Auto Action')]),
                'separator',
                m.add('menu', 'Adder Menu'),
                m.add('action', m('action', 'Adder Action')),
                m.add('menu', m('menu', 'Adder Menu'))
            ])),
        },
    ])),

    ('widget+[].setMenuBar(menu with action group)', m('widget', [
        {
            'menu_bar': m('menu_bar', m('menu', 'Menu', [
                m.add('section', 'Not an Action Group'),
                [
                    m('action', 'Action A', {'checkable': True}),
                    m('action', 'Action B', {'checkable': True})
                ],
                m.add('section', 'Implicit Action Group'),
                (
                    m('action', 'Action 1', {'checkable': True}),
                    m('action', 'Action 2', {'checkable': True})
                ),
                m.add('section', 'Explicit Action Group'),
                m('action_group', [
                    m('action', 'Action 3', {'checkable': True}),
                    m('action', 'Action 4', {'checkable': True})
                ]),
            ])),
        }
    ]))
])

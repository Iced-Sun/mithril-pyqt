from config import *

'''
run([
    ('invisible action@widget', m('widget', m('action', 'Action'))),
    ('invisible menu & action@widget', m('widget', m('menu', 'Menu', m('action', 'Action')))),
    ('invisible menu & visible action@widget+layout', m('widget', (m('menu', 'Menu', m('action', 'Action')),))),

    ('menubar@widget', m('widget', [m('menu_bar', m('menu', 'Menu', m('action', 'Action'))), label('1'), label('2')])),
    ('menubar in layout@widget', m('widget', [
        {
            'layout': 'grid_layout',
            'spacing': 20,
            'menu_bar': m('menu_bar', m('menu', 'Menu', m('action', 'Action'))),
        },
        label('1'), label('2')
    ])),

    ('multiple actions', m('widget', [
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

    ('nested menu', m('widget', [
        {
            'menu_bar': m('menu_bar', m('menu', 'Menu', [
                m('action', 'Auto Action'),
                m('menu',   'Auto Menu', m('action', 'Auto Action')),
                m('menu',   'Auto Menu', [m('action', 'Auto Action'), m('action', 'Auto Action')]),
                'separator',
                m.add('menu', 'Adder Menu'),
                ## we don't support add_*(m()), because it's just both ugly and subtle
                #m.add('action', m('action', 'Adder Action'))
                #m.add('menu', m('menu', 'Adder Menu'))
            ])),
        },
    ])),
])

'''

run([('test', m('widget', m('menu', 'Menu')))])

'''
run([
    ('menu with action group', m('widget', [
        {
            'menu_bar': m('menu_bar', m('menu', 'Menu', [
                m('action', 'Auto A'),
                #'separator',
                m('action_group', [m('action', 'Auto Action', {'checkable': True}), m('action', 'Auto Action', {'checkable': True})]),
                m('menu', 'Sub Menu', m('action_group', [m('action', 'Auto Action'), m('action', 'Auto Action')]))
                #'separator',
                #(m('action', 'Auto B-1', {'checkable': True}), m('action', 'Auto B-2', {'checkable': True})),
                #[m('action', 'Auto C-1'), m('action', 'Auto C-2')],
                #'separator',
            ])),
        }
    ]))
])
'''

'''
    #('', m('widget', m('menu', [m('action', 'Action A'), m('action', 'Action B'), 'Action C'])
    #return m('widget', m('menu', [m('action', 'action1'), m('action', 'action2')]))

    #('main_window', m('main_window', [label('1'), label('2'), label('3')])),
    #('main_window', m('main_window', {'central_widget': label('central')}, [label('1'), label('2'), label('3')])),

    #('menubar+menu@mainwindow', m('main_window', m('menu_bar', m('menu', 'File', m('action', 'action1'))))),
'''


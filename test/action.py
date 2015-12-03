from config import *

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
                m('action', 'Auto A'),
                'separator',
                m.add('menu', m('menu', 'Adder menu A', m('action', 'Auto B'))),
                m.add('menu', 'Adder menu B'),
                ## FIXME should support this?
                #m('menu', 'Auto menu', m.add('action', 'Auto C')),
                m('menu', 'Auto menu', m('action', 'Auto C')),

                m('menu', 'Auto menu with multiple actions', [m('action', 'Auto D'), m('action', 'Auto E')]),
            ])),
        },
    ])),

    ('menu with action group', m('widget', [
    ]))

    #('', m('widget', m('menu', [m('action', 'Action A'), m('action', 'Action B'), 'Action C'])
    #return m('widget', m('menu', [m('action', 'action1'), m('action', 'action2')]))

    #('main_window', m('main_window', [label('1'), label('2'), label('3')])),
    #('main_window', m('main_window', {'central_widget': label('central')}, [label('1'), label('2'), label('3')])),

    #('menubar+menu@mainwindow', m('main_window', m('menu_bar', m('menu', 'File', m('action', 'action1'))))),
])


'''
we have three relationships to support: parent-child, add_*, set_*

parent-child is not necessarily visually parent-child

generally, add_* is not owning

rule of thumb:
set_* is in attribute
add_* is in children with attach_method
parent_child is in children

|             | QWidget          | QToolBar   | QMenuBar   | QMenu   | QAction      | misc.                    |
|-------------+------------------+------------+------------+---------+--------------+--------------------------|
| QMainWindow | setCentralWidget | addToolBar | setMenuBar |         |              | addToolBarBreak          |
| QWidget     | addWidget        |            | addWidget  | -       | addAction(s) |                          |
| QMenuBar    |                  |            |            | addMenu | addAction    | addSeparator             |
| QMenu       |                  |            |            | addMenu | addAction    | addSection, addSeparator |
| QToolBar    |                  |            |            |         | addAction    | addSeparator, addWidget  |
| QLayout     |                  |            | setMenuBar |         |              |                          |
'''

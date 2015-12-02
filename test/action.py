from config import *

#return m('main_window', m('menu_bar', m('menu', 'File', m('action', 'action1'))))
#return m('widget', m('menu_bar', m('menu', 'File', m('action', 'action1'))))
#return m('widget', m('menu', [m('action', 'action1'), m('action', 'action2')]))

run([
    ('menubar@widget', m('widget', [m('menu_bar', m('menu', 'Menu', m('action', 'Action'))), label('1'), label('2')])),

    ('menubar in layout@widget', m('widget', [
        {
            'layout': 'grid_layout',
            'spacing': 100,
            'menu_bar': m('menu_bar', m('menu', 'Menu', m('action', 'Action'))),
        },
        label('1'),
        label('2')
    ])),

    ('invisible menu & action@widget', m('widget', m('menu', 'Menu', m('action', 'Action')))),
    ('invisible menu & visible action@widget', m('widget', (m('menu', 'Menu', m('action', 'Action')), label('Label')))),

    #('action@widget', m('widget', m('action', 'action1'))),

    #('main_window', m('main_window', [label('1'), label('2'), label('3')])),
    #('main_window', m('main_window', {'central_widget': label('central')}, [label('1'), label('2'), label('3')])),

    #('menubar+menu@mainwindow', m('main_window', m('menu_bar', m('menu', 'File', m('action', 'action1'))))),

    #('menu', m('widget', m('menu', m('action', 'action1')))),
    #('mixed action+widget', m('widget', (m('action', 'action2'), label('other')))),
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

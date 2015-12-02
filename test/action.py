from config import *

#return m('main_window', m('menu_bar', m('menu', 'File', m('action', 'action1'))))
#return m('widget', m('menu_bar', m('menu', 'File', m('action', 'action1'))))
#return m('widget', m('menu', [m('action', 'action1'), m('action', 'action2')]))

run([
    ('menubar@widget', m('widget', [m('menu_bar', m('menu', 'File', m('action', 'action1'))), label('1'), label('2')])),

    ('menubar in layout@widget', m('widget', [
        {
            'layout': 'grid_layout',
            'spacing': 100,
            'menu_bar': m('menu_bar', m('menu', 'File', m('action', 'action1'))),
        },
        label('1'),
        label('2')
    ])),

    ### FIXME have different behavior
    #('menu@widget', m('widget', m('menu', 'File', m('action', 'action1')))),
    #('menu@widget', m('widget', (m('menu', 'File', m('action', 'action1')), label('other')))),

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

|             | QWidget          | QToolBar   | QMenuBar   | QMenu   | QAction      | misc.                    |
|-------------+------------------+------------+------------+---------+--------------+--------------------------|
| QMainWindow | setCentralWidget | addToolBar | setMenuBar |         |              | addToolBarBreak          |
| QWidget     | addWidget        |            | addWidget  | -       | addAction(s) |                          |
| QMenuBar    |                  |            |            | addMenu | addAction    | addSeparator             |
| QMenu       |                  |            |            | addMenu | addAction    | addSection, addSeparator |
| QToolBar    |                  |            |            |         | addAction    | addSeparator, addWidget  |
| QLayout     |                  |            | setMenuBar |         |              |                          |
'''

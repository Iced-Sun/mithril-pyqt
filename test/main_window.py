from config import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

menu_bar = m('menu_bar', m('menu', 'File', m('action', 'action1')))
central_widget = m('widget', [label('AAA'), label('BBB'), label('CCC')])

run([
    ('main_window', m('main_window', {
        'window_title': 'Main',
        'window_icon': QIcon(':icons/battery-full.png'),     # both are OK
        'window_icon': m('icon', ':icons/battery-full.png'),
        'menu_bar': menu_bar,
        'central_widget': central_widget,
        'status_bar': m('status_bar')
    }, [
        m('tool_bar', m('action', 'action 1')),
        'tool_bar_break',
        m('tool_bar', m('action', 'action 2')),
        m.add('tool_bar', Qt.LeftToolBarArea, m('tool_bar', m('action', 'action 3')))
    ]))
])


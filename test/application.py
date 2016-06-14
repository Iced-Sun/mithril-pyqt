from config import *

mode_actions1 = (
    m('action', m('icon', ':icons/non-starred.png'), '<'),
    m('action', m('icon', ':icons/semi-starred-rtl.png'), '|'),
    m('action', m('icon', ':icons/starred.png'), '>'),
)

mode_actions = (
    m('action', '1', {'checkable': True}),
    m('action', '2', {'checkable': True}),
    m('action', '3', {'checkable': True}),
)

menu_bar = m('menu_bar', [
    m('menu', 'File', [mode_actions]),
    m('menu', 'Edit', [mode_actions])
])

central_widget = m('widget')

run(m('main_window', {
    'window_title': 'Application',
    'window_icon': m('icon', ':icons/battery-full.png'),
    'menu_bar': menu_bar,
    'central_widget': central_widget,
    'status_bar': m('status_bar')
}, [
    m('tool_bar', {'id': 'toolbar-file'}, m('action', 'shit')),
    m('tool_bar', {'id': 'toolbar-default'}),
    m('tool_bar', [mode_actions])
]))

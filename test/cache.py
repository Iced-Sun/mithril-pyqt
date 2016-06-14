from config import *

the_label = m('label', 'non cachable widget')
the_action = m('action', 'cachable action')

run(m('widget', [
    m('menu', [the_action, the_action, m('action', 'another action')]),
    the_label, the_label
]))

from mithril import *

from PyQt5.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self,*args):
        super().__init__(*args)
        print('label created')
    def __del__(self):
        print('label deleted')
    pass

#cell = m('Label', 'Hello world')
cell = m(Label, 'Hello world', {'margin': 10}, m('tool_bar'))

print(cell)

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

_ = m.render(None, cell)

sys.exit(app.exec())


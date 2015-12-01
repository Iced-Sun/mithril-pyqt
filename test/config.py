import sys
sys.path.append(sys.path[0]+'/../')

from mithril import *

def label(title):
    return m('Label', title)

def run(cell):
    import json
    print(json.dumps(cell, indent=2, ensure_ascii=False, default=lambda value: repr(value)))

    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet("* {border: 1px solid}")

    if isinstance(cell, list):
        from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel
        root = QWidget()
        layout = QGridLayout()
        for i, elem in enumerate(cell):
            layout.addWidget(QLabel(elem[0]+': '), i, 0)
            layout.addWidget(m.render(None, elem[1]), i, 1)
            continue
        root.setLayout(layout)
        root.show()
    else:
        _ = m.render(None, cell)
        pass

    sys.exit(app.exec())


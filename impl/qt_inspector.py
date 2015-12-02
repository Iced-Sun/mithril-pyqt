from PyQt5.QtWidgets import *

def find_qt_class(name):
    name_ = name if name.startswith('Q') else 'Q' + name

    if name_ in globals():
        return globals()[name_]
    else:
        raise RuntimeError('Tag "{}" is not a supported widget type.'.format(name))
    return

def get_default_attach_method(Parent, Child):
    method = lambda *args: None

    if Parent is type(None) or Child is type(None):
        pass
    elif issubclass(Parent, QLayout):
        if issubclass(Child, QLayout):
            method = Parent.addLayout
        elif issubclass(Child, QWidget):
            method = Parent.addWidget
        else:
            method = None
    elif issubclass(Child, QMenu):
        if issubclass(Parent, (QMenuBar, QMenu)):
            method = Parent.addMenu
        else:
            # FIXME should we allow arbitrary QWidget have a menu as a child?
            #method = None
            pass
    elif issubclass(Child, QAction):
        method = Parent.addAction
    else:
        method = None
        pass

    if method is None:
        raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
        pass

    return method

def apply_attach_method(parent, child, *args, **kwargs):
    method = get_default_attach_method(type(parent), type(child))
    method(parent, child, *args, **kwargs)
    return

def _get_default_unbound_attach_method(Parent, Child):
    Parent = Parent if isinstance(Parent, type) else type(Parent)
    Child = Child if isinstance(Child, type) else type(Child)

    if not issubclass(Parent, QObject) or not issubclass(Child, QObject):
        raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))

    method = lambda *args: None
    owning = False
    parent_set = False

    '''
    ## TODO use decent double dispatch
    elif issubclass(Child, QActionGroup):
        ## ActionGroup should be explicitly added by addActions() in client
        ## code
    #    method = Parent.addActions
        pass
    elif issubclass(Parent, QWidget):
        if issubclass(Parent, QMainWindow):
            if issubclass(Child, QToolBar):
                method = QMainWindow.addToolBar
            elif issubclass(Child, QMenuBar):
                method = QMainWindow.setMenuBar
                owning = True
            elif issubclass(Child, QWidget):
                method = QMainWindow.setCentralWidget
                owning = True
            else:
                raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
        else:
            raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
    elif issubclass(Parent, QLayout):
        if issubclass(Child, QWidget):
            method = Parent.addWidget
        else:
            raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
    else:
        raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
    '''
    return method#, owning, parent


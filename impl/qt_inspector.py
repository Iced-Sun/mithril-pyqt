from PyQt5.QtWidgets import *

def auto_reparentable(element):
    if isinstance(element, QLayout):
        return True
    else:
        return False
    pass

def suggest_container(parent, layout_type):
    if isinstance(parent, (QMenu, QMenuBar)):
        return parent
    else:
        if parent is not None and parent.layout() is None:
            return layout_type(parent)
        else:
            return layout_type()
        pass
    pass

def find_qt_class(name):
    name_ = name if name.startswith('Q') else 'Q' + name

    if name_ in globals():
        return globals()[name_]
    else:
        raise RuntimeError('Tag "{}" is not a supported widget type.'.format(name))
    return

def get_unbound_attach_method(Parent, Child):
    """Return an unbound method of Parent that will attach the child to the parent.
    """

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
            pass
    elif issubclass(Child, QAction):
        method = Parent.addAction
    else:
        pass

    if method is None:
        raise RuntimeError('Unsupported attach action {} -> {}'.format(Child, Parent))
        pass

    return method

def get_bound_attach_method(parent, child):
    """Return a bound method of type(parent) that binds both parent and child
    """
    return lambda *args, **kwargs: get_unbound_attach_method(type(parent), type(child))(parent, child, *args, **kwargs)

def apply_attach_method(parent, child, *args, **kwargs):
    get_bound_attach_method(parent, child)(*args, **kwargs)
    return


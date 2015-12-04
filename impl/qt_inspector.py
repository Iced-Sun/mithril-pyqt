import impl.util

from PyQt5.QtWidgets import *

def suggest_parent(parent_hint=None):
    if isinstance(parent_hint, QLayout):
        ## auto re-parent, need and should not set the parent
        return None
    else:
        return parent_hint
    pass

def suggest_container(parent, children, container_hint=True):
    if container_hint == True:
        ## auto guess
        if isinstance(children, list):
            return 'h_box_layout'
        elif isinstance(children, tuple):
            return 'v_box_layout'
        else:
            raise RuntimeError('Does not know how to assign a container for children "{}"'.format(children))
    elif container_hint is None:
        ## don't need a container
        return parent
    elif isinstance(container_hint, str):
        ## a string name of layout
        if not container_hint.endswith('_layout'):
            container_hint = container_hint + '_layout'
            pass

        return container_hint
    else:
        raise RuntimeError('Does not know how to handle the container_hint "{}"'.format(container_hint))

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
    elif issubclass(Child, QLayout):
        pass
    elif issubclass(Child, QMenu):
        if issubclass(Parent, (QMenuBar, QMenu)):
            method = Parent.addMenu
        else:
            method = None
    elif issubclass(Child, QAction):
        method = Parent.addAction
    elif issubclass(Child, QActionGroup):
        method = lambda parent, child: Parent.addActions(parent, child.actions())
    elif issubclass(Parent, QWidget) and issubclass(Child, QWidget):
        ## already attached, but without a layout manager
        pass
    else:
        method = None
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


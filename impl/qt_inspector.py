import impl.util

from PyQt5.QtWidgets import *

def suggest_parent(parent_hint):
    if isinstance(parent_hint, QLayout):
        ## auto re-parent, need and should not set the parent
        return None
    else:
        return parent_hint
    pass

def suggest_container(parent, children, container_hint):
    if container_hint == True:
        ## Automatically guess if we should add an intermediate object the
        ## contain a list/tuple children.
        ##
        ## For example, a QWidget usually needs a layout to place child
        ## widgets; while a QMenu accepts multiple QAction/QMenu by itself.
        if isinstance(parent, (QActionGroup, QLayout)):
            ## if `parent' can handle children
            return parent
        elif isinstance(parent, QMenu):
            ## QMenu can handle children, but sometimes we need a QActionGroup
            if isinstance(children, tuple):
                return 'action_group'
            else:
                return parent
        elif isinstance(children, list):
            return 'h_box_layout'
        elif isinstance(children, tuple):
            return 'v_box_layout'
        else:
            raise RuntimeError('Does not know how to assign a container for parent "{}" and children "{}"'.format(parent, children))
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
    return

def find_qt_class(name):
    name_ = name if name.startswith('Q') else 'Q' + name

    if name_ in globals():
        return globals()[name_]
    else:
        raise RuntimeError('Tag "{}" is not a supported widget type.'.format(name))
    return

def get_unbound_attach_method(Parent, Child):
    """Return an unbound method of Parent that will visually attach the child
    to the parent.
    """

    ## the attach method is no-op by default
    method = lambda *args: None

    ## double dispatch on Parent and Child
    ##
    ## Classes need love: QLayout, QActionGroup, QAction, QMenuBar, QMenu,
    ## where QMenuBar and QMenu are QWidget.
    ##
    ## The order of conditions matters (becaus QMenuBar and QMenu are QWidget).
    if Parent is type(None) or Child is type(None):
        pass
    elif issubclass(Parent, QLayout):
        if issubclass(Child, QLayout):
            method = Parent.addLayout
        elif issubclass(Child, QWidget):
            method = Parent.addWidget
        else:
            ## the child of layout should be either a QWidget or another
            ## QLayout
            method = None
    elif issubclass(Child, QLayout):
        pass
    elif issubclass(Child, QMenu):
        if issubclass(Parent, (QMenuBar, QMenu)):
            method = Parent.addMenu
        elif issubclass(Parent, QWidget):
            ##raise RuntimeWarning('QMenu cannot be visually attached directly to QWidget')
            pass
        else:
            ## This should not happen...
            method = None
    elif issubclass(Child, QAction):
        method = Parent.addAction
    elif issubclass(Child, QActionGroup):
        method = lambda parent, child: Parent.addActions(parent, child.actions())
    elif issubclass(Parent, QWidget) and issubclass(Child, QWidget):
        ## already visually attached
        pass
    else:
        ## this is an error
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


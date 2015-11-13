def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    if capitalize_first:
        return ''.join(x.capitalize() for x in components)
    else:
        return components[0] + ''.join(x.capitalize() for x in components[1:])

def m_impl(tag, *args):
    ## pythonic
    tag = _snake_to_camel(tag, capitalize_first=True) if isinstance(tag, str) else tag

    ## parse args
    tag_args, attributes, children = (), {}, None

    ## maybe too aggressive?
    #if len(args) > 0 and isinstance(args[0], (str, tuple, _M._M_placeholder, QObject)):
    if len(args) > 0 and isinstance(args[0], (str, tuple)):
        tag_args = args[0] if isinstance(args[0], tuple) else (args[0],)
        args = args[1:]

    if len(args) > 0 and isinstance(args[0], dict):
        attributes = args[0]
        args = args[1:]

    if len(args) > 0:
        children = args[0]
        args = args[1:]

    if len(args) > 0:
        raise RuntimeError('m() called with wrong number of arguments.')

    ## children should be a list of tuples
    children = [
        child if isinstance(child, tuple) else (child,)
        for child in (children if isinstance(children, list) else [children])
        if child is not None
    ]

    return {'tag': tag, 'args': list(tag_args), 'attrs': attributes, 'children': children}

def build(cell, cached=None):
    if isinstance(cell['tag'], str):
        from PyQt5 import QtWidgets
        if 'Q{}'.format(cell['tag']) in QtWidgets.__dict__:
            cell_type = getattr(QtWidgets, 'Q{}'.format(cell['tag']))
        else:
            raise RuntimeError('Tag "{}" is not a supported widget type.'.format(cell['tag']))
    else:
        cell_type = cell['tag']
        pass

    element = cell_type(*cell['args'])

    for key, val in cell['attrs'].items():
        if hasattr(element, _snake_to_camel('set_'+key)):
            ## properties that can be set
            #if val is _M._parent:
            #    val = parent_element
            #        else:
            #            pass
            getattr(element, _snake_to_camel('set_'+key))(val)
            pass
        continue
    
    return element

def render_impl(root, cell, forceRecreation=False):
    cache = build(cell)
    cache.show()
    #configs()
    return cache
    
def mount_impl(parent, Component, mount_method=None):
    app = QApplication(sys.argv)

    if hasattr(Component, 'Controller'):
        ctrl = Component.Controller()
        view = Component.view(ctrl)
    else:
        view = Component.view()
        pass

    if view is None:
        raise RuntimeError('{}.view() does not return a widget factory'.format(component))
    else:
        widget = view()
        widget.show()
        pass

    sys.exit(app.exec_())

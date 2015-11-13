def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    if capitalize_first:
        return ''.join(x.capitalize() for x in components)
    else:
        return components[0] + ''.join(x.capitalize() for x in components[1:])

def m_impl(tag, *args):
    ## the output
    cell = {}

    ## pythonic
    cell['tag'] = _snake_to_camel(tag, capitalize_first=True) if isinstance(tag, str) else tag

    ## for list::pop()
    args = list(args)

    ## arguments being forwarded to tag constructor
    #if len(args) > 0 and isinstance(args[0], (str, tuple, _M._M_placeholder, QObject)):
    if len(args) > 0 and isinstance(args[0], (str, tuple)):
        arg = args.pop(0)
        cell['args'] = list(arg if isinstance(arg, tuple) else (arg,))
        pass

    ## attributes for the tag
    if len(args) > 0 and isinstance(args[0], dict) and 'tag' not in args[0]:
        cell['attrs'] = args.pop(0)
        pass

    ## attached children
    if len(args) > 0:
        cell['children'] = args.pop(0)
        pass

    ## what a surprise
    if len(args) > 0:
        raise RuntimeError('m() called with wrong number of arguments.')

    ## children should be a list of tuples
    #children = [
    #    child if isinstance(child, tuple) else (child,)
    #    for child in (children if isinstance(children, list) else [children])
    #    if child is not None
    #]

    return cell

def build(parent_element, cell, cached=None):
    if isinstance(cell['tag'], str):
        from PyQt5 import QtWidgets
        if 'Q{}'.format(cell['tag']) in QtWidgets.__dict__:
            cell_type = getattr(QtWidgets, 'Q{}'.format(cell['tag']))
        else:
            raise RuntimeError('Tag "{}" is not a supported widget type.'.format(cell['tag']))
    else:
        cell_type = cell['tag']
        pass

    element = cell_type(*cell.get('args',[]), parent_element)

    children = cell.get('children')
    if isinstance(children, dict):
        ## the only child
        child_element = build(element, children)
    else:
        pass

    for key, val in cell.get('attrs',{}).items():
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
    cache = build(root, cell)
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

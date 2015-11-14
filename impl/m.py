def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    if capitalize_first:
        return ''.join(x.capitalize() for x in components)
    else:
        return components[0] + ''.join(x.capitalize() for x in components[1:])

def m(tag, *args):
    ## the output
    cell = {}

    ## wrap tag and tag_args in a list
    if not isinstance(tag, tuple):
        tag = [tag]
    else:
        tag = list(tag)
        pass

    ## pythonic
    if isinstance(tag[0], str):
        tag[0] = _snake_to_camel(tag[0], capitalize_first=True)
        pass

    ## set tag
    cell['tag'] = tag

    ## for list::pop()
    args = list(args)

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
    ## parse tag
    if isinstance(cell['tag'][0], str):
        from PyQt5 import QtWidgets
        if 'Q{}'.format(cell['tag'][0]) in QtWidgets.__dict__:
            cell_type = getattr(QtWidgets, 'Q{}'.format(cell['tag'][0]))
        else:
            raise RuntimeError('Tag "{}" is not a supported widget type.'.format(cell['tag'][0]))
    else:
        cell_type = cell['tag'][0]
        pass

    ## create this element
    element = cell_type(*cell['tag'][1:], parent_element)

    ## create children
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

def render(root, cell, forceRecreation=False):
    cache = build(root, cell)
    cache.show()
    #configs()
    return cache
    
def mount(parent, Component, mount_method=None):
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

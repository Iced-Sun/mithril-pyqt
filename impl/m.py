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

def build_dict(parent_element, data, cached):
    ## parse tag
    if isinstance(data['tag'][0], str):
        from PyQt5 import QtWidgets
        if 'Q{}'.format(data['tag'][0]) in QtWidgets.__dict__:
            element_type = getattr(QtWidgets, 'Q{}'.format(data['tag'][0]))
        else:
            raise RuntimeError('Tag "{}" is not a supported widget type.'.format(data['tag'][0]))
    else:
        element_type = data['tag'][0]
        pass

    ## create this element
    element = element_type(*data['tag'][1:], parent_element)

    ## build children
    children = build(element, data.get('children'), cached)

    ## apply attributes
    for key, val in data.get('attrs',{}).items():
        if hasattr(element, _snake_to_camel('set_'+key)):
            getattr(element, _snake_to_camel('set_'+key))(val)
            pass
        else:
            raise RuntimeError('Unexpected attribute {}'.format(key))
        continue

    return element

def build_list(parent_element, data, cached):
    ## always use layout
    from PyQt5.QtWidgets import QHBoxLayout
    container = QHBoxLayout(parent_element)

    for cell in data:
        if isinstance(cell, str):
            getattr(container, _snake_to_camel('add_{}'.format(cell)))()
        else:
            element = build(parent_element, cell)
            container.addWidget(element)
            pass
        continue

    return container

def build(parent_element, data, cached=None):
    if isinstance(data, dict):
        element = build_dict(parent_element, data, cached)
    elif isinstance(data, list):
        element = build_list(parent_element, data, cached)
    elif data is None:
        ## could be None when trying to build children
        element = None
    else:
        raise RuntimeError('Unexpected cell {}'.format(data))
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

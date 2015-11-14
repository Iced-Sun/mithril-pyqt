def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    if capitalize_first:
        return ''.join(x.capitalize() for x in components)
    else:
        return components[0] + ''.join(x.capitalize() for x in components[1:])

def m(tag, *args):
    cell = {}

    ## parse tag and its arguments
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
    # assume it's a dict without 'tag' key
    if len(args) > 0 and isinstance(args[0], dict) and 'tag' not in args[0]:
        cell['attrs'] = args.pop(0)
        pass

    ## attached children
    # assume it's a list, a tuple, or a dict with a 'tag' key
    if len(args) > 0 and isinstance(args[0], (list, tuple, dict)):
        cell['children'] = args.pop(0)
        pass

    ## forward rest arguments to tag
    if len(args) > 0:
        tag += args
        pass

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

def build_list(parent_element, data, cached, layout):
    ## get the layout factory
    if layout == 'HBox':
        from PyQt5.QtWidgets import QHBoxLayout
        container_type = QHBoxLayout
    elif layout == 'VBox':
        from PyQt5.QtWidgets import QVBoxLayout
        container_type = QVBoxLayout
    else:
        pass

    ## this layout could be a root layout of parent_element, or a nested one
    if parent_element is not None and parent_element.layout() is None:
        container = container_type(parent_element)
    else:
        container = container_type()
        pass

    ## iterate on children
    for cell in data:
        if isinstance(cell, str):
            getattr(container, _snake_to_camel('add_{}'.format(cell)))()
        elif isinstance(cell, tuple):
            getattr(container, _snake_to_camel('add_{}'.format(cell[0])))(*cell[1:])
        else:
            ## create the element without parent, since it will be auto
            ## reparenting
            element = build(None, cell)
            from PyQt5.QtWidgets import QLayout
            if isinstance(element, QLayout):
                container.addLayout(element)
            else:
                ## FIXME should we check?
                container.addWidget(element)
                pass
            pass
        continue

    return container

def build(parent_element, data, cached=None):
    ## dispatch on data type
    if isinstance(data, dict):
        element = build_dict(parent_element, data, cached)
    elif isinstance(data, list):
        element = build_list(parent_element, data, cached, 'HBox')
    elif isinstance(data, tuple):
        element = build_list(parent_element, data, cached, 'VBox')
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

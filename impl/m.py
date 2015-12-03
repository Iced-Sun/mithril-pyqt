import impl.qt_inspector
import impl.util

def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    return ''.join(x.capitalize() for x in components) if capitalize_first else components[0] + ''.join(x.capitalize() for x in components[1:])

def m(tag, *args):
    cell = {}

    ## parse args in reverse order
    # for list::pop()
    args = list(args)

    ## attached children
    # assume it's a list, a tuple, or a dict with a 'tag' key
    if args and (
            isinstance(args[-1], (list, tuple))
            or (isinstance(args[-1], dict) and 'tag' in args[-1]
            )):
        cell['children'] = args.pop()
        pass

    ## attributes for the tag
    # assume it's a dict without 'tag' key
    if args and isinstance(args[-1], dict) and 'tag' not in args[-1]:
        cell['attrs'] = args.pop()
        pass

    ## extract tag and its arguments
    if not isinstance(tag, tuple):
        tag = [tag]
    else:
        tag = list(tag)
        pass

    ## parse tag string
    if isinstance(tag[0], str):
        ## pythonic tag name
        tag[0] = _snake_to_camel(tag[0], capitalize_first=True)

        ## extract tag id
        splitted = tag[0].split('#')
        if len(splitted) == 2:
            tag[0] = splitted[0]
            cell['attrs'] = cell.get('attrs', {})
            cell['attrs']['id'] = splitted[1]
        elif len(splitted) == 1:
            pass
        else:
            raise RuntimeError('malformat tag name: {}'.format(tag[0]))
        pass

    ## set tag
    cell['tag'] = tag

    ## forward rest arguments to tag
    cell['tag'] += args

    return cell

def apply_attribute_to(element, key, val):
    if hasattr(element, _snake_to_camel('set_'+key)):
        if isinstance(val, dict) and 'tag' in val:
            ## this is a m() constructed element
            getattr(element, _snake_to_camel('set_'+key))(build(None, val))
        else:
            getattr(element, _snake_to_camel('set_'+key))(val)
            pass
    elif key.startswith('on_') and hasattr(element, _snake_to_camel(key[3:])):
        signal = getattr(element, _snake_to_camel(key[3:]))
        if callable(val):
            signal.connect(val)
        elif isinstance(val, dict):
            if 'selector' not in val:
                parts = val['slot'].split('::')
                selector = parts[0]
                method = parts[1]
            else:
                selector = val['selector']
                method = val['slot']
                pass

            if selector.startswith('#'):
                from impl.query import get_element_by_id
                target_element = get_element_by_id(selector[1:])
                if target_element is not None:
                    signal.connect(getattr(target_element, _snake_to_camel(method)))
                    pass
                pass
            pass
        else:
            raise RuntimeError('slot value {} to signal {} is malformed'.format(val, key))
    elif key.endswith('_on') and hasattr(element, _snake_to_camel(key[:-3])):
        slot = getattr(element, _snake_to_camel(key[:-3]))
        val.connect(slot)
    elif key == 'id':
        from impl.query import _m_constructed_elements
        if val in _m_constructed_elements:
            raise RuntimeError('The element with id {} already exists.'.format(val))
        else:
            _m_constructed_elements[val] = element
            pass
        pass
    else:
        raise RuntimeError('Unexpected attribute {}'.format(key))
    pass

def build_dict(parent_element, data, cached):
    ## parse tag
    if isinstance(data['tag'][0], str):
        element_type = impl.qt_inspector.find_qt_class(data['tag'][0])
    else:
        element_type = data['tag'][0]
        pass

    ## create this element with parent
    element = element_type(*data['tag'][1:], parent_element)

    ## additional actions to attach the element (because making an child
    ## element in QT is mainly for memory management, and sometimes for
    ## display, e.g., QMenu(parent=QMenuBar) doesn't show the menu in the menu
    ## bar)
    impl.qt_inspector.apply_attach_method(parent_element, element)

    ## apply attributes on this element
    for key, val in data.get('attrs',{}).items():
        apply_attribute_to(element, key, val)
        continue

    ## create child elements automatically parenting this element
    children = build(element, data.get('children'), cached)

    return element

def build_list(parent_element, data, cached):
    ## extract the attributes of the list
    if len(data) and isinstance(data[0], dict) and 'tag' not in data[0]:
        attrs = data[0]
        cells = data[1:]
    else:
        attrs = {}
        cells = data
        pass

    ## pick a layout
    layout = attrs.get('layout', True)

    # TODO layout=None to support no layout manager?
    if layout == True:
        if isinstance(cells, list):
            layout = 'h_box'
        elif isinstance(cells, tuple):
            layout = 'v_box'
        else:
            raise RuntimeError('Cannot automatically determine the layout type')
        pass

    ## get the layout factory
    if isinstance(layout, str):
        layout = layout if layout.endswith('_layout') else layout+'_layout'
        container_type = impl.qt_inspector.find_qt_class('Q' + _snake_to_camel(layout, capitalize_first=True))
    else:
        container_type = layout
        pass

    ## create the container
    container = impl.qt_inspector.suggest_container(parent_element, container_type)

    ## apply attributes to the layout
    for key, val in attrs.items():
        if key not in ('layout', 'columns'):
            apply_attribute_to(container, key, val)
            pass
        continue

    ## add child items
    for i, cell in enumerate(cells):
        ## create the adder object
        adder = cell if isinstance(cell, impl.util._Adder) else impl.util.add(cell)

        ## get the callback to add
        if isinstance(adder.target, str):
            adder.target = getattr(container, _snake_to_camel('add_{}'.format(adder.target)))
        else:
            if impl.qt_inspector.auto_reparentable(container):
                element = build(None, adder.target)
            else:
                element = build(container, adder.target)
                pass

            adder.target = impl.qt_inspector.get_bound_attach_method(container, element)
            pass

        ## special cares
        if 'layout' in attrs:
            if attrs['layout'] in ('grid', 'grid_layout'):
                if 'columns' in attrs:
                    ## a grid layout: insert position arguments
                    adder.forwarder.args = divmod(i, attrs['columns']) + adder.forwarder.args
                else:
                    pass
            elif attrs['layout'] in ('form', 'form_layout'):
                if adder.raw_target == 'row':
                    adder.forwarder.args = tuple(x if isinstance(x, str) else build(None, x) for x in adder.forwarder.args)
                else:
                    pass
            else:
                pass
            pass

        adder.apply()
        continue

    return container

def build(parent_element, data, cached=None):
    ## dispatch on data type
    if isinstance(data, dict):
        element = build_dict(parent_element, data, cached)
    elif isinstance(data, (list, tuple)):
        element = build_list(parent_element, data, cached)
    elif data is None:
        ## could be None when trying to build children
        element = None
    else:
        raise RuntimeError('Unsupported cell "{}"'.format(data))
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

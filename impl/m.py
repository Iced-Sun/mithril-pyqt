import impl.qt_inspector

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
        getattr(element, _snake_to_camel('set_'+key))(val)
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

def build_list(parent_element, data, attrs, cached):
    if attrs is None:
        attrs = {}
        pass

    if 'layout' in attrs:
        layout = attrs['layout']
    elif isinstance(data, list):
        layout = 'h_box_layout'
    elif isinstance(data, tuple):
        layout = 'v_box_layout'
    else:
        raise RuntimeError('Cannot determine the layout type')

    ## get the layout factory
    if isinstance(layout, str):
        container_type = impl.qt_inspector.find_qt_class('Q' + _snake_to_camel(layout, capitalize_first=True))
    else:
        container_type = layout
        pass

    ## create the layout
    if parent_element is not None and parent_element.layout() is None:
        ## this layout could be a root layout of parent_element
        container = container_type(parent_element)
    else:
        ## or a nested root layout
        container = container_type()
        pass

    ## apply attributes to the layout
    for key, val in attrs.items():
        if key != 'layout':
            apply_attribute_to(container, key, val)
            pass
        continue

    ## add child items
    for cell in data:
        if isinstance(cell, str):
            getattr(container, _snake_to_camel('add_{}'.format(cell)))()
        elif isinstance(cell, tuple) and isinstance(cell[0], str):
            ## FIXME tuple can represent a VBoxLayout or an in-place item
            ## insertion; really need such subtlety?
            getattr(container, _snake_to_camel('add_{}'.format(cell[0])))(*cell[1:])
        else:
            ## create the element without parent, since it will be auto
            ## re-parenting
            element = build(None, cell)

            ## attach the element to the container
            impl.qt_inspector.apply_attach_method(container, element)
            pass
        continue

    return container

def build(parent_element, data, cached=None):
    ## dispatch on data type
    if isinstance(data, dict):
        element = build_dict(parent_element, data, cached)
    elif isinstance(data, (list, tuple)):
        if len(data) > 0 and isinstance(data[0], dict) and 'tag' not in data[0]:
            element = build_list(parent_element, data[1:], data[0], cached)
        else:
            element = build_list(parent_element, data, None, cached)
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

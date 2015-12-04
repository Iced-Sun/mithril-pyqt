import impl.qt_inspector
import impl.util

def _snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    return ''.join(x.capitalize() for x in components) if capitalize_first else components[0] + ''.join(x.capitalize() for x in components[1:])

class _Cell_tag(object):
    pass

class _Contained_cell(list, _Cell_tag):
    pass

def _make_cell(obj=None):
    if obj is None:
        obj = {}
        pass

    if isinstance(obj, _Contained_cell):
        return obj
    elif isinstance(obj, (dict, list, tuple)):
        class _Tagged_cell(type(obj), _Cell_tag):
            pass
        return _Tagged_cell(obj)
    else:
        raise RuntimeError('Unsupported cell type {}'.format(obj))
    pass

def m(tag, *args):
    cell = _make_cell()

    ## parse args in reverse order
    # for list::pop()
    args = list(args)

    ## attached children: a list, tuple, or _Cell
    if args and isinstance(args[-1], (list, tuple, _Cell_tag)):
        cell['children'] = _make_cell(args.pop())
        pass

    ## attributes for the tag: a dict
    if args and isinstance(args[-1], dict):
        cell['attrs'] = args.pop()
        pass

    ## extract tag and its arguments
    if not isinstance(tag, tuple):
        tag = (tag,)
        pass

    ## parse tag string
    tag_name = tag[0]
    if isinstance(tag[0], str):
        ## extract tag id
        splitted = tag[0].split('#')
        if len(splitted) == 2:
            tag_name = splitted[0]
            cell['attrs'] = cell.get('attrs', {})
            cell['attrs']['id'] = splitted[1]
        elif len(splitted) == 1:
            pass
        else:
            raise RuntimeError('malformat tag name: {}'.format(tag[0]))

        ## pythonic tag name
        tag_name = _snake_to_camel(tag_name, capitalize_first=True)
        pass

    ## set tag
    cell['tag'] = (tag_name,) + tag[1:] + tuple(args)

    return cell

def apply_attribute_to(element, key, val):
    if hasattr(element, _snake_to_camel('set_'+key)):
        if isinstance(val, _Cell_tag):
            ## auto re-parent
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

def build_dict(parent, data, cached):
    ## parse tag
    if isinstance(data['tag'][0], str):
        element_type = impl.qt_inspector.find_qt_class(data['tag'][0])
    else:
        element_type = data['tag'][0]
        pass

    ## create this element with parent
    element = element_type(*data['tag'][1:], parent)

    ## additional actions to attach the element (because making an child
    ## element in QT is mainly for memory management, and sometimes for
    ## display, e.g., QMenu(parent=QMenuBar) doesn't show the menu in the menu
    ## bar)
    impl.qt_inspector.apply_attach_method(parent, element)

    ## apply attributes on this element
    for key, val in data.get('attrs',{}).items():
        apply_attribute_to(element, key, val)
        continue

    ## create child elements automatically parenting this element
    children = build(element, data.get('children'), cached)

    return element

def build_list(parent, data, cached):
    ## transform a plain list to m() object
    if not isinstance(data, _Contained_cell):
        ## extract the attributes from the list
        if len(data) and isinstance(data[0], dict) and not isinstance(data[0], _Cell_tag):
            attrs = data[0]
            data = data[1:]
        else:
            attrs = {}
            pass

        ## meta attributes
        layout = attrs.pop('layout', True)

        ## get a container tag or object
        container = impl.qt_inspector.suggest_container(parent, data, layout)

        if isinstance(container, str):
            container = build(parent, m(container, attrs, _Contained_cell(data)))
        else:
            ## no container in need
            container = build(parent, _Contained_cell(data))
            pass
        return container

    ## or the data have the parent as the container, hence add child items
    for i, cell in enumerate(data):
        element = build(impl.qt_inspector.suggest_parent(parent), _make_cell(cell))
        impl.qt_inspector.get_bound_attach_method(parent, element)()
        continue

    return None

def build_list1(parent_element, data, cached):
    ## extract the attributes of the list
    if len(data) and isinstance(data[0], dict) and not isinstance(data[0], _Cell_tag):
        attrs = data[0]
        cells = _make_cell(data[1:])
    else:
        attrs = {}
        cells = data
        pass

    ## pick a layout
    layout = attrs.get('layout', True)

    ## select a default layout by the collection type
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
    elif layout is None:
        container_type = None
    else:
        container_type = layout
        pass

    ## create the container
    container = impl.qt_inspector.suggest_container(parent_element, container_type)

    ## apply attributes to the layout
    for key, val in attrs.items():
        ## exclude custom attributes
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
            adder.target = _make_cell(adder.target)

            ## quirk on QActionGroup
            if isinstance(adder.target, (list,tuple)) and impl.qt_inspector.suggest_container(parent_element, None) == 'action_group':
                ## TODO can we/should we apply the same mechanism to layout?
                adder.target = m('action_group', adder.target)
                pass

            ## build child element
            if impl.qt_inspector.auto_reparentable(container):
                element = build(None, adder.target)
            else:
                element = build(container, adder.target)
                pass

            adder.target = impl.qt_inspector.get_bound_attach_method(container, element)
            pass

        ## build the element if necessary
        def _is_cell(x):
            if isinstance(x, (list, tuple)):
                return any([isinstance(y, _Cell_tag) for y in x])
            else:
                return isinstance(x, _Cell_tag)
            pass
        adder.forwarder.args = tuple(build(None, _make_cell(x)) if _is_cell(x) else x for x in adder.forwarder.args)

        ## quirks
        if attrs.get('layout') in ('grid', 'grid_layout') and 'columns' in attrs:
            ## a grid layout: insert position arguments
            adder.forwarder.args = divmod(i, attrs['columns']) + adder.forwarder.args
            pass

        ## fine
        adder.apply()
        continue

    return container

def build(parent_element, data, cached=None):
    ## dispatch on data type
    if not data:
        ## could be None when trying to build children
        element = None
    elif isinstance(data, _Cell_tag):
        if isinstance(data, dict):
            element = build_dict(parent_element, data, cached)
        elif isinstance(data, (list, tuple)):
            element = build_list(parent_element, data, cached)
        else:
            raise RuntimeError('Unsupported cell "{}: {}"'.format(type(data), data))
    else:
        raise RuntimeError('Unsupported cell "{}: {}"'.format(type(data), data))
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

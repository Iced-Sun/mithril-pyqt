import impl.qt_inspector
import impl.util

class _Cell_tag(object):
    pass

class _Contained_cell(list, _Cell_tag):
    def __init__(self, meta_attrs, *args):
        super().__init__(*args)
        self.meta_attrs = meta_attrs
        pass
    def __repr__(self):
        return '_Contained_cell({})'.format(super().__repr__())
    pass

def _make_cell(obj=None):
    if obj is None:
        obj = {}
        pass

    if isinstance(obj, _Contained_cell):
        return obj
    elif isinstance(obj, (dict, list, tuple)):
        for _ in (dict, list, tuple):
            if isinstance(obj, _):
                reduced_type = _
                break
            continue

        class _Tagged_cell(reduced_type, _Cell_tag):
            def __repr__(self):
                return '_Tagged_cell({})'.format(super().__repr__())
            pass
        return _Tagged_cell(obj)
    else:
        raise RuntimeError('Unsupported cell type {}'.format(obj))
    pass

def _like_a_cell(obj):
    ## If obj contains or is a cell
    if isinstance(obj, (list, tuple)):
        flat_obj = list(impl.util.flatten(obj))
    else:
        flat_obj = [obj]
        pass
    return any(isinstance(x, _Cell_tag) for x in flat_obj)

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
        tag_name = impl.util.snake_to_camel(tag_name, capitalize_first=True)
        pass

    ## set tag
    cell['tag'] = (tag_name,) + tag[1:] + tuple(args)

    return cell

def apply_attribute_to(element, key, val):
    if hasattr(element, impl.util.snake_to_camel('set_'+key)):
        if isinstance(val, _Cell_tag):
            ## auto re-parent
            getattr(element, impl.util.snake_to_camel('set_'+key))(build(None, val))
        else:
            getattr(element, impl.util.snake_to_camel('set_'+key))(val)
            pass
    elif key.startswith('on_') and hasattr(element, impl.util.snake_to_camel(key[3:])):
        signal = getattr(element, impl.util.snake_to_camel(key[3:]))
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
                    signal.connect(getattr(target_element, impl.util.snake_to_camel(method)))
                    pass
                pass
            pass
        else:
            raise RuntimeError('slot value {} to signal {} is malformed'.format(val, key))
    elif key.endswith('_on') and hasattr(element, impl.util.snake_to_camel(key[:-3])):
        slot = getattr(element, impl.util.snake_to_camel(key[:-3]))
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

    ## apply attributes on this element
    for key, val in data.get('attrs',{}).items():
        apply_attribute_to(element, key, val)
        continue

    ## create child elements automatically parenting this element
    if 'children' in data:
        build(element, data['children'], cached)
        pass

    ## additional actions to attach the element (because making an child
    ## element in QT is mainly for memory management, and sometimes for
    ## display, e.g., QMenu(parent=QMenuBar) doesn't show the menu in the menu
    ## bar)
    ##
    ## BEWARE must be after the children creation 'cause it is possible that
    ## the children are actually attached to parent (e.g., QActionGroup)
    impl.qt_inspector.apply_attach_method(parent, element)

    return element

def build_list(parent, data, cached):
    ## find a container for data before we actually insert them
    if not isinstance(data, _Contained_cell):
        supported_custom_attributes = {'layout', 'columns'}

        ## extract the attributes from the list
        if len(data) and isinstance(data[0], dict) and not isinstance(data[0], _Cell_tag):
            attrs = data[0]
            meta_attrs = {k:attrs.pop(k) for k in supported_custom_attributes & attrs.keys()}
            data = data[1:]
        else:
            attrs = {}
            meta_attrs = {}
            pass

        ## get a container tag or object
        container = impl.qt_inspector.suggest_container(parent, data, meta_attrs.get('layout', True))

        ## mark the data as with a container, and keep the meta_attrs
        cells = _Contained_cell(meta_attrs, data)

        ## build the container and its children
        if isinstance(container, (str,type)):
            ## returned container is a tag for m(), which means an intermediate
            ## element is required as a container
            container = build(parent, m(container, attrs, cells))
        else:
            ## no intermediate container in need
            container = build(parent, cells)
            pass

        return container

    ## now have the container
    for i, cell in enumerate(data):
        ## create the adder object
        adder = cell if isinstance(cell, impl.util._Adder) else impl.util.add(cell)

        ## get the callback to add
        if isinstance(adder.target, str):
            ## the callback is specified by name, e.g., `spacing' -> `addSpacing'
            adder.target = getattr(parent, impl.util.snake_to_camel('add_{}'.format(adder.target)))
        elif isinstance(adder.target, (_Cell_tag, list, tuple)):
            ## if the target is a cell or container (_make_cell will add a
            ## container_cell tag), deduce a callback by the types of parent
            ## and child
            element = build(impl.qt_inspector.suggest_parent(parent), _make_cell(adder.target))
            adder.target = impl.qt_inspector.get_bound_attach_method(parent, element)
        else:
            raise RuntimeError('Unsupported adder target {}'.format(adder.target))
            pass

        ## build cells inside the adder arguments
        adder.forwarder.args = [
            build(impl.qt_inspector.suggest_parent(parent), _make_cell(arg))
            if _like_a_cell(arg) else arg
            for arg in adder.forwarder.args
        ]

        ## quirks
        if 'columns' in data.meta_attrs:
             ## a grid layout: insert position arguments
            adder.forwarder.args = divmod(i, data.meta_attrs['columns']) + adder.forwarder.args
            pass

        ## fine
        adder.apply()
        continue

    return None

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

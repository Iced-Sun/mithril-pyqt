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

def build_dict(parent_element, data, cached):
    ## parse tag
    if isinstance(data['tag'][0], str):
        element_type = impl.qt_inspector.find_qt_class(data['tag'][0])
    else:
        element_type = data['tag'][0]
        pass

    ## create this element with parent
    element = element_type(*data['tag'][1:], parent_element)

    ## build children
    children = build(element, data.get('children'), cached)

    ## apply attributes
    for key, val in data.get('attrs',{}).items():
        if hasattr(element, _snake_to_camel('set_'+key)):
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
        elif isinstance(cell, tuple) and isinstance(cell[0], str):
            ## FIXME tuple can represent a VBoxLayout or an in-place item
            ## insertion; really need such subtlety?
            getattr(container, _snake_to_camel('add_{}'.format(cell[0])))(*cell[1:])
        else:
            ## create the element without parent, since it will be auto
            ## re-parenting
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

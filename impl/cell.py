import impl.util

"""A cell is basically a tagged dict, tuple or list, to be distinguished from
the plain objects.

"""

## public interface
def can_be_coverted_to_children_cells(obj):
    # m(_,_,children) accepts list/tuple/Cell as children
    return isinstance(obj, (list, tuple, _Cell))

def is_cell(obj, typ=None):
    if typ is None:
        return isinstance(obj, _Cell)
    elif typ == 'contained':
        return isinstance(obj, _Contained_cell)
    else:
        raise RuntimeError('Unknown tag "{}" to tell a cell'.format(obj))

def make_cell(obj, attrs=None):
    """promote a plain-type object as a cell by adding a tag

    """
    # special case for contained_cell
    if attrs is not None:
        if isinstance(obj, (list, tuple)):
            return _tag_cell(obj, attrs)
        else:
            raise RuntimeError('Unknown type {} to convert to a contained cell'.format(obj))
        pass

    # sanity check
    if is_cell(obj):
        return obj

    # tag it
    if isinstance(obj, (dict, list, tuple)):
        return _tag_cell(obj)
    else:
        raise RuntimeError('Unknown type {} to convert to a cell'.format(obj))
    pass

def is_or_has_a_cell(obj):
    if isinstance(obj, (list, tuple)):
        flat_obj = list(impl.util.flatten(obj))
    else:
        flat_obj = [obj]
        pass
    return any(isinstance(x, _Cell) for x in flat_obj)

## implementation
class _Cell(object):
    pass

class _Contained_cell(list, _Cell):
    """promote a cell-tagged list to a container cell, with extra attributes (in
    essence very alike to a dict cell).

    """
    def __init__(self, meta_attrs, *args):
        super().__init__(*args)
        self.meta_attrs = meta_attrs
        pass
    def __repr__(self):
        return '_Contained_cell({}) with meta_attributes({})'.format(super().__repr__(), self.meta_attrs.__repr__())
    pass

_tagged_cell_types = {}

def _tag_cell(obj, attrs=None):
    if attrs is not None:
        return _Contained_cell(attrs, obj)

    typ = type(obj)
    if typ not in _tagged_cell_types:
        class _Tagged_cell(typ, _Cell):
            def __repr__(self):
                return '_Tagged_{}_cell({})'.format(typ.__name__, super().__repr__())
            pass
        _tagged_cell_types[typ] = _Tagged_cell
        pass

    return _tagged_cell_types[typ](obj)


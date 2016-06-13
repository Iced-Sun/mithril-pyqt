## public interface
def can_be_coverted_to_children_cells(obj):
    # m(_,_,children) accepts list/tuple/Cell as children
    return isinstance(obj, (list, tuple, _Cell))

def is_cell(obj):
    return isinstance(obj, _Cell)

def make_cell(obj=None):
    """promote a plain-type object as a cell by adding a tag

    """
    if obj is None:
        obj = {}
        pass

    if isinstance(obj, _Contained_cell):
    #if isinstance(obj, _Cell):
        return obj
    elif isinstance(obj, dict):
        return _Dict_cell(obj)
    elif isinstance(obj, list):
        return _List_cell(obj)
    elif isinstance(obj, tuple):
        return _Tuple_cell(obj)
    else:
        raise RuntimeError('Unknown type {} to convert to a cell'.format(obj))
    pass

def _like_a_cell(obj):
    ## If obj contains or is a cell
    if isinstance(obj, (list, tuple)):
        flat_obj = list(impl.util.flatten(obj))
    else:
        flat_obj = [obj]
        pass
    return any(isinstance(x, _Cell) for x in flat_obj)

## implementation
class _Cell(object):
    pass

class _Dict_cell(dict, _Cell):
    def __repr__(self):
        return '_Dict_cell({})'.format(super().__repr__())
    pass

class _List_cell(list, _Cell):
    def __repr__(self):
        return '_List_cell({})'.format(super().__repr__())
    pass

class _Tuple_cell(tuple, _Cell):
    def __repr__(self):
        return '_Tuple_cell({})'.format(super().__repr__())
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


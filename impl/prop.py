class Property(object):
    def __init__(self, val):
        self._value = val
        pass

    def __get__(self, obj, objtype):
        return self._value

    def __set__(self, obj, val):
        self._value = val
        pass

def prop_impl():
    return

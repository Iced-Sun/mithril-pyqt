def snake_to_camel(name, capitalize_first=False):
    components = name.split('_')
    return ''.join(x.capitalize() for x in components) if capitalize_first else components[0] + ''.join(x.capitalize() for x in components[1:])

class _Forwarder(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        pass

    def apply(self, f):
        return f(*self.args, **self.kwargs)

    pass

def forward(*args, **kwargs):
    return _Forwarder(*args, **kwargs)

class _Adder(object):
    def __init__(self, target, *args, **kwargs):
        self.forwarder = forward(*args, **kwargs)
        self.raw_target = target
        self.target = target
        pass

    def apply(self):
        return self.forwarder.apply(self.target)

    def __repr__(self):
        return '{}, {}, {}'.format(self.target, self.forwarder.args, self.forwarder.kwargs)
    pass

def add(target, *args, **kwargs):
    return _Adder(target, *args, **kwargs)

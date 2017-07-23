"""https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict"""

from itertools import chain

try:              # Python 2
    str_base = basestring
    items = 'iteritems'
except NameError: # Python 3
    str_base = str, bytes, bytearray
    items = 'items'

class Setdict(dict):
    """docstring"""

    def __new__(cls, *args, **kwargs):
        """docstring"""
        return super(Setdict, cls).__new__(cls, *args, **kwargs)

    def __contains__(self, key):
        """docstring"""
        self._validate_key(key)

        return super(Setdict, self).__contains__(tuple(key))

    def __setitem__(self, key, value):
        """docstring"""
        self._validate_key(key)

        return super(Setdict, self).__setitem__(tuple(key), value)

    @staticmethod
    def _process_args(mapping=(), **kwargs):
        if hasattr(mapping, items):
            mapping = getattr(mapping, items)()
        return (
            (tuple(key), value) for key, value in chain(
                mapping, getattr(kwargs, items)()
            )
        )

    @staticmethod
    def _validate_key(key):
        """docstring"""
        if not isinstance(key, set):
            raise TypeError("key {key} is not of type set".format(key=key))

    def copy(self):
        """docstring"""
        return type(self)(self)

    def get(self, key, *nargs):
        """docstring"""
        self._validate_key(key)

        return super(Setdict, self).get(tuple(key), *nargs)

    def items(self):
        """docstring"""
        return map(
            lambda item: (set(item[0]), item[1]),
            super(Setdict, self).items()
        )

    def keys(self):
        """docstring"""
        return [set(key) for key in super(Setdict, self).keys()]

    def pop(self, key, *nargs, **kwargs):
        """docstring"""
        self._validate_key(key)

        return super(Setdict, self).pop(tuple(key), *nargs, **kwargs)

    def update(self, mapping=(), **kwargs):
        """docstring"""
        for arg in kwargs:
            print("arg={arg}".format(arg=arg))
        for key, _ in mapping.items():
            if not isinstance(key, tuple):
                raise TypeError("key {key} is not of type tuple".format(
                    key=key
                ))

        super(Setdict, self).update(self._process_args(mapping, **kwargs))

    def __str__(self):
        """docstring"""
        print("__str__")
        return "Setdict({{{setdict}}})".format(
            setdict=", ".join([
                "{key}: {value}".format(
                    key=str(set(key)),
                    value=str(value)
                ) for key, value in self.items()
            ])
        )

    def __repr__(self):
        """docstring"""
        print("__repr__")
        return "Setdict({{{setdict}}})".format(
            setdict=", ".join([
                "{key}: {value}".format(
                    key=str(tuple(key)),
                    value=str(value)
                ) for key, value in self.items()
            ])
        )

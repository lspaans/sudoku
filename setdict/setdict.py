"""setdict"""


class Setdict(object):

    def __init__(self, value=None):
        if value is None:
            self.value = {}
        else:
            self.value = value

    def _validate_key(self, key):
        if not isinstance(key, (set,)):
            raise TypeError(
                "key \"{key}\" is not of type set()".format(key=key)
            )

    def get(self, key, default=None):
        self._validate_key(key)

        if key in self:
            return self.value[tuple(key)]

        if default is not None:
            return default

        raise KeyError("key {key} does not exist".format(key=key))

    def get_key(self, value):
        for key in self.value.keys():
            if self.value[key] == value:
                return set(key)

        raise ValueError("value {value} does not exist".format(value=value))

    def get_value(self, key):
        self._validate_key(key)

        if key in self:
            return self.value[tuple(key)]

        raise KeyError("key {key} does not exist".format(key=key))

    def has_value(self, value):
        if value in self.value.values():
            return True
        return False

    def set(self, key, value):
        self._validate_key(key)

        self._value[tuple(key)] = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = {}

        if not isinstance(value, (dict,)):
            raise TypeError(
                "value \"{value}\" is not of type dict()".format(value=value)
            )

        for key, value in value.items():
            self.set(set(key), value)

    def __contains__(self, key):
        self._validate_key(key)

        if tuple(key) in self.value.keys():
            return True
        return False

    def __len__(self):
        return len(self.value)

    def __str__(self):
        import re
        return re.sub(
            re.compile("(\([^\)]*\)):"),
            "set(\g<1>):",
            str(self.value)
        )

    def __repr__(self):
        return "'{value}'".format(value=self.__str__())

"""setdict"""

import re


class Setdict(object):
    """docstring"""

    MESSAGE = {
        "en_US": {
            "wrong_key_type": "key \"{key}\" is not of type set()",
            "wrong_value_type": "value \"{value}\" is not of type dict()",
            "missing_key": "key {key} does not exist",
            "missing_value": "value {value} does not exist"
        }
    }

    def __init__(self, value=None, lang="en_US"):
        """docstring"""
        self._value = {}
        self._lang = lang

        if value is None:
            self.value = {}
        else:
            self.value = value

    def get(self, key, default=None):
        """docstring"""
        if not isinstance(key, (set,)):
            raise TypeError(self._message("wrong_key_type", key=key))

        if key in self:
            return self.value[tuple(key)]

        if default is not None:
            return default

        raise KeyError(self._message("missing_key", key=key))

    def get_key(self, value):
        """docstring"""
        for key in self.value.keys():
            if self.value[key] == value:
                return set(key)

        raise KeyError(self._message("missing_value", value=value))

    def get_value(self, key):
        """docstring"""
        if not isinstance(key, (set,)):
            raise TypeError(self._message("wrong_key_type", key=key))

        if key in self:
            return self.value[tuple(key)]

        raise KeyError(self._message("missing_key", key=key))

    def has_value(self, value):
        """docstring"""
        if value in self.value.values():
            return True
        return False

    def set(self, key, value):
        """docstring"""
        if not isinstance(key, (set,)):
            raise TypeError(self._message("wrong_key_type", key=key))

        self._value[tuple(key)] = value

    @property
    def value(self):
        """docstring"""
        return self._value

    @value.setter
    def value(self, value):
        """docstring"""
        if not isinstance(value, (dict,)):
            raise TypeError(self._message("wrong_value_type", value=value))

        for _key, _value in value.items():
            self.set(set(_key), _value)

    def _message(self, message, **kwargs):
        return Setdict.MESSAGE[self._lang][message].format(**kwargs)

    def __contains__(self, key):
        """docstring"""
        if not isinstance(key, (set,)):
            raise TypeError(self._message("wrong_key_type", key=key))

        if tuple(key) in self.value.keys():
            return True
        return False

    def __len__(self):
        """docstring"""
        return len(self.value)

    def __str__(self):
        """docstring"""
        return re.sub(
            re.compile(r"(\([^\)]*\)):"),
            r"set(\g<1>):",
            str(self.value)
        )

    def __repr__(self):
        """docstring"""
        return "'{value}'".format(value=self.__str__())

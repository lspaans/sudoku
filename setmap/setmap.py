"""setmap"""

from setdict import Setdict


class Setmap(object):
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
            self.value = Setdict()
        else:
            self.value = value

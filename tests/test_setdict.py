"""test_setdict"""

import pytest

from setdict import Setdict


@pytest.fixture
def setdict_object(scope="module"):
    """docstring"""
    return Setdict({tuple((1, 2, 3,)): "a"})


def test_setdict___init___method(setdict_object):
    """docstring"""
    assert isinstance(setdict_object, Setdict)


def test_setdict_value_setter(setdict_object):
    """docstring"""
    setdict_object.value = {tuple((3, 2, 1)): "a"}

    assert len(setdict_object) == 1


def test_setdict_value_setter_with_wrong_type(setdict_object):
    """docstring"""
    with pytest.raises(TypeError) as exception_info:
        setdict_object.value = {int(1): "a"}

    assert exception_info.type is TypeError


def test_setdict_value_getter(setdict_object):
    """docstring"""
    assert len(setdict_object.value) == 1


def test_setdict_set(setdict_object):
    """docstring"""
    setdict_object.set(set((1, 2, 3,)), "a")

    assert len(setdict_object) == 1


def test_setdict_set_with_wrong_type(setdict_object):
    """docstring"""
    with pytest.raises(TypeError) as exception_info:
        setdict_object.set(str("1"), "a")

    assert exception_info.type is TypeError


def test_setdict___contains__(setdict_object):
    """docstring"""
    assert set((1, 2, 3,)) in setdict_object


def test_setdict___contains__with_wrong_type(setdict_object):
    """docstring"""
    with pytest.raises(TypeError) as exception_info:
        float(1) in setdict_object

    assert exception_info.type is TypeError


def test_setdict_has_value(setdict_object):
    """docstring"""
    assert setdict_object.has_value("a")


def test_setdict_get(setdict_object):
    """docstring"""
    assert setdict_object.get(set((1, 2, 3,))) == "a"


def test_setdict_get_with_unused_default(setdict_object):
    """docstring"""
    assert setdict_object.get(set((1, 2, 3,)), "default") == "a"


def test_setdict_get_with_used_default(setdict_object):
    """docstring"""
    assert setdict_object.get(set((2, 3, 4)), "default") == "default"


def test_setdict_get_with_wrong_type(setdict_object):
    """docstring"""
    with pytest.raises(TypeError) as exception_info:
        setdict_object.get(int(1))

    assert exception_info.type is TypeError


def test_setdict_get_key(setdict_object):
    """docstring"""
    assert setdict_object.get_key("a") == set((1, 2, 3,))


def test_setdict_get_value(setdict_object):
    """docstring"""
    assert setdict_object.get_value(set((1, 2, 3,))) == "a"


def test_setdict_get_value_with_wrong_type(setdict_object):
    """docstring"""
    with pytest.raises(TypeError) as exception_info:
        setdict_object.get_value(str("1"))

    assert exception_info.type is TypeError


def test_setdict___str__method(setdict_object):
    """docstring"""
    assert str(setdict_object) == "{set((1, 2, 3)): 'a'}"


def test_setdict___repr__method(setdict_object):
    """docstring"""
    assert repr(setdict_object) == "'{set((1, 2, 3)): 'a'}'"

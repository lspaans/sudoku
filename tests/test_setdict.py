"""test_setdict"""

import pytest

from setdict import Setdict


@pytest.fixture
def setdict_object(scope="module"):
    return Setdict()


def test_setdict___init___method(setdict_object):
    assert isinstance(setdict_object, Setdict)


def test_setdict__validate_key_method(setdict_object):
    assert setdict_object._validate_key(set(())) is None

    with pytest.raises(TypeError) as exception_info:
        setdict_object._validate_key(int())

    assert exception_info.type is TypeError

    with pytest.raises(TypeError) as exception_info:
        setdict_object._validate_key(float())

    assert exception_info.type is TypeError

    with pytest.raises(TypeError) as exception_info:
        setdict_object._validate_key(str())

    assert exception_info.type is TypeError


def test_setdict_value_setter(setdict_object):
    setdict_object.value = {tuple((1, 2, 3,)): "a"}

    assert len(setdict_object) == 1


def test_setdict_value_getter(setdict_object):
    setdict_object.value = {tuple((1, 2, 3,)): "a"}

    assert len(setdict_object.value) == 1


def test_setdict_set(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert len(setdict_object) == 1


def test_setdict___contains__(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert set((1, 2, 3,)) in setdict_object


def test_setdict_has_value(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert setdict_object.has_value("a")


def test_setdict_get(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert setdict_object.get(set((1, 2, 3,))) == "a"


def test_setdict_get_key(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert setdict_object.get_key("a") == set((1, 2, 3,))


def test_setdict_get_value(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert setdict_object.get_value(set((1, 2, 3,))) == "a"


def test_setdict___str__method(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert str(setdict_object) == "{set((1, 2, 3)): 'a'}"


def test_setdict___repr__method(setdict_object):
    setdict_object.set(set((1, 2, 3,)), "a")

    assert repr(setdict_object) == "'{set((1, 2, 3)): 'a'}'"

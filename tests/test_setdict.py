"""test_setdict"""

import pytest

from setdict import Setdict

@pytest.fixture
def setdict_setup(scope="module"):
    return Setdict()

def test_setdict___init___method(setdict_setup):
    assert isinstance(setdict_setup, Setdict)

def test_setdict__validate_key_method(setdict_setup):
    assert setdict_setup._validate_key(set([])) is None

    with pytest.raises(TypeError) as exception_info:
        setdict_setup._validate_key(int())

    assert exception_info.type is TypeError

    with pytest.raises(TypeError) as exception_info:
        setdict_setup._validate_key(float())

    assert exception_info.type is TypeError

    with pytest.raises(TypeError) as exception_info:
        setdict_setup._validate_key(str())

    assert exception_info.type is TypeError

def test_setdict_get(setdict_setup):
    assert True is True

def test_setdict_get_key(setdict_setup):
    assert True is True

def test_setdict_get_value(setdict_setup):
    assert True is True

def test_setdict_has_key(setdict_setup):
    assert True is True

def test_setdict_has_value(setdict_setup):
    assert True is True

def test_setdict_set(setdict_setup):
    assert True is True

def test_setdict_value_getter(setdict_setup):
    assert True is True

def test_setdict_value_setter(setdict_setup):
    assert True is True

def test_setdict___str__method(setdict_setup):
    assert True is True

def test_setdict___repr__method(setdict_setup):
    assert True is True

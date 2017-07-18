"""test_setmap"""

import pytest

from setmap import Setmap


@pytest.fixture
def setmap_object(scope="module"):
    """docstring"""
    return Setmap()


def test_setmap___init___method(setmap_object):
    """docstring"""
    assert isinstance(setmap_object, Setmap)

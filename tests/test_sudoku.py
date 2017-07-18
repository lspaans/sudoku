"""test_sudoku"""

import pytest

from sudoku import Sudoku


@pytest.fixture
def sudoku_object(scope="module"):
    """docstring"""
    return Sudoku()


def test_sudoku___init___method(sudoku_object):
    """docstring"""
    assert isinstance(sudoku_object, Sudoku)

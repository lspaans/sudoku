"""test_game"""

import pytest

from game import Game


@pytest.fixture
def game_object(scope="module"):
    """docstring"""
    return Game()


def test_game___init___method(game_object):
    """docstring"""
    assert isinstance(game_object, Game)

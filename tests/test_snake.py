# pylint: disable=redefined-outer-name, import-error
"""
SnakeGame Test Module.
Optimized for Black, isort, and code coverage.
"""

from unittest.mock import patch

import pytest

from src.snake import SIZE, SnakeGame


@pytest.fixture
def game() -> SnakeGame:
    """Fixture to initialize the game without GUI."""
    with patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.font.Font"
    ):
        return SnakeGame()


def test_initial_state(game: SnakeGame) -> None:
    """Verify initial game state."""
    assert game.score == 0
    assert game.parts == 2
    assert game.running is True


def test_move_logic(game: SnakeGame) -> None:
    """Verify rightward movement logic."""
    initial_x = game.x_pos[0]
    game.move()
    assert game.x_pos[0] == initial_x + SIZE


def test_apple_collision(game: SnakeGame) -> None:
    """Verify score increase upon eating an apple."""
    game.x_pos[0] = 100
    game.y_pos[0] = 100
    game.apple_pos = (100, 100)
    game.check_logic()
    assert game.score == 1
    assert game.parts == 3

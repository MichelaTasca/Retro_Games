# pylint: disable=redefined-outer-name, import-error, no-member
"""PacManGame Test Module."""

from unittest.mock import MagicMock, patch

import pytest

from src.pacman import W_H, W_W, PacManGame


@pytest.fixture
def game():
    """Fixture without GUI."""
    with patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.font.SysFont"
    ):
        return PacManGame()


def test_initial_state(game):
    """Check init values."""
    assert game.score == 0
    assert game.running is True
    assert len(game.dots) > 0


def test_move_pacman_valid(game):
    """Test valid movement."""
    game.level = ["111", "100", "111"]
    game.p_pos = [1, 1]
    game.direction = "RIGHT"
    game.move_pacman()
    assert game.p_pos[0] == 2


def test_ghost_collision_ends_game(game):
    """Check collision."""
    game.p_pos = [5, 5]
    game.g_pos = [5, 5]
    game.update()
    assert game.running is False
    assert game.game_over_state is True


def test_constants():
    """Verify constants are imported correctly."""
    assert W_W > 0
    assert W_H > 0


def test_pacman_advanced_logic(game):
    """Test movement, dot collection, and ghost movement logic."""
    game.move_ghost()

    game.dots = set()
    game.update()
    assert game.game_over_state is True

    with patch("pygame.draw.rect"), patch("pygame.draw.circle"), patch(
        "pygame.display.flip"
    ):

        game.screen.blit = MagicMock()
        game.draw()

        with patch.object(game, "_wait_", return_value=False):
            game.game_over_screen()

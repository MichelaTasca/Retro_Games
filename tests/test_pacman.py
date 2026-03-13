# pylint: disable=redefined-outer-name, import-error
# pylint: disable=protected-access, no-member
"""PacManGame Test Module."""

from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.pacman import W_H, W_W, PacManGame


@pytest.fixture
def game():
    """Fixture without GUI."""
    with patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.font.SysFont"
    ):
        return PacManGame()


# --- CONSTANTS & INITIAL STATE ---


def test_constants():
    """Verify constants are imported correctly."""
    assert W_W > 0
    assert W_H > 0


def test_initial_state(game):
    """Check init values."""
    assert game.score == 0
    assert game.running is True
    assert len(game.dots) > 0


# --- PACMAN MOVEMENT ---


def test_move_pacman_valid(game):
    """Test valid movement."""
    game.level = [list("111"), list("100"), list("111")]
    game.p_pos = [1, 1]
    game.direction = "RIGHT"
    game.next_dir = "RIGHT"
    game.move_pacman()
    assert game.p_pos[0] == 2


def test_pacman_buffered_movement(game):
    """Test that next_dir falls back to current direction if blocked."""
    game.level = [list("1111"), list("1001"), list("1101"), list("1111")]
    game.p_pos = [1, 1]
    game.direction = "RIGHT"

    game.next_dir = "UP"
    game.move_pacman()
    assert game.p_pos == [2, 1]
    assert game.direction == "RIGHT"

    game.next_dir = "DOWN"
    game.move_pacman()
    assert game.p_pos == [2, 2]
    assert game.direction == "DOWN"


# --- GHOST MOVEMENT ---


def test_pacman_ghost_trapped(game):
    """Force the ghost into a dead end to test the U-turn logic."""
    game.level = [list("111"), list("101"), list("111")]
    game.g_pos = [1, 1]
    game.ghost_dir = (0, -1)
    game.move_ghost()
    assert game.ghost_dir == (0, 1)


# --- GAME LOGIC & COLLISIONS ---


def test_pacman_advanced_logic(game):
    """Test movement, dot collection, and ghost movement logic."""
    game.move_ghost()

    game.dots = set()
    game.update()
    assert game.game_over_state is True

    with patch("pygame.draw.rect"), patch("pygame.draw.circle"), patch(
        "pygame.draw.polygon"
    ), patch("pygame.display.flip"):
        game.screen.blit = MagicMock()
        game.mouth_open = True
        game.draw()

        with patch.object(game, "_wait_", return_value=False):
            game.game_over_screen()


def test_ghost_collision_ends_game(game):
    """Check collision."""
    game.p_pos = [5, 5]
    game.g_pos = [5, 5]
    game.update()
    assert game.running is False
    assert game.game_over_state is True


def test_pacman_win_condition(game):
    """Test the winning condition when the dots set is empty."""
    game.dots = {(1, 1)}
    game.p_pos = [1, 1]

    game.update()

    assert not game.dots
    assert game.game_over_state is True

    with patch("pygame.display.flip"), patch("pygame.draw.rect"), patch(
        "pygame.draw.circle"
    ), patch("pygame.draw.polygon"), patch.object(game, "_wait_", return_value=True):
        game.game_over_screen()


# --- RENDERING (UI) ---


def test_pacman_draw_all_directions(game):
    """Verify the rendering of the mouth polygon in all directions."""
    game.mouth_open = True
    with patch("pygame.draw.rect"), patch("pygame.draw.circle"), patch(
        "pygame.draw.polygon"
    ), patch("pygame.display.flip"):
        for direction in ["LEFT", "UP", "DOWN", "RIGHT"]:
            game.direction = direction
            game.draw()


# --- EXIT & MENU MANAGEMENT ---


def test_pacman_wait_retry_click(game):
    """Simulate a click on the RETRY button to reset the game."""
    with patch("pygame.event.get") as mock_get:
        simulated_click = MagicMock()
        simulated_click.type = pygame.MOUSEBUTTONDOWN
        retry_rect = pygame.Rect(182, 302, 160, 40)
        simulated_click.pos = retry_rect.center
        mock_get.return_value = [simulated_click]
        assert game._wait_(retry_rect, pygame.Rect(0, 0, 1, 1)) is True


def test_pacman_wait_menu_exit(game):
    """Test that clicking the menu button triggers subprocess and exits."""
    with patch("pygame.event.get") as mock_get, patch(
        "subprocess.Popen"
    ) as mock_popen, patch("sys.exit", side_effect=SystemExit), patch("pygame.quit"):

        menu_click = MagicMock()
        menu_click.type = pygame.MOUSEBUTTONDOWN
        menu_click.pos = (250, 380)
        mock_get.return_value = [menu_click]

        retry_rect = pygame.Rect(182, 302, 160, 40)
        menu_rect = pygame.Rect(182, 362, 160, 40)

        with pytest.raises(SystemExit):
            game._wait_(retry_rect, menu_rect)

        mock_popen.assert_called_once()

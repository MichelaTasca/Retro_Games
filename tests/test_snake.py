# pylint: disable=redefined-outer-name, import-error, protected-access, no-member
"""
SnakeGame Test Module.
Optimized for Black, isort, and code coverage.
"""

from unittest.mock import MagicMock, patch

import pygame
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
    game.update()
    assert game.score == 1
    assert game.parts == 3


def test_snake_collisions_and_ui(game):
    """Test snake collision with walls and game over UI."""
    game.x_pos[0] = -25
    game.update()
    assert game.game_over_state is True

    with patch("pygame.draw.rect"), patch("pygame.draw.line"), patch(
        "pygame.display.flip"
    ):
        game.screen.blit = MagicMock()
        game.draw()

        with patch.object(game, "_wait_"):
            game.game_over_screen()


def test_snake_input_and_events(game):
    """Test input handling and menu exit logic."""
    game._update_dir(pygame.K_w)
    assert game.direction == "W"
    game._update_dir(pygame.K_a)
    assert game.direction == "A"

    with patch("pygame.event.get") as mock_get:
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_s
        mock_get.return_value = [mock_event]
        game.handle_input()
        assert game.direction == "S"


def test_snake_wait_menu_exit(game):
    """Test that clicking the menu button in
    the game over screen exits the game."""
    with patch("pygame.event.get") as mock_get:
        menu_click = MagicMock()
        menu_click.type = pygame.MOUSEBUTTONDOWN
        menu_click.pos = (250, 370)
        mock_get.return_value = [menu_click]

        retry_rect = pygame.Rect(170, 290, 160, 40)
        menu_rect = pygame.Rect(170, 350, 160, 40)
        game._wait_(retry_rect, menu_rect)

        assert game.running is False
        assert game.game_over_state is False

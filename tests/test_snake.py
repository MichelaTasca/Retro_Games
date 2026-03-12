# pylint: disable=redefined-outer-name, import-error, protected-access, no-member
"""
SnakeGame Test Module.
Optimized for Black, isort, code coverage, and Multiplayer logic.
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
        g = SnakeGame()
        g.in_menu = False
        g.reset_game()
        return g


def test_initial_state(game: SnakeGame) -> None:
    """Verify initial game state for P1."""
    assert game.p1_score == 0
    assert game.p1_parts == 2
    assert game.running is True


def test_move_logic(game: SnakeGame) -> None:
    """Verify rightward movement logic for P1."""
    initial_x = game.p1_x[0]
    game.p1_dir = "D"
    game.move()
    assert game.p1_x[0] == initial_x + SIZE


def test_apple_collision(game: SnakeGame) -> None:
    """Verify score increase upon P1 eating an apple."""
    game.p1_x[0] = 100
    game.p1_y[0] = 100
    game.p1_apple = (100, 100)
    game.update()
    assert game.p1_score == 1
    assert game.p1_parts == 3


def test_snake_collisions_and_ui(game: SnakeGame) -> None:
    """Test P1 collision with walls and game over UI."""
    game.p1_x[0] = -25
    game.update()
    assert game.game_over_state is True

    with patch("pygame.draw.rect"), patch("pygame.draw.line"), patch(
        "pygame.display.flip"
    ):
        game.screen.blit = MagicMock()
        game.draw()

        with patch.object(game, "_wait_"):
            game.game_over_screen()


def test_snake_input_and_events(game: SnakeGame) -> None:
    """Test input handling for P1."""
    game._update_p1_dir(pygame.K_w)
    assert game.p1_dir == "W"
    game._update_p1_dir(pygame.K_a)
    assert game.p1_dir == "A"

    with patch("pygame.event.get") as mock_get:
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_s
        mock_get.return_value = [mock_event]
        game.handle_input()
        assert game.p1_dir == "S"


def test_snake_wait_menu_exit(game: SnakeGame) -> None:
    """Test that clicking the menu button triggers subprocess and exits."""
    simulated_click = MagicMock()
    simulated_click.type = pygame.MOUSEBUTTONDOWN
    simulated_click.pos = (250, 370)

    with patch("subprocess.Popen") as process_mock, patch(
        "pygame.event.get", return_value=[simulated_click]
    ), patch("sys.exit", side_effect=SystemExit), patch("pygame.quit"):

        retry_btn = pygame.Rect(170, 290, 160, 40)
        menu_btn = pygame.Rect(170, 350, 160, 40)

        with pytest.raises(SystemExit):
            game._wait_(retry_btn, menu_btn)
            process_mock.assert_called_once()

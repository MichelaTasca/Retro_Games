# pylint: disable=redefined-outer-name, import-error
# pylint: disable=protected-access, no-member
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
    with (
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.font.Font"),
    ):
        g = SnakeGame()
        g.in_menu = False
        g.reset_game()
        return g


# --- CORE STATES & MENU ---


def test_initial_state(game: SnakeGame) -> None:
    """Verify initial game state for P1."""
    assert game.p1_score == 0
    assert game.p1_parts == 2
    assert game.running is True


def test_snake_main_menu_1p(game: SnakeGame) -> None:
    """Test the selection of 1 Player mode from the Main Menu."""
    game.in_menu = True
    with (
        patch("pygame.event.get") as mock_get,
        patch("pygame.display.flip"),
        patch("pygame.draw.rect"),
    ):
        click_event = MagicMock()
        click_event.type = pygame.MOUSEBUTTONDOWN
        click_event.pos = (250, 230)
        mock_get.return_value = [click_event]

        game.main_menu()
        assert game.num_players == 1
        assert game.in_menu is False


def test_snake_main_menu_2p(game: SnakeGame) -> None:
    """Test the selection of 2 Players mode from the Main Menu."""
    game.in_menu = True
    with (
        patch("pygame.event.get") as mock_get,
        patch("pygame.display.flip"),
        patch("pygame.draw.rect"),
    ):
        click_event = MagicMock()
        click_event.type = pygame.MOUSEBUTTONDOWN
        click_event.pos = (250, 300)
        mock_get.return_value = [click_event]

        game.main_menu()
        assert game.num_players == 2
        assert game.in_menu is False


def test_snake_run_loop_states(game: SnakeGame) -> None:
    """Cover the main run loop for all game states."""
    game.in_menu = True
    with patch.object(game, "main_menu") as mock_menu:
        game.run(once=True)
        mock_menu.assert_called_once()

    game.in_menu = False
    game.running = True
    with (
        patch.object(game, "handle_input"),
        patch.object(game, "move"),
        patch.object(game, "update"),
        patch.object(game, "draw"),
    ):
        game.run(once=True)

    game.in_menu = False
    game.running = False
    game.game_over_state = True
    with patch.object(game, "game_over_screen") as mock_go:
        game.run(once=True)
        mock_go.assert_called_once()


def test_snake_run_game_over_exit(game: SnakeGame) -> None:
    """Verify the explicit 'return' condition inside the main loop."""
    game.in_menu = False
    game.running = False
    game.game_over_state = True

    def mock_screen():
        game.game_over_state = False

    with patch.object(game, "game_over_screen", side_effect=mock_screen):
        game.run()


# --- SINGLE PLAYER (P1) LOGIC & INPUT ---


def test_p1_input_all_directions(game: SnakeGame) -> None:
    """Verify all WASD keys for Player 1."""
    directions = [
        (pygame.K_w, "W"),
        (pygame.K_s, "S"),
        (pygame.K_a, "A"),
        (pygame.K_d, "D"),
    ]
    for key, expected in directions:
        game.p1_dir = ""
        game._update_p1_dir(key)
        assert game.p1_dir == expected


def test_snake_handle_input_event(game: SnakeGame) -> None:
    """
    Test that handle_input correctly processes KEYDOWN events
    and updates the player's direction accordingly.
    """
    with patch("pygame.event.get") as mock_get:
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_s
        mock_get.return_value = [mock_event]
        game.handle_input()
        assert game.p1_dir == "S"


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


def test_snake_new_apple_collisions(game: SnakeGame) -> None:
    """Force the random generator to cover
    'continue' statements on overlaps."""
    game.num_players = 2
    game.reset_game()
    game.walls = [(0, 0)]
    game.p1_x[0], game.p1_y[0] = 25, 0
    game.p2_x[0], game.p2_y[0] = 50, 0

    with patch("random.randint", side_effect=[0, 0, 1, 0, 2, 0, 3, 0]):
        game.new_apple(1)

    assert game.p1_apple == (75, 0)


def test_snake_p1_eat_itself(game: SnakeGame) -> None:
    """Test P1 colliding with its own body."""
    game.num_players = 1
    game.reset_game()
    game.p1_x[1] = game.p1_x[0]
    game.p1_y[1] = game.p1_y[0]

    game.update()

    assert game.game_over_state is True


def test_snake_walls_collision(game: SnakeGame) -> None:
    """Test collision with obstacles (Missing in current tests)."""
    game.num_players = 1
    game.walls = [(100, 100)]
    game.p1_x[0], game.p1_y[0] = 100, 100
    game.update()
    assert game.game_over_state is True


def test_snake_collisions_and_ui(game: SnakeGame) -> None:
    """Test P1 collision with walls and game over UI."""
    game.p1_x[0] = -25
    game.update()
    assert game.game_over_state is True

    with (
        patch("pygame.draw.rect"),
        patch("pygame.draw.line"),
        patch("pygame.display.flip"),
        patch.object(game.screen, "blit"),
    ):
        game.draw()
        with patch.object(game, "_wait_"):
            game.game_over_screen()


# --- MULTIPLAYER (P2) LOGIC & INPUT ---


def test_snake_multiplayer_logic(game: SnakeGame) -> None:
    """Test setup & palyer 2 movements."""
    game.num_players = 2
    game.reset_game()
    assert game.p2_parts == 2

    initial_p2_x = game.p2_x[0]
    game.p2_dir = "R"
    game.move()
    assert game.p2_x[0] == initial_p2_x + SIZE


def test_p2_input_arrows(game: SnakeGame) -> None:
    """Test if arrow buttons change P2 direction for all keys."""
    game.num_players = 2

    directions = [
        (pygame.K_UP, "U"),
        (pygame.K_DOWN, "D"),
        (pygame.K_LEFT, "L"),
        (pygame.K_RIGHT, "R"),
    ]

    for key, expected in directions:
        game.p2_dir = ""
        game._update_p2_dir(key)
        assert game.p2_dir == expected


def test_snake_p2_eat_apple(game: SnakeGame) -> None:
    """Test P2 eating an apple to cover P2 score logic."""
    game.num_players = 2
    game.reset_game()
    game.p2_x[0] = 100
    game.p2_y[0] = 100
    game.p2_apple = (100, 100)

    game.update()

    assert game.p2_score == 1
    assert game.p2_parts == 3


def test_snake_p1_death_by_p2(game: SnakeGame) -> None:
    """Test P1 death if it hits P2 body"""
    game.num_players = 2
    game.reset_game()
    game.p1_x[0] = game.p2_x[1]
    game.p1_y[0] = game.p2_y[1]
    game.update()
    assert game.game_over_state is True
    assert game.winner == 2


def test_snake_p2_death_by_p1(game: SnakeGame) -> None:
    """Test P2 death if it hits P1 body"""
    game.num_players = 2
    game.reset_game()
    game.p2_x[0] = game.p1_x[1]
    game.p2_y[0] = game.p1_y[1]
    game.update()
    assert game.game_over_state is True
    assert game.winner == 1


def test_snake_simultaneous_death(game: SnakeGame) -> None:
    """Test simultaneous death of P1 and P2 (multiplayer draw)."""
    game.num_players = 2
    game.reset_game()
    game.p1_x[0] = -100
    game.p2_x[0] = -100

    game.update()

    assert game.game_over_state is True
    assert game.winner == 0


def test_snake_draw_multiplayer_ui(game: SnakeGame) -> None:
    """Cover the P2 drawing logic"""
    game.num_players = 2
    with (
        patch("pygame.draw.rect"),
        patch("pygame.draw.line"),
        patch("pygame.display.flip"),
    ):
        game.draw()


# --- GAME OVER, UI, & WAIT LOGIC ---


def test_snake_game_over_draw_tie(game: SnakeGame) -> None:
    """Verify the rendering of the Game Over screen in case of a tie."""
    game.num_players = 2
    game.winner = 0
    with (
        patch("pygame.display.flip"),
        patch("pygame.draw.rect"),
        patch.object(game, "_wait_"),
    ):
        game.game_over_screen()


def test_snake_wait_retry_click(game: SnakeGame) -> None:
    """Simulate a click on MODES to return to the main menu."""
    with patch("pygame.event.get") as mock_get:
        click_event = MagicMock()
        click_event.type = pygame.MOUSEBUTTONDOWN
        retry_rect = pygame.Rect(170, 290, 160, 40)
        click_event.pos = retry_rect.center
        mock_get.return_value = [click_event]

        game._wait_(retry_rect, pygame.Rect(0, 0, 1, 1))

        assert game.in_menu is True
        assert game.game_over_state is False


def test_snake_wait_menu_exit(game: SnakeGame) -> None:
    """Test that clicking the menu button triggers subprocess and exits."""
    simulated_click = MagicMock()
    simulated_click.type = pygame.MOUSEBUTTONDOWN
    simulated_click.pos = (250, 370)

    with (
        patch("subprocess.Popen") as process_mock,
        patch("pygame.event.get", return_value=[simulated_click]),
        patch("sys.exit", side_effect=SystemExit),
        patch("pygame.quit"),
    ):

        retry_btn = pygame.Rect(170, 290, 160, 40)
        menu_btn = pygame.Rect(170, 350, 160, 40)

        with pytest.raises(SystemExit):
            game._wait_(retry_btn, menu_btn)
            process_mock.assert_called_once()


# --- QUIT EVENTS (SYSTEM EXITS) ---


def test_snake_quit_event(game: SnakeGame) -> None:
    """Test the QUIT event handling inside handle_input."""
    with (
        patch("pygame.event.get") as mock_get,
        patch("sys.exit", side_effect=SystemExit),
        patch("pygame.quit"),
    ):

        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mock_get.return_value = [quit_event]

        with pytest.raises(SystemExit):
            game.handle_input()


def test_snake_quit_main_menu(game: SnakeGame) -> None:
    """Test the QUIT event inside the main_menu loop."""
    game.in_menu = True
    with (
        patch("pygame.event.get") as mock_get,
        patch("sys.exit", side_effect=SystemExit),
        patch("pygame.quit"),
        patch("pygame.display.flip"),
        patch("pygame.draw.rect"),
    ):

        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mock_get.return_value = [quit_event]

        with pytest.raises(SystemExit):
            game.main_menu()


def test_snake_quit_wait(game: SnakeGame) -> None:
    """Test the QUIT event inside the _wait_ loop."""
    with (
        patch("pygame.event.get") as mock_get,
        patch("sys.exit", side_effect=SystemExit),
        patch("pygame.quit"),
    ):

        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mock_get.return_value = [quit_event]

        with pytest.raises(SystemExit):
            game._wait_(pygame.Rect(0, 0, 1, 1), pygame.Rect(0, 0, 1, 1))

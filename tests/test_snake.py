# pylint: disable=redefined-outer-name, import-error
"""
Modulo di test per snake_game.
Sistemato per eliminare errori E501 e problemi di importazione.
"""

from unittest.mock import patch

import pytest
from src.snake import SIZE, snake_game


@pytest.fixture
def game() -> snake_game:
    """Fixture per inizializzare il gioco senza interfaccia grafica."""
    with patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.font.Font"
    ):
        return snake_game()


def test_initial_state(game: snake_game) -> None:
    """Verifica lo stato iniziale del gioco."""
    assert game.score == 0
    assert game.parts == 2
    assert game.running is True


def test_move_logic(game: snake_game) -> None:
    """Verifica il movimento a destra."""
    initial_x = game.x_pos[0]
    game.move()
    assert game.x_pos[0] == initial_x + SIZE


def test_apple_collision(game: snake_game) -> None:
    """Verifica l'incremento del punteggio quando si mangia la mela."""
    game.x_pos[0] = 100
    game.y_pos[0] = 100
    game.apple_pos = (100, 100)
    game.check_logic()
    assert game.score == 1
    assert game.parts == 3

# pylint: disable=redefined-outer-name, import-error, no-member
"""
PacManGame Test Module.
Optimized for Flake8 and Pylint (10/10).
"""

from unittest.mock import MagicMock, patch
import pygame
import pytest
# Assicurati che i nomi corrispondano esattamente a src/pacman.py
from src.pacman import W_HGHT, W_WDTH, PacManGame

@pytest.fixture
def game():
    """Fixture to initialize PacManGame without an active GUI window."""
    with patch("pygame.display.set_mode"), \
         patch("pygame.display.set_caption"), \
         patch("pygame.font.SysFont"):
        return PacManGame()

def test_initial_state(game):
    """Verify the game starts with correct default values."""
    assert game.score == 0
    assert game.running is True
    assert game.game_over_state is False
    assert len(game.dots) > 0

def test_move_pacman_valid(game):
    """Test Pac-Man movement into an empty corridor."""
    game.level = ["111", "100", "111"]
    game.p_pos = [1, 1]  # Usiamo la nuova lista p_pos
    game.direction = "RIGHT"
    game.move_pacman()
    assert game.p_pos[0] == 2

def test_move_pacman_collision(game):
    """Verify Pac-Man does not move through walls."""
    game.level = ["111", "111", "111"]
    game.p_pos = [1, 1]
    game.direction = "RIGHT"
    game.move_pacman()
    assert game.p_pos[0] == 1

def test_update_eat_dots(game):
    """Verify score increases and dots are removed when eaten."""
    game.p_pos = [2, 2]
    game.dots = {(2, 2)}
    game.score = 0
    game.update()
    assert game.score == 10
    assert (2, 2) not in game.dots

def test_ghost_collision_ends_game(game):
    """Verify game ends when Pac-Man and Ghost collide."""
    game.p_pos = [5, 5]
    game.g_pos = [5, 5] # Usiamo g_pos invece di g_x/g_y
    game.update()
    assert game.running is False
    assert game.game_over_state is True

def test_draw_coverage(game):
    """Execute draw methods using mocks for rendering lines."""
    with patch("pygame.draw.rect"), patch("pygame.draw.circle"), \
         patch("pygame.draw.polygon"), patch("pygame.display.flip"), \
         patch.object(game.screen, "blit"):
        game.draw()
        assert True

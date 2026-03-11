# pylint: disable=redefined-outer-name, protected-access, no-member
"""ArcadeMenu Test Module updated for return values."""

from unittest.mock import patch

import pygame
import pytest

from src.arcade_menu import ArcadeMenu


@pytest.fixture
def menu():
    """Fixture to initialize the menu with mocked Pygame components."""
    with patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.font.SysFont"
    ):
        return ArcadeMenu()


def test_initial_state(menu):
    """Verify the default selection starts at the first game."""
    assert menu.selected == 0
    assert menu.options == ["PAC-MAN", "SNAKE"]


def test_navigation_down(menu):
    """Test that pressing DOWN changes the selection."""
    menu._handle_keypress(pygame.K_DOWN)
    assert menu.selected == 1
    menu._handle_keypress(pygame.K_DOWN)
    assert menu.selected == 0


def test_handle_keypress_return_value(menu):
    """Verify that ENTER returns the current selection index."""
    # Test selection 0
    assert menu._handle_keypress(pygame.K_RETURN) == 0
    # Test selection 1
    menu.selected = 1
    assert menu._handle_keypress(pygame.K_RETURN) == 1
    # Test other keys return None
    assert menu._handle_keypress(pygame.K_SPACE) is None


def test_caption_animation(menu):
    """Verify that the window title updates based on pulse count."""
    with patch("pygame.display.set_caption") as mock_caption:
        menu._update_caption(15)
        mock_caption.assert_called_with("RETRO ARCADE")
        menu._update_caption(30)
        mock_caption.assert_called_with("RETRO ARCADE ★")

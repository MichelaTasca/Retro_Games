# pylint: disable=redefined-outer-name, import-error, protected-access
"""
ArcadeMenu Test Module.
Testing menu navigation and sub-process launching.
"""

from unittest.mock import patch

import pygame
import pytest

from src.arcade_menu import ArcadeMenu


@pytest.fixture
def menu() -> ArcadeMenu:
    """Fixture to initialize the menu with mocked Pygame components."""
    with patch("pygame.display.set_mode"), patch(
        "pygame.display.set_caption"), patch(
        "pygame.font.SysFont"
    ), patch("pygame.font.Font"):
        return ArcadeMenu()


def test_initial_state(menu: ArcadeMenu) -> None:
    """Verify the default selection starts at the first game."""
    assert menu.selected == 0
    assert menu.options == ["PAC-MAN", "SNAKE"]


def test_navigation_down(menu: ArcadeMenu) -> None:
    """Test that pressing DOWN changes the selection."""
    menu._handle_keypress(pygame.K_DOWN)  # pylint: disable=no-member
    assert menu.selected == 1
    # Test wrapping around
    menu._handle_keypress(pygame.K_DOWN)  # pylint: disable=no-member
    assert menu.selected == 0


def test_navigation_up(menu: ArcadeMenu) -> None:
    """Test that pressing UP changes the selection (with wrapping)."""
    menu._handle_keypress(pygame.K_UP)  # pylint: disable=no-member
    assert menu.selected == 1  # Should wrap to last element


def test_caption_animation(menu: ArcadeMenu) -> None:
    """Verify that the window title updates based on pulse count."""
    with patch("pygame.display.set_caption") as mock_caption:
        menu._update_caption(15)
        mock_caption.assert_called_with("RETRO ARCADE")

        menu._update_caption(30)
        mock_caption.assert_called_with("RETRO ARCADE ★")

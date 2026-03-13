# pylint: disable=redefined-outer-name, protected-access, no-member
"""ArcadeMenu Test Module updated for return values."""

from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.arcade_menu import ArcadeMenu


@pytest.fixture
def menu():
    """Fixture to initialize the menu with mocked Pygame components."""
    with patch("pygame.display.set_mode"), patch(
        "pygame.display.set_caption"), patch(
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


def test_handle_keypress_logic(menu):
    """Verify that ENTER returns the current selection index
    and arrows navigate."""
    menu.selected = 0
    menu._handle_keypress(pygame.K_DOWN)
    assert menu.selected == 1

    result = menu._handle_keypress(pygame.K_RETURN)
    assert result == 1

    menu._handle_keypress(pygame.K_UP)
    assert menu.selected == 0

    result = menu._handle_keypress(pygame.K_RETURN)
    assert result == 0


def test_run_returns_selected(menu):
    """Verify that the run method returns the selected index on ENTER."""
    menu.selected = 1

    menu.clock = MagicMock()

    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_RETURN

    with patch("pygame.event.get", return_value=[mock_event]), patch.object(
        menu, "draw_menu"
    ):

        result = menu.run()
        assert result == 1


def test_caption_animation(menu):
    """Verify that the window title updates based on pulse count."""
    with patch("pygame.display.set_caption") as mock_caption:
        menu._update_caption(15)
        mock_caption.assert_called_with("RETRO ARCADE")
        menu._update_caption(30)
        mock_caption.assert_called_with("RETRO ARCADE ★")


def test_rendering_methods(menu):
    """Mocking PyGame functions to avoid TypeError."""
    with patch("pygame.draw.rect"), patch("pygame.draw.circle"), patch(
        "pygame.draw.line"
    ), patch("pygame.display.flip"):

        menu.scr.blit = MagicMock()

        for font in menu.fonts.values():
            font.render = MagicMock()

        menu.draw_menu()
        menu.draw_arcade_machine()

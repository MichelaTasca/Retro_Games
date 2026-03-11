"""Tests for the main module."""

from unittest.mock import patch

from main import main


def test_main_launch_pacman():
    """Test if main launches Pac-Man and then exits loop."""
    with patch("main.ArcadeMenu.run") as mock_menu, patch(
        "main.PacManGame.run"
    ) as mock_pacman, patch("main.pygame.quit"):

        mock_menu.side_effect = [0, StopIteration]

        try:
            main()
        except StopIteration:
            pass

        mock_pacman.assert_called_once()


def test_main_launch_snake():
    """Test if main launches Snake and then exits loop."""
    with patch("main.ArcadeMenu.run") as mock_menu, patch(
        "main.SnakeGame.run"
    ) as mock_snake, patch("main.pygame.quit"):

        mock_menu.side_effect = [1, StopIteration]

        try:
            main()
        except StopIteration:
            pass

        mock_snake.assert_called_once()


def test_main_exit_on_invalid_choice():
    """Test if main exits when an invalid choice is returned."""
    with patch("main.ArcadeMenu.run", return_value=99), patch(
        "main.pygame.quit"
    ), patch("main.sys.exit") as mock_exit:
        main()
        mock_exit.assert_called_once()

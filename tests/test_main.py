"""Tests for the main module."""

from unittest.mock import patch

from src.main import main


def test_main_launch_pacman():
    """Test if main launches Pac-Man when choice is 0."""
    with patch("src.main.ArcadeMenu.run", return_value=0), patch(
        "src.main.PacManGame.run"
    ) as mock_pacman, patch("src.main.pygame.quit"):
        main()
        mock_pacman.assert_called_once()


def test_main_launch_snake():
    """Test if main launches Snake when choice is 1."""
    with patch("src.main.ArcadeMenu.run", return_value=1), patch(
        "src.main.SnakeGame.run"
    ) as mock_snake, patch("src.main.pygame.quit"):
        main()
        mock_snake.assert_called_once()


def test_main_exit_on_invalid_choice():
    """Test if main exits when an invalid choice is returned."""
    with patch("src.main.ArcadeMenu.run", return_value=99), patch(
        "src.main.pygame.quit"
    ), patch("src.main.sys.exit") as mock_exit:
        main()
        mock_exit.assert_called_once()

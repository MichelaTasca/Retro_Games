"""Main module of the Retro Games project."""

import sys

import pygame

from src.arcade_menu import ArcadeMenu
from src.pacman import PacManGame
from src.snake import SnakeGame


def main() -> None:
    """
    Main entry point.
    Initializes the menu, gets the user's choice,
    and routes to the selected game.
    """
    # Initialize and run the menu to get the user choice
    menu = ArcadeMenu()
    choice = menu.run()

    # Quit the menu display cleanly before initializing a new game window
    pygame.quit()  # pylint: disable=no-member

    # Route to the appropriate game based on the choice returned by the menu
    # Calling run() directly avoids Mypy "Incompatible types" assignment errors
    if choice == 0:
        PacManGame().run()
    elif choice == 1:
        SnakeGame().run()
    else:
        sys.exit()


if __name__ == "__main__":
    main()

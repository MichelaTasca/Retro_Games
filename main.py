# pylint: disable=no-member
"""Main module of the Retro Games project."""

import pygame

from src.arcade_menu import ArcadeMenu
from src.pacman import PacManGame
from src.snake import SnakeGame


def main() -> None:
    """Main entry point with persistent game loop."""
    while True:

        menu = ArcadeMenu()
        choice = menu.run()

        pygame.display.quit()
        pygame.quit()

        if choice == 0:
            PacManGame().run()
        elif choice == 1:
            SnakeGame().run()
        else:
            break


if __name__ == "__main__":
    main()

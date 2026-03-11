# pylint: disable=no-member, duplicate-code
"""
Module for managing a retro 80s-style Arcade Menu.
Handles the selection between Pac-Man and Snake.
"""

import subprocess
import sys
from typing import List, Tuple

import pygame

# Graphical constants
Color = Tuple[int, int, int]

W_WDT: int = 700
WIND_HGT: int = 700
BLACK: Color = (0, 0, 0)
NEON_GREEN: Color = (0, 255, 120)
NEON_YELLOW: Color = (255, 255, 80)
NEON_BLUE: Color = (80, 180, 255)
NEON_RED: Color = (255, 70, 70)
DK_G: Color = (20, 20, 20)
LI_G: Color = (80, 80, 80)


class ArcadeMenu:
    """
    Main class that manages the arcade menu graphical interface.
    """

    def __init__(self) -> None:
        """Initialize Pygame, the screen, and graphical resources."""
        pygame.init()  # pylint: disable=no-member
        pygame.display.set_caption("RETRO ARCADE")
        self.scr = pygame.display.set_mode((W_WDT, WIND_HGT))
        self.clock = pygame.time.Clock()

        self.fonts = {
            "title": pygame.font.SysFont(
                ["Press Start 2P", "Arial", "sans-serif"], 36, bold=True
            ),
            "menu": pygame.font.SysFont([
                "Press Start 2P", "Arial", "sans-serif"], 20),
            "info": pygame.font.SysFont([
                "Press Start 2P", "Arial", "sans-serif"], 14),
        }

        self.options: List[str] = ["PAC-MAN", "SNAKE"]
        self.selected: int = 0

        # Create surface for the scanline effect
        self.scanlines = pygame.Surface(
            (W_WDT, WIND_HGT), pygame.SRCALPHA  # pylint: disable=no-member
        )
        for y in range(0, WIND_HGT, 2):
            pygame.draw.line(self.scanlines, (0, 0, 0, 40), (0, y), (W_WDT, y))

    def draw_arcade_machine(self) -> None:
        """Draw the aesthetic shell of the arcade machine."""
        scr = self.scr

        # Main cabinet body
        pygame.draw.rect(scr, DK_G, (150, 100, 400, 500), border_radius=15)
        pygame.draw.rect(scr, LI_G, (150, 100, 400, 500), 6, border_radius=15)

        # Upper part (marquee)
        pygame.draw.rect(scr, NEON_BLUE, (150, 70, 400, 40), border_radius=10)
        title = self.fonts["title"].render("RETRO ARCADE", True, NEON_YELLOW)
        scr.blit(title, title.get_rect(center=(W_WDT // 2, 90)))

        # Central screen area
        pygame.draw.rect(scr, BLACK, (180, 140, 340, 320))
        pygame.draw.rect(scr, NEON_GREEN, (180, 140, 340, 320), 3)

        # Decorative buttons
        pygame.draw.circle(scr, NEON_RED, (270, 500), 18)
        pygame.draw.circle(scr, NEON_BLUE, (430, 500), 18)

        # Bottom base
        pygame.draw.rect(scr, LI_G, (150, 560, 400, 40), border_radius=10)
        pygame.draw.line(scr, NEON_GREEN, (150, 560), (550, 560), 3)

    def draw_menu(self) -> None:
        """Render menu txt and options onto the screen."""
        self.scr.fill(BLACK)
        self.draw_arcade_machine()

        for i, option in enumerate(self.options):
            color = NEON_GREEN if i == self.selected else NEON_BLUE
            txt = self.fonts["menu"].render(option, True, color)
            self.scr.blit(txt, txt.get_rect(center=(W_WDT // 2, 220 + i * 60)))

        info_txt = "↑ ↓ to choose | ENTER to start"
        info = self.fonts["info"].render(info_txt, True, (100, 100, 100))
        self.scr.blit(info, info.get_rect(center=(W_WDT // 2, 620)))

        self.scr.blit(self.scanlines, (0, 0))
        pygame.display.flip()

    def launch_game(self) -> None:
        """Launch the sub-process for the selected game and close the menu."""
        game_files = {0: "src/pacman.py", 1: "src/snake.py"}
        script_to_launch = game_files.get(self.selected)

        if script_to_launch:
            with subprocess.Popen([sys.executable, script_to_launch]):
                pass

        pygame.quit()  # pylint: disable=no-member
        sys.exit()

    def run(self) -> int:
        """Main program loop. Returns the selected game index."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.selected  # Ritorna la scelta al main.py
                    self._handle_keypress(event.key)
            self.draw_menu()
            self.clock.tick(30)

    def _handle_keypress(self, key: int) -> int | None:
        """
        Handle keyboard input for navigation.
        Returns the selected index if ENTER is pressed, otherwise None.
        """
        if key == pygame.K_UP:  # pylint: disable=no-member
            self.selected = (self.selected - 1) % len(self.options)
        elif key == pygame.K_DOWN:  # pylint: disable=no-member
            self.selected = (self.selected + 1) % len(self.options)
        elif key == pygame.K_RETURN:  # pylint: disable=no-member
            return self.selected
        return None

    def _update_caption(self, pulse: int) -> None:
        """Create an animated effect in the window title."""
        if pulse % 30 == 0:
            pygame.display.set_caption("RETRO ARCADE ★")
        elif pulse % 15 == 0:
            pygame.display.set_caption("RETRO ARCADE")


if __name__ == "__main__":
    ArcadeMenu().run()

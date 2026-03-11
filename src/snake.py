# pylint: disable=no-member, duplicate-code, too-many-instance-attributes
"""
Retro Snake Game Module.
Final version with Game Over screen (Retry/Menu) and 10/10 Pylint score.
"""

import random
import sys
from typing import List, Tuple

import pygame

# Configuration Constants
WDTH: int = 500
HGHT: int = 500
SIZE: int = 25
SPEED: int = 120

# Color Palette (RGB)
DARK_GREEN: Tuple[int, int, int] = (10, 20, 10)
NEON_GREEN: Tuple[int, int, int] = (0, 255, 70)
NEON_RED: Tuple[int, int, int] = (255, 80, 80)
NEON_BLUE: Tuple[int, int, int] = (0, 180, 255)
LIGHT_BLUE: Tuple[int, int, int] = (0, 0, 255)
GRID_COLOR: Tuple[int, int, int] = (30, 50, 30)
GRAY: Tuple[int, int, int] = (50, 50, 50)
WHITE: Tuple[int, int, int] = (255, 255, 255)


# pylint: disable=too-many-instance-attributes
class SnakeGame:
    """Class handling Snake game logic and rendering."""

    def __init__(self) -> None:
        """Initialize Pygame and game state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WDTH, HGHT))
        pygame.display.set_caption("SNAKE RETRO")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)

        # Game State
        self.running = True
        self.game_over_state = False
        self.direction = "D"
        self.score = 0
        self.parts = 2

        # Positions Initialization
        capacity = (WDTH * HGHT) // (SIZE**2)
        self.x_pos: List[int] = [0] * capacity
        self.y_pos: List[int] = [0] * capacity
        self.apple_pos = (0, 0)
        self.reset_game()

    def reset_game(self) -> None:
        """Reset initial session parameters."""
        self.running = True
        self.game_over_state = False
        self.direction = "D"
        self.score = 0
        self.parts = 2
        self.x_pos = [0] * len(self.x_pos)
        self.y_pos = [0] * len(self.y_pos)
        self.new_apple()

    def new_apple(self) -> None:
        """Create an apple at a random aligned position."""
        ax = random.randint(0, (WDTH // SIZE) - 1) * SIZE
        ay = random.randint(0, (HGHT // SIZE) - 1) * SIZE
        self.apple_pos = (ax, ay)

    def draw(self) -> None:
        """Render graphical elements."""
        self.screen.fill(DARK_GREEN)

        for i in range(0, WDTH, SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (i, 0), (i, HGHT))
            pygame.draw.line(self.screen, GRID_COLOR, (0, i), (WDTH, i))

        apple_rect = (self.apple_pos[0], self.apple_pos[1], SIZE, SIZE)
        pygame.draw.rect(self.screen, NEON_RED, apple_rect)

        for i in range(self.parts):
            color = NEON_BLUE if i == 0 else LIGHT_BLUE
            pos_rect = (self.x_pos[i], self.y_pos[i], SIZE, SIZE)
            pygame.draw.rect(self.screen, color, pos_rect)

        score_surf = self.font.render(f"SCORE: {self.score}", True, NEON_GREEN)
        self.screen.blit(score_surf, (10, 10))
        pygame.display.flip()

    def move(self) -> None:
        """Update snake segment coordinates."""
        for i in range(self.parts, 0, -1):
            self.x_pos[i] = self.x_pos[i - 1]
            self.y_pos[i] = self.y_pos[i - 1]

        mv = {"W": (0, -SIZE), "S": (0, SIZE), "A": (-SIZE, 0), "D": (SIZE, 0)}
        dx, dy = mv[self.direction]
        self.x_pos[0] += dx
        self.y_pos[0] += dy

    def update(self) -> None:
        """Check for apple collection and collisions."""
        hx, hy = self.x_pos[0], self.y_pos[0]
        if hx == self.apple_pos[0] and hy == self.apple_pos[1]:
            self.parts += 1
            self.score += 1
            self.new_apple()

        for i in range(1, self.parts):
            if hx == self.x_pos[i] and hy == self.y_pos[i]:
                self.running = False
                self.game_over_state = True

        if not (0 <= hx < WDTH and 0 <= hy < HGHT):
            self.running = False
            self.game_over_state = True

    def game_over_screen(self) -> None:
        """Display Game Over screen with Retry and Menu options."""
        self.screen.fill(DARK_GREEN)
        msg = self.font.render("GAME OVER", True, NEON_RED)
        score_txt = self.font.render(f"FINAL SCORE: {self.score}", True, WHITE)

        retry_rect = pygame.Rect(WDTH // 2 - 80, HGHT // 2 + 40, 160, 40)
        menu_rect = pygame.Rect(WDTH // 2 - 80, HGHT // 2 + 100, 160, 40)

        pygame.draw.rect(self.screen, GRAY, retry_rect, border_radius=10)
        pygame.draw.rect(self.screen, NEON_BLUE, menu_rect, border_radius=10)

        r_txt = self.small_font.render("RETRY", True, WHITE)
        m_txt = self.small_font.render("MENU", True, WHITE)

        self.screen.blit(msg, msg.get_rect(center=(WDTH // 2, HGHT // 2 - 60)))
        self.screen.blit(
            score_txt, score_txt.get_rect(center=(WDTH // 2, HGHT // 2 - 10))
        )
        self.screen.blit(r_txt, r_txt.get_rect(center=retry_rect.center))
        self.screen.blit(m_txt, m_txt.get_rect(center=menu_rect.center))

        pygame.display.flip()
        self._wait_(retry_rect, menu_rect)

    def _wait_(self, retry_rect: pygame.Rect, menu_rect: pygame.Rect) -> None:
        """Wait for player to click Retry or Menu."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(event.pos):
                        self.reset_game()
                        waiting = False
                    elif menu_rect.collidepoint(event.pos):
                        self.running = False
                        self.game_over_state = False
                        return
            self.clock.tick(30)

    def handle_input(self) -> None:
        """Handle keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._update_dir(event.key)

    def _update_dir(self, key: int) -> None:
        """Update direction based on key press."""
        if key == pygame.K_a and self.direction != "D":
            self.direction = "A"
        elif key == pygame.K_d and self.direction != "A":
            self.direction = "D"
        elif key == pygame.K_w and self.direction != "S":
            self.direction = "W"
        elif key == pygame.K_s and self.direction != "W":
            self.direction = "S"

    def run(self) -> None:
        """Main game loop."""
        while True:
            if self.running:
                self.handle_input()
                self.move()
                self.update()
                self.draw()
                self.clock.tick(1000 // SPEED)
            elif self.game_over_state:
                self.game_over_screen()
                if not self.game_over_state and not self.running:
                    return


if __name__ == "__main__":
    SnakeGame().run()

# pylint: disable=no-member, duplicate-code, too-many-instance-attributes
"""
Retro Snake Game Module.
Menu, Single Player (with walls) & Two-Player modes.
Returns to Main Arcade Menu.
"""

import random
import subprocess
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
GRID_COLOR: Tuple[int, int, int] = (30, 50, 30)
GRAY: Tuple[int, int, int] = (50, 50, 50)
WHITE: Tuple[int, int, int] = (255, 255, 255)
WALL_COLOR: Tuple[int, int, int] = (150, 150, 150)

# Player 1 Colors (Red/Orange)
P1_HEAD: Tuple[int, int, int] = (255, 128, 0)
P1_BODY: Tuple[int, int, int] = (200, 0, 0)
P1_APPLE: Tuple[int, int, int] = (255, 80, 80)

# Player 2 Colors (Blue/Light Blue)
P2_HEAD: Tuple[int, int, int] = (0, 0, 255)
P2_BODY: Tuple[int, int, int] = (0, 180, 255)
P2_APPLE: Tuple[int, int, int] = (50, 100, 255)


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
        self.in_menu = True
        self.running = False
        self.game_over_state = False
        self.num_players = 1
        self.winner = 0  # 0: Tie/None, 1: P1, 2: P2
        self.capacity = (WDTH * HGHT) // (SIZE**2)

        # Arrays allocation
        self.p1_x: List[int] = [0] * self.capacity
        self.p1_y: List[int] = [0] * self.capacity
        self.p2_x: List[int] = [0] * self.capacity
        self.p2_y: List[int] = [0] * self.capacity
        self.walls: List[Tuple[int, int]] = []

        # State variables
        self.p1_dir = self.p2_dir = ""
        self.p1_score = self.p2_score = 0
        self.p1_parts = self.p2_parts = 0
        self.p1_apple = self.p2_apple = (0, 0)

    def main_menu(self) -> None:
        """Display Main Menu and wait for mode selection."""
        waiting = True
        while waiting:
            self.screen.fill(DARK_GREEN)
            title = self.font.render("SNAKE RETRO", True, P1_HEAD)

            btn_1p = pygame.Rect(WDTH // 2 - 100, HGHT // 2 - 20, 200, 50)
            btn_2p = pygame.Rect(WDTH // 2 - 100, HGHT // 2 + 50, 200, 50)

            pygame.draw.rect(self.screen, GRAY, btn_1p, border_radius=10)
            pygame.draw.rect(self.screen, P2_HEAD, btn_2p, border_radius=10)

            txt_1p = self.small_font.render("1 PLAYER (WALLS)", True, WHITE)
            txt_2p = self.small_font.render("2 PLAYERS", True, WHITE)

            self.screen.blit(title, title.get_rect(center=(WDTH // 2, HGHT // 2 - 100)))
            self.screen.blit(txt_1p, txt_1p.get_rect(center=btn_1p.center))
            self.screen.blit(txt_2p, txt_2p.get_rect(center=btn_2p.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_1p.collidepoint(event.pos):
                        self.num_players = 1
                        waiting = False
                    elif btn_2p.collidepoint(event.pos):
                        self.num_players = 2
                        waiting = False
            self.clock.tick(30)

        self.in_menu = False
        self.reset_game()

    def generate_walls(self) -> None:
        """Generate random walls for single player mode."""
        self.walls.clear()
        num_walls = 20
        for _ in range(num_walls):
            wx = random.randint(0, (WDTH // SIZE) - 1) * SIZE
            wy = random.randint(0, (HGHT // SIZE) - 1) * SIZE
            if (wx, wy) not in self.walls and not (wx < SIZE * 5 and wy < SIZE * 5):
                self.walls.append((wx, wy))

    def reset_game(self) -> None:
        """Reset initial session parameters."""
        self.running = True
        self.game_over_state = False
        self.winner = 0
        self.walls.clear()

        # Reset P1
        self.p1_dir = "D"
        self.p1_score = 0
        self.p1_parts = 2
        self.p1_x = [0] * self.capacity
        self.p1_y = [0] * self.capacity
        self.p1_x[0], self.p1_x[1] = SIZE * 2, SIZE * 1
        self.p1_y[0], self.p1_y[1] = SIZE * 2, SIZE * 2

        if self.num_players == 1:
            self.generate_walls()
            self.new_apple(1)
        else:
            # Reset P2
            self.p2_dir = "L"
            self.p2_score = 0
            self.p2_parts = 2
            self.p2_x = [0] * self.capacity
            self.p2_y = [0] * self.capacity
            self.p2_x[0], self.p2_x[1] = WDTH - SIZE * 3, WDTH - SIZE * 2
            self.p2_y[0], self.p2_y[1] = HGHT - SIZE * 3, HGHT - SIZE * 3
            self.new_apple(1)
            self.new_apple(2)

    def new_apple(self, player: int) -> None:
        """Create an apple at a random aligned safe position."""
        while True:
            ax = random.randint(0, (WDTH // SIZE) - 1) * SIZE
            ay = random.randint(0, (HGHT // SIZE) - 1) * SIZE

            if (ax, ay) in self.walls:
                continue

            in_p1 = any(
                ax == self.p1_x[i] and ay == self.p1_y[i] for i in range(self.p1_parts)
            )
            in_p2 = False
            if self.num_players == 2:
                in_p2 = any(
                    ax == self.p2_x[i] and ay == self.p2_y[i]
                    for i in range(self.p2_parts)
                )

            if not in_p1 and not in_p2:
                if player == 1:
                    self.p1_apple = (ax, ay)
                else:
                    self.p2_apple = (ax, ay)
                break

    def draw(self) -> None:
        """Render graphical elements."""
        self.screen.fill(DARK_GREEN)

        for i in range(0, WDTH, SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (i, 0), (i, HGHT))
            pygame.draw.line(self.screen, GRID_COLOR, (0, i), (WDTH, i))

        for wall in self.walls:
            pygame.draw.rect(self.screen, WALL_COLOR, (*wall, SIZE, SIZE))

        pygame.draw.rect(self.screen, P1_APPLE, (*self.p1_apple, SIZE, SIZE))
        for i in range(self.p1_parts):
            color = P1_HEAD if i == 0 else P1_BODY
            pygame.draw.rect(
                self.screen, color, (self.p1_x[i], self.p1_y[i], SIZE, SIZE)
            )

        sc1 = self.small_font.render(f"P1: {self.p1_score}", True, P1_HEAD)
        self.screen.blit(sc1, (10, 10))

        if self.num_players == 2:
            pygame.draw.rect(self.screen, P2_APPLE, (*self.p2_apple, SIZE, SIZE))
            for i in range(self.p2_parts):
                color = P2_HEAD if i == 0 else P2_BODY
                pygame.draw.rect(
                    self.screen, color, (self.p2_x[i], self.p2_y[i], SIZE, SIZE)
                )
            sc2 = self.small_font.render(f"P2: {self.p2_score}", True, P2_HEAD)
            self.screen.blit(sc2, sc2.get_rect(topright=(WDTH - 10, 10)))

        pygame.display.flip()

    def move(self) -> None:
        """Update snake segment coordinates."""
        for i in range(self.p1_parts, 0, -1):
            self.p1_x[i] = self.p1_x[i - 1]
            self.p1_y[i] = self.p1_y[i - 1]

        mv1 = {"W": (0, -SIZE), "S": (0, SIZE), "A": (-SIZE, 0), "D": (SIZE, 0)}
        self.p1_x[0] += mv1[self.p1_dir][0]
        self.p1_y[0] += mv1[self.p1_dir][1]

        if self.num_players == 2:
            for i in range(self.p2_parts, 0, -1):
                self.p2_x[i] = self.p2_x[i - 1]
                self.p2_y[i] = self.p2_y[i - 1]

            mv2 = {"U": (0, -SIZE), "D": (0, SIZE), "L": (-SIZE, 0), "R": (SIZE, 0)}
            self.p2_x[0] += mv2[self.p2_dir][0]
            self.p2_y[0] += mv2[self.p2_dir][1]

    def update(self) -> None:
        """Check for apple collection and all collisions."""
        hx1, hy1 = self.p1_x[0], self.p1_y[0]

        if hx1 == self.p1_apple[0] and hy1 == self.p1_apple[1]:
            self.p1_parts += 1
            self.p1_score += 1
            self.new_apple(1)

        p1_dead = self._check_death(
            hx1,
            hy1,
            self.p1_x,
            self.p1_y,
            self.p1_parts,
            self.p2_x,
            self.p2_y,
            self.p2_parts if self.num_players == 2 else 0,
        )
        p2_dead = False

        if self.num_players == 2:
            hx2, hy2 = self.p2_x[0], self.p2_y[0]
            if hx2 == self.p2_apple[0] and hy2 == self.p2_apple[1]:
                self.p2_parts += 1
                self.p2_score += 1
                self.new_apple(2)
            p2_dead = self._check_death(
                hx2,
                hy2,
                self.p2_x,
                self.p2_y,
                self.p2_parts,
                self.p1_x,
                self.p1_y,
                self.p1_parts,
            )

        if p1_dead or p2_dead:
            self.running = False
            self.game_over_state = True
            if self.num_players == 1:
                self.winner = 0
            else:
                if p1_dead and not p2_dead:
                    self.winner = 2
                elif p2_dead and not p1_dead:
                    self.winner = 1
                else:
                    self.winner = 0

    def _check_death(
        self,
        hx: int,
        hy: int,
        self_x: List[int],
        self_y: List[int],
        self_parts: int,
        other_x: List[int],
        other_y: List[int],
        other_parts: int,
    ) -> bool:
        """Helper to evaluate if a snake has collided with walls, bodies, or blocks."""
        if not (0 <= hx < WDTH and 0 <= hy < HGHT):
            return True
        if (hx, hy) in self.walls:
            return True
        for i in range(1, self_parts):
            if hx == self_x[i] and hy == self_y[i]:
                return True
        for i in range(other_parts):
            if hx == other_x[i] and hy == other_y[i]:
                return True
        return False

    def game_over_screen(self) -> None:
        """Display Game Over screen with Winner and Retry/Menu options."""
        self.screen.fill(DARK_GREEN)

        if self.num_players == 1:
            title = self.font.render("GAME OVER", True, P1_HEAD)
            sc_txt = self.font.render(f"SCORE: {self.p1_score}", True, WHITE)
        else:
            if self.winner == 1:
                title = self.font.render("PLAYER 1 WINS!", True, P1_HEAD)
            elif self.winner == 2:
                title = self.font.render("PLAYER 2 WINS!", True, P2_HEAD)
            else:
                title = self.font.render("DRAW!", True, WHITE)
            sc_txt = self.font.render(
                f"P1: {self.p1_score}  -  P2: {self.p2_score}", True, WHITE
            )

        retry_rect = pygame.Rect(WDTH // 2 - 80, HGHT // 2 + 40, 160, 40)
        menu_rect = pygame.Rect(WDTH // 2 - 80, HGHT // 2 + 100, 160, 40)

        pygame.draw.rect(self.screen, GRAY, retry_rect, border_radius=10)
        pygame.draw.rect(self.screen, P2_HEAD, menu_rect, border_radius=10)

        r_txt = self.small_font.render("MODES", True, WHITE)
        m_txt = self.small_font.render("MENU", True, WHITE)

        self.screen.blit(title, title.get_rect(center=(WDTH // 2, HGHT // 2 - 60)))
        self.screen.blit(sc_txt, sc_txt.get_rect(center=(WDTH // 2, HGHT // 2 - 10)))
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
                        self.game_over_state = False
                        self.in_menu = True
                        waiting = False
                    elif menu_rect.collidepoint(event.pos):
                        subprocess.Popen([sys.executable, "src/arcade_menu.py"])
                        pygame.quit()
                        sys.exit()
            self.clock.tick(30)

    def handle_input(self) -> None:
        """Handle keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._update_p1_dir(event.key)
                if self.num_players == 2:
                    self._update_p2_dir(event.key)

    def _update_p1_dir(self, key: int) -> None:
        """Update direction for Player 1 (WASD)."""
        if key == pygame.K_a and self.p1_dir != "D":
            self.p1_dir = "A"
        elif key == pygame.K_d and self.p1_dir != "A":
            self.p1_dir = "D"
        elif key == pygame.K_w and self.p1_dir != "S":
            self.p1_dir = "W"
        elif key == pygame.K_s and self.p1_dir != "W":
            self.p1_dir = "S"

    def _update_p2_dir(self, key: int) -> None:
        """Update direction for Player 2 (Arrows)."""
        if key == pygame.K_LEFT and self.p2_dir != "R":
            self.p2_dir = "L"
        elif key == pygame.K_RIGHT and self.p2_dir != "L":
            self.p2_dir = "R"
        elif key == pygame.K_UP and self.p2_dir != "D":
            self.p2_dir = "U"
        elif key == pygame.K_DOWN and self.p2_dir != "U":
            self.p2_dir = "D"

    def run(self, once: bool = False) -> None:
        """Main game loop."""
        while True:
            if self.in_menu:
                self.main_menu()
            elif self.running:
                self.handle_input()
                self.move()
                self.update()
                self.draw()
                self.clock.tick(1000 // SPEED)
            elif self.game_over_state:
                self.game_over_screen()
                if not self.game_over_state and not self.running and not self.in_menu:
                    return
            if once:
                break


if __name__ == "__main__":
    SnakeGame().run()

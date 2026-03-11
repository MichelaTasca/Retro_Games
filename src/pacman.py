# pylint: disable=no-member
"""
Pac-Man Retro Game Module.
Features random map generation and automated code quality compliance.
"""

import math
import random
import subprocess
import sys

import pygame

# Game Constants
T_SIZE = 25
GRID_WIDTH = 21
GRID_HEIGHT = 21
W_WDTH = GRID_WIDTH * T_SIZE
W_HGHT = GRID_HEIGHT * T_SIZE

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
EYE_WHITE = (240, 240, 240)
EYE_BLUE = (0, 102, 255)
GRAY = (50, 50, 50)


class PacManGame:
    """Main class handling Pac-Man game logic and rendering."""

    def __init__(self):
        """Initialize Pygame and game components."""
        pygame.init()
        pygame.display.set_caption("PAC-MAN (Random Pacman Maps)")
        self.screen = pygame.display.set_mode((W_WDTH, W_HGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Press Start 2P", 20, bold=True)
        self.small_font = pygame.font.SysFont("Press Start 2P", 14, bold=True)
        self.reset_game()

    def generate_pacman_map(self):
        """Generate a procedural maze map in Pac-Man style."""
        maze = [["1" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Regular horizontal corridors
        for y in range(2, GRID_HEIGHT - 2, 4):
            for x in range(1, GRID_WIDTH - 1):
                maze[y][x] = "0"

        # Regular vertical corridors
        for x in range(3, GRID_WIDTH - 3, 4):
            for y in range(1, GRID_HEIGHT - 1):
                maze[y][x] = "0"

        # Random openings to create map variety
        for _ in range(80):
            rx = random.randint(1, GRID_WIDTH - 2)
            ry = random.randint(1, GRID_HEIGHT - 2)
            maze[ry][rx] = "0"

        return ["".join(row) for row in maze]

    def reset_game(self):
        """Reset game state to initial values."""
        self.LEVEL = self.generate_pacman_map()
        self.p_x, self.p_y = 1, 1
        self.direction = "RIGHT"
        self.mouth_open = False
        self.mouth_timer = 0

        self.g_x, self.g_y = GRID_WIDTH - 2, GRID_HEIGHT - 2
        self.g_fx, self.ghost_fy = float(self.g_x), float(self.g_y)
        self.ghost_dir = (0, 0)

        self.score = 0
        self.dots = {
            (x, y)
            for y, row in enumerate(self.LEVEL)
            for x, tile in enumerate(row)
            if tile == "0"
        }
        self.running = True
        self.game_over_state = False

    def draw(self):
        """Render all game elements (walls, dots, characters)."""
        self.screen.fill(BLACK)

        # Walls
        for y, row in enumerate(self.LEVEL):
            for x, tile in enumerate(row):
                if tile == "1":
                    pygame.draw.rect(
                        self.screen,
                        BLUE,
                        (x * T_SIZE, y * T_SIZE, T_SIZE, T_SIZE),
                    )

        # Dots
        for x, y in self.dots:
            pygame.draw.circle(
                self.screen,
                WHITE,
                (x * T_SIZE + T_SIZE // 2, y * T_SIZE + T_SIZE // 2),
                4,
            )

        self._draw_pacman()
        self._draw_ghost()

        # Score display
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))
        pygame.display.flip()

    def _draw_pacman(self):
        """Draw Pac-Man character with animated mouth."""
        r = T_SIZE // 2 - 2
        d_a = {"RIGHT": 0, "DOWN": 90, "LEFT": 180, "UP": 270}[self.direction]
        mouth_angle = 45 if self.mouth_open else 8

        pac_surf = pygame.Surface((T_SIZE, T_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(pac_surf, YELLOW, (T_SIZE // 2, T_SIZE // 2), r)

        mouth_start = math.radians(d_a - mouth_angle)
        mouth_end = math.radians(d_a + mouth_angle)
        points = [(T_SIZE // 2, T_SIZE // 2)]
        for a in (mouth_start, mouth_end):
            points.append(
                (
                    T_SIZE // 2 + math.cos(a) * r,
                    T_SIZE // 2 + math.sin(a) * r,
                )
            )

        pygame.draw.polygon(pac_surf, (0, 0, 0, 255), points)
        self.screen.blit(pac_surf, (self.p_x * T_SIZE, self.p_y * T_SIZE))

    def _draw_ghost(self):
        """Draw Ghost character with eyes and waves."""
        gx = self.g_fx * T_SIZE + T_SIZE // 2
        gy = self.ghost_fy * T_SIZE + T_SIZE // 2
        g_r = T_SIZE // 2 - 2

        pygame.draw.circle(self.screen, RED, (gx, gy), g_r)
        # Eyes
        pygame.draw.circle(self.screen, EYE_WHITE, (gx - 5, gy - 4), 4)
        pygame.draw.circle(self.screen, EYE_WHITE, (gx + 5, gy - 4), 4)
        pygame.draw.circle(self.screen, EYE_BLUE, (gx - 5, gy - 4), 2)
        pygame.draw.circle(self.screen, EYE_BLUE, (gx + 5, gy - 4), 2)
        # Bottom waves
        for i in range(-1, 2):
            pygame.draw.circle(self.screen, RED, (gx + i * 6, gy + g_r - 2), 4)

    def move_pacman(self):
        """Handle Pac-Man movement and wall collision."""
        dx, dy = 0, 0
        if self.direction == "UP":
            dy = -1
        elif self.direction == "DOWN":
            dy = 1
        elif self.direction == "LEFT":
            dx = -1
        elif self.direction == "RIGHT":
            dx = 1

        new_x = self.p_x + dx
        new_y = self.p_y + dy

        if self.LEVEL[new_y][new_x] != "1":
            self.p_x, self.p_y = new_x, new_y

    def move_ghost(self):
        """Update Ghost position with simple hunting and patrol AI."""
        speed = 0.18
        gx, gy = round(self.g_fx), round(self.ghost_fy)

        if abs(self.g_fx - gx) < 0.05 and abs(self.ghost_fy - gy) < 0.05:
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_dirs = []

            for dx, dy in dirs:
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if self.LEVEL[ny][nx] != "1":
                        dist = math.hypot(self.p_x - nx, self.p_y - ny)
                        valid_dirs.append((dist, (dx, dy)))

            if valid_dirs:
                r = random.random()
                if r < 0.30:  # Chase
                    valid_dirs.sort(key=lambda t: t[0])
                elif r < 0.70:  # Random
                    random.shuffle(valid_dirs)
                else:  # Maintain direction
                    if self.ghost_dir in [d[1] for d in valid_dirs]:
                        self.g_fx += self.ghost_dir[0] * speed
                        self.ghost_fy += self.ghost_dir[1] * speed
                        return

                self.ghost_dir = valid_dirs[0][1]

        self.g_fx += self.ghost_dir[0] * speed
        self.ghost_fy += self.ghost_dir[1] * speed
        self.g_x, self.g_y = int(round(self.g_fx)), int(round(self.ghost_fy))

    def update(self):
        """Check for dot consumption and game end conditions."""
        if (self.p_x, self.p_y) in self.dots:
            self.dots.remove((self.p_x, self.p_y))
            self.score += 10
            self.mouth_open = True

        if not self.dots or (self.p_x == self.g_x and self.p_y == self.g_y):
            self.running = False
            self.game_over_state = True

    def game_over_screen(self):
        """Display Game Over screen and wait for user choice."""
        self.screen.fill(BLACK)
        win = not self.dots
        text = "YOU WIN!" if win else "GAME OVER"
        color = WHITE if win else RED

        m = self.font.render(text, True, color)
        score_m = self.font.render(f"SCORE: {self.score}", True, WHITE)

        retry_rect = pygame.Rect(W_WDTH // 2 - 80, W_HGHT // 2 + 60, 160, 40)
        menu_rect = pygame.Rect(W_WDTH // 2 - 80, W_HGHT // 2 + 110, 160, 40)

        pygame.draw.rect(self.screen, GRAY, retry_rect, border_r=10)
        pygame.draw.rect(self.screen, BLUE, menu_rect, border_r=10)

        r_text = self.small_font.render("RETRY", True, WHITE)
        m_text = self.small_font.render("MENU", True, WHITE)

        self.screen.blit(m, m.get_rect(center=(W_WDTH // 2, W_HGHT // 2 - 40)))
        self.screen.blit(
            score_m,
            score_m.get_rect(center=(W_WDTH // 2, W_HGHT // 2)),
        )
        self.screen.blit(r_text, r_text.get_rect(center=retry_rect.center))
        self.screen.blit(m_text, m_text.get_rect(center=menu_rect.center))
        pygame.display.flip()

        self._wait_for_input(retry_rect, menu_rect)

    def _wait_for_input(self, retry_rect, menu_rect):
        """Internal loop to handle Game Over menu interaction."""
        waiting = True
        while waiting:
            for evt in pygame.evt.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_RETURN:
                    self.reset_game()
                    waiting = False
                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(evt.pos):
                        self.reset_game()
                        waiting = False
                    elif menu_rect.collidepoint(evt.pos):
                        pygame.quit()
                        subprocess.Popen([sys.executable, "ArcadeMenu.py"])
                        sys.exit()
            self.clock.tick(30)

    def run(self):
        """Execute the main game loop."""
        while True:
            for evt in pygame.evt.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN:
                    key_map = {
                        pygame.K_w: "UP",
                        pygame.K_s: "DOWN",
                        pygame.K_a: "LEFT",
                        pygame.K_d: "RIGHT",
                    }
                    if evt.key in key_map:
                        self.direction = key_map[evt.key]

            if self.running:
                self.move_pacman()
                self.move_ghost()
                self.update()
                self.mouth_timer += 1
                if self.mouth_timer % 4 == 0:
                    self.mouth_open = not self.mouth_open
                self.draw()
                self.clock.tick(30)
            elif self.game_over_state:
                self.game_over_screen()
                self.game_over_state = False


if __name__ == "__main__":
    PacManGame().run()

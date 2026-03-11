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
T_S = 25
GRID_WIDTH = 21
GRID_HEIGHT = 21
W_W = GRID_WIDTH * T_S
W_H = GRID_HEIGHT * T_S

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
EYE_W = (240, 240, 240)
EYE_BLUE = (0, 102, 255)
GRAY = (50, 50, 50)


class PacManGame:
    """Main class handling Pac-Man game logic and rendering."""

    def __init__(self):
        """Initialize Pygame and all game attributes."""
        pygame.init()
        pygame.display.set_caption("PAC-MAN (Random Pacman Maps)")
        self.screen = pygame.display.set_mode((W_W, W_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Press Start 2P", 20, bold=True)
        self.small_font = pygame.font.SysFont("Press Start 2P", 14, bold=True)

        # Initialize all attributes to satisfy W0201
        self.level = []
        self.p_pos = [1, 1]  # x, y
        self.direction = "RIGHT"
        self.mouth_open = False
        self.mouth_timer = 0
        self.g_pos = [GRID_WIDTH - 2, GRID_HEIGHT - 2]
        self.gf = [float(self.g_pos[0]), float(self.g_pos[1])]
        self.ghost_dir = (0, 0)
        self.score = 0
        self.dots = set()
        self.running = True
        self.game_over_state = False

        self.reset_game()

    def generate_pacman_map(self):
        """Generate a procedural maze map in Pac-Man style."""
        maze = [["1" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(2, GRID_HEIGHT - 2, 4):
            for x in range(1, GRID_WIDTH - 1):
                maze[y][x] = "0"
        for x in range(3, GRID_WIDTH - 3, 4):
            for y in range(1, GRID_HEIGHT - 1):
                maze[y][x] = "0"
        for _ in range(80):
            rx, ry = random.randint(1, GRID_WIDTH - 2), random.randint(
                1, GRID_HEIGHT - 2
            )
            maze[ry][rx] = "0"
        return ["".join(row) for row in maze]

    def reset_game(self):
        """Reset game state to initial values."""
        self.level = self.generate_pacman_map()
        self.p_pos = [1, 1]
        self.direction = "RIGHT"
        self.mouth_open = False
        self.mouth_timer = 0
        self.g_pos = [GRID_WIDTH - 2, GRID_HEIGHT - 2]
        self.gf = [float(self.g_pos[0]), float(self.g_pos[1])]
        self.ghost_dir = (0, 0)
        self.score = 0
        self.dots = {
            (x, y)
            for y, row in enumerate(self.level)
            for x, tile in enumerate(row)
            if tile == "0"
        }
        self.running = True
        self.game_over_state = False

    def draw(self):
        """Render all game elements."""
        self.screen.fill(BLACK)
        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == "1":
                    pygame.draw.rect(self.screen, BLUE, (x * T_S, y * T_S, T_S, T_S))

        for x, y in self.dots:
            pygame.draw.circle(
                self.screen,
                WHITE,
                (x * T_S + T_S // 2, y * T_S + T_S // 2),
                4,
            )

        self._draw_pacman()
        self._draw_ghost()
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))
        pygame.display.flip()

    def _draw_pacman(self):
        """Draw Pac-Man character."""
        radius = T_S // 2 - 2
        angles = {"RIGHT": 0, "DOWN": 90, "LEFT": 180, "UP": 270}
        d_a = angles[self.direction]
        mouth_angle = 45 if self.mouth_open else 8

        pac_surf = pygame.Surface((T_S, T_S), pygame.SRCALPHA)
        pygame.draw.circle(pac_surf, YELLOW, (T_S // 2, T_S // 2), radius)

        m_start, m_end = math.radians(d_a - mouth_angle), math.radians(
            d_a + mouth_angle
        )
        points = [
            (T_S // 2, T_S // 2),
            (
                T_S // 2 + math.cos(m_start) * radius,
                T_S // 2 + math.sin(m_start) * radius,
            ),
            (
                T_S // 2 + math.cos(m_end) * radius,
                T_S // 2 + math.sin(m_end) * radius,
            ),
        ]

        pygame.draw.polygon(pac_surf, BLACK, points)
        self.screen.blit(pac_surf, (self.p_pos[0] * T_S, self.p_pos[1] * T_S))

    def _draw_ghost(self):
        """Draw Ghost character."""
        gx = self.gf[0] * T_S + T_S // 2
        gy = self.gf[1] * T_S + T_S // 2
        g_r = T_S // 2 - 2
        pygame.draw.circle(self.screen, RED, (gx, gy), g_r)
        for offset in [-5, 5]:
            pygame.draw.circle(self.screen, EYE_W, (gx + offset, gy - 4), 4)
            pygame.draw.circle(self.screen, EYE_BLUE, (gx + offset, gy - 4), 2)
        for i in range(-1, 2):
            pygame.draw.circle(self.screen, RED, (gx + i * 6, gy + g_r - 2), 4)

    def move_pacman(self):
        """Handle Pac-Man movement."""
        mv = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
        dx, dy = mv[self.direction]
        nx, ny = self.p_pos[0] + dx, self.p_pos[1] + dy
        if self.level[ny][nx] != "1":
            self.p_pos = [nx, ny]

    def move_ghost(self):
        """Update Ghost position AI."""
        speed = 0.18
        gx_r, gy_r = round(self.gf[0]), round(self.gf[1])

        if abs(self.gf[0] - gx_r) < 0.05 and abs(self.gf[1] - gy_r) < 0.05:
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid = []
            for dx, dy in dirs:
                nx, ny = gx_r + dx, gy_r + dy
                if (
                    0 <= nx < GRID_WIDTH
                    and 0 <= ny < GRID_HEIGHT
                    and self.level[ny][nx] != "1"
                ):
                    dist = math.hypot(self.p_pos[0] - nx, self.p_pos[1] - ny)
                    valid.append((dist, (dx, dy)))
            if valid:
                rand_val = random.random()
                if rand_val < 0.30:
                    valid.sort(key=lambda t: t[0])
                elif rand_val < 0.70:
                    random.shuffle(valid)
                self.ghost_dir = valid[0][1]

        self.gf[0] += self.ghost_dir[0] * speed
        self.gf[1] += self.ghost_dir[1] * speed
        self.g_pos = [int(round(self.gf[0])), int(round(self.gf[1]))]

    def update(self):
        """Check game logic states."""
        p_tuple = tuple(self.p_pos)
        if p_tuple in self.dots:
            self.dots.remove(p_tuple)
            self.score += 10
            self.mouth_open = True
        if not self.dots or (
            self.p_pos[0] == self.g_pos[0] and self.p_pos[1] == self.g_pos[1]
        ):
            self.running = False
            self.game_over_state = True

    def game_over_screen(self):
        """Display Game Over screen."""
        self.screen.fill(BLACK)
        win = not self.dots
        txt, col = ("YOU WIN!", WHITE) if win else ("GAME OVER", RED)
        m_rend = self.font.render(txt, True, col)
        s_rend = self.font.render(f"SCORE: {self.score}", True, WHITE)

        retry_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 60, 160, 40)
        menu_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 110, 160, 40)

        pygame.draw.rect(self.screen, GRAY, retry_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLUE, menu_rect, border_radius=10)

        self.screen.blit(m_rend, m_rend.get_rect(center=(W_W // 2, W_H // 2 - 40)))
        self.screen.blit(s_rend, s_rend.get_rect(center=(W_W // 2, W_H // 2)))

        r_t = self.small_font.render("RETRY", True, WHITE)
        m_t = self.small_font.render("MENU", True, WHITE)
        self.screen.blit(r_t, r_t.get_rect(center=retry_rect.center))
        self.screen.blit(m_t, m_t.get_rect(center=menu_rect.center))

        pygame.display.flip()
        self._wait_for_input(retry_rect, menu_rect)

    def _wait_for_input(self, retry_rect, menu_rect):
        """Handle menu interactions."""
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_RETURN:
                    self.reset_game()
                    return
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(evt.pos):
                        self.reset_game()
                        return
                    if menu_rect.collidepoint(evt.pos):
                        pygame.quit()
                        # Fixed R1732: subprocess management
                        with subprocess.Popen([sys.executable, "ArcadeMenu.py"]) as _:
                            sys.exit()
            self.clock.tick(30)

    def run(self):
        """Main game loop."""
        key_map = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT",
        }
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN and evt.key in key_map:
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

# pylint: disable=no-member, duplicate-code, too-many-instance-attributes
"""
Pac-Man Retro Game Module.
Procedural maze generation, Ghost AI, and Game Over menu with return logic.
"""

import random
import sys

import pygame

# Game Constants
T_S = 25
GRID_WIDTH = 21
GRID_HEIGHT = 21
W_W = GRID_WIDTH * T_S
W_H = GRID_HEIGHT * T_S

# Colors
BLA, BLUE, YLW, WH = (0, 0, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)
RED, EYE_W, E_B, GR = (255, 0, 0), (240, 240, 240), (0, 102, 255), (50, 50, 50)


class PacManGame:
    """Main class handling Pac-Man game logic and rendering."""

    def __init__(self):
        """Initialize Pygame and game state."""
        pygame.init()
        pygame.display.set_caption("PAC-MAN RETRO")
        self.screen = pygame.display.set_mode((W_W, W_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14, bold=True)

        self.level, self.dots = [], set()
        self.p_pos = [1, 1]
        self.direction = "RIGHT"
        self.mouth_open, self.mouth_timer = False, 0
        self.g_pos = [19, 19]
        self.gf = [19.0, 19.0]
        self.ghost_dir = (0, 0)
        self.score, self.running, self.game_over_state = 0, True, False
        self.reset_game()

    def generate_pacman_map(self):
        """Procedural maze generation."""
        maze = [["1" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(2, GRID_HEIGHT - 2, 4):
            for x in range(1, GRID_WIDTH - 1):
                maze[y][x] = "0"
        for x in range(3, GRID_WIDTH - 3, 4):
            for y in range(1, GRID_HEIGHT - 1):
                maze[y][x] = "0"
        for _ in range(80):
            maze[random.randint(1, 19)][random.randint(1, 19)] = "0"
        return ["".join(row) for row in maze]

    def reset_game(self):
        """Reset game state."""
        self.level = self.generate_pacman_map()
        self.dots = {
            (x, y)
            for y, r in enumerate(self.level)
            for x, t in enumerate(r)
            if t == "0"
        }
        self.p_pos, self.g_pos = [1, 1], [19, 19]
        self.gf = [float(self.g_pos[0]), float(self.g_pos[1])]
        self.running, self.score, self.game_over_state = True, 0, False

    def move_pacman(self):
        """Handle movement logic."""
        mv = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
        dx, dy = mv[self.direction]
        nx, ny = self.p_pos[0] + dx, self.p_pos[1] + dy
        if self.level[ny][nx] != "1":
            self.p_pos = [nx, ny]

    def move_ghost(self):
        """Ghost AI movement."""
        speed = 0.15
        gx, gy = round(self.gf[0]), round(self.gf[1])
        if abs(self.gf[0] - gx) < 0.1 and abs(self.gf[1] - gy) < 0.1:
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            val = [d for d in dirs if self.level[gy + d[1]][gx + d[0]] != "1"]
            if val:
                self.ghost_dir = random.choice(val)
        self.gf[0] += self.ghost_dir[0] * speed
        self.gf[1] += self.ghost_dir[1] * speed
        self.g_pos = [int(round(self.gf[0])), int(round(self.gf[1]))]

    def update(self):
        """Check collisions and state."""
        if tuple(self.p_pos) in self.dots:
            self.dots.remove(tuple(self.p_pos))
            self.score += 10
        if not self.dots or self.p_pos == self.g_pos:
            self.running = False
            self.game_over_state = True

    def draw(self):
        """Render game elements."""
        self.screen.fill(BLA)
        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == "1":
                    pygame.draw.rect(self.screen, BLUE, (x * T_S, y * T_S, T_S, T_S))
        for dx, dy in self.dots:
            pygame.draw.circle(self.screen, WH, (dx * T_S + 12, dy * T_S + 12), 4)

        pygame.draw.circle(
            self.screen, YLW, (self.p_pos[0] * T_S + 12, self.p_pos[1] * T_S + 12), 10
        )
        pygame.draw.circle(
            self.screen,
            RED,
            (int(self.gf[0] * T_S + 12), int(self.gf[1] * T_S + 12)),
            10,
        )

        score_txt = self.font.render(f"SCORE: {self.score}", True, WH)
        self.screen.blit(score_txt, (10, 5))
        pygame.display.flip()

    def game_over_screen(self):
        """Display Game Over menu."""
        self.screen.fill(BLA)
        msg_text = "YOU WIN!" if not self.dots else "GAME OVER"
        msg = self.font.render(msg_text, True, RED if self.dots else WH)

        retry_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 40, 160, 40)
        menu_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 100, 160, 40)

        pygame.draw.rect(self.screen, GR, retry_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLUE, menu_rect, border_radius=10)

        self.screen.blit(msg, msg.get_rect(center=(W_W // 2, W_H // 2 - 20)))
        self.screen.blit(
            self.small_font.render("RETRY", True, WH),
            self.small_font.render("RETRY", True, WH).get_rect(
                center=retry_rect.center
            ),
        )
        self.screen.blit(
            self.small_font.render("MENU", True, WH),
            self.small_font.render("MENU", True, WH).get_rect(center=menu_rect.center),
        )

        pygame.display.flip()
        return self._wait_(retry_rect, menu_rect)

    def _wait_(self, retry_rect, menu_rect):
        """Wait for player. Returns True to continue, False to return menu."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(event.pos):
                        self.reset_game()
                        return True
                    if menu_rect.collidepoint(event.pos):
                        return False
            self.clock.tick(30)

    def run(self):
        """Main Loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    k_m = {
                        pygame.K_w: "UP",
                        pygame.K_s: "DOWN",
                        pygame.K_a: "LEFT",
                        pygame.K_d: "RIGHT",
                    }
                    if event.key in k_m:
                        self.direction = k_m[event.key]

            if self.running:
                self.move_pacman()
                self.move_ghost()
                self.update()
                self.draw()
                self.clock.tick(15)
            elif self.game_over_state:
                if not self.game_over_screen():
                    return
                self.game_over_state = False


if __name__ == "__main__":
    PacManGame().run()

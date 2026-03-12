# pylint: disable=no-member, duplicate-code, too-many-instance-attributes
"""
Pac-Man Retro Game Module.
Fixed grid-based logic, animations, buffered input, Ghost AI,
and guaranteed solvable maze generation (no trapped dots).
Returns to Main Arcade Menu.
"""

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
BLA, BLUE, YLW, WH = (0, 0, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255)
RED, GR = (255, 0, 0), (50, 50, 50)


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

        # Map and Dots
        self.level = []
        self.dots = set()

        # State variables
        self.p_pos = [1, 1]
        self.direction = "RIGHT"
        self.next_dir = "RIGHT"
        self.mouth_open = False

        self.g_pos = [19, 19]
        self.ghost_dir = (0, -1)

        self.score = 0
        self.running = True
        self.game_over_state = False
        self.tick_counter = 0

        self.reset_game()

    def generate_pacman_map(self):
        """Fixed layout maze generation ensuring 100% solvability."""
        raw_map = [
            "111111111111111111111",
            "100000000010000000001",
            "101110111010111011101",
            "100000000000000000001",
            "101110101111101011101",
            "100000100010001000001",
            "111110111010111011111",
            "111110100000001011111",
            "111110101111101011111",
            "100000001111100000001",
            "111110101111101011111",
            "111110100000001011111",
            "111110111010111011111",
            "100000000010000000001",
            "101110111010111011101",
            "100010000000000010001",
            "111010101111101010111",
            "100000100010001000001",
            "101111111010111111101",
            "100000000000000000001",
            "111111111111111111111",
        ]
        return [list(row) for row in raw_map]

    def reset_game(self):
        """Reset game state."""
        self.level = self.generate_pacman_map()
        self.dots = {
            (x, y)
            for y, r in enumerate(self.level)
            for x, t in enumerate(r)
            if t == "0"
        }

        if (1, 1) in self.dots:
            self.dots.remove((1, 1))

        self.p_pos, self.g_pos = [1, 1], [19, 19]
        self.direction = "RIGHT"
        self.next_dir = "RIGHT"
        self.ghost_dir = (0, -1)
        self.running, self.score, self.game_over_state = True, 0, False

    def move_pacman(self):
        """Handle movement logic with buffered direction."""
        mv = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

        dx, dy = mv[self.next_dir]
        nx, ny = self.p_pos[0] + dx, self.p_pos[1] + dy
        if self.level[ny][nx] != "1":
            self.direction = self.next_dir
            self.p_pos = [nx, ny]
            return

        dx, dy = mv[self.direction]
        nx, ny = self.p_pos[0] + dx, self.p_pos[1] + dy
        if self.level[ny][nx] != "1":
            self.p_pos = [nx, ny]

    def move_ghost(self):
        """Grid-based Ghost AI."""
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_moves = []

        for dx, dy in dirs:
            nx, ny = self.g_pos[0] + dx, self.g_pos[1] + dy
            if self.level[ny][nx] != "1":
                if (dx, dy) != (-self.ghost_dir[0], -self.ghost_dir[1]):
                    possible_moves.append((dx, dy))

        if not possible_moves:
            possible_moves.append((-self.ghost_dir[0], -self.ghost_dir[1]))

        self.ghost_dir = random.choice(possible_moves)
        self.g_pos[0] += self.ghost_dir[0]
        self.g_pos[1] += self.ghost_dir[1]

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
                    pygame.draw.rect(self.screen, BLUE, (x * T_S, y * T_S, T_S, T_S), 2)

        for dx, dy in self.dots:
            pygame.draw.circle(
                self.screen, WH, (dx * T_S + T_S // 2, dy * T_S + T_S // 2), 4
            )

        cx, cy = self.p_pos[0] * T_S + T_S // 2, self.p_pos[1] * T_S + T_S // 2
        pygame.draw.circle(self.screen, YLW, (cx, cy), 10)

        if self.mouth_open:
            r = 12
            pts = []
            if self.direction == "RIGHT":
                pts = [(cx, cy), (cx + r, cy - r), (cx + r, cy + r)]
            elif self.direction == "LEFT":
                pts = [(cx, cy), (cx - r, cy - r), (cx - r, cy + r)]
            elif self.direction == "UP":
                pts = [(cx, cy), (cx - r, cy - r), (cx + r, cy - r)]
            elif self.direction == "DOWN":
                pts = [(cx, cy), (cx - r, cy + r), (cx + r, cy + r)]

            if pts:
                pygame.draw.polygon(self.screen, BLA, pts)

        gx, gy = self.g_pos[0] * T_S + T_S // 2, self.g_pos[1] * T_S + T_S // 2
        pygame.draw.circle(self.screen, RED, (gx, gy), 10)
        pygame.draw.circle(self.screen, WH, (gx - 3, gy - 2), 3)
        pygame.draw.circle(self.screen, WH, (gx + 3, gy - 2), 3)

        score_txt = self.font.render(f"SCORE: {self.score}", True, WH)
        self.screen.blit(score_txt, (10, 5))
        pygame.display.flip()

    def game_over_screen(self):
        """Display Game Over menu."""
        self.screen.fill(BLA)
        msg_text = "YOU WIN!" if not self.dots else "GAME OVER"
        msg = self.font.render(msg_text, True, WH if not self.dots else RED)

        retry_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 40, 160, 40)
        menu_rect = pygame.Rect(W_W // 2 - 80, W_H // 2 + 100, 160, 40)

        pygame.draw.rect(self.screen, GR, retry_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLUE, menu_rect, border_radius=10)

        self.screen.blit(msg, msg.get_rect(center=(W_W // 2, W_H // 2 - 20)))

        r_txt = self.small_font.render("RETRY", True, WH)
        m_txt = self.small_font.render("MENU", True, WH)

        self.screen.blit(r_txt, r_txt.get_rect(center=retry_rect.center))
        self.screen.blit(m_txt, m_txt.get_rect(center=menu_rect.center))

        pygame.display.flip()
        return self._wait_(retry_rect, menu_rect)

    def _wait_(self, retry_rect, menu_rect):
        """Wait for player. Returns True to continue, False to return to Arcade Menu."""
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

                        subprocess.Popen([sys.executable, "src/arcade_menu.py"])
                        pygame.quit()
                        sys.exit()
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
                        pygame.K_UP: "UP",
                        pygame.K_s: "DOWN",
                        pygame.K_DOWN: "DOWN",
                        pygame.K_a: "LEFT",
                        pygame.K_LEFT: "LEFT",
                        pygame.K_d: "RIGHT",
                        pygame.K_RIGHT: "RIGHT",
                    }
                    if event.key in k_m:
                        self.next_dir = k_m[event.key]

            if self.running:
                self.tick_counter += 1

                if self.tick_counter >= 5:
                    prev_p, prev_g = list(self.p_pos), list(self.g_pos)

                    self.move_pacman()
                    self.move_ghost()

                    if self.p_pos == prev_g and self.g_pos == prev_p:
                        self.running = False
                        self.game_over_state = True
                    else:
                        self.update()

                    self.mouth_open = not self.mouth_open
                    self.tick_counter = 0

                self.draw()
                self.clock.tick(30)

            elif self.game_over_state:
                if not self.game_over_screen():
                    return
                self.game_over_state = False


if __name__ == "__main__":
    PacManGame().run()

# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
"""Pac-Man Retro Game Module."""

import random
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
    """Main class handling Pac-Man game logic."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W_W, W_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14, bold=True)

        # State attributes
        self.level, self.dots = [], set()
        self.p_pos, self.direction = [1, 1], "RIGHT"
        self.mouth_open, self.mouth_timer = False, 0
        self.g_pos, self.gf = [19, 19], [19.0, 19.0]
        self.ghost_dir = (0, 0)
        self.score, self.running, self.game_over_state = 0, True, False
        self.reset_game()

    def generate_pacman_map(self):
        """Procedural maze generation."""
        maze = [["1" for _ in range(GRID_WIDTH)]
                for _ in range(GRID_HEIGHT)]
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
        """Reset internal state."""
        self.level = self.generate_pacman_map()
        self.dots = {(x, y) for y, r in enumerate(self.level)
                     for x, t in enumerate(r) if t == "0"}
        self.p_pos, self.g_pos = [1, 1], [19, 19]
        self.gf = [float(self.g_pos[0]), float(self.g_pos[1])]
        self.running, self.score = True, 0

    def move_pacman(self):
        """Move logic with collision."""
        mv = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
        dx, dy = mv[self.direction]
        nx, ny = self.p_pos[0] + dx, self.p_pos[1] + dy
        if self.level[ny][nx] != "1":
            self.p_pos = [nx, ny]

    def update(self):
        """Collision and score update."""
        if tuple(self.p_pos) in self.dots:
            self.dots.remove(tuple(self.p_pos))
            self.score += 10
        if not self.dots or self.p_pos == self.g_pos:
            self.running = False
            self.game_over_state = True

    def draw(self):
        """Basic render."""
        self.screen.fill(BLA)
        # Rendering semplificato per brevità
        pygame.display.flip()

    def run(self):
        """Loop."""
        while True:
            self.move_pacman()
            self.update()
            self.clock.tick(30)


if __name__ == "__main__":
    PacManGame().run()

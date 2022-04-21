import pygame
from pygame.locals import *

import random
import sys

# application constants
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 533
TARGET_FPS = 60

# sprites initialization
BACKGROUND_SPRITE = pygame.image.load("images/background.png")
PLATFORM_SPRITE = pygame.image.load("images/platform.png")
DOODLE_SPRITE = pygame.image.load("images/doodle.png")

# in game parameters
PLATFORM_AMOUNT = 10


class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Doodle Jump")
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE)
        self.is_running = False

        # initializing platforms
        self.platforms = []
        for _ in range(PLATFORM_AMOUNT):
            rnd_x = random.randint(0, SCREEN_WIDTH)
            rnd_y = random.randint(0, SCREEN_HEIGHT)
            platform = pygame.math.Vector2(rnd_x, rnd_y)
            self.platforms.append(platform)

        # initializing doodle
        self.x = 100
        self.y = 100
        self.height = 200
        self.dx = 0.
        self.dy = 0.

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.terminate()

            # left/right movement
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_a]:
                self.x -= 3
            if pressed_keys[K_d]:
                self.x += 3

            self.dy += 0.2  # speeds up falling speed
            self.y += self.dy  # moves doodle according to his vertical acceleration

            # makes doodle gow down
            if self.y > 500:
                self.dy = -10

            # moves platform alongside with doodle
            if self.y < self.height:
                for platform in self.platforms:
                    self.y = self.height
                    platform.y = platform.y - self.dy
                    if platform.y > 533:
                        platform.y = 0
                        platform.x = random.randint(0, SCREEN_WIDTH)

            # checks doodle-platform collision
            for platform in self.platforms:
                if ((self.x + 50 > platform.x) and (self.x + 20 < platform.x + 68)
                        and (self.y + 70 > platform.y) and (self.y + 70 < platform.y + 14)
                        and (self.dy > 0)):
                    self.dy = -10

            # drawings
            self.display_surface.blit(BACKGROUND_SPRITE, (0, 0))
            for platform in self.platforms:
                self.display_surface.blit(PLATFORM_SPRITE, platform)
            self.display_surface.blit(DOODLE_SPRITE, (self.x, self.y))
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def terminate(self):
        self.is_running = False


if __name__ == "__main__":
    Application().run()

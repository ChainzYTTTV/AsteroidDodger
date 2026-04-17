import pygame
from SilversPyPhysics.momentum import Momentum

class Player:
    def __init__(self, x, y):
        self.Health = 100
        self.momentum = Momentum()

        self.rect = pygame.Rect(x, y, 50, 50)

    def handleInput(self, keys):
        direction = keys[pygame.K_a] - keys[pygame.K_d]

        if keys[pygame.K_a]:
            direction = -1
        if keys[pygame.K_d]:
            direction = 1

        self.momentum.update(direction)
        self.rect.x += self.momentum.velocity_x

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 255), self.rect)
import random
import pygame

class Enemy:
    def __init__(self, x, y, w, h, level):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        speedTier = (level - 1) // 3

        minSpeed = 2 + (level * 0.5)
        maxSpeed = minSpeed + 1
        self.fallSpeed = random.uniform(minSpeed, maxSpeed)

        overAllMaxSpeed = 18
        if self.fallSpeed >= overAllMaxSpeed:
            self.fallSpeed = overAllMaxSpeed

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
    def update(self):
        self.y += self.fallSpeed
        self.rect.y = int(self.y)

    def offScreenCheck(self, screenHight):
        return self.rect.top > screenHight

    def draw(self, win):
        pygame.draw.rect(win,(128, 128, 128), self.rect)
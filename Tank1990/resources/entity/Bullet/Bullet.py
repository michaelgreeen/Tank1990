import pygame
from Tank1990.resources.configuration.Common import BULLET_VELOCITY


class Bullet():
    def __init__(self, x, y, caliber, length, direction_vector, color):
        self.x = x
        self.y = y
        if direction_vector[0] == 0:
            self.height = length
            self.width = caliber
        else:
            self.height = caliber
            self.width = length
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)
        self.direction_vector = direction_vector
        self.vel = BULLET_VELOCITY

    def update(self):
        self.x += self.vel * self.direction_vector[0]
        self.y += self.vel * self.direction_vector[1]
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
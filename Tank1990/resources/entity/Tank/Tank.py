import pickle

import pygame

from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Bullet.Bullet import Bullet


class Tank:
    def __init__(self, x, y, width, height, direction_vector, color):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.rect = (x, y, width, height)
        self.vel: int = VEHICLE_VELOCITY
        self.color = color
        self.direction_vector = direction_vector
        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.shooting_cooldown = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and (self.x - self.vel >= 0):
            self.x -= self.vel
            self.direction_vector = LEFT_UNIT_VECTOR
        if keys[pygame.K_RIGHT] and (self.x + self.width + self.vel <= SCREEN_WIDTH):
            self.x += self.vel
            self.direction_vector = RIGHT_UNIT_VECTOR
        if keys[pygame.K_UP] and (self.y - self.vel >= 0):
            self.y -= self.vel
            self.direction_vector = UP_UNIT_VECTOR
        if keys[pygame.K_DOWN] and (self.y + self.height + self.vel <= SCREEN_HEIGHT):
            self.y += self.vel
            self.direction_vector = DOWN_UNIT_VECTOR
        self.update()

    def update(self):
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1

        self.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.rect = (self.x, self.y, self.width, self.height)

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shooting_cooldown == 0:
            self.shooting_cooldown = 30
            return Bullet(self.center[0], self.center[1], BULLET_CALIBER, BULLET_LENGTH, self.direction_vector, self.color)
        else:
            return

    def serializeTank(self):
        return pickle.dumps(self)

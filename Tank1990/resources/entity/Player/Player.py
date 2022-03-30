import pygame
from conf.Common import *

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 10

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and (self.x - self.vel >= 0):
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and (self.x + self.width + self.vel <= SCREEN_WIDTH):
            self.x += self.vel
        if keys[pygame.K_UP] and (self.y - self.vel >= 0):
            self.y -= self.vel
        if keys[pygame.K_DOWN] and (self.y + self.height + self.vel <= SCREEN_HEIGHT):
            self.y += self.vel

        self.update()

    def update(self):
        self.center = ((self.x +self.width)/2,(self.y + self.width)/2)
        self.rect = (self.x, self.y, self.width, self.height)
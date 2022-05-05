import pygame
from Tank1990.resources.configuration.Common import *

class Map:
    def __init__(self):
        self.MapObjects = [[] for x in range(10)]
        self.brick = pygame.transform.scale(pygame.image.load("..\\img\\brick.png"),
                                            (INTERVAL_VERTICAL, INTERVAL_HORIZONTAL))
        self.road = pygame.transform.scale(pygame.image.load("..\\img\\road.png"),
                                           (INTERVAL_VERTICAL, INTERVAL_HORIZONTAL))
        self.sand = pygame.transform.scale(pygame.image.load("..\\img\\sandbagBeige.png"),
                                           (INTERVAL_VERTICAL, INTERVAL_HORIZONTAL))

    def draw(self, win):
        for i in range(MAP_ROWS):
            for j in range(MAP_COLUMNS):
                if self.MapObjects[i][j] == 0:
                    win.blit(self.road, (INTERVAL_VERTICAL * i, INTERVAL_HORIZONTAL * j))
                elif self.MapObjects[i][j] == 1:
                    win.blit(self.brick, (INTERVAL_VERTICAL * i, INTERVAL_HORIZONTAL * j))
                elif self.MapObjects[i][j] == 2:
                    win.blit(self.sand, (INTERVAL_VERTICAL * i, INTERVAL_HORIZONTAL * j))

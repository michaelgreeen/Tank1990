import pygame
from Tank1990.resources.configuration.Common import *

class Map:
    def __init__(self):
        self.MapObjects = [[] for x in range(MAP_COLUMNS)]
        self.brick = pygame.transform.scale(pygame.image.load("..\\img\\brick.png").convert(),(INTERVAL_HORIZONTAL,INTERVAL_VERTICAL))
        self.road = pygame.transform.scale(pygame.image.load("..\\img\\road.png").convert(),(INTERVAL_HORIZONTAL,INTERVAL_VERTICAL))
        self.sand = pygame.transform.scale(pygame.image.load("..\\img\\sandBeige.png").convert(),(INTERVAL_HORIZONTAL,INTERVAL_VERTICAL))
        self.barrelGreen = pygame.transform.scale(pygame.image.load("..\\img\\barrelGreen_side.png").convert(),(INTERVAL_HORIZONTAL,INTERVAL_VERTICAL))
        self.fastAsphalt = pygame.transform.scale(pygame.image.load("..\\img\\fast-asphalt.png").convert(),(INTERVAL_HORIZONTAL,INTERVAL_VERTICAL))
    def draw(self, win):
        for i in range(MAP_ROWS):
            for j in range(MAP_COLUMNS):
                if self.MapObjects[i][j] == 0:
                    win.blit(self.road,(INTERVAL_VERTICAL * j, INTERVAL_HORIZONTAL * i))
                elif self.MapObjects[i][j] == 1:
                    win.blit(self.brick,(INTERVAL_VERTICAL * j, INTERVAL_HORIZONTAL * i))
                elif self.MapObjects[i][j] == 2:
                    win.blit(self.sand,(INTERVAL_VERTICAL * j, INTERVAL_HORIZONTAL * i))
                elif self.MapObjects[i][j] == 3:
                    win.blit(self.barrelGreen,(INTERVAL_VERTICAL * j, INTERVAL_HORIZONTAL * i))
                elif self.MapObjects[i][j] == 4:
                    win.blit(self.fastAsphalt,(INTERVAL_VERTICAL * j, INTERVAL_HORIZONTAL * i))

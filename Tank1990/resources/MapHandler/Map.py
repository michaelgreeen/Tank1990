import pygame
from Tank1990.resources.configuration.Common import *

class Map:
    def __init__(self):
        self.MapObjects = [[] for x in range(10)]
        self.rows = 10
        self.columns = 10
        self.brick = pygame.transform.scale(pygame.image.load("..\\img\\brick.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))
        self.road = pygame.transform.scale(pygame.image.load("..\\img\\road.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))
        self.sand = pygame.transform.scale(pygame.image.load("..\\img\\sandbagBeige.png"),(SCREEN_WIDTH/self.columns,SCREEN_HEIGHT/self.rows))

    def draw(self, win):
        intervalHorizontal = SCREEN_WIDTH / self.columns
        intervalVertical = SCREEN_HEIGHT / self.rows
        for i in range(self.rows):
            for j in range(self.columns):
                if self.MapObjects[i][j] == 0:
                    win.blit(self.road,(intervalVertical * j, intervalHorizontal * i))
                elif self.MapObjects[i][j] == 1:
                    win.blit(self.brick,(intervalVertical * j, intervalHorizontal * i))
                elif self.MapObjects[i][j] == 2:
                    win.blit(self.sand,(intervalVertical * j, intervalHorizontal * i))

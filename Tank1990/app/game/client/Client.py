import pygame

from Tank1990.resources.MapHandler.Map import Map
from Tank1990.resources.entity.network.Network import Network
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
import pickle
from Tank1990.resources.message_types.bulletCreateMessage.bulletCreateMessage import bulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.bulletUpdateRequest import bulletUpdateRequest
from Tank1990.resources.message_types.mapUpdateMessage.mapUpdateMessage import mapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.playerCreateMessage import playerCreateMessage
from Tank1990.resources.message_types.requestMapEvents.RequestMapEvents import RequestMapEvents
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateRequest import tankUpdateRequest


class Client:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Client")
        self.running = True
        self.network: Network = Network()
        createPlayerMessageObject: playerCreateMessage = pickle.loads(self.network.getInitPlayerObject())
        self.player: Player = createPlayerMessageObject.player

        self.bulletObjects = []
        self.tankObjects = []
        self.eventObjects = []
        self.map = self.initializeMapOutline(createPlayerMessageObject.mapOutline)

    def initializeMapOutline(self, mapOutline):
        map = Map()
        map.MapObjects = mapOutline
        return map

    def tankMoveCheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.network.send(tankUpdateMessage(LEFT_UNIT_VECTOR).getMessage())
        if keys[pygame.K_RIGHT]:
            self.network.send(tankUpdateMessage(RIGHT_UNIT_VECTOR).getMessage())
        if keys[pygame.K_UP]:
            self.network.send(tankUpdateMessage(UP_UNIT_VECTOR).getMessage())
        if keys[pygame.K_DOWN]:
            self.network.send(tankUpdateMessage(DOWN_UNIT_VECTOR).getMessage())

    def shootCheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.network.send(bulletCreateMessage().getMessage())

    def updateGameObjects(self):
        self.tankObjects = pickle.loads(self.network.send(tankUpdateRequest().getMessage())).tanks
        self.bulletObjects = pickle.loads(self.network.send(bulletUpdateRequest().getMessage())).bullets
        self.eventObjects = pickle.loads(self.network.send(RequestMapEvents().getMessage())).map_event_list
        self.map = self.initializeMapOutline(pickle.loads(self.network.send(mapUpdateMessage().getMessage())).map_outline)

    def redrawWindow(self):
        self.win.fill((0, 0, 0))
        self.map.draw(self.win)
        for bullet in self.bulletObjects:
            bullet.draw(self.win)


        for tank in self.tankObjects:
            tank.draw(self.win)

        pygame.display.update()



def main():
    client = Client()
    clock = pygame.time.Clock()
    while client.running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
                pygame.quit()
        client.tankMoveCheck()
        client.shootCheck()
        client.updateGameObjects()
        client.redrawWindow()


if __name__ == "__main__":
    main()
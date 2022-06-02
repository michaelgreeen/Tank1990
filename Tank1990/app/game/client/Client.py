import os

import pygame

from Tank1990.resources.MapHandler.Map import Map
from Tank1990.resources.entity.network.Network import Network
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
import pickle
from Tank1990.resources.message_types.bulletCreateMessage.BulletCreateMessage import BulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.BulletUpdateRequest import BulletUpdateRequest
from Tank1990.resources.message_types.crowdControlMessage.RequestOrderIssuance import RequestOrderIssuance
from Tank1990.resources.message_types.mapUpdateMessage.MapUpdateMessage import MapUpdateMessage
from Tank1990.resources.message_types.playerCreateMessage.PlayerCreateMessage import PlayerCreateMessage
from Tank1990.resources.message_types.requestMapEvents.RequestMapEvents import RequestMapEvents
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateMessage import TankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateRequest import TankUpdateRequest
from Tank1990.resources.message_types.crowdControlMessage.CreateCrowdFollowMessage import CreateCrowdFollowMessage


class Client:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Client")
        self.running = True
        self.network: Network = Network()
        createPlayerMessageObject: PlayerCreateMessage = pickle.loads(self.network.getInitPlayerObject())
        self.player: Player = createPlayerMessageObject.player
        self.issuing_orders = False
        self.bulletObjects = []
        self.tankObjects = []
        self.eventObjects = []
        self.map = self.initializeMapOutline(createPlayerMessageObject.mapOutline)
        self.clicked_grid = (None, None)
        self.grid_outline_image = pygame.image.load("../img/green_square_outline.png") if self.player.team.color == GREEN \
            else pygame.image.load("../img/orange_square_outline.png")
        self.grid_outline_image = pygame.transform.scale(self.grid_outline_image, (INTERVAL_VERTICAL, INTERVAL_HORIZONTAL))

    def displayCommunicates(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        content = ""
        if self.issuing_orders:
            content = "YOU ARE ISSUING ORDERS"
        else:
            content = "YOU ARE NOT ISSUING ORDERS"


        text = font.render(content, True, BRIGHT_YELLOW)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT - 32)
        self.win.blit(text, textRect)

    def initializeMapOutline(self, mapOutline):
        map = Map()
        map.MapObjects = mapOutline
        return map

    def tankMoveCheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.network.send(TankUpdateMessage(LEFT_UNIT_VECTOR).getMessage())
        elif keys[pygame.K_RIGHT]:
            self.network.send(TankUpdateMessage(RIGHT_UNIT_VECTOR).getMessage())
        elif keys[pygame.K_UP]:
            self.network.send(TankUpdateMessage(UP_UNIT_VECTOR).getMessage())
        elif keys[pygame.K_DOWN]:
            self.network.send(TankUpdateMessage(DOWN_UNIT_VECTOR).getMessage())



    def issueOrderCheck(self):

            for event in pygame.event.get():
                if self.issuing_orders:
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        X_grid = int(pos[0]//INTERVAL_HORIZONTAL)
                        Y_grid = int(pos[1]//INTERVAL_VERTICAL)
                        self.clicked_grid = (X_grid * INTERVAL_HORIZONTAL, Y_grid * INTERVAL_VERTICAL)
                if event.type == pygame.KEYUP and event.key == pygame.K_o:
                    order_issuing_player_id = pickle.loads(self.network.send(RequestOrderIssuance().getMessage())).issuing_player_id
                    if order_issuing_player_id == self.player.id:
                        self.issuing_orders = True
                    else:
                        self.issuing_orders = False










    def crowdControlCheck(self):
        keys = pygame.key.get_pressed()
        follow_request = False

        if keys[pygame.K_f] and self.issuing_orders:
            follow_request =  not follow_request
            self.network.send(CreateCrowdFollowMessage(self.player.tank, follow_request).getMessage())

    def shootCheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.network.send(BulletCreateMessage().getMessage())

    def updateGameObjects(self):
        self.tankObjects = pickle.loads(self.network.send(TankUpdateRequest().getMessage())).tanks
        self.bulletObjects = pickle.loads(self.network.send(BulletUpdateRequest().getMessage())).bullets
        self.player.tank = pickle.loads(self.network.send(CreateCrowdFollowMessage(self.player.tank, False).getMessage())).tank
        self.eventObjects.extend(pickle.loads(self.network.send(RequestMapEvents().getMessage())).map_event_list)
        self.map = self.initializeMapOutline(pickle.loads(self.network.send(MapUpdateMessage().getMessage())).map_outline)

    def redrawWindow(self):
        self.win.fill((0, 0, 0))
        self.map.draw(self.win)


        if self.clicked_grid != (None, None):
            self.win.blit(self.grid_outline_image, self.clicked_grid)


        for bullet in self.bulletObjects:
            bullet.draw(self.win)


        for tank in self.tankObjects:
            tank.draw(self.win)

        for event in self.eventObjects:
            event.update()
            if event.stage_counter >= len(event.stage_img):
                self.eventObjects.remove(event)
            else:
                event.draw(self.win)
        self.displayCommunicates()

        pygame.display.update()



def main():
    pygame.init()
    if os.path.exists("../sound/sabaton-ghost-division-8bit.mp3"):
        pygame.mixer.init()
        pygame.mixer.music.load("../sound/sabaton-ghost-division-8bit.mp3")
        pygame.mixer.music.play(-1)

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

        client.crowdControlCheck()
        client.issueOrderCheck()
        client.redrawWindow()


if __name__ == "__main__":
    main()
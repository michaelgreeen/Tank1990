import pygame

from Tank1990.resources.entity.Bullet.Bullet import Bullet
from Tank1990.resources.entity.network.Network import Network
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.resources.configuration.Common import *
import pickle
from Tank1990.resources.entity.Tank.Tank import Tank
from Tank1990.resources.message_types.bulletCreateMessage.bulletCreateMessage import bulletCreateMessage
from Tank1990.resources.message_types.bulletCreateMessage.bulletUpdateRequest import bulletUpdateRequest

from Tank1990.resources.message_types.playerCreateMessage.playerCreateMessage import playerCreateMessage
from Tank1990.resources.message_types.tankUpdateMessage.batchTankUpdateMessage import batchTankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage
from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateRequest import tankUpdateRequest


class Client:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Client")
        #pygame.mixer.init()
        #pygame.mixer.music.load("../sound/sabaton-ghost-division-official-lyric-video.mp3")
        #pygame.mixer.music.play(loops = -1)
        self.running = True
        self.network: Network = Network()
        createPlayerMessageObject: playerCreateMessage = pickle.loads(self.network.getInitPlayerObject())
        self.player: Player = createPlayerMessageObject.player

        self.bulletObjects = []
        self.tankObjects = []



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


    def redrawWindow(self, background):
        self.win.fill((0, 0, 0))
        self.win.blit(background, (0, 0))

        for bullet in self.bulletObjects:
            bullet.draw(self.win)


        for tank in self.tankObjects:
            tank.draw(self.win)

        pygame.display.update()



def main():
    client = Client()
    clock = pygame.time.Clock()
    background = pygame.image.load("..\\img\\Dirt1.png").convert()
    while client.running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
                pygame.quit()
        client.tankMoveCheck()
        client.shootCheck()
        client.updateGameObjects()
        client.redrawWindow(background)


if __name__ == "__main__":
    main()
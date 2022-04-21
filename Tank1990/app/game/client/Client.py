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



class Client:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Client")
        pygame.mixer.init()
        pygame.mixer.music.load("../sound/sabaton-ghost-division-official-lyric-video.mp3")
        pygame.mixer.music.play(loops = -1)
        self.running = True
        self.network: Network = Network()
        createPlayerMessageObject: playerCreateMessage = pickle.loads(self.network.getInitPlayerObject())
        self.player: Player = createPlayerMessageObject.player
        #List of players on the server
        self.serverPlayerInfo = []
        self.bulletObjects = []


    def updatePlayerInfoOnServer(self):
        batchTankUpdateMessageFromServer: batchTankUpdateMessage = pickle.loads(self.network.send(tankUpdateMessage(self.player.id, self.player.tank.x, self.player.tank.y, self.player.tank.direction_vector, self.player.team.color).getMessage()))
        print(batchTankUpdateMessageFromServer)
        self.serverPlayerInfo.clear()
        for tankUpdateMessageFromServer in batchTankUpdateMessageFromServer.tankUpdateMessages:
            message: tankUpdateMessage = tankUpdateMessageFromServer
            playerEntry = (message.player_id, message.new_x, message.new_y, message.new_direction_vector, message.team_color)
            self.serverPlayerInfo.append(playerEntry)

    def createBulletOnServer(self, bullet):
        createBulletMessage = bulletCreateMessage(bullet)
        self.network.send(createBulletMessage.getMessage())

    def updateBulletObjects(self):
        updateRequest = bulletUpdateRequest()
        serverResponse = self.network.send(updateRequest.getMessage())
        serverResponse = pickle.loads(serverResponse)
        for bullet_creation_message in serverResponse.bullets_to_add:
            self.bulletObjects.append(bullet_creation_message.bullet)


            
            
    

    def redrawWindow(self, background):
        self.win.fill((0, 0, 0))
        self.win.blit(background, (0, 0))
        for bullet in self.bulletObjects:
            bullet.draw(self.win)

        for playerInfo in self.serverPlayerInfo:
            tank = Tank(playerInfo[1], playerInfo[2], playerInfo[3], playerInfo[4])
            tank.draw(self.win)
        pygame.display.update()



def main():
    client = Client()
    clock = pygame.time.Clock()
    background = pygame.image.load("..\\img\\Dirt1.png")
    while client.running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
                pygame.quit()
        client.player.tank.move()
        client.updatePlayerInfoOnServer()
        bullet = client.player.tank.shoot()
        if type(bullet) == Bullet:
            client.createBulletOnServer(bullet)
        client.updateBulletObjects()
        for bullet in client.bulletObjects:
            bullet.update()
            if bullet.x > SCREEN_WIDTH or bullet.x < 0 or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                client.bulletObjects.remove(bullet)


        client.redrawWindow(background)


if __name__ == "__main__":
    main()
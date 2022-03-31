from typing import List
import pygame
from Tank1990.network.Network import Network
from Tank1990.resources.entity.Player.Player import Player
from Tank1990.conf.Common import *



class Client:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Client")
        self.network: Network = Network()
        startPos = read_pos_team(self.network.getPos())
        self.running: bool = True
        width = VEHICLE_WIDTH
        height = VEHICLE_HEIGHT
        if startPos[2] == "RED":
            color = RED
        else:
            color = GREEN
        self.player = Player(startPos[0], startPos[1], width, height, color)
        #Information about other players stored in format [0] : x_pos, [1] : y_pos, [2] color
        self.serverPlayerInfo = []

    def initPlayerInfoOnServer(self):
        print("INITIALIZING PLAYER ON SERVER \n")
        print("X POS: " + str(self.player.x) + "\t" + "Y POS: " + str(self.player.y))
        self.network.send(make_pos_team((self.player.x, self.player.y, self.player.color_string)))

    def updatePlayerInfoOnServer(self):
        player_info_string_list = self.network.send("PLAYER_LIST_REQUEST")
        print(player_info_string_list)
        self.serverPlayerInfo.clear()
        player_info_string_list = player_info_string_list.split("\n")
        player_info_string_list.remove("")
        print(player_info_string_list)
        for player_info in player_info_string_list:
            player_info = player_info.split(",")
            self.serverPlayerInfo.append((int(player_info[0]), int(player_info[1]), player_info[2]))
    

        


    def getPlayersFromServer(self):
        read_pos_team(self.network.send(make_pos_team((self.player.x, self.player.y, self.player.color_string))))


    def redrawWindow(self):
        self.win.fill((255, 255, 255))
        self.updatePlayerInfoOnServer()
        for playerInfo in self.serverPlayerInfo:
            createdPlayer = Player(playerInfo[0], playerInfo[1], VEHICLE_WIDTH, VEHICLE_HEIGHT, playerInfo[2])
            createdPlayer.draw(self.win)
        pygame.display.update()



def main():
    client = Client()
    clock = pygame.time.Clock()
    client.initPlayerInfoOnServer()

    while client.running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
                pygame.quit()
        client.player.move()
       # client.updatePlayerInfoOnServer()
        client.redrawWindow()


if __name__ == "__main__":
    main()
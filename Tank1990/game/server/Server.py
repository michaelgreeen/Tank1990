import socket
from _thread import *
import sys
import threading
from Tank1990.conf.Common import *
from Tank1990.resources.entity.Team.Team import Team
from Tank1990.resources.entity.Player.Player import Player
import Tank1990.game.server.ClientThread

PLAYER_TEAMS_LOCK = threading.Lock()

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Using dictionary (HashMap) for best efficiency in accessing teams
        self.teams = {"Green": Team("Green"), "Red": Team("Red")}

    def addPlayer(self, player: Player):
        #For now we assume that each team will have 2 players
        #At first we check which team has the bigger number of players
        #If they both have an equal count we add to the team Green
        #To be modified later probably 
        teamGreen:Team = self.teams.get("Green")
        teamRed:Team = self.teams.get("Red")
        if len(teamGreen.getPlayers()) > len(teamRed.getPlayers()):
            teamRed.addPlayer(player)
            return "RED"
        else:
            teamGreen.addPlayer(player)
            return "GREEN"
    def removePlayer(self, player: Player):
        teamGreen:Team = self.teams.get("Green")
        teamRed:Team = self.teams.get("Red")
        if player in teamGreen.getPlayers():
            teamGreen.removePlayer(player)
        if player in teamRed.getPlayers():
            teamRed.removePlayer(player)

    def bindSocket(self, ipAddress: str, port: str):
        try:
            self.socket.bind((ipAddress, port))
        except socket.error as e:
            str(e)
        self.socket.listen(5)
        print("Waiting for a connection, Server Started")

        

    def runServer(self):
        while True:
            connection, address = self.socket.accept()
            print("Connected to: ", address)
            start_new_thread(Tank1990.game.server.ClientThread.clientThread, (self, connection, len(self.teams.get("Red").getPlayers() + self.teams.get("Green").getPlayers())))


def main():
    server = Server()
    server.bindSocket(IP_ADDRESS, PORT)
    server.runServer()

if __name__ == "__main__":
    main()




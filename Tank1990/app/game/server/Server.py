import socket
from threading import Thread
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Team.Team import Team
from Tank1990.resources.entity.Player.Player import Player

from Tank1990.app.game.server.ClientThread import clientThread




class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        #Using dictionary (HashMap) for best efficiency in accessing teams
        self.teams = {"Green": Team("Green", GREEN), "Red": Team("Red", RED)}
        self.ids = {0, 1, 2, 3}
        self.bullet_objects_queue = []

    def addPlayer(self, player: Player):
        #For now we assume that each team will have 2 players
        #At first we check which team has the bigger number of players
        #If they both have an equal count we add to the team Green
        #To be modified later probably
        teamGreen:Team = self.teams.get("Green")
        teamRed:Team = self.teams.get("Red")
        if len(teamGreen.players) > len(teamRed.players):
            player.assignToTeam(teamRed)
        else:
            player.assignToTeam(teamGreen)

    def removePlayer(self, player: Player):
        teamGreen:Team = self.teams.get("Green")
        teamRed:Team = self.teams.get("Red")
        if player in teamGreen.players:
            teamGreen.removePlayer(player)
        if player in teamRed.players:
            teamRed.removePlayer(player)

    def bindSocket(self, ipAddress: str, port: str):
        try:
            self.socket.bind((ipAddress, port))
        except socket.error as e:
            str(e)
        self.socket.listen(4)
        print("Waiting for a connection, Server Started")



    def runServer(self):

        while True:
            connection, address = self.socket.accept()
            self.clients.append(connection)
            print("Connected to: ", address)
            thread = Thread(target = clientThread, args = (self, connection, len(self.teams.get("Red").players + self.teams.get("Green").players)))
            thread.run()


def main():
    server = Server()
    server.bindSocket(IP_ADDRESS, PORT)
    server.runServer()

if __name__ == "__main__":
    main()




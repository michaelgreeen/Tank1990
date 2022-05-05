import socket
from threading import Thread, Lock

from Tank1990.app.game.server.ServerHandler import ServerHandlingThread
from Tank1990.resources.configuration.Common import *
from Tank1990.resources.entity.Team.Team import Team
from Tank1990.resources.entity.Player.Player import Player

from Tank1990.app.game.server.ClientThread import clientThread




class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Using dictionary (HashMap) for best efficiency in accessing teams
        self.teams = {"Green": Team("Green", GREEN), "Red": Team("Red", RED)}
        self.bullet_objects = []
        self.ids = {0, 1, 2, 3}
        self.bullet_objects_queue = []

        #Player slots with approporiate id's
        self.player_slots = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}

        self.message_queues_lock = {"PLAYER_MOVE_LOCK": Lock(), "BULLET_CREATE_LOCK": Lock()}

        #Player move messages format:
        #Player id, move direction
        #Bullet create message format
        #Id of shooting player
        self.message_queues = {"PLAYER_MOVE": [], "BULLET_CREATE": []}

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
        self.socket.listen(len(self.player_slots))
        print("Waiting for a connection, Server Started")



    def runServer(self):
        server_handling_thread = Thread(target = ServerHandlingThread, args = (self,))
        server_handling_thread.start()
        while True:
            connection, address = self.socket.accept()
            print("Connected to: ", address)
            thread = Thread(target = clientThread, args = (self, connection))
            thread.start()


def main():
    server = Server()
    server.bindSocket(IP_ADDRESS, PORT)
    server.runServer()

if __name__ == "__main__":
    main()




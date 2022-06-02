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
        self.player_slots = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}

        self.message_queues_lock = {"PLAYER_MOVE_LOCK": Lock(), "BULLET_CREATE_LOCK": Lock(), "FOLLOW_EVENT_LOCK": Lock()}
        self.player_map_events_locks = [Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock()]
        self.player_map_events = [[], [], [], [], [], [], [], [], [], []]


        #Player move messages format:
        #Player id, move direction
        #Bullet create message format
        #Id of shooting player
        self.message_queues = {"PLAYER_MOVE": [], "BULLET_CREATE": [], "FOLLOW_EVENT": []}

        self.mapOutline = [[0, 0, 0, 1, 2, 1, 2, 1, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 2, 0, 0, 3, 3, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 2, 0, 3, 2, 2, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 4, 4, 0, 0, 4, 4, 4, 4, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 1, 1, 1, 3, 2, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 0, 2, 0, 1, 3, 2, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 1, 1, 1, 1, 2, 0, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 2, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 2, 0, 3, 1, 3, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 0, 1, 2, 1, 2, 1, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 2, 0, 0, 3, 3, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 2, 0, 3, 2, 2, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 4, 4, 0, 0, 4, 4, 4, 4, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 2, 1, 1, 1, 3, 2, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 0, 2, 0, 1, 3, 2, 2, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 1, 1, 1, 1, 2, 0, 1, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 2, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0],
                           [0, 0, 1, 2, 0, 3, 1, 3, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 0]
                           ]

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
        teamGreen = self.teams.get("Green")
        teamRed = self.teams.get("Red")
        if player in teamGreen.players:
            teamGreen.removePlayer(player)
        if player in teamRed.players:
            teamRed.removePlayer(player)

    def bindSocket(self, ipAddress: str, port: str):
        try:
            self.socket.bind((ipAddress, port))
        except socket.error as e:
            print(str(e))
        self.socket.listen(PLAYER_COUNT)
        print("Waiting for a connection, Server Started")



    def runServer(self):
        server_handling_thread = Thread(target = ServerHandlingThread, args = (self,))
        server_handling_thread.start()

        while True:
            connection, address = self.socket.accept()
            print("Connected to: ", address)
            player_number = 0
            for slot in self.player_slots:
                if self.player_slots[slot].isBot:
                    player_number = slot
                    break
                else:
                    continue

            thread = Thread(target=clientThread, args=(self, connection, player_number))
            self.player_slots[player_number].isBot = False

            thread.start()


def main():
    server = Server()
    server.bindSocket(IP_ADDRESS, PORT)
    server.runServer()

if __name__ == "__main__":
    main()




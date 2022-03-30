import socket
from _thread import *
import sys
from conf.Common import *
from game.server.ClientThread import clientThread

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []

    def bindSocket(self, ipAddress: str, port: str):
        try:
            self.socket.bind(ipAddress, port)
        except socket.error as e:
            str(e)
        self.socket.listen(5)
        print("Waiting for a connection, Server Started")

    def runServer(self):
        while True:
            connection, address = self.socket.accept()
            print("Connected to: " + address)
            self.players.append(address)
            start_new_thread(clientThread, (connection, len(self.players) - 1))


def main():
    server = Server()
    server.bindSocket(IP_ADDRESS, PORT)
    server.runServer()

if __name__ == "__main__":
    main()




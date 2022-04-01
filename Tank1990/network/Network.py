import socket
from Tank1990.conf.Common import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP_ADDRESS
        self.port = PORT
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connection succesfull")
            receive = self.client.recv(2048//2).decode()
            print("Received: " + receive)
            return receive
        except:
            print("Receive failed")
            pass

    def send(self, data):
        try:
            print("Sending: " + data)
            self.client.send(str.encode(data))
            receive = self.client.recv(2048//2).decode()
            print("Received: " + receive)
            return receive
        except socket.error as e:
            print(e)
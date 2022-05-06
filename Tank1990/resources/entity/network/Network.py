import socket
from Tank1990.resources.configuration.Common import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP_ADDRESS
        self.port = PORT
        self.addr = (self.server, self.port)
        self.initPlayerObject = self.connect()

    def getInitPlayerObject(self):
        return self.initPlayerObject

    def connect(self):
        try:
            self.client.connect(self.addr)
            #print("Connection succesfull")
            receive = self.client.recv(4096//1)
            #print("Received: ", receive)
            return receive
        except:
            print("Receive failed")
            pass

    def send(self, data):
        try:
            #print("Sending: ", data)
            self.client.send(data)
            receive = self.client.recv(4096//1)
            #print("Received: ", receive)
            return receive
        except socket.error as e:
            print("Receive Failed")
            print(e)
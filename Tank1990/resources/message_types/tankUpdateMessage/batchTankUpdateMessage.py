import pickle

from Tank1990.resources.message_types.tankUpdateMessage.tankUpdateMessage import tankUpdateMessage


class batchTankUpdateMessage:
    def __init__(self):
        self.tankUpdateMessages = []

    def addTankUpdateMessage(self, message: tankUpdateMessage):
        self.tankUpdateMessages.append(message)

    def getMessage(self):
        return pickle.dumps(self)

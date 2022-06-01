import pickle

from Tank1990.resources.message_types.tankUpdateMessage.TankUpdateMessage import TankUpdateMessage


class BatchTankUpdateMessage:
    def __init__(self):
        self.tankUpdateMessages = []

    def addTankUpdateMessage(self, message: TankUpdateMessage):
        self.tankUpdateMessages.append(message)

    def getMessage(self):
        return pickle.dumps(self)

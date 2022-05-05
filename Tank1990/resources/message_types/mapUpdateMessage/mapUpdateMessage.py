import pickle


class mapUpdateMessage:
    def __init__(self,newMap):
        self.map = newMap

    def getMessage(self):
        return pickle.dumps(self)
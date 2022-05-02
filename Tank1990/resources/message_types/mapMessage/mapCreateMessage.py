import pickle

class mapCreateMessage:
    def __init__(self,Map:map):
        self.map = map

    def getMessage(self):
        return pickle.dumps(self)
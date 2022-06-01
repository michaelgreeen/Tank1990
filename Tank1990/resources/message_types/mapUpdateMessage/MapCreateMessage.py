import pickle


class MapCreateMessage:
    def __init__(self, map):
        self.mapOutline = map

    def getMessage(self):
        return pickle.dumps(self)

import pickle


class MapUpdateMessage:
    def __init__(self):
        self.map_outline =[[]]

    def getMessage(self):
        return pickle.dumps(self)

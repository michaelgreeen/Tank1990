import pickle


class tankUpdateMessage:
    def __init__(self, direction_vector):
        self.direction_vector = direction_vector

    def getMessage(self):
        return pickle.dumps(self)



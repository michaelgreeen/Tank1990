import pickle


class tankUpdateRequest:
    def __init__(self):
        self.tanks = []

    def getMessage(self):
        return pickle.dumps(self)
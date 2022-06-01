import pickle


class TankUpdateRequest:
    def __init__(self):
        self.tanks = []

    def getMessage(self):
        return pickle.dumps(self)
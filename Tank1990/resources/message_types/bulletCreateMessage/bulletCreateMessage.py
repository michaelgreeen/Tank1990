import pickle
class bulletCreateMessage:

    def __init__(self, bullet):
        self.bullet = bullet

    def getMessage(self):
        return pickle.dumps(self)
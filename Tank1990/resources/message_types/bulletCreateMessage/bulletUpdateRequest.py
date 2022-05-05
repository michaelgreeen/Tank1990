import pickle
class bulletUpdateRequest():
    def __init__(self):
        self.bullets = []

    def getMessage(self):
        return pickle.dumps(self)
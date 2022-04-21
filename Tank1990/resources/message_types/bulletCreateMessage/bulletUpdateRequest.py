import pickle
class bulletUpdateRequest():
    def __init__(self):
        self.bullets_to_add = []

    def getMessage(self):
        return pickle.dumps(self)
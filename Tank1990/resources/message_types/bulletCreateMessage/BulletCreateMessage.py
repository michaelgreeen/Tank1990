import pickle
class BulletCreateMessage:

    def __init__(self):
        pass


    def getMessage(self):
        return pickle.dumps(self)
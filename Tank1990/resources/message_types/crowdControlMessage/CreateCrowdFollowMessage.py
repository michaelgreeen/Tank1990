import pickle


class CreateCrowdFollowMessage:
    def __init__(self, tank, followRequest):
        self.tank = tank
        self.followRequest = followRequest

    def getMessage(self):
        return pickle.dumps(self)

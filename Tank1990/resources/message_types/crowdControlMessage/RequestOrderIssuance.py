import pickle


class RequestOrderIssuance():
    def __init__(self):
        self.issuing_player_id = None


    def getMessage(self):
        return pickle.dumps(self)

import pickle


class RequestOrderIssuance:
    def __init__(self, player_id):
        self.issuing_player_id = player_id


    def getMessage(self):
        return pickle.dumps(self)

import pickle


class RequestMapEvents:
    def __init__(self):
        self.map_event_list = []


    def getMessage(self):
        return pickle.dumps(self)

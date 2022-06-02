import pickle


class TargetGridMessage():
    def __init__(self, target_grid):
        self.target_grid = target_grid


    def getMessage(self):
        return pickle.dumps(self)

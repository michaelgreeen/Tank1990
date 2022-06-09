import pickle

class AttackOrderMessage:

    def __init__(self, attack_closest_enemy):
        self.attack_closest_enemy = attack_closest_enemy

    def getMessage(self):
        return pickle.dumps(self)
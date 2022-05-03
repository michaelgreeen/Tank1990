import pickle


class tankUpdateMessage:
    def __init__(self, player_id, new_x, new_y, new_direction_vector, team_color):
        self.player_id = player_id
        self.new_x = new_x
        self.new_y = new_y
        self.new_direction_vector = new_direction_vector
        self.team_color = team_color

    def getMessage(self):
        return pickle.dumps(self)



class ExplosionEffect:
    def __init__(self, x, y):
        self.stage_counter = 0
        self.x = x
        self.y = y

    def update(self):
        self.stage_counter += 1
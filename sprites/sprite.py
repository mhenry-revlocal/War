class Sprite(object):
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
    def act(self, height, width, game_controller, events):
        pass
    def draw(self, game_display, height, width, game_controller):
        pass
    def reset(self):
        pass
    def get_boundries(self):
        pass
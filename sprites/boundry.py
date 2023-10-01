class Boundry(object):
    def __init__(self, x, y, h, w):
        self.x_coord = x
        self.y_coord = y
        self.height = h
        self.width = w
    def intersects(self, boundry):
        x_diff = abs(self.x_coord - boundry.x_coord)
        y_diff = abs(self.y_coord - boundry.y_coord)
        if self.x_coord < boundry.x_coord:
            x_lap = x_diff < self.width
        else:
            x_lap = x_diff < boundry.width
        if self.y_coord < boundry.y_coord:
            y_lap = y_diff < self.height
        else:
            y_lap = y_diff < boundry.height
        return x_lap and y_lap
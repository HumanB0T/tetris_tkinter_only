PIXEL_SIZE = 20

class Tetrimino:

    def __init__(self, coords, game_window):
        self.coords = coords
        self.game_window = game_window


class ITetrimino(Tetrimino):

    def move_down(self):
        self.coords = list(map(lambda xy: (xy[0], xy[1] + PIXEL_SIZE), self.coords))

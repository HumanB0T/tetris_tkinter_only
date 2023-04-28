import random

# Settings
PIXEL_SIZE = 20               # Do not change it
SIDE_WAYS_HOW_MANY_TIMES = 2  # How many times you can move tetrimino in sideways before it drop down
SPEED = 200                   # In milliseconds. The higher the amount the move is slower


class Tetrimino:
    collided_area = []

    def __init__(self, game_window):
        self.game_window = game_window
        self.current_coords = []
        self.moving_sideways_counter = 0
        self.perspective = ""
        self.horizontal_middle_statement = ""

    def __len__(self):
        return len(self.current_coords)

    def move(self, game_window):
        self.count_sideways_moving(game_window)

        if game_window.direction == "Down":
            self.current_coords = list(map(lambda xy: (xy[0], xy[1] + PIXEL_SIZE), self.current_coords))

        if self.get_most_left_x() > 40:
            if game_window.direction == "Left":
                self.current_coords = list(map(lambda xy: (xy[0] - PIXEL_SIZE, xy[1]), self.current_coords))

        if self.get_most_right_x() < 580:
            if game_window.direction == "Right":
                self.current_coords = list(map(lambda xy: (xy[0] + PIXEL_SIZE, xy[1]), self.current_coords))

        if game_window.direction == "Up":
            if self.perspective == "vertical":
                self.rotate_to_horizontal()
            else:
                self.rotate_to_vertical()

        game_window.create_graphics(self.current_coords)
        game_window.direction = "Down"
        game_window.after(SPEED, game_window.perform_actions)

    def count_sideways_moving(self, game_window):
        if game_window.direction in ("Left", "Right", "Up"):
            self.moving_sideways_counter += 1

        if self.moving_sideways_counter > SIDE_WAYS_HOW_MANY_TIMES:
            self.moving_sideways_counter = 0
            game_window.direction = "Down"

    def rotate_to_horizontal(self):
        pass

    def rotate_to_vertical(self):
        pass

    def get_most_left_x(self):
        return min([item[0] for item in self.current_coords])

    def get_most_right_x(self):
        return max([item[0] for item in self.current_coords])

    @staticmethod
    def generate_random_tetrimino(game_window):
        chosen_tetrimino = random.choice([ITetrimino])
        return chosen_tetrimino(game_window)


class ITetrimino(Tetrimino):

    def __init__(self, game_window):
        super().__init__(game_window)
        # starting coords defined below
        self.current_coords = [[300, 20], [300, 40], [300, 60], [300, 80]]
        self.perspective = "vertical"
        self.horizontal_middle_statement = "first_middle"

    def rotate_to_horizontal(self):
        y = self.current_coords[-1][1]  # This is the most down positioned pixel
        x = self.current_coords[-1][0] - 40  # This is the most left x after rotation
        new_coords = []
        for _ in range(len(self)):
            new_coords.append([x, y])
            x += 20

        self.current_coords = new_coords
        self.perspective = "horizontal"

    def rotate_to_vertical(self):
        x, y = int(), int()
        if self.horizontal_middle_statement == "first_middle":
            x = self.current_coords[1][0]
            y = self.current_coords[0][1] + 40  # This is the most down positioned pixel after rotation
            self.horizontal_middle_statement = "second_middle"
        elif self.horizontal_middle_statement == "second_middle":
            x = self.current_coords[2][0]
            y = self.current_coords[0][1] + 60  # This is the most down positioned pixel after rotation

        new_coords = []
        for _ in range(len(self)):
            new_coords.append([x, y])
            y -= 20

        self.current_coords = new_coords
        self.perspective = "vertical"


class TTetrimino(Tetrimino):

    def __init__(self, game_window):
        super().__init__(game_window)
        # starting coords defined below
        self.current_coords = [[260, 40], [280, 40], [300, 40], [280, 60]]





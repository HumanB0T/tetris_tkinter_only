import random

# Settings
PIXEL_SIZE = 20               # Do not change it
SIDE_WAYS_HOW_MANY_TIMES = 4  # How many times you can move tetrimino in sideways before it move down
SPEED = 150                   # In milliseconds. The higher the amount the move is slower


class Tetrimino:
    collided_area = []

    def __init__(self, game_window):
        self.game_window = game_window
        self.current_coords = []
        self.moving_sideways_counter = 0
        self.perspective = ""
        self.horizontal_middle_statement = ""
        self.speed = SPEED
        self.is_accelerated_flag = False

    def __len__(self):
        return len(self.current_coords)

    def move_block(self, game_window):
        self.count_sideways_moving(game_window)

        if not self.is_accelerated_flag:
            if game_window.direction == "Down":
                self.is_accelerated_flag = True
                self.speed = 20

        if game_window.direction == "moving_down":
            self.current_coords = list(map(lambda xy: (xy[0], xy[1] + PIXEL_SIZE), self.current_coords))

        if self.check_if_move_left_is_possible():
            if game_window.direction == "Left":
                self.current_coords = self.move_left()

        if self.check_if_move_right_is_possible():
            if game_window.direction == "Right":
                self.current_coords = self.move_right()

        game_window.create_graphics(self.current_coords)
        game_window.direction = "moving_down"
        game_window.after(self.speed, game_window.perform_actions)

    def move_left(self):
        return list(map(lambda xy: (xy[0] - PIXEL_SIZE, xy[1]), self.current_coords))

    def move_right(self):
        return list(map(lambda xy: (xy[0] + PIXEL_SIZE, xy[1]), self.current_coords))

    def count_sideways_moving(self, game_window):
        if game_window.direction in ("Left", "Right", "Up"):
            self.moving_sideways_counter += 1

        if self.moving_sideways_counter > SIDE_WAYS_HOW_MANY_TIMES:
            self.moving_sideways_counter = 0
            game_window.direction = "moving_down"

    def check_if_move_left_is_possible(self):
        if self.get_most_left_x() > 40:
            coords_after_move_left = self.move_left()
            for coord in coords_after_move_left:
                if coord in Tetrimino.collided_area:
                    return False

            return True

    def check_if_move_right_is_possible(self):
        if self.get_most_right_x() < 580:
            coords_after_move_right = self.move_right()
            for coord in coords_after_move_right:
                if coord in Tetrimino.collided_area:
                    return False

            return True

    def rotate_to_horizontal(self):
        pass

    def rotate_to_vertical(self):
        pass

    def get_most_left_x(self):
        return min([item[0] for item in self.current_coords])

    def get_most_right_x(self):
        return max([item[0] for item in self.current_coords])

    def get_most_down_y(self):
        return max([item[1] for item in self.current_coords])

    def get_most_high_y(self):
        return min([item[1] for item in self.current_coords])

    def get_current_coords_but_all_y_highered_by_pixel_size(self):
        return list(map(lambda xy: (xy[0], xy[1]+PIXEL_SIZE), self.current_coords))

    def check_collision(self):
        if self.get_most_down_y() == 780:
            return True

        coords_to_check_collision = self.get_current_coords_but_all_y_highered_by_pixel_size()
        for coord in coords_to_check_collision:
            if coord in Tetrimino.collided_area:
                return True

    def clear_floor(self):
        y = self.get_most_down_y()
        existing_y_floor_coords = [coord for coord in Tetrimino.collided_area if coord[1] == y]
        if len(existing_y_floor_coords) >= 28:
            collided_area = set(Tetrimino.collided_area)
            existing_y_floor_coords = set(existing_y_floor_coords)
            new_floors = list(collided_area ^ existing_y_floor_coords)
            Tetrimino.collided_area = [(coord[0], coord[1]) if coord[1] > y
                                           else (coord[0], coord[1]+20)
                                           for coord in new_floors]

    @staticmethod
    def check_if_lost():
        if len(Tetrimino.collided_area):
            if min([coord[1] for coord in Tetrimino.collided_area]) <= 100:
                return True

    @staticmethod
    def generate_random_tetrimino(game_window):
        chosen_tetrimino = random.choice([L1Tetrimino])
        return chosen_tetrimino(game_window)


class ITetrimino(Tetrimino):

    def __init__(self, game_window):
        super().__init__(game_window)
        # starting coords defined below
        self.current_coords = [[300, 20], [300, 40], [300, 60], [300, 80]]
        self.perspective = "vertical"
        self.horizontal_middle_statement = "first_middle"

    def move_block(self, game_window):
        if game_window.direction == "Up":
            if self.perspective == "vertical":
                self.rotate_to_horizontal()
            else:
                self.rotate_to_vertical()
        super().move_block(game_window)

    def rotate_to_horizontal(self):
        y = self.current_coords[-1][1]  # This is the most down positioned pixel
        x = self.current_coords[-1][0] - 40  # This is the most left x after rotation
        new_coords = []
        for _ in range(len(self)):
            new_coords.append([x, y])
            x += 20

        new_most_left_x = min([x_coord[0] for x_coord in new_coords])
        new_most_right_x = max([x_coord[0] for x_coord in new_coords])

        if new_most_left_x >= 30 and new_most_right_x <= 590:
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
        self.current_coords = [[280, 40], [300, 40], [320, 40], [300, 20]]
        self.rotation_state = "First"

    def move_block(self, game_window):
        if game_window.direction == "Up":
            if self.rotation_state == "First":
                self.current_coords[0] = [self.current_coords[0][0] + 20, self.current_coords[0][1] + 20]
                self.rotation_state = "Second"
            elif self.rotation_state == "Second":
                self.current_coords[3] = [self.current_coords[3][0] - 20, self.current_coords[3][1] + 20]
                self.rotation_state = "Third"
            elif self.rotation_state == "Third":
                self.current_coords[2] = [self.current_coords[2][0] - 20, self.current_coords[2][1] - 20]
                self.rotation_state = "Fourth"
            elif self.rotation_state == "Fourth":
                self.current_coords[0] = self.current_coords[3]
                self.current_coords[3] = self.current_coords[2]
                self.current_coords[2] = [self.current_coords[2][0] + 20, self.current_coords[2][1] + 20]
                self.rotation_state = "First"

        super().move_block(game_window)


class L1Tetrimino(Tetrimino):

    def __init__(self, game_window):
        super().__init__(game_window)
        self.current_coords = [[280, 40], [300, 40], [320, 40], [320, 60]]
        self.rotation_state = "First"
        self.if_rotated_previously_flag = False

    def move_block(self, game_window):
        if game_window.direction == "Up":
            if self.rotation_state == "First":
                self.current_coords[0] = [self.current_coords[0][0], self.current_coords[0][1] + 20]
                self.current_coords[2] = [self.current_coords[2][0] - 20, self.current_coords[2][1] - 20]
                self.current_coords[3] = [self.current_coords[3][0] - 20, self.current_coords[3][1]]
                self.rotation_state = "Second"
            elif self.rotation_state == "Second":
                self.current_coords[0] = [self.current_coords[0][0], self.current_coords[0][1] - 40]
                self.current_coords[2] = [self.current_coords[2][0] - 20, self.current_coords[2][1] + 20]
                self.current_coords[3] = [self.current_coords[3][0] + 20, self.current_coords[3][1] - 20]
                self.rotation_state = "Third"
            elif self.rotation_state == "Third":
                self.current_coords[0] = [self.current_coords[0][0] + 20, self.current_coords[0][1] + 40]
                self.current_coords[2] = [self.current_coords[2][0] + 20, self.current_coords[2][1] - 20]
                self.current_coords[3] = [self.current_coords[3][0], self.current_coords[3][1] - 20]
                self.rotation_state = "Fourth"
            elif self.rotation_state == "Fourth":
                # I finished here
                pass
                self.rotation_state = "First"

        super().move_block(game_window)















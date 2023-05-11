import tkinter as tk
from PIL import Image, ImageTk
from tetris_classes.Tetriminos import Tetrimino


class Tetris(tk.Canvas):

    def __init__(self):
        super().__init__(width=620, height=820, background="black", highlightthickness=0)

        self.create_rectangle(30, 30, 590, 790, outline="yellow")
        self.current_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.bind_all("<Key>", self.on_key_press)
        self.direction = "moving_down"
        self.perform_actions()

    def perform_actions(self):
        if Tetrimino.check_if_lost():
            self.create_text(self.winfo_width() / 2,
                             self.winfo_height() / 2,
                             text=f"LOST",
                             font=("Courier 38", 30),
                             fill="red")
            return 0
        if self.current_tetrimino.check_collision():
            for xy in self.current_tetrimino.current_coords:
                Tetrimino.collided_area.append(xy)
                self.current_tetrimino.clear_floor()
            self.current_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.current_tetrimino.move_block(self)

    def create_graphics(self, coords):
        tetris_brick = Image.open("graphics/tetrimino_pixel.png")
        self.image = ImageTk.PhotoImage(tetris_brick)
        for position in Tetrimino.collided_area:
            self.create_image(*position, image=self.image)
        for position in coords:
            self.create_image(*position, image=self.image)

    def on_key_press(self, e):
        pressed_key = e.keysym
        # The instruction below is made to prevent speeding up the block after it collides with terrain.
        # User may still be holding "Down" key and the block will speed up from the highest position.
        # This is to prevent these situations.
        if self.current_tetrimino.get_most_high_y() < 60:
            possible_directions = ("Left", "Right", "Up")
        elif not self.current_tetrimino.is_accelerated_flag:
            possible_directions = ("Left", "Right", "Up", "Down")
        else:
            possible_directions = ("Left", "Right", "Up")
        if pressed_key in possible_directions:
            self.direction = pressed_key







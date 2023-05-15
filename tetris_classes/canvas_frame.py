import tkinter as tk
from PIL import Image, ImageTk
from tetris_classes.Tetriminos import Tetrimino, RockTetrimino


class Tetris(tk.Canvas):

    def __init__(self):
        super().__init__(width=720, height=820, background="black", highlightthickness=0)

        self.create_rectangle(30, 30, 590, 790, outline="yellow")
        self.current_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.next_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.bind_all("<Key>", self.on_key_press)
        self.direction = "moving_down"
        self.block_image = None
        self.next_block_image = None
        self.terrain_image = None
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
            self.current_tetrimino = self.next_tetrimino
            self.next_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.current_tetrimino.move_block(self)

    def create_graphics(self, coords):
        self.block_image = ImageTk.PhotoImage(self.current_tetrimino.image)
        self.terrain_image = ImageTk.PhotoImage(Tetrimino.terrain)
        for position in Tetrimino.collided_area:
            self.create_image(*position, image=self.terrain_image)

        for position in coords:
            self.create_image(*position, image=self.block_image)

        self.show_next_tetrimino()

    def show_next_tetrimino(self):
        self.next_block_image = ImageTk.PhotoImage(self.next_tetrimino.image)
        self.create_text(655,
                         50,
                         text=f"Next:",
                         font=("Courier 38", 30),
                         fill="white")

        for position in self.next_tetrimino.next_display_coords:
            self.create_image(*position, image=self.next_block_image)

    def on_key_press(self, e):
        pressed_key = e.keysym

        if pressed_key in self.current_tetrimino.possible_directions:
            self.direction = pressed_key

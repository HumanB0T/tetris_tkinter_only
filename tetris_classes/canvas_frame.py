import tkinter as tk
from PIL import Image, ImageTk
from tetris_classes.tetrimino_classes import Tetrimino, ITetrimino




class Tetris(tk.Canvas):

    def __init__(self):
        super().__init__(width=620, height=820, background="black", highlightthickness=0)

        self.create_rectangle(30, 30, 590, 790, outline="yellow")
        self.current_tetrimino = Tetrimino.generate_random_tetrimino(self)
        self.bind_all("<Key>", self.on_key_press)
        self.direction = "Down"
        self.perform_actions()

    def perform_actions(self):
        print(self.current_tetrimino.get_most_left_x())
        self.current_tetrimino.move(self)

    def create_graphics(self, coords):
        tetris_brick = Image.open("graphics/tetrimino_pixel.png")
        self.image = ImageTk.PhotoImage(tetris_brick)
        for position in coords:
            self.create_image(*position, image=self.image)

    def on_key_press(self, e):
        pressed_key = e.keysym
        possible_directions = ("Left", "Right", "Up")
        if pressed_key in possible_directions:
            self.direction = pressed_key





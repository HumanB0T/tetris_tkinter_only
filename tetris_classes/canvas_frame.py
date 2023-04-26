import tkinter as tk
from PIL import Image, ImageTk
from tetris_classes.tetrimino_classes import Tetrimino, ITetrimino

TETRIS_BRICK = Image.open("graphics/tetrimino_pixel.png")


class Tetris(tk.Canvas):

    def __init__(self):
        super().__init__(width=620, height=820, background="black", highlightthickness=0)

        self.create_rectangle(30, 30, 590, 790, outline="yellow")
        self.tetrimino = ITetrimino([[240, 20], [240, 40], [240, 60], [240, 80]], self)
        self.perform_actions()

    def perform_actions(self):
        self.create_graphics(self.tetrimino.coords)
        self.tetrimino.move_down()
        self.after(300, self.perform_actions)

    def create_graphics(self, coords):
        self.image = ImageTk.PhotoImage(TETRIS_BRICK)
        for position in coords:
            self.create_image(*position, image=self.image)




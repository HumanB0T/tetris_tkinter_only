import tkinter as tk
from tetris_classes.canvas_frame import Tetris


root = tk.Tk()

root.title("Tetris v1.0 by HumanB0t")
root.geometry("720x820")
tetris = Tetris()
tetris.pack()

root.mainloop()


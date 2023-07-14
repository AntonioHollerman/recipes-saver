from holding_functions import *
import tkinter as tk
from tkinter import ttk


class RecipesWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.home_frame = HomeFrame(self)
        self.edit_frame = EditFrame(self)

    def run(self):
        self.mainloop()

    def swap_frame(self):
        pass


class HomeFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow):
        super().__init__(master)
        self.master = master


class EditFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow):
        super().__init__(master)
        self.master = master

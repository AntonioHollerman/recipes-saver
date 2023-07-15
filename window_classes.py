from holding_functions import *
import tkinter as tk
from tkinter import ttk
from random import choice
from typing import List, Dict


class RecipesWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        holding_recipes: List[recipe_row] = all_saved_recipes()
        self.recipes: Dict[int: recipe_row] = {}
        for recipe in holding_recipes:
            self.recipes[recipe.recipe_id] = recipe
        if holding_recipes:
            self.current_recipe = choice(holding_recipes)
        else:
            self.current_recipe = None

        self.home_frame = HomeFrame(self, self.current_recipe)
        self.edit_frame = EditFrame(self, self.current_recipe)
        self.current_window = 'Home Frame'

    def run(self):
        self.mainloop()

    def swap_frame(self):
        pass


class HomeFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row | None):
        super().__init__(master)
        self.master_win = master
        self.current_recipe_frame = CurrentRecipeFrame(self, recipe)
        self.current_recipe = recipe

    def next_recipe(self):
        available_ids = list(filter(next_id_filter(self.current_recipe.recipe_id), self.master_win.recipes.keys()))
        available_ids.sort()
        if available_ids:
            new_current_recipe = self.master_win.recipes[available_ids[0]]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe
        else:
            self.current_recipe = None
            self.master_win.current_recipe = None

    def previous_recipe(self):
        available_ids = list(filter(previous_id_filter(self.current_recipe.recipe_id), self.master_win.recipes.keys()))
        available_ids.sort(reverse=True)
        if available_ids:
            new_current_recipe = self.master_win.recipes[available_ids[0]]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe


class CurrentRecipeFrame(ttk.Frame):
    def __init__(self, master: HomeFrame, recipe: recipe_row | None):
        super().__init__(master)
        self.edit_frame = master
        if recipe is not None:
            self.recipe_info = recipe
        else:
            self.recipe_info = recipe_row(-1, 'New Recipe', ['Edit Ingredients'], 'None', 'Add Description', 'None',
                                          'None')


class EditFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.recipe_info = recipe

    def save_recipe(self):
        if self.recipe_info.recipe_id == -1:
            add_recipe(*self.recipe_info[1:])
            self.master_win.recipes[self.recipe_info.recipe_id] = self.recipe_info
        else:
            update_recipe(*self.recipe_info)

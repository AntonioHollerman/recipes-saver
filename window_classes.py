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

    def random_recipe(self):
        available_ids = list(self.master_win.recipes.keys())
        available_ids.remove(self.current_recipe.recipe_id)
        if available_ids:
            new_current_recipe = self.master_win.recipes[choice(available_ids)]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe

    def refresh_window(self):
        pass


class CurrentRecipeFrame(ttk.Frame):
    def __init__(self, master: HomeFrame, recipe: recipe_row | None):
        super().__init__(master)
        self.edit_frame = master
        if recipe is not None:
            self.recipe_info = recipe
        else:
            self.recipe_info = recipe_row(-1, 'Recipe Name Here', ['Edit Ingredients'], 'None', 'Add Description',
                                          'None', 'None')


class EditFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.recipe_info = recipe
        self.ingredients_frame = IngredientsListFrame(self)
        self.tk_website_link = tk.StringVar(self)
        self.tk_fileloc = tk.StringVar(self)
        if recipe.instructions_type == "web_link":
            self.tk_website_link.set(recipe.recipe_instructions)
        if recipe.instructions_type == "file_location":
            self.tk_fileloc.set(recipe.recipe_instructions)

        self.tk_recipe_instruc_type = tk.StringVar(self, value=recipe.instructions_type)
        self.weblink_radio = ttk.Radiobutton(self, value="web_link", variable=self.tk_recipe_instruc_type,
                                             text="Web site: ")
        self.fileloc_radio = ttk.Radiobutton(self, value="file_location", variable=self.tk_recipe_instruc_type,
                                             text="File Location: ")
        self.weblink_entry = ttk.Entry(self, textvariable=self.tk_website_link)
        self.fileloc_entry = ttk.Entry(self, textvariable=self.tk_fileloc)
        self.fileloc_button = ttk.Button(self, text="Select File", command=self.select_file)
        self.back_button = ttk.Button(self, text="<- Back", command=self.back_button_command)
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_button_command)

        self.tk_recipe_title = tk.StringVar(self, value=recipe.recipe_name)
        self.title_entry = ttk.Entry(self, textvariable=self.tk_recipe_title)
        self.desc_box = tk.Text(self, height=5)
        self.desc_box.insert("1.0", recipe.recipe_desc)

        self.weblink_radio.grid(row=1, column=0, sticky="e", padx=3, pady=3)
        self.fileloc_radio.grid(row=2, column=0, sticky="e", padx=3, pady=3)
        self.weblink_entry.grid(row=1, column=1, sticky="we", padx=3, pady=3)
        self.fileloc_entry.grid(row=2, column=1, sticky="we", padx=3, pady=3)
        self.fileloc_button.grid(row=3, column=1, sticky="n", padx=3, pady=3)
        self.back_button.grid(row=4, column=0, sticky="w", padx=3, pady=3)
        self.reset_button.grid(row=4, column=1, sticky="e", padx=3, pady=3)
        self.title_entry.grid(row=1, column=2, sticky="ew", padx=3, pady=3)
        self.desc_box.grid(row=3, column=2, rowspan=3, sticky="news", padx=3, pady=3)
        self.ingredients_frame.grid(row=0, column=2, sticky="nesw", padx=3, pady=3)

        if recipe.recipe_image != "None" and os.path.exists(recipe.recipe_image):
            try:
                self.display_image(True)
            except Exception as err:
                self.display_image(file_found=False)
                print(err)
        else:
            self.display_image(file_found=False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=8)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def save_recipe(self):
        id_ = self.recipe_info.recipe_id

        new_ingredient_list = []
        for index, row in enumerate(self.ingredients_frame.ingredients_row_widgets):
            ingredient: tk.StringVar = row[0]
            if index not in self.ingredients_frame.ignore:
                new_ingredient_list.append(ingredient.get())

        new_recipe = recipe_row(id_, name, new_ingredient_list, recipe_image, recipe_desc, recipe_instructions,
                                instructions_type)
        if new_recipe.recipe_id == -1:
            new_id = add_recipe(*self.recipe_info[1:])
            self.master_win.recipes[new_id] = new_recipe
            self.master_win.current_recipe = new_recipe
        else:
            update_recipe(*self.recipe_info)

    def back_button_command(self):
        pass

    def reset_button_command(self):
        pass

    def display_image(self, file_found):
        if file_found:
            ttk.Button(self, text="select image", command=self.select_image).grid(row=0, column=0, columnspan=2)
        else:
            ttk.Button(self, text="select image", command=self.select_image).grid(row=0, column=0, columnspan=2)

    def select_image(self):
        pass

    def select_file(self):
        pass


class IngredientsListFrame(ttk.Frame):
    def __init__(self, master: EditFrame):
        super().__init__(master)
        self.edit_frame = master
        self.ingredients_row_widgets: List[List[tk.StringVar | ttk.Entry | ttk.Button | ttk.Separator]] = []
        self.mini_frame = ttk.Frame(self)
        self.ignore = set()

        self.add_ingredient_button = ttk.Button(self, text="Add Ingredient", command=self.add_ingredient)
        ttk.Label(self, text="Ingredients", anchor="center").grid(row=0, column=1, columnspan=2, sticky="ew")

        self.mini_frame.columnconfigure(0, weight=5)
        self.mini_frame.columnconfigure(1, weight=2)
        for index, ingredient in enumerate(self.edit_frame.recipe_info.recipe_ingredients):
            self.ingredients_row_widgets.append([])
            self.ingredients_row_widgets[index].append(tk.StringVar(self.edit_frame.master_win, value=ingredient))
            ingredient_entry = ttk.Entry(self.mini_frame, textvariable=self.ingredients_row_widgets[index][0])
            self.ingredients_row_widgets[index].append(ingredient_entry)
            delete_button = ttk.Button(self.mini_frame, text="X", width=5, command=self.remove_ingredient(index))
            row_seperator = ttk.Separator(self.mini_frame)
            self.ingredients_row_widgets[index].append(delete_button)
            self.ingredients_row_widgets[index].append(row_seperator)

            next_row = index * 2
            ingredient_entry.grid(row=next_row, column=0, sticky="ew")
            delete_button.grid(row=next_row, column=1, sticky="w")
            row_seperator.grid(row=next_row+1, column=0, columnspan=2, sticky="ew")

            self.mini_frame.rowconfigure(next_row, weight=5)
            self.mini_frame.rowconfigure(next_row+1, weight=1)

        self.mini_frame.grid(row=1, column=0, columnspan=2, sticky="nesw")
        self.add_ingredient_button.grid(row=2, column=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=2)

    def add_ingredient(self):
        self.ingredients_row_widgets.append([])
        self.ingredients_row_widgets[-1].append(tk.StringVar(self.edit_frame.master_win))
        ingredient_entry = ttk.Entry(self.mini_frame, textvariable=self.ingredients_row_widgets[-1][0])
        self.ingredients_row_widgets[-1].append(ingredient_entry)
        delete_button = ttk.Button(self.mini_frame, text="X", width=5,
                                   command=self.remove_ingredient(len(self.ingredients_row_widgets) - 1))
        row_seperator = ttk.Separator(self.mini_frame)
        self.ingredients_row_widgets[-1].append(delete_button)
        self.ingredients_row_widgets[-1].append(row_seperator)

        next_row = len(self.ingredients_row_widgets) * 2
        ingredient_entry.grid(row=next_row, column=0, sticky="ew")
        delete_button.grid(row=next_row, column=1, sticky="w")
        row_seperator.grid(row=next_row + 1, column=0, columnspan=2, sticky="ew")

        self.mini_frame.rowconfigure(next_row, weight=5)
        self.mini_frame.rowconfigure(next_row + 1, weight=1)

    def remove_ingredient(self, index):
        def to_return():
            for widget in self.ingredients_row_widgets[index]:
                try:
                    widget.destroy()
                except AttributeError:
                    pass
                self.ignore.add(index)
        return to_return


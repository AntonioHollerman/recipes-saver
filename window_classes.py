from holding_functions import *
import tkinter as tk
from tkinter import ttk, filedialog
from random import choice
from typing import List, Dict
from PIL import Image, ImageTk


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

        # self.home_frame = HomeFrame(self, self.current_recipe)
        # self.edit_frame = EditFrame(self, self.current_recipe)
        # self.current_window = 'Home Frame'

    def run(self):
        self.mainloop()

    def swap_frame(self):
        pass


class HomeFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.current_recipe_frame = CurrentRecipeFrame(self, recipe)
        self.current_recipe = recipe

        self.random_button = ttk.Button(self, text="Random", command=self.random_recipe)
        self.next_button = ttk.Button(self, text="-->", command=self.next_recipe)
        self.back_button = ttk.Button(self, text="<--", command=self.previous_recipe)
        self.edit_button = ttk.Button(self, text="Edit")
        self.crate_button = ttk.Button(self, text="Add New Recipe")

        ttk.Label(self, text="Your recipes are below", justify="center", anchor="center").grid(row=0,
                                                                                               column=1, sticky="ew")
        ttk.Separator(self).grid(row=1, column=0, columnspan=3, sticky="ew")
        self.random_button.grid(row=2, column=1)
        self.back_button.grid(row=3, column=0, sticky="w")
        self.next_button.grid(row=3, column=2, sticky="e")
        self.edit_button.grid(row=4, column=0, sticky="w")
        self.crate_button.grid(row=4, column=2, sticky="e")
        self.current_recipe_frame.grid(row=3, column=1, sticky="nesw")

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=9)
        self.rowconfigure(4, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

    def next_recipe(self):
        available_ids = list(filter(next_id_filter(self.current_recipe.recipe_id), self.master_win.recipes.keys()))
        available_ids.sort()
        if available_ids:
            new_current_recipe = self.master_win.recipes[available_ids[0]]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe

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

    def create_recipe(self):
        new_id = add_recipe('Recipe Name Here', ['Edit Ingredients'], 'None', 'Add Description', 'None', 'None')
        self.current_recipe = recipe_row(new_id, 'Recipe Name Here', ['Edit Ingredients'], 'None', 'Add Description',
                                         'None', 'None')
        self.master_win.current_recipe = self.current_recipe
        self.master_win.recipes[new_id] = self.current_recipe


class CurrentRecipeFrame(ttk.Frame):
    def __init__(self, master: HomeFrame, recipe: recipe_row):
        super().__init__(master)
        self.home_frame = master
        self.recipe_info = recipe_row
        self.tk_widgets: List[ttk.Separator | ttk.Button | ttk.Label] = []
        self.recipe_photo = None
        self.new_image = None

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=8)
        self.rowconfigure(2, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.refresh(recipe)

    def refresh(self, recipe: recipe_row):
        if self.tk_widgets:
            for widget in self.tk_widgets:
                widget.destroy()
            self.tk_widgets = []
        self.recipe_info = recipe

        recipe_title = ttk.Label(self, text=recipe.recipe_name, anchor="center", justify="center")
        ingredients_label = ttk.Label(self, text="Ingredients", anchor="center", justify="center")
        line_seperator = ttk.Separator(self)
        ingredients_list_box = tk.Listbox(self, height=len(recipe.recipe_ingredients))
        open_instruction_button = ttk.Button(self, text="Open: ")
        instructions_location_label = ttk.Label(self, text=recipe.recipe_instructions, anchor="e", justify="left")
        for ingredient in recipe.recipe_ingredients:
            ingredients_list_box.insert(tk.END, ingredient)
        ingredients_list_box["state"] = "disabled"

        recipe_title.grid(row=0, column=0, sticky="ew")
        ingredients_label.grid(row=0, column=1, sticky="ew")
        ingredients_list_box.grid(row=1, column=1, sticky="nesw")
        open_instruction_button.grid(row=2, column=0, sticky="e")
        instructions_location_label.grid(row=2, column=1, sticky="ew")

        self.tk_widgets.append(recipe_title)
        self.tk_widgets.append(ingredients_label)
        self.tk_widgets.append(ingredients_list_box)
        self.tk_widgets.append(line_seperator)
        self.tk_widgets.append(open_instruction_button)
        self.tk_widgets.append(instructions_location_label)

        if recipe.recipe_image != "None" and os.path.exists(recipe.recipe_image):
            try:
                self.display_image(True, recipe.recipe_image)
            except Exception as err:
                self.display_image(False)
                print(err)
        else:
            self.display_image(False)

    def display_image(self, file_found, recipe_path=None):
        if file_found:
            recipe_image = Image.open(recipe_path)
            self.recipe_photo = ImageTk.PhotoImage(recipe_image)
            recipe_label = ttk.Label(self, image=self.recipe_photo)
            recipe_label.grid(row=1, column=0)
            self.tk_widgets.append(recipe_label)
        else:
            image_button = ttk.Button(self, text="select image", command=self.select_image)
            image_button.grid(row=1, column=0)
            self.tk_widgets.append(image_button)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        try:
            self.display_image(True, image_path)
            self.new_image = image_path
        except Exception as err:
            print(err)


class EditFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.recipe_info = recipe
        self.ingredients_frame = IngredientsListFrame(self)
        self.tk_website_link = tk.StringVar(self)
        self.tk_fileloc = tk.StringVar(self)
        self.new_image = None
        self.recipe_photo = None

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
                self.display_image(True, recipe.recipe_image)
            except Exception as err:
                self.display_image(False)
                print(err)
        else:
            self.display_image(False)

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
        self.master_win.recipes[id_] = new_recipe
        if id_ in self.master_win.recipes:
            pass
        else:
            pass

    def back_button_command(self):
        pass

    def reset_button_command(self):
        pass

    def display_image(self, file_found, recipe_path=None):
        if file_found:
            recipe_image = Image.open(recipe_path)
            self.recipe_photo = ImageTk.PhotoImage(recipe_image)
            recipe_label = ttk.Label(self, image=self.recipe_photo)
            recipe_label.grid(row=0, column=0, columnspan=2)
        else:
            image_button = ttk.Button(self, text="select image", command=self.select_image)
            image_button.grid(row=0, column=0, columnspan=2)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        try:
            self.display_image(True, image_path)
            self.new_image = image_path
        except Exception as err:
            print(err)

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


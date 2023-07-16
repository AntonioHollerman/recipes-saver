import sqlite3
import os
import webbrowser
from collections import namedtuple

db_conn = sqlite3.connect('recipes_info.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
db_cur = db_conn.cursor()

recipe_row = namedtuple('recipe_row', ['recipe_id', 'recipe_name', 'recipe_ingredients', 'recipe_image',
                                       'recipe_desc', 'recipe_instructions', 'instructions_type'])

try:
    db_cur.execute("""CREATE TABLE recipes(
recipe_id SERIAL PRIMARY KEY,
recipe_name TEXT,
recipe_ingredients TEXT,
recipe_image TEXT,
recipe_desc TEXT,
recipe_instructions TEXT,
instructions_type TEXT
)""")
except sqlite3.OperationalError:
    db_cur.execute("SELECT recipe_id FROM recipes ORDER BY recipe_id DESC LIMIT 1")
    current_data = db_cur.fetchall()
    if not current_data:
        next_recipe_id = 0
    else:
        next_recipe_id = int(current_data[0][0]) + 1
else:
    next_recipe_id = 0


def add_recipe(name, ingredients: list | tuple, image_path, desc, instructions, instruction_type):
    """
    Inserts values into the sqlite database
    :param name: The name of the recipe
    :param ingredients: The ingredients for the recipe
    :param image_path: File path to the image
    :param desc: The description of the meal
    :param instructions: The web link or file for the instructions of the recipe
    :param instruction_type: Informs if the instructions are a web link or a file
    :return: newest recipe id
    """
    ingredients = "-(.o)0)0_-23".join(ingredients)
    global next_recipe_id
    db_cur.execute("INSERT INTO recipes "
                   "(recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, "
                   "recipe_instructions, instructions_type) "
                   "VALUES "
                   f"({next_recipe_id}, '{name}', '{ingredients}', '{image_path}', '{desc}', '{instructions}', "
                   f"'{instruction_type}')")
    next_recipe_id += 1
    return next_recipe_id - 1


def remove_recipe(recipe_id: int):
    """
    Removes a recipe from the database
    :param recipe_id: The id for the recipe that wants to be deleted
    :return: None
    """
    db_cur.execute("DELETE FROM recipes "
                   f"WHERE recipe_id = {recipe_id}")


def open_instructions(recipe_id: int):
    """
    Execute a file or open the browser of the wanted recipe
    :param recipe_id: The id for the recipe that wants to be deleted
    :return: None
    """
    db_cur.execute(f"SELECT recipe_instructions, instructions_type FROM recipes WHERE recipe_id = {recipe_id}")
    recipe_instructions, instructions_type = db_cur.fetchone()
    if instructions_type == "web_link":
        webbrowser.open(recipe_instructions)
        return True
    elif instructions_type == "file_location":
        found_path = os.path.exists(recipe_instructions)
        if found_path:
            os.system(f"start {recipe_instructions}")
            return True
        else:
            return False
    else:
        return False


def all_saved_recipes():
    """
    Returns every row
    :return: A list of rows that is a tuple that contains (recipe_id, recipe_name, recipe_ingredients, recipe_image,
    recipe_desc, recipe_instructions, instructions_type)
    """
    db_cur.execute("SELECT recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, recipe_instructions, "
                   "instructions_type FROM recipes ORDER BY recipe_id")
    data = db_cur.fetchall()
    to_return = []
    for row in data:
        recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, recipe_instructions, \
            instructions_type = row
        recipe_ingredients = recipe_ingredients.split("-(.o)0)0_-23")
        to_return.append(recipe_row(recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc,
                                    recipe_instructions, instructions_type))
    return to_return


def get_recipe(recipe_id: int):
    """
    Returns one row
    :param recipe_id: The id of the recipe wanted
    :return: The row is a tuple that contains (recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc,
    recipe_instructions, instructions_type)
    """
    db_cur.execute("SELECT recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, recipe_instructions, "
                   f"instructions_type FROM recipes WHERE recipe_id = {recipe_id}")
    recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, recipe_instructions, instructions_type = \
        db_cur.fetchone()
    recipe_ingredients = recipe_ingredients.split("-(.o)0)0_-23")
    return recipe_row(recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, recipe_instructions,
                      instructions_type)


def update_recipe(recipe_id, name, ingredients: list | tuple, image_path, desc, instructions, instruction_type):
    ingredients = "-(.o)0)0_-23".join(ingredients)
    db_cur.execute("UPDATE recipes SET"
                   f"recipe_name = '{name}', recipe_ingredients = '{ingredients}', recipe_image = '{image_path}', "
                   f"recipe_desc = '{desc}', recipe_instructions = '{instructions}', "
                   f"instructions_type = '{instruction_type}' "
                   f"WHERE recipe_id = {recipe_id}")


def next_id_filter(current_id):
    def to_return(working_id):
        return working_id > current_id
    return to_return


def previous_id_filter(current_id):
    def to_return(working_id):
        return working_id < current_id
    return to_return

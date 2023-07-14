import sqlite3

db_conn = sqlite3.connect('recipes_info.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
db_cur = db_conn.cursor()

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
    :param desc:
    :param instructions:
    :param instruction_type:
    :return: None
    """
    global next_recipe_id
    db_cur.execute("INSERT INTO recipes "
                   "(recipe_id, recipe_name, recipe_ingredients, recipe_image, recipe_desc, "
                   "recipe_instructions, instructions_type) "
                   "VALUES "
                   f"({next_recipe_id}, '{name}', '{ingredients}', '{image_path}', '{desc}', '{instructions}', "
                   f"'{instruction_type}')")
    next_recipe_id += 1


def remove_recipe(recipe_id):
    db_cur.execute("DELETE FROM recipes "
                   f"WHERE recipe_id = {recipe_id}")

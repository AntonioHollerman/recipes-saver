from window_classes import *

main_window = RecipesWindow()
main_window.mainloop()

if main_window.current_window == 'Edit Frame':
    main_window.current_window.save_recipe()

all_ids = get_ids()
for recipe_id, recipe in main_window.recipes.items():
    if recipe_id in all_ids:
        update_recipe(recipe)
    else:
        add_recipe(*recipe[1:])

for recipe_id in all_ids:
    if recipe_id not in main_window.recipes:
        remove_recipe(recipe_id)

db_conn.commit()
db_cur.close()

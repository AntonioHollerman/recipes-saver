from window_classes import *

main_window = RecipesWindow()
main_window.run()

if main_window.current_window == 'Edit Frame':
    main_window.edit_frame.save_recipe()

db_conn.commit()
db_cur.close()

from window_classes import *

main_window = RecipesWindow()
main_window.run()

db_conn.commit()
db_cur.close()

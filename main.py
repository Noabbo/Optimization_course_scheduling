import gui
import error_handler
user_args = gui.welcome_page()
error_msg = error_handler.check_args(user_args)
if error_msg != "":
    gui.print_error(error_msg)
else:
    
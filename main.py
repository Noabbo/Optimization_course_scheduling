import gui
import error_handler
import client
user_args = gui.welcome_page()
error_handler = ErrorHandler()
status,data = error_handler.args_controller(user_args)
if status == 0 :
    exit(status)
else:
    client = Client(data[0],data[1],data[2],data[3])
    gui.print_title("Pulling data from database ...")
    gui.print_title("Working ...")
    gui.print_schedule()
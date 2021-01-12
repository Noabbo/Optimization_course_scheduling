import gui
import error_handler
user_args = gui.welcome_page()
arg_check_response = error_handler.check_args(user_args)
err_msg = arg_check_response[0]
err_codes = arg_check_response[1]
while err_msg != "":
    gui.print_error(err_msg)
    gui.print_title("Would you like to fix issues ? y/n")
    command = input(">>>").lower()
    if command != "n":
        user_args = error_handler.fix_args(user_args,err_codes)
        arg_check_response = error_handler.check_args(user_args)
        err_msg = arg_check_response[0]
        err_codes = arg_check_response[1]
    else:
        gui.print_title("Shuting down system")
        exit(0)
gui.print_title("Pulling data from database ...")
gui.print_title("Working ...")
gui.print_schedule()
import gui
import error_handler
import client
import data as local_data
import db_controller
import admin
import user
user_args = gui.welcome_page()
if user_args != "admin":
    error_handler = error_handler.ErrorHandler()
    status,data = error_handler.args_controller(user_args)
    if status == 0 :
        exit(status)
    else:
        client = client.Client(data[0],data[1],data[2],data[3])
        db_controller = db_controller.DataBaseController()
        user.User(client,db_controller).run()
else:
    client = client.Client(0,[],[],[])
    db_controller = db_controller.DataBaseController()
    admin.Admin(client,db_controller).run()
import gui
import data
class Admin:
    def __init__(self,db_controller):
        self.db_controller = db_controller
        gui.print_title("Hello Admin!")
    
    def run(self):
        run = True
        while run:
            command = None
            gui.admin_page()
            try:
                command = int(input(">>>"))
            except Exception:
                gui.print_error("Bad command")
            if command == 1: 
                self.db_controller.auto_insert()
                print("DataBase Ready")
            if command == 2: 
                self.db_controller.clear()
                print("DataBase Cleared")
            if command == 3: run = False
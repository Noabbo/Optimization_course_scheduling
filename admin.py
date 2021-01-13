import gui
class Admin:
    def __init__(self,client,db_controller):
        self.client = client
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
            if command == 1: self.auto_insert()
            if command == 2: self.find()
            if command == 3: self.clear()
            if command == 4: run = False

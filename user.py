class User():
    def __init__(self,db_controller):
        self.db_controller = db_controller
    
    def run(self):
        print("user run")
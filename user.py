class User():
    def __init__(self,client,db_controller):
        self.client = client
        self.db_controller = db_controller
    
    def run(self):
        print("user run")
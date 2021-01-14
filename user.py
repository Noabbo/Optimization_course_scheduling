class User():
    def __init__(self,appData):
        self.appData = appData
    
    def run(self):
        self.appData.db_controller.pull(self.appData)
        print(self.appData.local)
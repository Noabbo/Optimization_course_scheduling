import course
class User():
    def __init__(self,appData):
        self.appData = appData
    
    def run(self):
        self.preprocess()
           
    def preprocess(self):
        self.appData.db_controller.pull(self.appData)
        local = []
        year = self.appData.user_args[0]
        redo_courses = self.appData.user_args[1]
        optional_courses = self.appData.user_args[2]
        unavailable = self.appData.user_args[3]
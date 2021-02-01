import pymongo as mongo_client
import gui
class DataBaseController:
    def __init__(self):
        self.cluster = mongo_client.MongoClient("mongodb+srv://allen_bronshtein:_123456@optimization-project-cl.zpogl.mongodb.net/Optimization-DB?retryWrites=true&w=majority")
        self.db = self.cluster["Optimization-DB"]
        self.collection = self.db["Courses"]
    
    def auto_insert(self,appData):
        items = appData.auto_generate_courses()
        try:
            self.collection.insert_many(items)
        except Exception:
            gui.print_error("Something went wrong while inserting to DB")

    def clear(self):
        try:
            self.collection.delete_many({})
        except Exception:
            gui.print_error("Something went wrong while clearing DB")

    def pull(self,appData):
        try:
            appData.local = self.collection.find({})
        except Exception:
            gui.print_error("Something went wrong while pulling from DB")
    
    def find(self,appData,value):
        try:
            appData.buffer = self.collection.find(value)
        except Exception:
            gui.print_error("Something went wrong while searching in DB")
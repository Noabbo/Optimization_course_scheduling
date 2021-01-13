import mongo_client
class DataBaseController:
    def __init__(self):
        self.cluster = mongo_client.MongoClient("mongodb+srv://allen_bronshtein:_123456@optimization-project-cl.zpogl.mongodb.net/Optimization-DB?retryWrites=true&w=majority")
        self.db = self.cluster["Optimization-DB"]
        self.collection = self.db["Courses"]
    def clear(self):
        print("unimplemented clearing db ...")

    def insert(self):
        print("unimplemented inserting to db ...")

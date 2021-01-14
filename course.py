class Course:
    def __init__(self,document):
        self.number = document["_id"]
        self.name = document["name"]
        self.year = document["year"]
        self.is_must = document["is_must"]
        self.groups = document["groups"]
        # continue here
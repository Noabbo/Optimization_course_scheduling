import schedule
class Course:
    def __init__(self,document):
        self.number = document["_id"]
        self.name = document["name"]
        self.year = document["year"]
        self.is_must = document["is_must"]
        self.groups = document["groups"]
        self.prior = document["pre-courses"]
        self.rating = self.get_rating(document)
        self.duration = self.get_duration()
    
    def __eq__(self, other):
        return self.number == other.number
    
    def get_duration(self):
        day_time = schedule.format_day_time(str(self.groups[0]))
        return day_time[2]-day_time[1]
    
    def get_rating(self,document):
        if "rating" in document:
            return document["rating"]
        else:
            return None
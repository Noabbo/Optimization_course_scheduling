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
    def __lt__(self, other):
        return self.number < other.number
    def __gt__(self,other):
        return self.number > other.number
    def __le__(self,other):
        return self.number<=other.number
    def __ge__(self,other):
        return self.number>=other.number
    def __ne__(self,other):
        return self.number != other.number
    
    
    def get_duration(self):
        day_time = schedule.format_day_time(str(self.groups[0]))
        return day_time[2]-day_time[1]
    
    def get_rating(self,document):
        if "rating" in document:
            return document["rating"]
        else:
            return None
    
    def remove_unavailable_groups(self,time):
        unavailable_day_time = schedule.format_day_time(time)
        remove_list = []
        for group in self.groups:
            group_day_time = schedule.format_day_time(group)
            if schedule.clashing(unavailable_day_time,group_day_time):
                remove_list.append(group)
        for group in remove_list:
            if group in self.groups:
                self.groups.remove(group)
        remove_list.clear()

    def clashing(self,other):
        for this_group in self.groups:
            for other_group in other.groups:
                this_group_day_time = schedule.format_day_time(this_group)
                other_group_day_time = schedule.format_day_time(other_group)
                if schedule.clashing(this_group_day_time,other_group_day_time):
                    return True
        return False

                

import course as course_class
import gui
import random
import schedule as schedule_py
import math
MAX_MORNINGS_FUNCTION = 0
MAX_EVENINGS_FUNCTION = 1
MINIMUM_DAYS_FUNCTION = 2

# MORNING 08:00 - 14:00
# EVENING 14:00 - 21:00

INITIAL_POPULATION = 100
BAD_MAX_GRADE = 59
GOOD_MIN_GRADE = BAD_MAX_GRADE + 1
GOOD_WINDOWS_MAX_GRADE = 20
GOOD_FUNCTION_MAX_GRADE = 80
GOOD_MIN_GRADE = BAD_MAX_GRADE + 1
GOOD_MAX_GRADE = 100
END_OF_TIMES = 1000
MAX_MORNINGS = 36
MAX_EVENINGS = 37
MAX_DAYS = 6
MIN_DAYS = 1
OVER_POPULATION_NUMBER = math.ceil(INITIAL_POPULATION*3.5)
OVER_POPULATED = False
UNDER_POPULATION_NUMBER = math.floor(INITIAL_POPULATION*0.7)
UNDER_POPULATED = False
NORMAL_FLOOD_FACTOR = 0.5
OVER_POPULATED_FLOOD_FACTOR = 0.7
UNDER_POPULATED_FLOOD_FACTOR = 0.3
MIN_CHILDREN = 1
MAX_CHILDREN = 5
MAX_CHILDREN_OVER_POPULATED = 3
MIN_CHILDREN_UNDER_POPULATED = 3

def bad_grader(bad_schedules):
  global BAD_MAX_GRADE 
  if len(bad_schedules) == 0:
    gui.print_error("Cannot grade , no schedules recieved")
    min_clash = float('inf')
    max_clash = 0
    for schedule in bad_schedules:
      hours = schedule.clashing_hours
      if max_clash < hours:
        max_clash = hours
      if hours<min_clash:
        min_clash = hours
    if max_clash - min_clash == 0:
      for schedule in bad_schedules:
        schedule.grade = BAD_MAX_GRADE
    else:
      for schedule in bad_schedules:
        i = schedule.clashing_hours
        schedule.grade = ((max_clash-i)/(max_clash-min_clash))*BAD_MAX_GRADE
def good_grader(good_schedules,target):
    if len(good_schedules) == 0:
        gui.print_error("Cannot grade , no schedules recieved")
    min_windows = float('inf')
    max_windows = 0
    for schedule in good_schedules:
      windows = schedule.windows
      if max_windows < windows:
        max_windows = windows
      if windows<min_windows:
        min_windows = windows
    if max_windows - min_windows == 0:
      for schedule in good_schedules:
        schedule.grade = GOOD_WINDOWS_MAX_GRADE
    else:
      for schedule in good_schedules:
        i = schedule.clashing_hours
        schedule.grade = ((max_windows-i)/(max_windows-min_windows))*GOOD_WINDOWS_MAX_GRADE

    schedule.count_day_mor_eve()
    if target == MAX_MORNINGS_FUNCTION:
        i = schedule.mornning_hours
        schedule.grade += (i/MAX_MORNINGS)*GOOD_FUNCTION_MAX_GRADE
    elif target == MAX_EVENINGS_FUNCTION:
        i = schedule.evening_hours
        schedule.grade += (i/MAX_EVENINGS)*GOOD_FUNCTION_MAX_GRADE
    elif target == MINIMUM_DAYS_FUNCTION:
        i = schedule.days
        schedule.grade += ((MAX_DAYS-i)/(MAX_DAYS - 1))*GOOD_FUNCTION_MAX_GRADE
    #CURRENTLY GRADES 0 - 100 ---> 60 - 100
    for schedule in good_schedules:
        i = schedule.grade
        schedule.grade = GOOD_MIN_GRADE + (i/100)*(GOOD_MAX_GRADE-GOOD_MIN_GRADE)


    

class User():
    def __init__(self,appData):
        self.appData = appData
        self.ordered_courses = []
    
    def run(self):
        gui.print_title("System collecting data ... please wait")
        status,msg = self.preprocess()
        if status == 0:
            gui.print_error(msg)
        else:
            gui.print_title("Data collection finished. Optimizing ...")
            best = self.optimize()
            self.conclude(best)
            
            


            
    def preprocess(self):
        ## INIT ##
        self.appData.db_controller.pull(self.appData)
        all_courses = self.appData.local
        all_courses_objects = []
        for document in all_courses:
            course = course_class.Course(document)
            if course not in all_courses_objects:
                all_courses_objects.append(course)
        all_courses = all_courses_objects
        year = int(self.appData.user_args[0])
        redo_courses = self.appData.user_args[1]
        optional_courses = self.appData.user_args[2]
        unavailable = self.appData.user_args[3]
        redo_courses_object = []
        for redo_course in redo_courses:
            self.appData.db_controller.find(self.appData,{"_id":int(redo_course)})
            for doc in self.appData.buffer:
                course = course_class.Course(doc)
                if course not in redo_courses_object:
                    redo_courses_object.append(course)
        redo_courses = redo_courses_object
        optional_courses_object = []
        for optional_course in optional_courses:
            self.appData.db_controller.find(self.appData,{"_id":int(optional_course)})
            for doc in self.appData.buffer:
                course = course_class.Course(doc)
                if course not in optional_courses_object:
                    optional_courses_object.append(course)
        optional_courses = optional_courses_object
        remove_list = []
        ## INIT END ##
        self.filter_redo_courses(redo_courses,year)
        self.filter_optional_courses(redo_courses,optional_courses)
        self.filter_all_courses(all_courses,redo_courses,optional_courses,year)
        all_courses = sorted(all_courses)
        self.filter_groups(all_courses,unavailable)
        self.filter_clashes(all_courses)
        ##### CHECK IF ALL COURSES < 74 #####
        if len(all_courses) >= 74:
            return 0, "Total number of courses is greater than size of schedule"
        if len(all_courses) == 0:
            return 0 , "Course list is empty"   
        self.appData.local = all_courses
        return 1, ""
    def filter_redo_courses(self,redo_courses,year):
        remove_list = []
        for course in redo_courses:
            if course.is_must == False or course.year >= year:
                remove_list.append(course)

        for course in remove_list:
            if course in redo_courses:
                redo_courses.remove(course)        
        remove_list.clear()  
    def filter_optional_courses(self,redo_courses,optional_courses):
        remove_list = []
        for course in optional_courses:
            if course.is_must == True:
                remove_list.append(course)     
        for course in remove_list:
            if course in optional_courses:
                optional_courses.remove(course)
        remove_list.clear()
        for redo_course in redo_courses:
            for optional_course in optional_courses:
                if redo_course.number in optional_course.prior and (optional_course not in remove_list):
                    remove_list.append(optional_course)      
        for course in remove_list:
            if course in optional_courses:
                optional_courses.remove(course)
        remove_list.clear()        
    def filter_all_courses(self,all_courses,redo_courses,optional_courses,year):
        _remove = []
        for course in all_courses:
            if course.year != year or course.year == 0:
                _remove.append(course)        
        for course in _remove:
            if course in all_courses:   
                all_courses.remove(course)        
        for course in redo_courses:
            all_courses.append(course)        
        for course in optional_courses:
            all_courses.append(course)
    def filter_groups(self,all_courses,unavailable):
        remove_list = []
        for course in all_courses:
            for time in unavailable:
                course.remove_unavailable_groups(time)
            if len(course.groups) == 0 and course.is_must == True:
                return 0,"Course " + str(course.number) + " has 0 groups available"
            if len(course.groups) == 0 and course.is_must == False and course not in remove_list:
                remove_list.append(course)     
        for course in remove_list:
            if course in all_courses:
                all_courses.remove(course)
    def filter_clashes(self,all_courses):
        remove_list = []
        size = len(all_courses)
        for i in range(0,size):
            for j in range(i+1,size):
                if i == j: continue
            first_course = all_courses[i]
            second_course = all_courses[j]
            if first_course.clashing(second_course):
                    return 0, "The course " + str(first_course.number) + " and " + str(second_course.number) + " dont sit together"
        for course in remove_list:
            if course in all_courses:
                all_courses.remove(course)
    def get_function(self):
        gui.print_title("What do you want to achieve ? [1]. Max mornings\n [2]. Max Evenings \n [3]. Minimum Days")
        gui.request_user_input()
        while True:
            if self.appData.buffer == '1':
                self.appData.function = MAX_MORNINGS_FUNCTION
                break
            if self.appData.buffer == '2':
                self.appData.function = MAX_EVENINGS_FUNCTION
                break
            if self.appData.buffer == '3':
                self.appData.buffer = MINIMUM_DAYS_FUNCTION
                break

    def optimize(self):
        self.get_function()
        global END_OF_TIMES
        population = []
        year = 0
        self.initial(population)
        while year != END_OF_TIMES:
            self.grade(population)
            population = self.dimograph(population)
            population = self.flood(population)
            population = self.dimograph(population)
            children = self.concieve(population)
            self.birth(population,children)
            population = self.dimograph(population)
            if self.has_optimal(population):
                break
            year += 1
        return population[len(population)-1]
    def initial(self,population):
        global INITIAL_POPULATION
        for course in self.appData.local:
            self.ordered_courses.append(course)
        for i in range(0,INITIAL_POPULATION):
            for course in self.ordered_courses:
                genes = []
                gen = random.choice(course.groups)
                genes.append(gen)
            citizen = schedule_py.Schedule(genes)
            population.append(citizen)   
    def grade(self,population):
        good_citizens = []
        bad_citizens = []
        for citizen in population:
            if citizen.type == schedule_py.GOOD:
                good_citizens.append(citizen)
            elif citizen.type == schedule_py.BAD:
                bad_citizens.append(citizen)
        bad_grader(bad_citizens)
        good_grader(good_citizens,self.appData.buffer)
    def dimograph(self,population):
        global OVER_POPULATION_NUMBER,UNDER_POPULATION_NUMBER,OVER_POPULATED,UNDER_POPULATED
        population = sorted(population)
        if len(population) >= OVER_POPULATION_NUMBER:
            OVER_POPULATED = True
            UNDER_POPULATED = False
        elif len(population) <= UNDER_POPULATION_NUMBER:
            UNDER_POPULATED = True
            OVER_POPULATED = False
        else:
            OVER_POPULATED = False
            UNDER_POPULATED = False
        return population
    def flood(self,population):
        global OVER_POPULATED,UNDER_POPULATED,OVER_POPULATED_FLOOD_FACTOR,UNDER_POPULATED_FLOOD_FACTOR,NORMAL_FLOOD_FACTOR
        population_number = len(population)
        number_to_flood = 0
        if OVER_POPULATED: number_to_flood = math.floor(population_number*OVER_POPULATED_FLOOD_FACTOR)
        elif UNDER_POPULATED: number_to_flood = math.floor(population_number*UNDER_POPULATED_FLOOD_FACTOR)
        else: number_to_flood = math.floor(population_number*NORMAL_FLOOD_FACTOR)
        for i in range(0,number_to_flood):
            if population:
                population.pop(0)
        return population
    def concieve(self,population):
        global OVER_POPULATED,UNDER_POPULATED,MAX_CHILDREN_OVER_POPULATED,MIN_CHILDREN_UNDER_POPULATED,MIN_CHILDREN,MAX_CHILDREN
        i=0
        num_of_genes = 0
        children = []
        if len(population)>0:
            num_of_genes = len(population[0])
            while i<len(population)-1:
                parents = [population[i],population[i+1]]
                children_number = 0
                if OVER_POPULATED: children_number = random.randint(MIN_CHILDREN,MAX_CHILDREN_OVER_POPULATED)
                elif UNDER_POPULATED: children_number = random.randint(MIN_CHILDREN_UNDER_POPULATED,MAX_CHILDREN)
                else: children_number = random.randint(MIN_CHILDREN,MAX_CHILDREN)
                for i in range(0,children_number):
                    child_genes = []
                    child = None
                    for j in range(0,num_of_genes):
                        parent = random.choice(parents)
                        gen = parent[j]
                        child_genes.append(gen)
                    child = schedule_py.Schedule(child_genes)
                    children.append(child)
                i+=2
        return children    
    def birth(self,population,children):
        for child in children:
            population.append(child)
    def has_optimal(self,population):
        alpha = population[len(population)-1]
        return alpha.grade == 100
    
    def conclude(self,best):
        if best.type == schedule_py.BAD:
                gui.print_body("Couldnt find optimal schedule")
        elif best.type == schedule_py.GOOD:
            gui.print_title("Optimal Solution:")
            num_of_courses = len(best)
            for i in range(0,num_of_courses):
                gui.print_body("Course " + str(self.ordered_courses[i]) + ": " + str(best[i])+ "\n")
            gui.print_body("Total hours in morning: " + str(best.morning_hours))
            gui.print_body("Total hours in evening: " + str(best.evening_hours))
            gui.print_body("Total days: " + str(best.days))
            gui.print_body("Total windows: " + str(best.windows))
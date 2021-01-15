import course as course_class
import gui
class User():
    def __init__(self,appData):
        self.appData = appData
    
    def run(self):
        status,msg = self.preprocess()
        if status == 0:
            gui.print_error(msg)
        else:
            print("we can continue to 2nd phase")
            
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
        ## REMOVE REDO COURSES WHICH ARE NOT MUST OR OUR CURRENT YEAR ##
        for course in redo_courses:
            if course.is_must == False or course.year >= year:
                remove_list.append(course)

        for course in remove_list:
            if course in redo_courses:
                redo_courses.remove(course)
                gui.print_body("Removed " + str(course.number) + " from redo courses list")
        
        remove_list.clear()
        ################################################################

        ## REMOVE OPTIONAL COURSES WHICH ARE MUST ##
        for course in optional_courses:
            if course.is_must == True:
                remove_list.append(course)
        
        for course in remove_list:
            if course in optional_courses:
                optional_courses.remove(course)
                gui.print_body("Removed " + str(course.number) + " from optional courses list")
        
        remove_list.clear()
        ############################################

        ## REMOVE OPTIONAL COURSES WHICH WE CANT TAKE ##
        for redo_course in redo_courses:
            for optional_course in optional_courses:
                if redo_course.number in optional_course.prior and (optional_course not in remove_list):
                    remove_list.append(optional_course)
        
        for course in remove_list:
            if course in optional_courses:
                optional_courses.remove(course)
                gui.print_body("Removed " + str(course.number) + " from optional courses list")
        remove_list.clear()
        ################################################

        ## STAY ONLY WITH OUR YEAR COURSES , AND ADD REDO AND OPTIONAL AFTER FILTER ##
        for course in all_courses:
            if course.year != year or course.year == 0:
                remove_list.append(course)
        
        for course in remove_list:
            all_courses.remove(course)
            gui.print_body("Removed " + str(course.number) + " from year " + str(course.year))

        
        remove_list.clear()

        for course in redo_courses:
            all_courses.append(course)
        
        for course in optional_courses:
            all_courses.append(course)
        ##############################################################################

        ## REMOVE UNAVAILABLE GROUPS (TIMES) , AND REMOVE COURSES WHICH NUM OF GROUPS IS 0##
        for course in all_courses:
            for time in unavailable:
                if time in course.groups:
                    course.groups.remove(time)
            if len(course.groups) == 0 and course.is_must == True:
                return 0,"Course " + str(course.number) + " has 0 groups available"
            if len(course.groups) == 0 and course.is_must == False and course not in remove_list:
                remove_list.append(course)
        
        for course in remove_list:
            if course in all_courses:
                gui.print_body("Removed " + str(course.number) + " which has 0 groups")
                all_courses.remove(course)

        remove_list.clear()
        ###################################################################################
        ## CHECK IF 2 COURSES DONT SIT ##
        ## MUST - MUST : RETURN 0 ##
        ## MUST - OPTIONAL : MUST ##
        ## OPTIONAL - OPTIONAL : CHOOSE HIGHER RANKING , IF SAME CHOOSE HIGHER DURATION , IF SAME CHOOSE RANDOMLY ##
        size = len(all_courses)
        for i in range(0,size):
            for j in range(i+1,size):
                if i == j: continue
            first_course = all_courses[i]
            second_course = all_courses[j]
            if len(first_course.groups) == 1 and len(second_course.groups) == 1 and first_course.groups[0] == second_course.groups[0]:
                if first_course.is_must == True and second_course.is_must == True:
                    return 0, "The course " + str(first_course.number) + " and " + str(second_course.number) + " dont sit together"
                elif first_course.is_must == True:
                    if second_course not in remove_list:
                        remove_list.append(second_course)
                elif second_course.is_must == True:
                    if first_course not in remove_list:
                        remove_list.append(first_course)
                else:
                    if first_course.rating > second_course.rating:
                        if second_course not in remove_list:
                            remove_list.append(second_course)
                    elif first_course.rating < second_course.rating: 
                        if first_course not in remove_list:
                            remove_list.append(first_course)
                    elif first_course.duration > second_course.duration:
                        if second_course not in remove_list:
                            remove_list.append(second_course)
                    elif first_course.duration < second_course.duration:
                        if first_course not in remove_list:
                            remove_list.append(first_course)
                    elif first_course not in remove_list:
                        remove_list.append(first_course)

        for course in remove_list:
            if course in all_courses:
                gui.print_body("Removed " + str(course.number) + " which doesn't fit with other courses")
                all_courses.remove(course)
        remove_list.clear()

        ##### CHECK IF ALL COURSES < 74 #####
        if len(all_courses) >= 74:
            return 0, "Total number of courses is greater than size of schedule"
        
        self.appData.local = all_courses
        print(len(self.appData.local))
        return 1, ""

    

                    




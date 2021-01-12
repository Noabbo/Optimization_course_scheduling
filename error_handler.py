import gui
class ErrorHandler:
    def check_year(self,year,msg,err_codes):
        try:
            year = int(year)
        except Exception:
            msg += year + " is not a valid year\n"
            err_codes.append(0)
        return msg,err_codes

    def check_courses(self,type,courses,msg,err_codes):
        for course in courses:
            try:
                course = int(course)
            except Exception:
                msg += course + " is not a valid course number\n"
                err_codes.append((type,course))
        return msg,err_codes

    def check_times(self,times,msg,err_codes):
        DAYS = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
        for time in times:
            has_err = False
            try:
                form = time.split(" ")
                hours = form[1].split("-")
                day = form[0].strip()
                start_hour = hours[0].strip()
                end_hour = hours[1].strip()
                if day not in DAYS:
                    has_err = True
                start_hour = int(start_hour)%24
                end_hour = int(end_hour)%24   
                if start_hour>end_hour:
                    has_err = True         
            except Exception:
                has_err = True
            if has_err:
                msg += time + " is not a valid time format\n"
                err_codes.append((3,time))
        return msg,err_codes

    def check_args(self,args):
        msg = ""
        err_codes = []
        year = args[0].strip()
        redo_courses = args[1]
        optional_courses = args[2]
        unavailable = args[3]
        msg,err_codes = self.check_year(year,msg,err_codes)
        msg,err_codes = self.check_courses(1,redo_courses,msg,err_codes)
        msg,err_codes = self.check_courses(2,optional_courses,msg,err_codes)
        msg,err_codes = self.check_times(unavailable,msg,err_codes)
        return msg,err_codes

    def fix_args(self,args,err_codes):
        year = args[0]
        redo_courses = args[1]
        optional_courses = args[2]
        unavailable = args[3]
        for error in err_codes:
            if error == 0:
                gui.print_title("Please insert your current year number")
                year = input(">>>")
            elif error[0] == 1:
                course = error[1]
                gui.print_title("Redo Courses : Would you like to fix " + str(course) + gui.str_y_n)
                command = input(">>>").lower()
                redo_courses.remove(course)
                if command != 'n':
                    new_course = input("new course>>>").lower()
                    redo_courses.append(new_course)
            elif error[0] == 2:
                course = error[1]
                gui.print_title("Choice Courses : Would you like to fix " + str(course) + gui.str_y_n)
                command = input(">>>").lower()
                optional_courses.remove(course)
                if command != 'n':
                    new_course = input("new course>>>").lower()
                    optional_courses.append(new_course)
            elif error[0] == 3:
                time = error[1]
                gui.print_title("Time : Would you like to fix " + str(time) + gui.str_y_n)
                command = input(">>>").lower()
                unavailable.remove(time)
                if command != 'n':
                    new_time = input("new time>>>").lower()
                    unavailable.append(new_time)
        return year,redo_courses,optional_courses,unavailable

    def args_controller(self,user_args):
        arg_check_response = self.check_args(user_args)
        err_msg = arg_check_response[0]
        err_codes = arg_check_response[1]
        while err_msg != "":
            gui.print_error(err_msg)
            gui.print_title("Would you like to fix issues ? y/n")
            command = input(">>>").lower()
            if command != "n":
                user_args = self.fix_args(user_args,err_codes)
                arg_check_response = self.check_args(user_args)
                err_msg = arg_check_response[0]
                err_codes = arg_check_response[1]
            else:
                gui.print_title("Shuting down system")
                return 0,None
        return 1,user_args  
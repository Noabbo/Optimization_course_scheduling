str_y_n = " ? y/n"

def welcome_page():
    print_title("Please insert your current year number")
    year = input(">>>")
    redo_courses = []
    optional_courses = []
    unavailable = []
    print_title("Please enter course numbers you must redo, press 'r' to finish")
    while True:
        course = input(">>>").lower()
        if course == 'r':
            break
        redo_courses.append(course)
    print_title("Please enter optional course numbers you would like to take , press 'r' to finish")
    while True:
        course = input(">>>").lower()
        if course == 'r':
            break
        optional_courses.append(course)
    print_title("Please enter days and hours in those days you cant study ex. sunday 8-14"
                + " Press 'r' to finish")
    while True:
        block = input(">>>").lower()
        if block == 'r':
            break
        unavailable.append(block)
    return year,redo_courses,optional_courses,unavailable

def print_title(msg):
    print("\033[92m"+ str(msg) + "\033[0m")

def print_error(msg):
    print("\033[91m"+ str(msg) + "\033[0m")

def print_schedule():
    print("Printing Schedule")

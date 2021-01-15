str_y_n = " ? y/n"

def welcome_page(appData):
    print_title("Would you like to enter as admin? " + str_y_n)
    request_user_input(appData)
    if appData.buffer != 'n':
        appData.set_user_args(appData.ADMIN_KEY)
    else:
        print_title("Please insert your current year number")
        request_user_input(appData)
        year = appData.buffer
        redo_courses = []
        optional_courses = []
        unavailable = []
        print_title("Please enter course numbers you must redo, press 'r' to finish")
        while True:
            request_user_input(appData)
            course = appData.buffer
            if course == 'r':
                break
            redo_courses.append(course)
        print_title("Please enter optional course numbers you would like to take , press 'r' to finish")
        while True:
            request_user_input(appData)
            course = appData.buffer
            if course == 'r':
                break
            optional_courses.append(course)
        print_title("Enter times you cant study ex. sunday 8-14 Press 'r' to finish")
        while True:
            request_user_input(appData)
            block = appData.buffer
            if block == 'r':
                break
            unavailable.append(block)
        appData.set_user_args((year,redo_courses,optional_courses,unavailable))

def print_title(msg):
    print("\033[92m"+ str(msg) + "\033[0m")

def print_body(msg):
    print(msg)

def print_error(msg):
    print("\033[91m"+ str(msg) + "\033[0m")

def admin_page(appData):
    print_title("[1]. Auto insert\n[2]. Clear Collection\n[3]. Break")
    request_user_input(appData)

def request_user_input(appData):
    appData.buffer = input(">>>").lower().strip()
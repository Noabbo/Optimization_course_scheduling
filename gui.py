def welcome_page():
    print("Please insert your current year number")
    year = input(">>>")
    redo_courses = []
    optional_courses = []
    unavailable = []
    print("Please enter course numbers you must redo, press 'r' to finish")
    while True:
        course = input(">>>").lower()
        if course == 'r':
            break
        redo_courses.append(course)
    print("Please enter optional course numbers you would like to take , press 'r' to finish")
    while True:
        course = input(">>>").lower()
        print(course)
        if course == 'r':
            break
        optional_courses.append(course)
    print("Please enter days and hours in those days you cant study ex. sunday 8-14\n"
                + "Press 'r' to finish")
    while True:
        block = input(">>>").lower()
        if block == 'r':
            break
        unavailable.append(block)
    return (year,redo_courses,optional_courses,unavailable)
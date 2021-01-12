def check_args(args):
    msg = ""
    year = args[0].strip()
    redo_courses = args[1]
    optional_courses = args[2]
    unavailable = args[3]
    try:
        year = int(year)
    except Exception:
        msg += year + " is not a valid year\n"
    for course in redo_courses:
        try:
            course = int(course)
        except Exception:
            msg += course + " is not a valid course number\n"
    for course in optional_courses:
        try:
            course = int(course)
        except Exception:
            msg += course + " is not a valid course number\n"
    return msg









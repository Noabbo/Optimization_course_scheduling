import db_controller
import random
# Course number first year : 1 - 73
# Course number second year : 74 - 118
# Course number third year : 119 - 128
# Optional courses : 150 - 200


DAYS = ["sunday","monday","tuesday","wednesday","thursday","friday"]
TIMES = ["08","09","10","11","12","13","14","15","16","17","18","19","20","21"]
FIRST_YEAR_COURSES_NUM = 73
SECOND_YEAR_COURSES_NUM = 45
THIRD_YEAR_COURSES_NUM = 10
TOTAL_HOURS_WEEK = 13
TOTAL_HOURS_WEEKEND = 8
CLIENT = None
def auto_generate_courses():
  time_slots = create_time_slots()
  courses = []
  for i in range(1,74):
    course = {}
    course["_id"] = i
    course["name"] = "MUST " + str(i)
    course["year"] = 1
    course["is_must"] = True
    course["groups"] = time_slots
    course["pre-courses"] = []
    courses.append(course)
  for i in range(74,119):
    course = {}
    course["_id"] = i
    course["name"] = "MUST " + str(i)
    course["year"] = 2
    course["is_must"] = True
    course["groups"] = time_slots
    course["pre-courses"] = [i-73]
    courses.append(course)
  for i in range(119,129):
    course = {}
    course["_id"] = i
    course["name"] = "MUST " + str(i)
    course["year"] = 3
    course["is_must"] = True
    course["groups"] = time_slots
    course["pre-courses"] = [i-45]
    courses.append(course)
  for i in range(150,201):
    course = {}
    course["_id"] = i
    course["name"] = "OPTIONAL " + str(i)
    course["year"] = 0
    course["is_must"] = False
    course["groups"] = time_slots
    course["rating"] = random.randint(1,10)
    course["pre-courses"] = []
    courses.append(course)
  return courses
def create_time_slots():
  available = []
  for i in range(0,6):
    if DAYS[i] != "friday":
      for j in range (0,TOTAL_HOURS_WEEK):
        date = DAYS[i] + " " + TIMES[j] + "-" + TIMES[j+1]
        available.append(date)
    else:
      for j in range (0,TOTAL_HOURS_WEEKEND):
        date = DAYS[i] + " " + TIMES[j] + "-" + TIMES[j+1]
        available.append(date)
  return available


  
import gui
def format_day_time(str):
  try:
    date = str.split(" ")
    day = date[0].strip()
    time = date[1].split("-")
    start_hour = int(time[0].strip())
    end_hour = int(time[1].strip())
    return day,start_hour,end_hour
  except Exception:
    gui.print_error("Error formating day time")
    return None
    
def reformat_day_time(day_time):
  return str(day_time[0]) + " " + str(day_time[1]) + "-" + str(day_time[2])

def clashing(day_time_1,day_time_2):
  if day_time_1[0] == day_time_2[0]:
    if day_time_1[1] == day_time_2[1]:
      return True
    elif day_time_1[1] < day_time_2[1] and day_time_1[2] > day_time_2[1]:
        return True
    elif day_time_2[1] < day_time_1[1] and day_time_2[2] > day_time_1[1]:
        return True
  else:
    return False
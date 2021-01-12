class Client:
  def __init__(self, year, redo_courses,optional_courses,unavailable):
    self.year = year
    self.redo_courses = redo_courses
    self.optional_courses = optional_courses
    self.unavailable = unavailable

  def get_year(self):
      return self.year
  def get_redo_courses(self):
      return self.redo_courses
  def get_optional_courses(self):
      return self.get_optional_courses
  def get_unavailable(self):
      return self.get_unavailable

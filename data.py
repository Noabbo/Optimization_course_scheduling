import db_controller
class Data:
  def __init__(self, client):
      self.client = client
      self.local = db_controller.pull()
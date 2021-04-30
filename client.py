import time


class client:
  def __init__(self, client):
      self._client = client
      self.last_interaction = time.time()

  def isInactive(self, minutes):
      if time.time() - self.last_interaction > minutes * 60:
        return True
      return False
  
  def get_name(self):
    return str(self._client)

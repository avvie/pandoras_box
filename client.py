import time


class client:
  def __init__(self, client):
      self._client = client
      self.last_interaction = time.time()
      self.message_to_roll = {}

  def isInactive(self, minutes):
      if time.time() - self.last_interaction > minutes * 60:
        return True
      return False
  
  def get_name(self):
    return str(self._client)

  def add_roll(self, message, roll_parameters):
    self.message_to_roll.update({message : roll_parameters})

  def get_roll_params(self, message):
    if(message not in self.message_to_roll):
      return None
    data = self.message_to_roll[message]
    self.message_to_roll.pop(message)
    return data
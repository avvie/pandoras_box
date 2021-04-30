import quantumrandom

class roller:
  def __init__(self):
    self.data = []

  def roll_d10(self):
    return quantumrandom.randint(0, 20)
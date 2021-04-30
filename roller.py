import quantumrandom
import re
from Crypto.Random.random import randint

class roller:
  def __init__(self):
    self.data = []

  def d10(self):
    return randint(1, 10)

  def roll_d10_with_modifier(self, command):
    return re.search(r"[/]\d+[d]\d+[d]\d+", command)

  def roll_d10(self, command):
    return re.search(r"[/]\d+[d]\d+", command)

  def roll_d10_chance(self, command):
    return re.search(r"[/][d]\d+", command)

  def roll_d10_chance_with_modifier(self, command):
    return re.search(r"[/][d]\d+", command)

  def parse_command(self, command):
    x = self.roll_d10_with_modifier(command)

    if x is not None:
      literals = re.split("\s", self.substitute_characters(x))
      del literals[0]
      return literals
    
    x = self.roll_d10(command)
    if x is not None:
      literals = re.split("\s", self.substitute_characters(x))
      del literals[0]
      literals.append(6)
      return literals
    
    x = self.roll_d10_chance(command)
    if x is not None:
      literals = re.split("\s", self.substitute_characters(x))
      del literals[0]
      literals[0] = 1
      literals.append(6)
      return literals
    
    x = self.roll_d10_chance_with_modifier(command)
    if x is not None:
      literals = re.split("\s", self.substitute_characters(x))
      del literals[0]
      literals[0] = 1
      return literals
    
    return None

  def substitute_characters(self, command):
    return re.sub("/|d", " ", command.string)

  def handle_message(self, command, message):
    result = self.parse_command(command)

    if result is None:
      return None
    else:
      processed_list = self.processed_result(result)
      success = 0
      


  def processed_result(self, result):
    processed = []
    for i in range(0, int(result[0])):
      processed.append(self.d10())
    return processed

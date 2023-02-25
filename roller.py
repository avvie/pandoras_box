import re
import discord
from random import randint

class roller:
  def __init__(self, client):
    self.data = ['\U0001F3B2']

  def roll(self, limit):
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

  async def handle_message(self, command, prev_succ = 0):
    result = self.parse_command(command)

    if result is None:
      return None
    else:
      processed_list = self.processed_result(result)
      success = prev_succ
      diff = int(result[2])
      if diff > 10:
        success = success + 10 - diff
        diff = 10
      dice_results = "["
      tens = 0
      for elem in processed_list:
        dice_results = dice_results + str(elem) + " "
        if elem >= diff:
          success = success + 1
        elif elem == 1:
          success = success - 1
        if elem == 10:
          tens = tens + 1
      dice_results = dice_results + "]"
      

      message = str(success) + " successes rolled! "
      if tens > 0:
        message = message + " You rolled: " + str(tens) + " 10s! "
        #more logic for reroll here
        
      message = message + dice_results
      return (message, tens, diff, success)


  def processed_result(self, result):
    processed = []
    for i in range(0, int(result[0])):
      processed.append(self.roll(int(result[1])))
    return processed

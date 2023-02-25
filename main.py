import discord
import os
import threading
import sched, time
from roller import roller
from client import client as user

# Variable Init
s = sched.scheduler(time.time, time.sleep)
timeToSleepBeforeCleanUp = 60 # in minutes
client = discord.Client()
droller = roller(client)
users = {}
X = []
reactions = ['\U0001F3B2']


# Events
@client.event
async def on_ready():
  print('logged in as')
  #X = threading.Thread(target = clean_thread).start()

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if(message.author in users):
      currentClient = users[message.author]
    else:
      print("adding: " + str(message.author))
      users.update({message.author : user(message.author)})
      currentClient = users[message.author]

    if message.content.startswith('/'):
      (result, tens, diff, success) = await droller.handle_message(message.content)
      new_message = await message.channel.send(result)
      currentClient.add_roll(new_message, [message.author,tens, diff, success])
      if tens > 0:
        await new_message.add_reaction(reactions[0])

@client.event
async def on_reaction_add(reaction, user):
  if user == client.user:
    return
  if user in users:
    currentClient = users[user]
    params = currentClient.get_roll_params(reaction.message)
    if params is None:
      return 
    message = "/" + str(params[1]) + 'd10d' + str(params[2] )
    (result, tens, diff, success) = await droller.handle_message(message, params[3])
    new_message = await reaction.message.channel.send(result)
    currentClient.add_roll(new_message, [user,tens, diff, success])
    if tens > 0:
      await new_message.add_reaction(reactions[0])
  

# Free Up Memory every so often 

def clean_inactive():
  print("check to clean, list length: " + str(len(users)))
  for key,value in users.copy().items():
    if value.isInactive(timeToSleepBeforeCleanUp):
      print("removing: " + str(value.get_name()))
      users.pop(key)

def clean_thread():
  print('start thread')
  while(True):
    time.sleep(timeToSleepBeforeCleanUp * 60)
    clean_inactive()


# Start Client 
client.run(os.getenv('TOKEN'))


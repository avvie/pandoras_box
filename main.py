import discord
import os 
import threading
import sched, time
import atexit
from roller import roller
from client import client as user

# Variable Init
s = sched.scheduler(time.time, time.sleep)
timeToSleepBeforeCleanUp = 0.1 # in minutes
client = discord.Client()
droller = roller()
users = {}
X = []


# Events
@client.event
async def on_ready():
  print('logged in as')
  X = threading.Thread(target = clean_thread).start()

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
      await message.channel.send('Hello! ' + str(currentClient._client))

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


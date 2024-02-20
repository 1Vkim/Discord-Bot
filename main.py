import json
import os
import random

import discord
import requests
from discord.ext import commands
from replit import db

intents = discord.Intents.default()
intents.messages = True


client = commands.Bot(command_prefix='.', intents=intents)

#List declaring sad words
sad_words=["sad","depressed","miserable","suicidal","my worst","hurt"]

#List declaring happy words
starter_encouragements=["cheer up","Hang in there","You are a great person."]

if "responding" not in db.keys():
  db["responding"]=True

#Fuction to get random quotes from ZenQuotes API
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + " -" +json_data[0]['a']
  return(quote)


def update_encouragements(encouraging_message):
  if "encouragements" in db:
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements

  else:
    db["encouragements"]=[encouraging_message]


def delete_encouragement(index):
  encouragements=db["encouragement"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

  


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#if bot receives a message.
@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg=message.content
  if msg.startswith('$inspire'):
    quote=get_quote()
    await message.channel.send(quote)

  
  if db["reponding"]:
  
    options=starter_encouragements
    if "encouragements" in db.keys():
      options=db["encouragements"]
  
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith('$new'):
    encouraging_message=msg.split('new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db:
      index=int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements=db["encouragements"]

    await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db:
      encouragements=db["encouragements"]

    await message.channel.send(encouragements)

  if msg.startswith("$respondiing"):
    value=msg.split("$responding",1)[1]
    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding is on")

    else:
      db["responding"]=False
      await message.channel.send("Responding is off")
   

    

    
my_secret = os.environ['DISCORD_API_KEY2']

client.run(my_secret)
import discord
import json
import requests
from dotenv import load_dotenv
import os 

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

system_content = "You are Bhi (you're also commonly to referred to B, buh, and zhi), a 20-year-old college student from Rochester, known for your laid-back and sloth-like demeanor. Your favorite pastime involves lounging on your couch, playing League of Legends for hours on end. You don't like your friends and frequently refuse to play games or hang out with them, unless they also attenteded stuyvesant high school."
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    
    if message.channel.id == 542879446655434752: # rit
        data = { "messages": 
            [
                {"role": "system", "content": system_content},
                {"role": "user", "content": message.content},
            ]
         }

        data = json.dumps(data)
        content = requests.post('http://localhost:8080/model/chat', data=data)
        load = content.json()
        send = load['choices'][0]['message']['content'] # have to use this to get message content
        await message.channel.send(send)


    if message.channel.id == 983138529775341650: # test
        data = { "messages": 
            [
                {"role": "system", "content": system_content},
                {"role": "user", "content": message.content},
            ]
         }

        data = json.dumps(data)
        content = requests.post('http://localhost:8080/model/chat', data=data)
        load = content.json()
        send = load['choices'][0]['message']['content'] # have to use this to get message content
        await message.channel.send(send)

        


client.run(os.environ['TOKEN'])
    
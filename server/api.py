import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    
    if message.channel.id == 542879446655434752: # rit
        pass

    if message.channel.id == 983138529775341650: # test
        pass
    
import bot
import torch
import pickle
from model import TextClassifier
import discord


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    susge = '<:susge:1211184808039030825>'
    ok = "<:2x:1211184856923643934>"

    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    model = TextClassifier(18284)
    model.load_state_dict(torch.load('model.pth'))
    model.to('cuda')

    def inference(text):
        pred = model(torch.tensor(vectorizer.transform([text]).todense(), dtype=torch.float32).to('cuda')).item()
        if (pred > 0.5):
            return f"There is a {round(pred * 100, 2)}% chance that this is buh {ok}"
        else:
            return f"There is a {round(pred * 100, 2)}% chance that this is buh {susge}"

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
    
    @client.event
    async def on_message(message):
        if message.author == client.user or message.author.bot:
            return
        if message.channel.id == 983138529775341650: # test
            await message.reply(inference(message.content))
    client.run('')

if __name__ == '__main__':
    main()
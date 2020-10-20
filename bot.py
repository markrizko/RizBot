# bot.py
# Official discord bot of the Rizko-Yamin family
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to ' + f'{guild.name}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    escape = 'Вы должны сбежать из Таркова!'

    if message.content == '!escape':
        await message.channel.send(escape)

client.run(TOKEN)
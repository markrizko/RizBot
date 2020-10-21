# bot.py
# Official discord bot of the Rizko-Yamin family
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = '!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to ' + f'{guild.name}!')

@bot.command()
async def escape(ctx):
    await ctx.send('Вы должны сбежать из Таркова!')

@bot.command()
async def flip_coin(ctx):
    coin = random.random()
    # print(coin)
    if coin < 0.5:
        await ctx.send('Heads')
    else:
        await ctx.send('Tails')

bot.run(TOKEN)
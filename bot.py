# bot.py
# Official discord bot of the Rizko-Yamin family
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import praw

bot = commands.Bot(command_prefix = '!')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RID = os.getenv('REDDIT_ID')
RSECRET = os.getenv('REDDIT_SECRET')

reddit = praw.Reddit(client_id = RID, client_secret = RSECRET, user_agent = 'RizBot:%s:1.0' %RID)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to ' + f'{guild.name}!')

@bot.command()
async def helpme(ctx):
    await ctx.send("Available Commands:\n!flip_coin: Flip a coin"
    + "\n!escape: YOU MUST ESCAPE FROM THE TARKOV\n!memeofday: Fetches top post "
    + "from /r/memes for the day.\n!top [subreddit] [count]: fetches top "
    + "X posts from subreddit.")

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

@bot.command()
async def memeofday(ctx):
    memes = reddit.subreddit('memes').top("day", limit=1)
    for meme in memes:
        await ctx.send(meme.url)

@bot.command()
async def top(ctx, sub, count=1):
    posts = reddit.subreddit(sub).top('day', limit=count)
    for post in posts:
        await ctx.send(post.url)

bot.run(TOKEN)
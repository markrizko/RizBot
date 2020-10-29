# bot.py
# Official discord bot of the Rizko-Yamin family
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Member
import random
import praw
import firebase_admin
from firebase_admin import firestore, credentials

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RID = os.getenv('REDDIT_ID')
RSECRET = os.getenv('REDDIT_SECRET')
FIRESTORE_CERT_PATH = os.getenv('FIRESTORE_CERT_PATH')

bot = commands.Bot(command_prefix = '!')

cred = credentials.Certificate(FIRESTORE_CERT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

reddit = praw.Reddit(client_id = RID, client_secret = RSECRET, user_agent = 'RizBot:%s:1.0' %RID)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to ' + f'{guild.name}!')

@bot.command()
async def helpme(ctx):
    await ctx.send("```Available Commands: \
     \n\t.flip_coin: Flip a coin \
     \n\t.escape: YOU MUST ESCAPE FROM THE TARKOV \
     \n\t.memeofday: Fetches top post from /r/memes for the day. \
     \n\t.top [subreddit] [count]: fetches top X posts from subreddit.```")

@bot.command()
async def escape(ctx):
    await ctx.send('Вы должны сбежать из Таркова!')

@bot.command()
async def flip_coin(ctx):
    coin = random.random()
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

@bot.command()
async def karma(ctx, user: Member, action):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if ctx.author == user:
        await ctx.send("Can't give karma to yourself")
        return
    users_ref = db.collection(guild.name).document(str(user.id))
    snapshot = users_ref.get()
    karma = snapshot.get('karma')
    if karma == None:
        karma = 0
    if action == '++':
        karma += 1
    elif action == '--':
        karma -= 1
    users_ref.set({
        u'karma': karma
    })
    await ctx.send(f"{user.name} you now have {str(karma)} points")

bot.run(TOKEN)

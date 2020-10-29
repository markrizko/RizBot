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
     \n\t!escape: YOU MUST ESCAPE FROM THE TARKOV \
     \n\t!flip_coin: Flip a coin \
     \n\t!karma [user] [++/--] \
     \n\t!memeofday: Fetches top post from /r/memes for the day! \
     \n\t!rank: Display karma leaderboards \
     \n\t!top [subreddit] [count]: fetches top X posts from subreddit.```")

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
async def rank(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    users_ref = db.collection(guild.name)
    query = users_ref.order_by(
    u'karma', direction=firestore.Query.DESCENDING)
    results = query.get()
    place = 1
    top_charts = "```Leaderboard:"
    for result in results:
        karma = result.get("karma")
        member = guild.get_member(int(result.id))
        top_charts = top_charts + f"\n\t {place}. {member.name}: {karma}"
        place += 1
    await ctx.send(top_charts + "```")

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
    point_str = "point" if karma == 1 else "points"
    await ctx.send(f"{user.name} you now have {str(karma)} {point_str}")

bot.run(TOKEN)

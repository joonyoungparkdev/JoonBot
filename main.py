# main.py
import os
import discord
from discord.ext import commands
import json
import time
from reservations import check_all_courts

# Load token from config/secrets.json
with open('config/secrets.json') as f:
    secrets = json.load(f)

# TOKEN = secrets["token"]    # for local testing
TOKEN = os.environ['DISCORD_TOKEN']  # Get from environment variable

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def runscript(ctx):
    start_time = time.time()
    results = check_all_courts()
    end_time = time.time()
    elapsed_time = end_time - start_time
    await ctx.send(f'Script executed! Output:\n{results}')
    await ctx.send(f"Script completed in {elapsed_time:.2f} seconds")

bot.run(TOKEN)

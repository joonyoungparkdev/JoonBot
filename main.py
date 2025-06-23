# main.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import time
import logging
from reservations import check_all_courts

# Load token from config/secrets.json
load_dotenv()  # Load from .env

# TOKEN = secrets["token"]    # for local testing
try:
    TOKEN = os.environ['DISCORD_TOKEN']  # Get from environment variable
except:
    TOKEN = os.getenv('DISCORD_TOKEN')  # for local testing

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    logger.info(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def runscript(ctx):
    await ctx.send('Starting reservation retrieval...')
    logger.info('Starting reservation retrieval...')

    start_time = time.time()
    results = await check_all_courts()
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    await ctx.send(f'Script executed! Output:\n{results}')
    await ctx.send(f"Script completed in {elapsed_time:.2f} seconds")
    
    # Send screenshots
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        if screenshot_files:
            await ctx.send("Screenshots:")
            # Send all screenshots in one message
            files = []
            for screenshot_file in screenshot_files:
                screenshot_path = os.path.join(screenshots_dir, screenshot_file)
                try:
                    files.append(discord.File(screenshot_path))
                except Exception as e:
                    logger.error(f"Failed to prepare screenshot {screenshot_file}: {e}")
                    await ctx.send(f"Failed to prepare screenshot {screenshot_file}")
            
            if files:
                try:
                    await ctx.send(files=files)
                except Exception as e:
                    logger.error(f"Failed to send screenshots: {e}")
                    await ctx.send("Failed to send screenshots")
        else:
            await ctx.send("No screenshots found.")
    else:
        await ctx.send("Screenshots directory not found.")
    
    logger.info('Script complete')

bot.run(TOKEN)

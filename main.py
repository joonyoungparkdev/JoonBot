# main.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import time
import logging
import pytz
from datetime import datetime, timedelta
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
    try:
        await ctx.send('Starting reservation retrieval...')
        logger.info('Starting reservation retrieval...')

        start_time = time.time()
        results = await check_all_courts()
        end_time = time.time()
        elapsed_time = end_time - start_time

        pacific_tz = pytz.timezone('US/Pacific')
        tomorrow = datetime.now(pacific_tz) + timedelta(days=1)
        
        # Format results with each court on a new line
        formatted_results = f'Availability for {tomorrow.strftime("%b %d, %Y")}:\n'
        for court_name, timeslots in results.items():
            if timeslots:
                formatted_results += f'**{court_name}**: {", ".join(timeslots)}\n'
            else:
                formatted_results += f'**{court_name}**: No available timeslots\n'
        formatted_results += f"Script completed in {elapsed_time:.2f} seconds"

        await ctx.send(formatted_results)
        
        # Send screenshots
        screenshots_dir = "screenshots"
        if os.path.exists(screenshots_dir):
            screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
            if screenshot_files:
                # Send all screenshots in one message
                files = []
                for screenshot_file in screenshot_files:
                    screenshot_path = os.path.join(screenshots_dir, screenshot_file)
                    try:
                        files.append(discord.File(screenshot_path))
                    except Exception as e:
                        logger.error(f"Failed to prepare screenshot {screenshot_file}: {e}")
                        logger.error(f"Error type: {type(e).__name__}")
                        logger.error(f"Error details: {str(e)}")
                        await ctx.send(f"Failed to prepare screenshot {screenshot_file}")
                
                if files:
                    try:
                        await ctx.send(files=files)
                        logger.info(f"Successfully sent {len(files)} screenshots")
                    except Exception as e:
                        logger.error(f"Failed to send screenshots: {e}")
                        logger.error(f"Error type: {type(e).__name__}")
                        logger.error(f"Error details: {str(e)}")
                        await ctx.send("Failed to send screenshots")
            else:
                logger.warning("No screenshot files found in screenshots directory")
                await ctx.send("No screenshots found.")
        else:
            logger.warning("Screenshots directory does not exist")
            await ctx.send("Screenshots directory not found.")
            
    except Exception as e:
        logger.error(f"An error occurred in runscript command: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await ctx.send(f"An error occurred: {e}")

    logger.info('Script complete')

bot.run(TOKEN)

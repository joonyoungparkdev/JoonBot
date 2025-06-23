# main.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import time
import logging
import pytz
import json
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

def load_setup_config():
    """
    Loads the setup configuration from config/setup.json.
    
    Returns:
        dict: Configuration dictionary containing channel information.
    """
    try:
        with open('config/setup.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load setup config: {e}")
        return {}

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    logger.info(f'Bot is ready. Logged in as {bot.user}')
    # Start the scheduled task
    scheduled_reservation_check.start()

@tasks.loop(minutes=1)
async def scheduled_reservation_check():
    """
    Automatically runs the reservation check at 11:55 PM Pacific Time every night.
    Checks every minute to ensure precise timing.
    """
    pacific_tz = pytz.timezone('US/Pacific')
    now = datetime.now(pacific_tz)
    logger.info(f"Current time: {now}")
    
    # Check if it's 11:55 PM Pacific Time
    if (now.hour == 23 or now.hour == 21) and now.minute == 55:
        logger.info("Running scheduled reservation check at 11:55 PM Pacific Time")
        
        try:
            # Load setup configuration
            setup_config = load_setup_config()
            
            # Get the tennis channel from config
            if 'Tennis_Channel' in setup_config:
                channel_id = setup_config['Tennis_Channel']['Channel_ID']
                channel = bot.get_channel(int(channel_id))
                
                if channel:
                    await run_reservation_check(channel)
                else:
                    logger.error(f"Could not find channel with ID: {channel_id}")
            else:
                logger.error("Tennis_Channel configuration not found in setup.json")
                        
        except Exception as e:
            logger.error(f"Error in scheduled reservation check: {e}")

async def run_reservation_check(channel):
    """
    Runs the reservation check and sends results to the specified channel.
    """
    try:
        await channel.send('Starting manual reservation retrieval...')
        logger.info('Starting manual reservation retrieval...')

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

        await channel.send(formatted_results)
        
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
                        await channel.send(f"Failed to prepare screenshot {screenshot_file}")
                
                if files:
                    try:
                        await channel.send(files=files)
                        logger.info(f"Successfully sent {len(files)} screenshots")
                    except Exception as e:
                        logger.error(f"Failed to send screenshots: {e}")
                        logger.error(f"Error type: {type(e).__name__}")
                        logger.error(f"Error details: {str(e)}")
                        await channel.send("Failed to send screenshots")
            else:
                logger.warning("No screenshot files found in screenshots directory")
                await channel.send("No screenshots found.")
        else:
            logger.warning("Screenshots directory does not exist")
            await channel.send("Screenshots directory not found.")
            
    except Exception as e:
        logger.error(f"An error occurred in scheduled reservation check: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await channel.send(f"An error occurred: {e}")

    logger.info('Scheduled script complete')

@bot.command()
async def runscript(ctx):
    try:
        await run_reservation_check(ctx.channel)
    except Exception as e:
        logger.error(f"An error occurred in runscript command: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await ctx.send(f"An error occurred: {e}")

    logger.info('Script complete')

bot.run(TOKEN)

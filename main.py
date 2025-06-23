# main.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging
from reservations import run_reservation_check, create_scheduled_task

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
    
    # Create and start the scheduled task
    scheduled_task = create_scheduled_task(bot)
    scheduled_task.start()

@bot.command()
async def reservations(ctx):
    """
    Manual command to run the reservation check.
    """
    try:
        await run_reservation_check(ctx.channel, is_scheduled=False)
    except Exception as e:
        logger.error(f"An error occurred in runscript command: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await ctx.send(f"An error occurred: {e}")

    logger.info('Manual script complete')

bot.run(TOKEN)

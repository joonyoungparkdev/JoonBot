import json
import os
import time
import asyncio
import logging
import tempfile
import uuid
import pytz
import discord
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logger = logging.getLogger(__name__)

def load_setup_config():
    """
    Loads the setup configuration from tennis_reservations/config/setup.json.
    
    Returns:
        dict: Configuration dictionary containing channel information.
    """
    try:
        with open('tennis_reservations/config/setup.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load setup config: {e}")
        return {}

def setup_driver():
    """
    Sets up and returns a headless Chrome WebDriver with a predefined window size.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    # Create a unique user data directory using timestamp and UUID
    unique_id = f"chrome_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    user_data_dir = os.path.join(tempfile.gettempdir(), unique_id)
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--log-level=3')  # Only fatal errors
    options.add_argument('--no-sandbox')  # Required for Heroku
    options.add_argument('--disable-dev-shm-usage')  # Required for Heroku
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--remote-debugging-port=9222')  # Required for Heroku
    options.add_argument(f'--user-data-dir={user_data_dir}')  # Unique user data directory
    options.add_argument('--disable-extensions')  # Disable extensions
    options.add_argument('--disable-plugins')  # Disable plugins
    service = Service()
    return webdriver.Chrome(service=service, options=options)

def get_tomorrow_label():
    """
    Returns the formatted date string for tomorrow in Pacific Time to match the webpage's aria-label format.

    Returns:
        str: Date string formatted as 'Mon DD, YYYY' (e.g., 'Jun 23, 2025') in Pacific Time.
    """
    pacific_tz = pytz.timezone('US/Pacific')
    tomorrow = datetime.now(pacific_tz) + timedelta(days=1)
    logger.info(f"Tomorrow: {tomorrow}")
    return tomorrow.strftime("%b %d, %Y")

async def get_timeslots_for_url(name, url, tomorrow_str):
    """
    Navigates to the court reservation page and extracts timeslots available for tomorrow.

    Args:
        name (str): Name of the court.
        url (str): URL of the court reservation page.
        tomorrow_str (str): Date string used to locate the correct calendar day.

    Returns:
        list: List of available time slots as strings.
    """
    driver = setup_driver()
    result = []

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        date_time_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.facility-detail-actual__date-time-input-field")
        ))
        date_time_button.click()
        await asyncio.sleep(1)

        day_selector = f"div[aria-label^='{tomorrow_str}']"
        try:
            day_cell = driver.find_element(By.CSS_SELECTOR, day_selector)

            try:
                more_button = day_cell.find_element(By.CSS_SELECTOR, "span.an-popper a.more-link")
                more_button.click()
                await asyncio.sleep(1)

                options_list = day_cell.find_elements(By.CSS_SELECTOR, ".menu-option-item")
                result = [opt.text for opt in options_list if opt.text.strip()]

            except:
                try:
                    single_timeslot = day_cell.find_element(By.CSS_SELECTOR, "a.timeslots__avaliable")
                    aria_label = single_timeslot.get_attribute("aria-label").replace(" available", "")
                    result = [aria_label]
                except:
                    result = []

        except:
            result = []

        driver.execute_script("document.body.style.zoom='80%'")
        driver.execute_script("window.scrollBy(0, -200);")

        screenshot_path = os.path.join("screenshots", f"{name}.png")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Saved screenshot for {name}: {screenshot_path}")
        logger.info(f"Found {len(result)} timeslots for {name}: {result}")

    except Exception as e:
        print(f"An error occurred for {name}: {e}")
        logger.error(f"An error occurred for {name}: {e}")
        result = []

    finally:
        driver.quit()

    return result

async def check_all_courts(courts_file='tennis_reservations/config/courts.json'):
    """
    Loads all court URLs from the provided JSON file, retrieves timeslots for each,
    and returns the results.

    Args:
        courts_file (str): Path to the JSON file containing court names and URLs.

    Returns:
        dict: Dictionary mapping court names to lists of available timeslots.
    """
    with open(courts_file, 'r') as f:
        url_dict = json.load(f)

    os.makedirs("screenshots", exist_ok=True)
    tomorrow_str = get_tomorrow_label()
    results = {}

    for name, url in url_dict.items():
        results[name] = await get_timeslots_for_url(name, url, tomorrow_str)

    return results

async def run_reservation_check(channel, is_scheduled=False):
    """
    Runs the reservation check and sends results to the specified channel.
    
    Args:
        channel: Discord channel to send results to
        is_scheduled (bool): Whether this is a scheduled run or manual run
    """
    try:
        run_type = "scheduled" if is_scheduled else "manual"
        await channel.send(f'Starting {run_type} reservation retrieval...')
        logger.info(f'Starting {run_type} reservation retrieval...')

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
        logger.error(f"An error occurred in {run_type} reservation check: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await channel.send(f"An error occurred: {e}")

    logger.info(f'{run_type.capitalize()} script complete')

def create_scheduled_task(bot):
    """
    Creates and returns a scheduled task for the bot.
    
    Args:
        bot: Discord bot instance
        
    Returns:
        tasks.Loop: Scheduled task that runs reservation checks
    """
    from discord.ext import tasks
    
    @tasks.loop(minutes=1)
    async def scheduled_reservation_check():
        """
        Automatically runs the reservation check at 11:55 PM Pacific Time every night.
        Checks every minute to ensure precise timing.
        """
        pacific_tz = pytz.timezone('US/Pacific')
        now = datetime.now(pacific_tz)
        
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
                        await run_reservation_check(channel, is_scheduled=True)
                    else:
                        logger.error(f"Could not find channel with ID: {channel_id}")
                else:
                    logger.error("Tennis_Channel configuration not found in setup.json")
                            
            except Exception as e:
                logger.error(f"Error in scheduled reservation check: {e}")
    
    return scheduled_reservation_check

if __name__ == '__main__':
    start_time = time.time()
    results = asyncio.run(check_all_courts())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(results)
    print(f"Script completed in {elapsed_time:.2f} seconds")

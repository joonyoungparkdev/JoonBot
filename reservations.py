import json
import os
import time
import asyncio
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logger = logging.getLogger(__name__)

def setup_driver():
    """
    Sets up and returns a headless Chrome WebDriver with a predefined window size.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--log-level=3')  # Only fatal errors
    options.add_argument('--no-sandbox')  # Required for Heroku
    options.add_argument('--disable-dev-shm-usage')  # Required for Heroku
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--remote-debugging-port=9222')  # Required for Heroku
    # options.add_argument('--user-data-dir=/tmp/chrome-user-data')  # Unique user data directory
    options.add_argument('--disable-extensions')  # Disable extensions
    options.add_argument('--disable-plugins')  # Disable plugins
    service = Service()
    return webdriver.Chrome(service=service, options=options)

def get_tomorrow_label():
    """
    Returns the formatted date string for tomorrow to match the webpage's aria-label format.

    Returns:
        str: Date string formatted as 'Mon DD, YYYY' (e.g., 'Jun 23, 2025').
    """
    tomorrow = datetime.now() + timedelta(days=1)
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

async def check_all_courts(courts_file='config/courts.json'):
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

if __name__ == '__main__':
    start_time = time.time()
    results = asyncio.run(check_all_courts())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(results)
    print(f"Script completed in {elapsed_time:.2f} seconds")

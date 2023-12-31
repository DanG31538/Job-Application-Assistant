from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import applier  # assuming applier.py contains the necessary functions
import logging
import traceback

# Configure logging to write to a file
logging.basicConfig(filename='/app/logs/myapp.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def load_identifiers(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

identifiers = load_identifiers('identifiers.json')

EMAIL = os.getenv('LINKEDIN_EMAIL')
PASSWORD = os.getenv('LINKEDIN_PASSWORD')

def initialize_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def orchestrate(driver, identifiers):
    try:
        try:
            applier.login_to_linkedin(driver, EMAIL, PASSWORD, identifiers)
        except Exception as e:
            logging.error("Error during login: {}".format(e))
            traceback.print_exc()

        job_titles = [ "Machine Learning Engineer"]
        location = "New York City"

        for job_title in job_titles:
            try:
                applier.search_jobs(driver, job_title, location, identifiers)
                job_links = applier.get_job_links(driver, identifiers)

                for job_link in job_links:
                    try:
                        driver.get(job_link)
                        applier.apply_for_job(driver, identifiers)
                    except Exception as e:
                        logging.error(f"Error during applying for job at {job_link}: {e}")
                        traceback.print_exc()

            except Exception as e:
                logging.error(f"Error during job search for title '{job_title}': {e}")
                traceback.print_exc()

    except Exception as e:
        logging.error("An unexpected error occurred in orchestrate function: {}".format(e))
        traceback.print_exc()

if __name__ == '__main__':
    driver = initialize_driver()
    try:
        orchestrate(driver, identifiers)
    except Exception as e:
        logging.error("Failed to run orchestrate function")
        traceback.print_exc()
    # Note: driver.quit() is removed to keep the browser open

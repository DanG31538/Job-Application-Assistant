from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import pickle
import os

def load_identifiers(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def initialize_driver():
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def wait_for_verification(driver, identifiers, timeout=300):
    """
    Waits for the user to complete the verification step manually.
    The default timeout is 5 minutes (300 seconds).
    """
    try:
        verification_input_selector = identifiers['Login']['Verification']['Input Field']['Identifier']
        submit_button_selector = identifiers['Login']['Verification']['Submit Button']['Identifier']
        
        # Wait for the verification input field to be present
        verification_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, verification_input_selector))
        )
        print("Verification page detected.")

        # Ask user to input the verification code
        verification_code = input("Enter the verification code here: ")
        verification_input.send_keys(verification_code)

        # Click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, submit_button_selector)
        submit_button.click()
        print("Verification code submitted.")

    except TimeoutException:
        print("Verification element not found or timeout reached.")
    except Exception as e:
        print(f"An error occurred during verification: {e}")


def login_to_linkedin(driver, email, password, identifiers):
    try:
        cookies_path = 'path/to/cookies.pkl'  # Adjust this path as needed
        login_url = identifiers['Login']['URL']
        email_input_identifier = identifiers['Login']['Email/Username Input']['Identifier']
        password_input_identifier = identifiers['Login']['Password Input']['Identifier']
        sign_in_button_identifier = identifiers['Login']['Sign in Button']['Identifier']
        verification_input_selector = identifiers['Login']['Verification']['Input Field']['Identifier']
        submit_button_selector = identifiers['Login']['Verification']['Submit Button']['Identifier']

        driver.get(login_url)

        # Load cookies if they exist
        if os.path.exists(cookies_path):
            cookies = pickle.load(open(cookies_path, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()  # Refresh page to apply cookies
        else:
            # Normal login process
            username_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, email_input_identifier))
            )
            username_element.send_keys(email)

            password_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, password_input_identifier))
            )
            password_element.send_keys(password)

            sign_in_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sign_in_button_identifier))
            )
            sign_in_button.click()

            # Check for LinkedIn verification page
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, verification_input_selector))
                )
                verification_input = driver.find_element(By.CSS_SELECTOR, verification_input_selector)
                verification_code = input("Enter the verification code here: ")
                verification_input.send_keys(verification_code)

                submit_button = driver.find_element(By.CSS_SELECTOR, submit_button_selector)
                submit_button.click()
                print("Verification code submitted.")
            except TimeoutException:
                # If verification page is not detected, continue with the script
                print("No verification step detected. Proceeding...")

            # Ensure the directory for cookies exists before saving them
            cookies_dir = os.path.dirname(cookies_path)
            if not os.path.exists(cookies_dir):
                os.makedirs(cookies_dir)

            # Save cookies after successful login
            pickle.dump(driver.get_cookies(), open(cookies_path, "wb"))

    except WebDriverException as e:
        print(f"General WebDriver error during login: {e}")
        # Continue execution even if an error occurs




def search_jobs(driver, job_title, location, identifiers):
    try:
        # Navigate to LinkedIn home page
        driver.get("https://www.linkedin.com")

        # Click on 'Jobs' tab
        jobs_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Navigation']['Jobs Tab']['Identifier']))
        )
        jobs_tab.click()

        # Wait for the Jobs page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Job Title Input']['Identifier']))
        )

        # Input job title
        job_title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='Search by title, skill, or company']"))
        )
        job_title_input.send_keys(job_title)

        # Input location
        location_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='City, state, or zip code']"))
        )
        location_input.clear()
        location_input.send_keys(location)

        # Refocus on job title input and initiate search by pressing Enter
        job_title_input.click()
        job_title_input.send_keys(Keys.ENTER)


        # Click on 'All Filters'
        try:
            all_filters_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-reusables__all-filters-pill-button"))
            )
            all_filters_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error clicking on All Filters button: {e}")
            return  # Exit the function if unable to click on All Filters button

        # Check 'Full-time' option and click 'Show results'
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='f_WT'] + label"))
            ).click()

            show_results_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='all_filters_apply']"))
            )
            show_results_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error applying filters: {e}")
            return  # Exit the function if unable to apply filters

        # Check 'Remote' option and click 'Show results'
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='f_WRA'] + label"))
            ).click()

            show_results_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='all_filters_apply']"))
            )
            show_results_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error applying filters: {e}")
            return  # Exit the function if unable to apply filters

    except WebDriverException as e:
        print(f"General WebDriver error during job search: {e}")
        # Continue execution even if a general WebDriver exception occurs



def apply_filters(driver, identifiers):
    try:
        # Click on 'All Filters'
        try:
            all_filters_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers["Job Search"]["All Filters Button"]["Identifier"]))
            )
            all_filters_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error clicking 'All Filters': {e}")
            return  # Exit the function if unable to click 'All Filters'

        # Toggle 'Easy Apply' if not already enabled
        try:
            easy_apply_toggle = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers["Job Search"]["Easy Apply Toggle"]["Identifier"]))
            )
            if easy_apply_toggle.get_attribute('aria-checked') == 'false':
                easy_apply_toggle.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error toggling 'Easy Apply': {e}")
            return  # Exit the function if unable to toggle 'Easy Apply'

        # Click on 'Show results' button
        try:
            show_results_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers["Job Search"]["Show Results Button"]["Identifier"]))
            )
            show_results_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error clicking 'Show Results': {e}")
            return  # Exit the function if unable to click 'Show Results'

        # Click on 'Show results' button
        try:
            show_results_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers["Job Search"]["Show Results Button"]["Identifier"]))
            )
            show_results_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error clicking 'Show Results': {e}")
            return  # Exit the function if unable to click 'Show Results'

    except WebDriverException as e:
        print(f"General WebDriver error during applying filters: {e}")
        # Continue execution even if a general WebDriver exception occurs



def get_job_links(driver, identifiers):
    job_links = []

    try:
        while True:
            try:
                # Ensure the job listings have loaded
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, identifiers['Job Listing']['Listings Container']['Identifier']))
                )
                print("Job listings loaded successfully.")

                # Extract links from the current page
                job_listings = driver.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Listings Container']['Identifier'])
                for listing in job_listings:
                    try:
                        easy_apply_elements = listing.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Easy Apply Label']['Identifier'])
                        if easy_apply_elements:
                            link_element = listing.find_element(By.CSS_SELECTOR, identifiers['Job Listing']['Job Link']['Identifier'])
                            link = link_element.get_attribute('href')
                            if link:
                                job_links.append(link)
                    except NoSuchElementException:
                        print("No such element while extracting job links in current page.")
                        continue  # Continue with the next listing
                    except StaleElementReferenceException:
                        print("Stale element reference encountered while extracting job links.")
                        continue  # Continue with the next listing

                # Check for and navigate to the next page
                next_page_buttons = driver.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Next Page Button']['Identifier'])
                if not next_page_buttons:
                    print("No more pages to navigate. Exiting loop.")
                    break
                next_page_button = next_page_buttons[0]
                driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
                next_page_button.click()
            except TimeoutException:
                print("Timeout while waiting for job listings to load.")
                break  # Break the loop if the page times out

    except Exception as e:
        print(f"Unexpected error while extracting job links: {e}")
        # Continue execution even if an unexpected exception occurs

    return job_links


def search_and_apply_for_jobs(driver, job_titles, location, email, password):
    undesired_keywords = ["Staff", "Lead"]
    
    try:
        print("Logging into LinkedIn.")
        login_to_linkedin(driver, email, password)
        
        for job_title in job_titles:
            try:
                print(f"Searching for job title: {job_title}")
                search_jobs(driver, job_title, location)
            except Exception as e:
                print(f"Error during job search for title '{job_title}': {e}")
                continue  # Continue with the next job title if an error occurs

            print("Retrieving job links.")
            job_links = get_job_links(driver)
            if not job_links:
                print("No job links found. Moving to next job title.")
                continue  # Continue with the next job title if no job links are found

            for job_link in job_links:
                try:
                    print(f"Navigating to job link: {job_link}")
                    driver.get(job_link)
                    
                    job_page_title = driver.title
                    print(f"Job page title: {job_page_title}")
                    
                    if any(keyword in job_page_title for keyword in undesired_keywords):
                        print(f"Skipping job due to undesired keyword in title: {job_page_title}")
                        continue  # Continue with the next job link if undesired keyword found
                    
                    print("Applying for job.")
                    apply_for_job(driver)
                
                except Exception as e:
                    print(f"Error while applying for job at {job_link}: {e}")
                    continue  # Continue with the next job link if an error occurs during application
    
    except Exception as e:
        print(f"Error logging into LinkedIn: {e}")
        # Continue execution even if an error occurs during login




# Sample usage:
#job_titles = ["machine learning engineer", "learning engineer", "engineer"]
#search_and_apply_for_jobs(driver, job_titles, "desired_location", "your_email", "your_password")




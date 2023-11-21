from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

def load_identifiers(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def initialize_driver():
    try:
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        return driver
    except WebDriverException as e:
        print(f"Error initializing the Chrome WebDriver: {e}")
        return None
    
def login_to_linkedin(driver, email, password, identifiers):
    try:
        login_url = identifiers['Login']['URL']
        email_input_identifier = identifiers['Login']['Email/Username Input']['Identifier']
        password_input_identifier = identifiers['Login']['Password Input']['Identifier']
        sign_in_button_identifier = identifiers['Login']['Sign in Button']['Identifier']

        driver.get(login_url)
        try:
            username_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, email_input_identifier)))
            username_element.send_keys(email)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding email input field: {e}")
            return

        try:
            password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, password_input_identifier)))
            password_element.send_keys(password)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding password input field: {e}")
            return

        try:
            sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sign_in_button_identifier)))
            sign_in_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or clicking the sign-in button: {e}")
            return

    except WebDriverException as e:
        print(f"General WebDriver error during login: {e}")

def search_jobs(driver, job_title, location, identifiers):
    try:
        driver.get(identifiers['Job Search']['URL'])
        
        try:
            job_title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Job Title Input']['Identifier']))
            )
            job_title_input.send_keys(job_title)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding job title input field: {e}")
            return

        try:
            magnifying_glass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Magnifying Glass (Initialize Search Fields) Icon']['Identifier']))
            )
            magnifying_glass.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or clicking the magnifying glass icon: {e}")
            return

        try:
            location_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Location Input']['Identifier']))
            )
            location_input.send_keys(location)
            location_input.send_keys(Keys.ENTER)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or using the location input field: {e}")
            return

        try:
            all_filters_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['All Filters Button']['Identifier']))
            )
            all_filters_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or clicking the 'All Filters' button: {e}")
            return

        try:
            easy_apply_toggle = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Easy Apply Toggle']['Identifier']))
            )
            if easy_apply_toggle.get_attribute('aria-checked') == 'false':
                easy_apply_toggle.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or using the 'Easy Apply' toggle: {e}")
            return

        try:
            show_results_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-reusables-filters-modal-show-results-button='true']"))
            )
            show_results_btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding or clicking the 'Show Results' button: {e}")
            return

    except WebDriverException as e:
        print(f"General WebDriver error during job search: {e}")


def apply_filters(driver, identifiers):
    try:
        # Try to retrieve the 'Show Results' button identifier
        try:
            show_results_button_id = identifiers["Job Search"]["Show Results Button"]["Identifier"]
        except KeyError as e:
            print(f"Error finding 'Show Results' button identifier in JSON: {e}")
            return

        # Try to find and click the 'Show Results' button
        try:
            show_results_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, show_results_button_id))
            )
            show_results_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error during applying filters: {e}")
            return

    except WebDriverException as e:
        print(f"General WebDriver error during applying filters: {e}")

def get_job_links(driver, identifiers):
    job_links = []
    
    try:
        while True:  # Continue looping as long as there's a next page
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
                            if link:  # Ensure the link is not None
                                job_links.append(link)
                    except NoSuchElementException:
                        print("No such element while extracting job links in current page.")
                    except StaleElementReferenceException:
                        print("Stale element reference encountered while extracting job links.")

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
                break

    except Exception as e:
        print(f"Unexpected error while extracting job links: {e}")

    return job_links



def apply_for_job(driver, identifiers):
    try:
        # Click Easy Apply button
        easy_apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Easy Apply Button']['Identifier']))
        )
        easy_apply_button.click()
        print("Clicked Easy Apply button.")

        # Fill out form fields
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Apply for Job']['Form Fields']['Email Address']['Identifier']))
        )
        email_input.send_keys('dangarcia31538@gmail.com')  # Replace with actual email
        
        # Additional form fields logic here...

        # Click next button after filling out fields
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Next Button']['Identifier']))
        )
        next_button.click()
        print("Clicked Next button.")

        # Review and submission process
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Review Button']['Identifier']))
        )
        review_button.click()
        print("Clicked Review button.")

        # Uncheck "Follow Company" toggle
        follow_company_toggle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Apply for Job']['Follow Company Toggle']['Identifier']))
        )
        if follow_company_toggle.is_selected():
            follow_company_toggle.click()
            print("Unchecked Follow Company toggle.")

        # Submit Application
        submit_application_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Submit Application Button']['Identifier']))
        )
        submit_application_button.click()
        print("Submitted application.")

    except NoSuchElementException:
        print("Element not found while applying for the job.")
    except TimeoutException:
        print("Timeout occurred while applying for the job.")
    except StaleElementReferenceException:
        print("Stale element reference encountered while applying for the job.")
    except Exception as e:
        print(f"Unexpected error while applying for the job: {e}")


def search_and_apply_for_jobs(driver, job_titles, location, email, password):
    undesired_keywords = ["Staff", "Lead"]
    
    try:
        print("Logging into LinkedIn.")
        login_to_linkedin(driver, email, password)
        
        for job_title in job_titles:
            try:
                print(f"Searching for job title: {job_title}")
                search_jobs(driver, job_title, location)
                
                print("Retrieving job links.")
                job_links = get_job_links(driver)
                
                for job_link in job_links:
                    try:
                        print(f"Navigating to job link: {job_link}")
                        driver.get(job_link)
                        
                        job_page_title = driver.title
                        print(f"Job page title: {job_page_title}")
                        
                        if any(keyword in job_page_title for keyword in undesired_keywords):
                            print(f"Skipping job due to undesired keyword in title: {job_page_title}")
                            continue
                        
                        print("Applying for job.")
                        apply_for_job(driver)
                    
                    except Exception as e:
                        print(f"Error while applying for job at {job_link}: {e}")
                
            except Exception as e:
                print(f"Error during job search for title '{job_title}': {e}")
    
    except Exception as e:
        print(f"Error logging into LinkedIn: {e}")



# Sample usage:
#job_titles = ["machine learning engineer", "learning engineer", "engineer"]
#search_and_apply_for_jobs(driver, job_titles, "desired_location", "your_email", "your_password")




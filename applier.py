from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException,NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

# Load the JSON data from the file
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
    
def login_to_linkedin(driver, email, password):
    try:
        # Use the identifiers from the JSON file
        login_url = identifiers['Login']['URL']
        email_input_identifier = identifiers['Login']['Email/Username Input']['Identifier']
        password_input_identifier = identifiers['Login']['Password Input']['Identifier']
        sign_in_button_identifier = identifiers['Login']['Sign in Button']['Identifier']

        driver.get(login_url)
        
        # Wait and input email
        username_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'LOGIN_EMAIL_PLACEHOLDER')))
        username_element.send_keys(email)
        
        # Wait and input password
        password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'LOGIN_PASSWORD_PLACEHOLDER')))
        password_element.send_keys(password)
        
        # Wait and click sign-in
        sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'LOGIN_SIGNINBTN_PLACEHOLDER')))
        sign_in_button.click()
        
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during login: {e}")

def search_jobs(driver, job_title, location, identifiers):
    try:
        # Navigate to the job search page
        driver.get(identifiers['Job Search']['URL'])
        
        # Wait and input job title
        job_title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Job Title Input']['Identifier']))
        )
        job_title_input.send_keys(job_title)
        
        # Wait and click magnifying glass to initiate search
        magnifying_glass = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Magnifying Glass (Initialize Search Fields) Icon']['Identifier']))
        )
        magnifying_glass.click()
        
        # Wait and input location
        location_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Location Input']['Identifier']))
        )
        location_input.send_keys(location)
        location_input.send_keys(Keys.ENTER)  # Press Enter to initiate search
        
        # Wait for and click the "All Filters" button
        all_filters_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['All Filters Button']['Identifier']))
        )
        all_filters_btn.click()
        
        # Wait for and toggle the "Easy Apply" switch
        easy_apply_toggle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Job Search']['Easy Apply Toggle']['Identifier']))
        )
        # Check if the toggle is off, then click to turn it on
        if easy_apply_toggle.get_attribute('aria-checked') == 'false':
            easy_apply_toggle.click()

        # Wait for and click the "Show Results" button to apply the filters
        show_results_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-reusables-filters-modal-show-results-button='true']"))  # Using a data attribute for selection
        )
        show_results_btn.click()

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during job search: {e}")

def apply_filters(driver, identifiers):
    try:
        # Retrieve the identifier for 'Show Results' button from the JSON
        show_results_button_id = identifiers["Job Search"]["Show Results Button"]["Identifier"]
        
        # Wait and click 'Show Results' button using its identifier from the JSON
        show_results_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, show_results_button_id)))
        show_results_button.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during applying filters: {e}")

def get_job_links(driver, identifiers):
    job_links = []
    
    # Continue looping as long as there's a next page
    while True:
        try:
            # Use WebDriverWait to ensure the job listings have loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, identifiers['Job Listing']['Listings Container']['Identifier']))
            )
            
            # Extract links from the current page
            job_listings = driver.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Listings Container']['Identifier'])
            for listing in job_listings:
                # Check if the listing has an "Easy Apply" label
                easy_apply_elements = listing.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Easy Apply Label']['Identifier'])
                if easy_apply_elements:
                    link_element = listing.find_element(By.CSS_SELECTOR, identifiers['Job Listing']['Job Link']['Identifier'])
                    link = link_element.get_attribute('href')
                    if link:  # Ensure the link is not None
                        job_links.append(link)
            
            # Check if there's a next page. If not, break out of the loop.
            next_page_buttons = driver.find_elements(By.CSS_SELECTOR, identifiers['Job Listing']['Next Page Button']['Identifier'])
            if not next_page_buttons:
                break
            
            # Navigate to the next page
            next_page_button = next_page_buttons[0]
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)  # Scroll the next page button into view
            next_page_button.click()
        
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error while extracting job links: {e}")
            break  # If there's an error, break out of the loop to prevent infinite looping

    return job_links


def apply_for_job(driver, identifiers):
    try:
        # Wait and click Easy Apply button
        easy_apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Easy Apply Button']['Identifier']))
        )
        easy_apply_button.click()
        
        # Fill out the form fields using the provided identifiers
        # Example for email, you will need to repeat this for each form field:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Apply for Job']['Form Fields']['Email Address']['Identifier']))
        )
        email_input.send_keys('dangarcia31538@gmail.com')  # Replace with actual email or variable
        
        # ... logic for filling out other fields ...
        
        # Logic for resume upload (if applicable):
        #resume_upload = WebDriverWait(driver, 10).until(
            #EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Apply for Job']['Resume Upload']['Identifier']))
        #)
        #resume_upload.send_keys('/path/to/your/resume.pdf')  # Replace with the actual path to the resume file
        
        # Click next button after filling out fields
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Next Button']['Identifier']))
        )
        next_button.click()
        
        # Logic to handle review and submission process
        # Click Review button if needed
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Review Button']['Identifier']))
        )
        review_button.click()
        
        # Logic to uncheck "Follow Company" toggle if it's checked by default
        follow_company_toggle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, identifiers['Apply for Job']['Follow Company Toggle']['Identifier']))
        )
        if follow_company_toggle.is_selected():
            follow_company_toggle.click()

        # Click Submit Application button
        submit_application_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, identifiers['Apply for Job']['Submit Application Button']['Identifier']))
        )
        submit_application_button.click()
    
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
        print(f"Error while applying for the job: {e}")

def search_and_apply_for_jobs(driver, job_titles, location, email, password):
    undesired_keywords = ["Staff", "Lead"]
    
    try:
        # Login to LinkedIn
        login_to_linkedin(driver, email, password)
        
        for job_title in job_titles:
            try:
                # Search for the current job title
                search_jobs(driver, job_title, location)
                
                # Get job links for the current search results
                job_links = get_job_links(driver)
                
                for job_link in job_links:
                    try:
                        # Navigate to the job's page
                        driver.get(job_link)
                        
                        # Extract the job title from the page
                        job_page_title = driver.title
                        
                        # Check if the job title contains undesired keywords
                        if any(keyword in job_page_title for keyword in undesired_keywords):
                            continue
                        
                        # Apply for the job
                        apply_for_job(driver)
                    
                    except Exception as e:
                        print(f"Error while applying for job {job_link}: {e}")
                
            except Exception as e:
                print(f"Error during job search for title '{job_title}': {e}")
    
    except Exception as e:
        print(f"Login error: {e}")


# Sample usage:
#job_titles = ["machine learning engineer", "learning engineer", "engineer"]
#search_and_apply_for_jobs(driver, job_titles, "desired_location", "your_email", "your_password")




from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException,NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
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
        username_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, email_input_identifier)))
        username_element.send_keys(email)
        
        # Wait and input password
        password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, password_input_identifier)))
        password_element.send_keys(password)
        
        # Wait and click sign-in
        sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, sign_in_button_identifier)))
        sign_in_button.click()
        
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during login: {e}")
def search_jobs(driver, job_title, location):
    try:
        # Use the identifiers from the JSON file
        search_url = identifiers['Job Search']['URL']
        job_title_input_identifier = identifiers['Job Search']['Job Title Input']['Identifier']
        magnifying_glass_identifier = identifiers['Job Search']['Magnifying Glass (Initialize Search Fields) Icon']['Identifier']
        location_input_identifier = identifiers['Job Search']['Location Input']['Identifier']
        initiate_search_identifier = identifiers['Job Search']['Initiate Search']['Identifier']

        driver.get(search_url)
        
        # Wait and input job title
        job_title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, job_title_input_identifier)))
        job_title_input.send_keys(job_title)
        
        # Wait and click magnifying glass
        magnifying_glass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, magnifying_glass_identifier)))
        magnifying_glass.click()
        
        # Wait and input location
        location_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, location_input_identifier)))
        location_input.send_keys(location)
        
        # Wait and click initiate search
        initiate_search_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, initiate_search_identifier)))  # Assuming it's an XPATH
        initiate_search_btn.click()
        
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during job search: {e}")


def get_job_links(driver):
    job_links = []
    
    # Use the identifiers from the JSON file
    job_listing_container_identifier = identifiers['Iterate Through Job Listings']['Job Link']['Identifier']
    next_page_button_identifier = identifiers['Iterate Through Job Listings']['Next Page Button']['Identifier']  # Assuming you add this identifier to the JSON

    # Continue looping as long as there's a next page
    while True:
        try:
            # Use WebDriverWait to ensure the job listings have loaded
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, job_listing_container_identifier)))
            
            # Extract links from the current page
            job_links_elements = driver.find_elements(By.ID, job_listing_container_identifier)
            for link_element in job_links_elements:
                link = link_element.get_attribute('href')
                if link:  # Ensure the link is not None
                    job_links.append(link)
            
            # Check if there's a next page. If not, break out of the loop.
            next_page_buttons = driver.find_elements(By.ID, next_page_button_identifier)
            if not next_page_buttons:
                break
            
            # Navigate to the next page
            next_page_buttons[0].click()
        
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error while extracting job links: {e}")
            break  # If there's an error, break out of the loop to prevent infinite looping

    return job_links

def apply_for_job(driver):
    try:
        # Use the identifiers from the JSON file
        easy_apply_button_identifier = identifiers['Apply for Job']['Easy Apply Button']['Identifier']
        email_input_identifier = identifiers['Apply for Job']['Form Fields']['Email Address']['Identifier']
        phone_code_input_identifier = identifiers['Apply for Job']['Form Fields']['Phone Country Code']['Identifier']
        phone_number_input_identifier = identifiers['Apply for Job']['Form Fields']['Mobile Phone Number']['Identifier']
        next_button_identifier = identifiers['Apply for Job']['Form Fields']['Next Button']['Identifier']
        resume_upload_identifier = identifiers['Apply for Job']['Form Fields']['Resume']['Upload']['Identifier']
        next_button_after_upload_identifier = identifiers['Apply for Job']['Form Fields']['Resume']['Next']['Identifier']
        
        # Values provided from the JSON or elsewhere
        email_input_value = identifiers['Apply for Job']['Form Fields']['Email Address']['Value']
        phone_code_input_value = identifiers['Apply for Job']['Form Fields']['Phone Country Code']['Value']
        phone_number_input_value = identifiers['Apply for Job']['Form Fields']['Mobile Phone Number']['Value']
        resume_file_path = identifiers['Apply for Job']['Form Fields']['Resume']['Upload']['FilePath']

        # Wait and click Easy Apply button
        easy_apply_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, easy_apply_button_identifier)))
        easy_apply_button.click()
        
        # Fill out the form
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, email_input_identifier)))
        email_input.send_keys(email_input_value)
        
        phone_code_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, phone_code_input_identifier)))
        phone_code_input.send_keys(phone_code_input_value)
        
        phone_number_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, phone_number_input_identifier)))
        phone_number_input.send_keys(phone_number_input_value)
        
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, next_button_identifier)))
        next_button.click()

        # Resume upload
        resume_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, resume_upload_identifier)))
        resume_upload.send_keys(resume_file_path)
        
        next_button_after_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, next_button_after_upload_identifier)))
        next_button_after_upload.click()
    
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




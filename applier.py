from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException,NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

def initialize_driver():
    try:
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        return driver
    except WebDriverException as e:
        print(f"Error initializing the Chrome WebDriver: {e}")
        return None
    
def login_to_linkedin(driver, email, password):
    try:
        driver.get('LOGIN_URL_PLACEHOLDER')
        
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

def search_jobs(driver, job_title, location):
    try:
        driver.get('JOBSEARCH_URL_PLACEHOLDER')
        
        # Wait and input job title
        job_title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'JOBSEARCH_TITLE_PLACEHOLDER')))
        job_title_input.send_keys(job_title)
        
        # Wait and click magnifying glass
        magnifying_glass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'JOBSEARCH_MAGNIFYINGGLASS_PLACEHOLDER')))
        magnifying_glass.click()
        
        # Wait and input location
        location_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'JOBSEARCH_LOCATION_PLACEHOLDER')))
        location_input.send_keys(location)
        
        # Wait and click initiate search
        initiate_search_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'JOBSEARCH_INITIATESEARCH_PLACEHOLDER')))
        initiate_search_btn.click()
        
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during job search: {e}")

def get_job_links(driver):
    job_links = []
    
    # Continue looping as long as there's a next page
    while True:
        try:
            # Use WebDriverWait to ensure the job listings have loaded
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'JOBLISTING_CONTAINER_PLACEHOLDER')))
            
            # Extract links from the current page
            job_links_elements = driver.find_elements(By.ID, 'JOBLISTING_JOB_LINK_PLACEHOLDER')
            for link_element in job_links_elements:
                link = link_element.get_attribute('href')
                if link:  # Ensure the link is not None
                    job_links.append(link)
            
            # Check if there's a next page. If not, break out of the loop.
            next_page_buttons = driver.find_elements(By.ID, 'NEXT_PAGE_BUTTON_PLACEHOLDER')
            if not next_page_buttons:
                break
            
            # Navigate to the next page
            next_page_buttons[0].click()
        
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error while extracting job links: {e}")
            break  # If there's an error, break out of the loop to prevent infinite looping

    return job_links

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

def apply_for_job(driver):
    try:
        # Wait and click Easy Apply button
        easy_apply_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLY_EASYAPPLYBTN_PLACEHOLDER')))
        easy_apply_button.click()
        
        # Logic to fill out the form. Placeholder for some fields:
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_EMAIL_PLACEHOLDER')))
        email_input.send_keys('APPLYFORM_EMAIL_VALUE_PLACEHOLDER')
        
        phone_code_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_PHONECODE_PLACEHOLDER')))
        phone_code_input.send_keys('APPLYFORM_PHONECODE_VALUE_PLACEHOLDER')
        
        phone_number_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_PHONENUMBER_PLACEHOLDER')))
        phone_number_input.send_keys('APPLYFORM_PHONENUMBER_VALUE_PLACEHOLDER')
        
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_NEXTBTN_PLACEHOLDER')))
        next_button.click()

        # Logic for resume upload:
        resume_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_RESUME_UPLOAD_PLACEHOLDER')))
        resume_upload.send_keys('PATH_TO_RESUME_FILE_PLACEHOLDER')
        
        next_button_after_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'APPLYFORM_AFTERUPLOAD_NEXTBTN_PLACEHOLDER')))
        next_button_after_upload.click()
    
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
        print(f"Error while applying for the job: {e}")


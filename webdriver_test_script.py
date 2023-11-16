from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_chrome():
    options = webdriver.ChromeOptions()
    # Specify the path to the Chromium binary
    options.binary_location = "/path/to/chromium"  # Replace with the actual path
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()

if __name__ == "__main__":
    test_chrome()

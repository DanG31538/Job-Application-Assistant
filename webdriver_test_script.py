from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def test_chrome():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()

if __name__ == "__main__":
    test_chrome()

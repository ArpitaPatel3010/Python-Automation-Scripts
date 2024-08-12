
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def login_automation():
    # Configuration
    email = "your_email@example.com"
    password = "your_password"
    login_url = "your_login_url"
    dashboard_url = "your_dashboard_url"
    driver_path = '/usr/local/bin/chromedriver'  # Path to your chromedriver executable
    driver_close_flag = 0
    should_driver_reason = "NA"
    wrong_credentials = 0
    # Options and capabilities for Chrome
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Service and Driver Initialization
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.set_script_timeout(180)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })
        
        driver.get(login_url)

        # Wait until the login form is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='authentication-username']//input[@type='text']"))
        )
        
        # Enter email
        email_element = driver.find_element(By.XPATH, "//div[@class='authentication-username']//input[@type='text']")
        email_element.clear()
        email_element.send_keys(email)

        # Enter password
        password_element = driver.find_element(By.XPATH, "//div[@class='authentication-password']//input[@type='password']")
        password_element.clear()
        password_element.send_keys(password)

        # Optionally click the remember me checkbox
        try:
            remember_button = driver.find_element(By.XPATH, "//form[@class='login__form']//input[@type='checkbox']")
            remember_button.click()
        except NoSuchElementException:
            print("Remember me checkbox not found")

        # Submit the login form
        submit_button = driver.find_element(By.XPATH, "//form[@class='login__form']//button")
        submit_button.click()

        # Wait for a response to check if login was successful
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.login__form span[color=danger]'))
        )

        try:
            authentication_text = driver.find_element(By.CSS_SELECTOR, '.login__form span[color=danger]').text
            if authentication_text and "The username and password you entered did not match our records" in authentication_text:
                print("Wrong username and password")
                wrong_credentials = 1
                driver_close_flag = 1
                if driver_close_flag == 1:
                    driver.close()
            else:
                if dashboard_url == driver.current_url:
                    print("Welcome to Dashboard , you are successfully logged in")
                    wrong_credentials = 0
                    driver_close_flag = 0

            
            
        except NoSuchElementException:
            print("Login successful or unexpected page state")

    except WebDriverException as e:
        print(f"WebDriverException: {e}")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    login_automation()
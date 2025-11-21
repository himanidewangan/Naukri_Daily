import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------
# CONFIG
# ----------------------

NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.path.abspath("resume.pdf")

# ----------------------
# BROWSER SETUP
# ----------------------

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")

    # Headless when running inside CI
    if os.getenv("CI"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)

# ----------------------
# AUTOMATION
# ----------------------

def upload_resume():
    print("Starting Naukri automation...")

    if not os.path.exists(RESUME_PATH):
        print("ERROR: Resume file not found:", RESUME_PATH)
        return

    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    try:
        # Login Page
        driver.get("https://www.naukri.com/nlogin/login")
        print("Opened login page")

        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(NAUKRI_EMAIL)
        wait.until(EC.presence_of_element_located((By.ID, "passwordField"))).send_keys(NAUKRI_PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Logged in successfully")

        # Go to Profile Page
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'profile')]"))).click()
        print("Opening profile page...")

        # Upload Resume
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        upload_input.send_keys(RESUME_PATH)
        print("Resume uploaded successfully!")

        # Wait to ensure upload completes
        time.sleep(5)

    except Exception as e:
        print("ERROR:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    upload_resume()

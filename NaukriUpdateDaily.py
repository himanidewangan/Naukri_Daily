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

NAUKRI_EMAIL = os.getenv("EMAIL")
NAUKRI_PASSWORD = os.getenv("PASSWORD")
RESUME_PATH = os.path.abspath("HimaniCV.pdf")

# ----------------------
# BROWSER SETUP
# ----------------------

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Headless mode for GitHub Actions CI
    if os.getenv("CI"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)

# ----------------------
# AUTOMATION LOGIC
# ----------------------

def upload_resume():
    print("Starting Naukri automation...")

    if not os.path.exists(RESUME_PATH):
        print("❌ ERROR: Resume file not found:", RESUME_PATH)
        return

    driver = get_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # 1. Open Login Page
        driver.get("https://www.naukri.com/nlogin/login")
        print("Opened login page")

        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(NAUKRI_EMAIL)
        wait.until(EC.presence_of_element_located((By.ID, "passwordField"))).send_keys(NAUKRI_PASSWORD)

        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Logged in successfully")

        # 2. Go to Profile Page
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href,'profile')]")
        )).click()
        print("Opening profile page...")

        time.sleep(5)

        # 3. Upload Resume (correct locator)
        upload_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='attachCV']"))
        )

        upload_input.send_keys(RESUME_PATH)
        print("Resume upload command executed!")

        time.sleep(6)
        print("Resume uploaded successfully!")

    except Exception as e:
        print("❌ ERROR:", e)

    finally:
        driver.quit()


# ----------------------
# RUN SCRIPT
# ----------------------

if __name__ == "__main__":
    upload_resume()

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NAUKRI_EMAIL = os.getenv("EMAIL")
NAUKRI_PASSWORD = os.getenv("PASSWORD")
RESUME_PATH = os.path.abspath("HimaniCV.pdf")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")

    if os.getenv("CI"):
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def upload_resume():
    print("🚀 Starting automation...")

    if not os.path.exists(RESUME_PATH):
        print("❌ Resume not found:", RESUME_PATH)
        return

    driver = get_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # Login
        driver.get("https://www.naukri.com/nlogin/login")
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(NAUKRI_EMAIL)
        wait.until(EC.presence_of_element_located((By.ID, "passwordField"))).send_keys(NAUKRI_PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("✔ Logged in")

        # Open Profile Page
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'profile')]"))).click()
        print("✔ Profile page opened")

        time.sleep(5)

        # Make input visible (Naukri hides it)
        driver.execute_script("""
            let fi = document.querySelector('#attachCV');
            if (fi) {
                fi.style.display = 'block';
                fi.style.visibility = 'visible';
                fi.style.opacity = 1;
            }
        """)

        time.sleep(1)

        # Upload resume
        upload_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#attachCV")))
        upload_box.send_keys(RESUME_PATH)
        print("✔ File path sent to upload input")

        time.sleep(3)

        # Trigger Naukri internal resume upload JS function
        driver.execute_script("""
            if (typeof UploadCV !== 'undefined') {
                UploadCV();
            }
        """)
        print("✔ JavaScript upload triggered")

        time.sleep(8)

        print("🎉 Resume uploaded successfully!")

    except Exception as e:
        print("❌ ERROR:", e)
        driver.save_screenshot("error.png")

    finally:
        driver.quit()



if __name__ == "__main__":
    upload_resume()

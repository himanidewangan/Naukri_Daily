import os
import time
from playwright.sync_api import sync_playwright

NAUKRI_EMAIL = os.getenv("EMAIL")
NAUKRI_PASSWORD = os.getenv("PASSWORD")
RESUME_PATH = os.path.abspath("HimaniCV.pdf")

def run():
    print("Starting Playwright...")

    if not os.path.exists(RESUME_PATH):
        print("❌ Resume file not found:", RESUME_PATH)
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # IMPORTANT: not headless
        context = browser.new_context()
        page = context.new_page()

        print("Opening Naukri login page...")
        page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

        page.fill("#usernameField", NAUKRI_EMAIL)
        page.fill("#passwordField", NAUKRI_PASSWORD)
        page.click("text=Login")

        print("Logging in...")
        page.wait_for_timeout(5000)

        print("Opening profile page...")
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)

        print("Uploading resume...")
        page.set_input_files("input[type='file']", RESUME_PATH)

        print("Waiting for upload to complete...")
        time.sleep(6)

        print("✔ Resume uploaded successfully!")

        browser.close()

if __name__ == "__main__":
    run()

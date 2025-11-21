import os
from playwright.sync_api import sync_playwright
import time

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Your resume file (make sure workflow downloads it)
RESUME_PATH = "HimaniCV.pdf"


def run():
    with sync_playwright() as p:
        print("Starting Playwright...")

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Opening login page…")
        page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

        # Wait for username field to load
        page.wait_for_selector("input[placeholder='Enter your active Email ID / Username']", timeout=40000)

        print("Filling login credentials…")
        page.fill("input[placeholder='Enter your active Email ID / Username']", EMAIL)
        page.fill("input[placeholder='Enter your password']", PASSWORD)

        print("Clicking login button…")
        page.click("button[type='submit']")

        # Wait for login redirect
        page.wait_for_load_state("networkidle")
        time.sleep(5)

        print("Logged in successfully!")

        # Go to the profile page
        print("Opening profile page…")
        page.goto("https://www.naukri.com/mnjuser/profile", timeout=60000)
        page.wait_for_load_state("networkidle")
        time.sleep(5)

        # Upload resume
        print("Uploading resume…")
        page.set_input_files("input[type='file']", RESUME_PATH)

        time.sleep(5)

        print("Resume upload completed!")

        browser.close()


if __name__ == "__main__":
    run()

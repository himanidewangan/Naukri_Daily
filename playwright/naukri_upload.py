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
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening login page...")
        page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

        # Login
        page.fill("#usernameField", NAUKRI_EMAIL)
        page.fill("#passwordField", NAUKRI_PASSWORD)
        page.click("button[type='submit']")
        print("Logged in... waiting for redirect")

        page.wait_for_timeout(6000)

        # Open Main Home Page (safe)
        page.goto("https://www.naukri.com", timeout=60000)

        # Click My Profile from top-right menu
        print("Clicking My Profile…")
        page.click("img[alt='naukri user profile']")

        page.wait_for_timeout(5000)

        # Click “View & Update Profile”
        print("Opening profile editor…")
        page.click("text=View & Update Profile")

        page.wait_for_timeout(6000)

        # Scroll to resume section
        print("Scrolling to resume upload...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        # Upload resume
        print("Uploading resume...")
        page.set_input_files("input[type='file']", RESUME_PATH)

        print("Waiting for upload to finish…")
        time.sleep(8)
        print("✔ Resume uploaded successfully!")

        browser.close()

if __name__ == "__main__":
    run()

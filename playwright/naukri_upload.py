import os
import time
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RESUME_PATH = os.path.abspath("HimaniCV.pdf")

def run():
    print("Starting Playwright...")

    if not os.path.exists(RESUME_PATH):
        print("❌ Resume file not found:", RESUME_PATH)
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-http2"])
        context = browser.new_context()
        page = context.new_page()

        print("Opening login page…")
        page.goto("https://www.naukri.com/nlogin/login")

        # Login
        page.fill("#usernameField", EMAIL)
        page.fill("#passwordField", PASSWORD)
        page.click("button[type='submit']")
        print("Logged in… waiting for home page…")

        page.wait_for_timeout(8000)

        # Click profile icon (top right)
        print("Clicking profile icon…")
        page.click("img[alt='naukri user profile']")

        page.wait_for_timeout(5000)

        # Click "View & Update Profile"
        print("Opening profile editor…")
        page.click("text=View & Update Profile")

        page.wait_for_timeout(8000)

        # Scroll to resume upload input
        print("Scrolling…")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)

        print("Uploading resume…")
        page.set_input_files("input[type='file']", RESUME_PATH)

        print("Waiting for upload…")
        time.sleep(10)

        print("✔ SUCCESS: Resume uploaded!")

        browser.close()


if __name__ == "__main__":
    run()

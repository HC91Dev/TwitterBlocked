import sys
import asyncio
import json
import time
import os
import platform
from pyppeteer import launch
import traceback
from PyQt5 import QtWidgets, QtCore, QtGui


# Twitter blocklist URL
BLOCKLIST_URL = "https://x.com/settings/blocked/all"

def find_chrome_path():
    """Detect the OS and return the path to Chrome."""
    system = platform.system()
    
    # Check for Chrome on Linux
    if system == "Linux":
        paths = [
            "/usr/bin/google-chrome",  # Common path for Chrome on Linux
            "/opt/google/chrome/google-chrome"  # Your current path
        ]
    
    # Check for Chrome on Windows
    elif system == "Windows":
        paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]

    # Check if any of the paths exist
    for path in paths:
        if os.path.exists(path):
            return path
    
    # If no path is found, return None
    return None

# PyQt Window Class
class TwitterBlocklistScraper(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the GUI components
        self.setWindowTitle("Twitter Blocklist Scraper")
        self.setGeometry(100, 100, 400, 400)

        layout = QtWidgets.QVBoxLayout()

        self.title = QtWidgets.QLabel("Twitter Blocklist Scraper", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Helvetica", 15))
        layout.addWidget(self.title)

        self.username_label = QtWidgets.QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_input = QtWidgets.QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QtWidgets.QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Headless mode checkbox
        self.headless_checkbox = QtWidgets.QCheckBox("Run in headless mode")
        self.headless_checkbox.setChecked(True)  # Default to headless mode enabled
        layout.addWidget(self.headless_checkbox)

        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.start_button = QtWidgets.QPushButton("Start Scraping", self)
        self.start_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.start_button)

        self.exit_button = QtWidgets.QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def log_message(self, message):
        """Log messages to the GUI."""
        self.log_output.append(message)
        self.log_output.repaint()

    async def login(self, page, username, password):
        """Log in to Twitter using provided username and password."""
        try:
            self.log_message("Navigating to Twitter login page...")
            await page.goto('https://x.com/login', {'waitUntil': 'networkidle2'})

            # Wait for the username input and type the username
            self.log_message("Entering username...")
            await page.waitForSelector('input[name="text"]')
            await page.type('input[name="text"]', username)

            # Click the "Next" button after entering the username
            self.log_message("Clicking Next button after entering username...")
            next_button = await page.xpath('//span[contains(text(), "Next")]')
            if next_button:
                await next_button[0].click()
            else:
                self.log_message("Error: 'Next' button not found.")
                return

            await asyncio.sleep(3)  # Wait for the next page to load

            # Wait for the password input and type the password
            self.log_message("Entering password...")
            await page.waitForSelector('input[name="password"]')
            await page.type('input[name="password"]', password)

            # Click the "Log in" button after entering the password
            self.log_message("Clicking Log in button after entering password...")
            login_button = await page.xpath('//span[contains(text(), "Log in")]')
            if login_button:
                await login_button[0].click()
            else:
                self.log_message("Error: 'Log in' button not found.")
                return

            await page.waitForNavigation({'waitUntil': 'networkidle2'})
            self.log_message("Logged in successfully!")
        except Exception as e:
            self.log_message(f"Error during login: {e}")
            traceback.print_exc()

    async def dismiss_cookie_popup(self, page):
        """Dismiss the cookie consent popup by clicking 'Refuse non-essential cookies'."""
        try:
            self.log_message("Looking for 'Refuse non-essential cookies' button...")
            # Wait for the cookie consent button
            refuse_button = await page.xpath('//span[contains(text(), "Refuse non-essential cookies")]')
            if refuse_button:
                await refuse_button[0].click()
                self.log_message("'Refuse non-essential cookies' clicked.")
            else:
                self.log_message("No 'Refuse non-essential cookies' button found.")
        except Exception as e:
            self.log_message(f"Error dismissing cookie popup: {e}")
            traceback.print_exc()

    async def click_all_tab(self, page):
        """Click the 'All' tab on the blocklist page."""
        try:
            self.log_message("Clicking the 'All' tab on the blocklist page...")
            all_tab_button = await page.xpath('//span[contains(text(), "All")]')
            if all_tab_button:
                await all_tab_button[0].click()
                self.log_message("'All' tab clicked.")
            else:
                self.log_message("Error: 'All' tab not found.")
        except Exception as e:
            self.log_message(f"Error while clicking the 'All' tab: {e}")
            traceback.print_exc()

    
    async def scroll_to_load_all(self, page, scroll_done):
        """Scroll the page down programmatically until the scroll height stops increasing."""
        try:
            self.log_message("Starting to scroll through the blocklist to load all blocked users...")

            previous_height = await page.evaluate('document.body.scrollHeight')

            while True:
                # Scroll down
                await page.evaluate('window.scrollBy(0, 1000)')
                await asyncio.sleep(2)  # Allow time for content to load

                # Check the current page height
                current_height = await page.evaluate('document.body.scrollHeight')

                if current_height == previous_height:
                    self.log_message("Page height did not change. Attempting one final scroll...")

                    # Perform one more scroll to ensure no content is missed
                    await page.evaluate('window.scrollBy(0, 1000)')
                    await asyncio.sleep(2)

                    current_height = await page.evaluate('document.body.scrollHeight')
                    if current_height == previous_height:
                        self.log_message("No more content to load. Stopping scrolling.")
                        break

                previous_height = current_height

            # Set the scroll_done flag to True once scrolling is complete
            scroll_done.set()
            self.log_message("Finished scrolling through blocklist.")
        except Exception as e:
            self.log_message(f"Error during scrolling: {e}")
            traceback.print_exc()


    async def continuously_capture_usernames(self, page, all_blocked_users, scroll_done):
        """Continuously capture dynamically loaded blocked usernames while scrolling."""
        try:
            self.log_message("Starting continuous capture of blocked usernames...")

            while not scroll_done.is_set():  # Loop until scrolling is complete
                # Extract blocked usernames from all span elements that start with '@'
                new_usernames = await page.evaluate('''() => {
                    let users = [];
                    document.querySelectorAll('span').forEach(span => {
                        const username = span.textContent;
                        if (username && username.startsWith('@')) {
                            users.push(username);
                        }
                    });
                    return users;
                }''')

                # Add new usernames to the shared set (set will prevent duplicates)
                for username in new_usernames:
                    if username not in all_blocked_users:
                        all_blocked_users.add(username)

                self.log_message(f"Total unique blocked users so far: {len(all_blocked_users)}")

                await asyncio.sleep(1)  # Keep checking usernames every 1 second

            self.log_message("Stopped capturing usernames as scrolling is complete.")

        except Exception as e:
            self.log_message(f"Error during continuous username capture: {e}")
            traceback.print_exc()


    async def get_blocked_users(self, username, password):
        """Scrape the blocked users from the blocklist page and store them as JSON."""
        browser = None
        try:
            headless = self.headless_checkbox.isChecked()  # Check if headless mode is enabled
            chrome_path = find_chrome_path()  # Get Chrome path based on OS
            
            if chrome_path is None:
                self.log_message("Error: Could not find Chrome browser on your system.")
                return
            
            self.log_message(f"Launching Pyppeteer browser (headless={headless}) using Chrome at {chrome_path}...")

            # Launch Pyppeteer with the detected Chrome path
            browser = await launch(
                headless=headless,
                executablePath=chrome_path,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-blink-features=AutomationControlled']
            )
            page = await browser.newPage()

            await self.login(page, username, password)

            self.log_message("Navigating to blocklist page...")
            await page.goto(BLOCKLIST_URL, {'waitUntil': 'networkidle2'})
            await self.dismiss_cookie_popup(page)
            await self.click_all_tab(page)

            # Shared set to collect blocked usernames dynamically
            all_blocked_users = set()

            # Flag to signal when scrolling is complete
            scroll_done = asyncio.Event()

            # Create tasks for scrolling and continuous username capture
            username_task = asyncio.create_task(self.continuously_capture_usernames(page, all_blocked_users, scroll_done))
            scroll_task = asyncio.create_task(self.scroll_to_load_all(page, scroll_done))

            # Wait for both tasks to complete
            await asyncio.gather(username_task, scroll_task)

            # Save the blocked users to a JSON file
            with open('blocked_users.json', 'w') as json_file:
                json.dump(list(all_blocked_users), json_file, indent=4)

            self.log_message(f"Finished scraping and saved {len(all_blocked_users)} blocked users to 'blocked_users.json'.")
        except Exception as e:
            self.log_message(f"Error during scraping: {e}")
            traceback.print_exc()
        finally:
            if browser:
                await browser.close()



    def start_scraping(self):
        """Start the scraping process."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Use asyncio.run() to execute the async function
        asyncio.run(self.get_blocked_users(username, password))


def main():
    app = QtWidgets.QApplication(sys.argv)
    scraper = TwitterBlocklistScraper()
    scraper.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

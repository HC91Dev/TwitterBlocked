# Twitter Blocklist Scraper

A PyQt5 application that allows users to scrape their blocked users from Twitter and save the list as a JSON file. The application uses Pyppeteer to automate the browser for scraping.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Extension Files](#extension-files)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- Scrapes the list of blocked users from your Twitter account.
- Saves the list of blocked usernames in a JSON file (`blocked_users.json`).
- Provides a user-friendly GUI using PyQt5.
- Supports headless mode for scraping.

## Installation

To install the application, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HC91Dev/TwitterBlocked.git
   cd TwitterBlocked
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**

   ```bash
   python your_script_name.py
   ```

2. **Log in with your Twitter username and password.**
3. **Select whether to run in headless mode (optional).**
4. **Click "Start Scraping" to begin the scraping process.**
5. **The list of blocked users will be saved to `blocked_users.json` in the project directory.**

## Extension Files

This project includes the following extension files:

- **content.js**: This script can be used to interact with web pages or extract information from them when used as part of a browser extension.

- **popup.html**: This file defines the layout and design of the popup interface that appears when the extension icon is clicked. You can customize it to display the scraped data or provide additional functionalities.

- **background.js**: This script runs in the background and handles events such as browser action clicks, managing the extension's lifecycle, and possibly storing data.

### Using the Extension Files

1. **Set up the extension**:
   - Create a new folder for your browser extension (if not already created).
   - Place `content.js`, `popup.html`, and `background.js` into this folder along with the existing `manifest.json` file.

2. **Load the extension in Chrome**:
   - Open your browser and go to the extensions page (usually found under `chrome://extensions` for Chrome).
   - Enable "Developer mode."
   - Click on "Load unpacked" and select the folder where you placed the extension files.

3. **Load the extension in Firefox**:
   - Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.
   - Click on "Load Temporary Add-on."
   - Select the `manifest.json` file from the folder where you placed the extension files.
   - The extension will be loaded temporarily, and you can interact with it until you restart Firefox.

4. **Use the extension**:
   - Click on the extension icon in your browser toolbar to open the popup and interact with your scraped data from `blocked_users.json`.

## Requirements

- Python 3.x
- PyQt5
- Pyppeteer

Make sure to have Google Chrome installed, as the scraper uses it for automation.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Any improvements, bug fixes, or suggestions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

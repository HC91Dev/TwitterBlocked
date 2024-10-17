# Twitter Blocklist Scraper

A PyQt5 application that allows users to scrape their blocked users from Twitter and save the list as a JSON file. The application uses Pyppeteer to automate the browser for scraping.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- Scrapes the list of blocked users from your Twitter account.
- Saves the list of blocked usernames in a JSON file.
- Provides a user-friendly GUI using PyQt5.
- Supports headless mode for scraping.

## Installation

To install the application, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/twitter-blocklist-scraper.git
   cd twitter-blocklist-scraper
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

## Requirements

- Python 3.x
- PyQt5
- Pyppeteer

Make sure to have Google Chrome installed, as the scraper uses it for automation.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Any improvements, bug fixes, or suggestions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
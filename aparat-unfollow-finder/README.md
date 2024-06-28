# Aparat Unfollow Finder

This script identifies and unfollows users who have stopped following you on Aparat using Selenium and ChromeDriver.

## Technologies Used:

- Python
- Selenium
- ChromeDriver

## Features:

- Securely logs into your Aparat account.
- Retrieve lists of followers and accounts you are following.
- Compares these lists and provides an option to unfollow users not following you back.
- Dynamically loads the followers/following list pages through automated scrolling.

## How to use

- Clone the project
- Install Python (v3.11.5)
- Run `pip install -r requirements.txt` to install necessary dependencies.
- Download `ChromeDriver` from [this link](https://developer.chrome.com/docs/chromedriver/downloads).
- Copy the `chromedriver.exe` file to the `drivers` directory. If the directory does not exist, create it.
- Rename the `.env.example` file to `.env` and then update the `.env` file with your Aparat credentials (`APARAT_USERNAME`, `APARAT_PASSWORD`) and the path to `CHROME_DRIVER_PATH`.


## Run app

In the project directory, you can run:

`python main.py`

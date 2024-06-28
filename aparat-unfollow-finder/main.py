import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')


class Unfollower:
    def __init__(self):
        driver_path = os.path.abspath(os.environ.get('CHROME_DRIVER_PATH'))

        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)

    def get_followers(self):
        followers_list = []

        self.driver.get('https://www.aparat.com/dashboard/followed/followers')

        while 1:
            self.scroll()
            response = input("Is the end page?")

            if response == 'y':
                break

        count = len(self.driver.find_elements(By.CSS_SELECTOR, '#list1 > div > div > div > div'))

        for i in range(count):
            followers_list.append(self.driver.find_element(By.CSS_SELECTOR, f'#list1 > div > div:nth-child({i + 1})').get_attribute('href'))

        return followers_list

    def get_following(self):
        following_list = []

        self.driver.get('https://www.aparat.com/dashboard/followed')

        while 1:
            self.scroll()
            response = input("Is the end page?")

            if response == 'y':
                break

        count = len(self.driver.find_elements(By.CSS_SELECTOR, '#list1 > div > div > div > div'))

        for i in range(count):
            following_list.append(self.driver.find_element(By.CSS_SELECTOR, f'#list1 > div > div:nth-child({i + 1})').get_attribute('href'))

        return following_list

    def unfollow(self, link):
        self.driver.get(link)
        self.driver.find_element(By.XPATH, "//*[@id='listWrapperundefined']/div/div/div[1]/div[2]/div/button").click()

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def login(self, username, password):
        self.driver.get('https://www.aparat.com/signin')

        time.sleep(5)

        username_input = self.driver.find_element(By.XPATH, "//*[@id='username']")
        username_input.send_keys(username)

        login_button = self.driver.find_element(By.XPATH, "//*[@id='main-container']/section/div/div[2]/form/button")
        login_button.click()

        time.sleep(5)

        password_input = self.driver.find_element(By.XPATH, "//*[@id='password']")
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, "//*[@id='main-container']/section/div/div/form/button")
        login_button.click()

        time.sleep(5)

        self.driver.get('https://www.aparat.com/dashboard/followed')


if __name__ == '__main__':
    bot = Unfollower()
    bot.login(username=os.environ.get('APARAT_USERNAME'), password=os.environ.get('APARAT_PASSWORD'))
    followers = bot.get_followers()
    following = bot.get_following()

    print(len(followers), len(following))

    # for channel in following:
    #     if channel not in followers:
    #         bot.unfollow(link=channel)

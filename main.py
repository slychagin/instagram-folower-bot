import time
import os
from time import sleep
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv(override=True)

SIMILAR_ACCOUNT = os.environ.get("SIMILAR_ACCOUNT")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


class InstaFollower:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def login(self):
        """
        Login in our Instagram account
        :return: None
        """
        self.driver.get("https://www.instagram.com/accounts/login/")
        sleep(3)

        enter_email = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        enter_password = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')

        enter_email.send_keys(USERNAME)
        enter_password.send_keys(PASSWORD)
        enter_password.send_keys(Keys.ENTER)

        sleep(3)
        save_data = self.driver.find_element(By.XPATH,
                                             '//*[@id="react-root"]/section/main/div/div/div/section/div/button')
        save_data.click()

        sleep(3)
        turn_notifications = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div['
                                                                '1]/div/div[2]/div/div/div/div/div/div/div/div['
                                                                '3]/button[2]')
        turn_notifications.click()

    def find_followers(self):
        """
        Find all followers in interested account.
        Set number of scroll in range function (for example: 5 scroll * 15 followers on scroll = 75 followers)
        :return: None
        """
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")
        sleep(2)
        enter_followers = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div['
                                                             '1]/div[1]/section/main/div/header/section/ul/li['
                                                             '2]/a/div')
        enter_followers.click()
        sleep(5)
        modal = self.driver.find_element(By.CSS_SELECTOR, 'div._aano')
        for i in range(5):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        """
        Subscribe to all subscribers.
        :return: None
        """
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'li button')
        for button in all_buttons:
            try:
                button.click()
                sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(By.CSS_SELECTOR, 'button._a9--._a9_1')
                cancel_button.click()


insta_bot = InstaFollower()
insta_bot.login()
insta_bot.find_followers()
insta_bot.follow()

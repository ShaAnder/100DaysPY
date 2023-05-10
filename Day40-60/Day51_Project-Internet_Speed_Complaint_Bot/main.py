### --- IMPORTS --- ###

#our selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time
import speedtest

from dotenv import load_dotenv
import os

### --- ENVS / VARS --- ###

load_dotenv()

twitter_login = os.getenv("LOGIN")
twitter_pw = os.getenv("PW")
twitter_name = os.getenv("NAME")

promised_up = float(400)
promised_down = float(400)
### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)

#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"

### --- CLASS --- ###

class InternetSpeedTwitterBot():
    
    def __init__(self, dr) -> None:
        s = Service(executable_path=dr)
        self.driver = webdriver.Chrome(service=s, options=options)
        self.st = speedtest.Speedtest()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        """gets the speedtest values for our complaint"""
        #originally the idea was to scrape speedtest but decided to go with a different route and use pythons own speedtest modu
        print("Getting speeds")
        upload = round(self.st.upload() / 100000, 2)
        download = round(self.st.download() / 100000, 2)
        self.up = upload
        self.down = download

    def tweet_at_provider(self):
        tweet = f"Hey Internet Provider, why is my internet speed {self.down} down / {self.up} up " \
        f"when I pay for {promised_down} down / {promised_up} up"
        time.sleep(2)

        twitter_url = "https://twitter.com/i/flow/login"
        tweet_area_xpath = '//div[@data-contents]'
        tweet_btn_xpath = '//div[@data-testid="tweetButtonInline"]'

        self.driver.get(twitter_url)
        self.driver.maximize_window()
        time.sleep(1)
        login = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        login.send_keys(twitter_login + Keys.ENTER)
        time.sleep(1)
        name = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        name.send_keys(twitter_name + Keys.ENTER)
        time.sleep(1)
        pw = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        pw.send_keys(twitter_pw + Keys.ENTER)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, tweet_area_xpath)))
        tweet_area = self.driver.find_element(By.XPATH, tweet_area_xpath)
        tweet_area.send_keys(tweet)
 
        tweet_btn = self.driver.find_element(By.XPATH, tweet_btn_xpath)
        tweet_btn.click()
### --- MAIN --- ### 

#initialize our object

twitter_bot = InternetSpeedTwitterBot(driver_path)

print(twitter_bot.get_internet_speed())

twitter_bot.tweet_at_provider()
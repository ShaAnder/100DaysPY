### --- IMPORTS --- ###

#our selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

import time

from dotenv import load_dotenv
import os

### --- ENVS --- ###

load_dotenv()

insta_login = os.getenv("LOGIN")
insta_pw = os.getenv("PW")

### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)

#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"

### --- CLASS --- ###

class InstaFollower():
    
    def __init__(self, dr) -> None:
        s = Service(executable_path=dr)
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.maximize_window()
        self.chosen_account = "python.learning"


    def logins(self, l, p):
        """LOGS INTO INSTA"""
        #we bypass a lot of popups and window handling by logging into fb first 
        self.driver.get("https://www.instagram.com")
        time.sleep(1)
        #Open the facebook and log in credentials
        email = self.driver.find_element(By.CSS_SELECTOR, '#loginForm input')
        email.send_keys(l)
        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys(p + Keys.ENTER)
        time.sleep(3)

    def handle_popups(self):
        """Handles cookies and notif popups"""
        # try:
        #     not_now = self.driver.find_element(By.XPATH, '//*[@id="mount_0_0_BE"]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button')
        #     not_now.click()
        #     time.sleep(1)
        #     # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._a9_1'))).click()
        #     time.sleep(1)
        # except NoSuchElementException or TimeoutException:
        #     print("Could not close popups")
        try:
            popup1 = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')
            popup1.click()
            time.sleep(5)
 
            popup2 = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]'
                                                        '/div/div/div/div/div/div/div/div[3]/button[2]')
            popup2.click()
        except NoSuchElementException:
            #if it can't find a popup go to page we want to follow people on
            self.driver.get(f"https://www.instagram.com/{self.chosen_account}/followers")
            pass


    def follow(self):
        """Follows the followers"""

        while True:
            try:
                #get a list of the buttons
                button_list = self.driver.find_elements(By.CSS_SELECTOR, "button")
                #for each button in the list, print the text, if the text == Follow, click that button, using a selenium script to do it
                for button in button_list:
                    print(button.text)
                    if button.text == "Follow":
                        time.sleep(2)
                        self.driver.execute_script("arguments[0].click();", button)
                        time.sleep(2)
                    #print the lenght of the list
                    print(len(button_list))
                print("Time to scroll the list :^)")

                #next we want to get the body of the follower list
                follow_body = self.driver.find_element(By.XPATH, "//div[@class='_aano']")
                #set a scroll amount, to keep track, we don't wanna follow all 1 mil followers
                scroll = 0
                #now let's loop a scroll function, once it follows all the people on the list it will scroll down and the list should refresh
                while scroll < 2:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', follow_body)
                    time.sleep(2)
                    scroll +=1


            except Exception:
                print("e")

### --- MAIN --- ###
    
insta = InstaFollower(driver_path)    
insta.logins(l=insta_login, p=insta_pw)
time.sleep(1)
insta.handle_popups()
time.sleep(1)
insta.follow()
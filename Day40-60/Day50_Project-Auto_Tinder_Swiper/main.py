### --- IMPORTS --- ###

from selenium import webdriver
#we want these for setting up wait timers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#we want to import these from selenium to catch errors
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException

#we want keys from selenium to tab stuff
from selenium.webdriver.common.keys import Keys

import time

from dotenv import load_dotenv
import os

### --- ENVS --- ###

load_dotenv()

fb_login = os.getenv("LOGIN")
fb_pw = os.getenv("PW")


### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)

#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=driver_path)

### --- FUNCS --- ###

def handle_tinder_popups():
    time.sleep(2)
    #we want to identify the tinder popups
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')))
    #then click through them 
    for i in range(2):
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div/div[3]/button[1]/div[2]/div[2]').click()
    time.sleep(2)

def logins(l, p):
    """LOGS INTO FB THEN TINDER WITH FB"""
    #we bypass a lot of popups and window handling by logging into fb first 
    driver.get("https://www.facebook.com/")
    #Open the facebook and log in credentials
    email = driver.find_element(By.NAME, "email")
    email.send_keys(l)
    password = driver.find_element(By.NAME, "pass")
    password.send_keys(p)
    password.send_keys(Keys.ENTER)
    #liberal use of time.sleep for stuff to load
    time.sleep(2)
    #Open a new tab in the same window (bypasses the need for window handling)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + "t")
    #then to tinder login
    driver.get('https://tinder.com/')
    driver.maximize_window()
    # Click the log in button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="c24809439"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]'))).click()
    #click login with fb
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="c-1703571637"]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]/div/div'))).click()


def navigate_tinder(): 
    #instead of looking for a button we can use selenium keys to swipe left or right, on tinder pc you can swipe right with the left key (it's right manually, selenium is diff)
    #create a swipe loop
    loop = 0
    while loop < 50:
        #find the button if it's there click
        try:
            focus_profile = driver.find_element(By.CSS_SELECTOR, 'body')
            time.sleep(2)
            focus_profile.send_keys(Keys.LEFT)
        #sometimes tinder hit's you with popups like add to homepage / gold ect we handle it here
        except ElementClickInterceptedException:
            time.sleep(1)
            not_interested = driver.find_element(By.CLASS_NAME, "117p5q9z")
            not_interested.click()
            time.sleep(1)
        loop +=1
        
logins(l=fb_login, p=fb_pw)
handle_tinder_popups()
navigate_tinder()
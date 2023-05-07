### --- IMPORTS --- ###

from selenium import webdriver
#we want these for setting up wait timers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#this for allowing key prompts
from selenium.webdriver.common.keys import Keys

import time

#envs
import os
from dotenv import load_dotenv

### --- LOAD ENVS --- ###

load_dotenv()

SEARCH = os.getenv("LINKED_IN_SEARCH")
USER = os.getenv("LOGIN")
PW = os.getenv("PASS")

### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)

#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=driver_path)

#get the website
driver.get(SEARCH)

### --- FUNCTIONS --- ###

def login(U=USER, P=PW):
    time.sleep(1)
    email = driver.find_element(By.XPATH, '//*[@id="username"]')
    email.send_keys(U)
    time.sleep(1)
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    password.send_keys(P)
    time.sleep(1)
    sign_in = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()

### --- MAINLOOP --- ###

#webdriver will wait until, the element appears and becomes clickable
sign_in_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/header/nav/div/a[2]"))).click()

login(USER, PW)
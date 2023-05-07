### --- IMPORTS --- ###

from selenium import webdriver
#we want these for setting up wait timers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import time
### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)

#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=driver_path)

#get the website
driver.get("https://orteil.dashnet.org/cookieclicker/")
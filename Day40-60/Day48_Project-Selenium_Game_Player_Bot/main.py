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

###--FUNCTIONS---###
 
def setup():
    """Quick function to close all the popups set language ect"""
    popup_list = [
    '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p',
    '//*[@id="langSelect-EN"]',
    '/html/body/div[3]/div/ins/img[3]',
    '/html/body/div[1]/div/a[1]',
    '//*[@id="note-1"]/div[1]'
             ]
    for item in popup_list:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, item))).click()
        time.sleep(1)

def click_cookie():
    """Clicks the cookie"""
    big_cookie = driver.find_element(By.XPATH, '//*[@id="bigCookie"]')
    big_cookie.click()
 
def purchase_upgrade():
    """Purchases upgrades, when an upgrade is bought the next one along becomes the new 0"""
    try:
        upgrade = driver.find_element(By.ID, "upgrade0")
        upgrade.click()
    except:
        pass
 
def buy_item():
    """Loops through the store list and tries to purchase most expensive item then the next most ect"""
    for i in range(16, -1, -1):
        try:
            product = driver.find_element(By.ID, f"product{i}")
            product.click()
        except:
            pass
 
def close_popup():
    """Closes achievement popups
    """
    try:
        popup_close = driver.find_element(By.XPATH, '//*[@id="notes"]/div[5]')
        popup_close.click()
    except:
        pass
 
def cookie_buff():
    """Pressed the cookie buff popup, never seen it so this remains blank until i do"""
    pass
 
###---BUILD THE BOT---###
 
#we want our loop counter here, as well as our time
GAME_ON = True
Loop = 0
MINS = 10

#wanna set the end time for the game
end_time = datetime.now()+timedelta(minutes=MINS)

#setup function to get to the game
setup()
time.sleep(1)

#main loop, will click cookie and every x loops buy upgrades close achievements

while GAME_ON == True:
    click_cookie()
    time.sleep(0.01)
    Loop +=1
    if Loop %100 == 0:
        buy_item()
        time.sleep(0.01)
        purchase_upgrade()
    if Loop %1000 == 0:
        close_popup()
        cookie_buff()
    if end_time < datetime.now():
        GAME_ON == False
        print("Game Over")
        time.sleep(1)
        driver.close()        
### --- IMPORTS --- ###

from selenium import webdriver
#we want these for setting up wait timers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

#we have a bunch of popups and notifs that appear on the screen at the start we want to get rid of and because 
#they popup on every launch we're writing this for loop here to get rid of them:
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


### --- MAIN COMPONENTS --- ###

#our game runtime
TIME = 600

#we want to find our cookie
cookie = driver.find_element(By.XPATH, '//*[@id="bigCookie"]')
#then make a list for all the store items
store_items = [] 
#now we loop through and find every store item
for n in range(0, 18):
    store_items.append(driver.find_element(By.ID, f'product{n}'))

#the course wanted us to set a time loop so that it didn't run indefinitely
end_time = time.time() + TIME
#while our current time is less than our end time, play the game
while time.time() < end_time:
    #click the cookie
    cookie.click()
    #now let's iterate backwards through store items, it'll try and click on the item even if it doesn't show up and move backward through the list
    for item in range(len(store_items) - 1, -1, -1): 
        #try clicking, if can click if can't pass
        try:
            store_items[item].get_attribute('onclick')
            store_items[item].click()
            
        except:
            pass
 
print("Time to sleep!")
driver.close()

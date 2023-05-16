### --- IMPORTS --- ###
 
#-- Selenium --#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
 
#-- BS4 --#
from bs4 import BeautifulSoup
import requests
import json
 
#-- ENV --#
import os
from dotenv import load_dotenv
 
#-- Time --#
import time as t
 
###--- LOAD ENV & VARIABLES ---###
 
#initialize .env
load_dotenv()

z = os.getenv("ZILLOW")
f = os.getenv("RENT_FORM") 

### --- DRIVER SETUP --- ###

#we import options to add extra functionality to our webdriver
options = webdriver.ChromeOptions()
#this one allows us to keep the window open
options.add_experimental_option("detach", True)
#setup webdriver
driver_path = "Dev_Tools/chromedriver.exe"
 
###--- Initialize the class ---###
 
class HouseListingbot:
    def __init__(self, dr) -> None:
        #selenium options and settings
        s = Service(executable_path=dr)
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.maximize_window()
        #get our envs here:
        self.website = z
        self.form = f
        #we want our lists for the form filling later


        #we want the headers for zillow
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
                        }
 
    def BS4ScrapeListings(self):
        """OPENS | SCROLLS | SCRAPES zillow site to get our listings
        """
        #let's get our page
        self.driver.get(self.website)
        t.sleep(1)
        #then let's scroll
        y = 1000
        for n in range(5):
            self.driver.execute_script(f"window.scrollTo(0, {y});")
            y += 800
            t.sleep(0.5)

        #finally we get the soup of our page
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # now let's extract our data and put it into lists gonna use list comp here
        addresses = soup.find_all(attrs={'data-test': 'property-card-addr'})
        #we want to actually split the address and strip it away if it has one of these
        self.all_addresses = [address.getText().split('|')[-1].strip() for address in addresses]
        prices = soup.find_all(attrs={'data-test': 'property-card-price'})
        #split any plus signs 
        self.all_prices = [price.getText().split('+')[0] for price in prices]
        links = soup.find_all(attrs={'data-test': 'property-card-link'}, href=True)
        #fix any links, some cards don't have zillow website at the start so we add them in only if it doesn't have
        self.all_links = [f'https://www.zillow.com{link["href"]}' for link in links[::2]]

    def fill_form(self):
        #we give it a range to count from, just chose links here
        for i in range(len(self.all_links)):
            self.driver.get(self.form)
            t.sleep(3)
            #now we fill in the form with the info given, open the form add the path to question and then send answer
            fill_address = self.driver.find_element(By.XPATH,
            '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            fill_address.click()
            fill_address.send_keys(self.all_addresses[i])
        
            fill_prices = self.driver.find_element(By.XPATH,
            '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            fill_prices.click()
            fill_prices.send_keys(self.all_prices[i])
        
            fill_links = self.driver.find_element(By.XPATH,
            '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            fill_links.click()
            fill_links.send_keys(self.all_links[i])
        
            submit_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.click()
 
### --- MAIN --- ###

housebot = HouseListingbot(driver_path)
t.sleep(2)
housebot.BS4ScrapeListings()
t.sleep(2)
housebot.fill_form()
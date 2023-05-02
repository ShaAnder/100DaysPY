### --- IMPORTS --- ###

#we want request and bs4 to get data
import requests
from bs4 import BeautifulSoup
#we gon need lxml for this one chief
import lxml

#we want date time to set a time to check and also time to stall the program into not spamming the command
from datetime import datetime
import time

#os and loadenv for env vars
import os
from dotenv import load_dotenv

import smtplib


### --- SETUP AND VARS --- ###


#setup our email_sender

#we want our price URL for the sake of simplicity we're going to track the project url
URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

#now we want to load in our variables
load_dotenv()
OUR_EMAIL = os.getenv("EMAIL")
OUR_PW = os.getenv("PW")
EMAIL_TO = os.getenv("SEND_EMAIL")

#finally we want to setup our time and price variables
# current_time = datetime.now().strftime("%H:%M:%S")
#testing
current_time = "09:00:00"
target_time = "09:00:00"

target_price = 100

### --- REQUEST AND MAKE SOUP --- ###

AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0"
LANGUAGE = "en-GB,en-US;q=0.9,en;q=0.8"

#first we need to setup headers  to allow us to access the site
header = {
    "USer-Agent": AGENT,
    "Accept-Language": LANGUAGE,
}

#now we request our data
response = requests.get(URL, headers=header)
price_page = response.text

#now make ze soup
soup = BeautifulSoup(price_page, "lxml")

#finally we get the current price of the item we want to track and then strip it down to a float
current_price = float(soup.find(class_="a-offscreen").text.strip("$"))

### --- SEND AN EMAIL --- ### 

#finally we want to make up an email that will if the price is lower than a choice price will notify us


SMTP = "smtp.gmail.com"
SUBJECT = "NEW DEAL ALERT!"
MESSAGE = f"The item you're currently tracking is now on sale!\nYour chosen price was ${target_price} and it's current price is ${current_price}\nCheck out the link below to purchase!\n{URL}"

def send_email(SMTP, EMAIL, PW, EMAIL_TO, MESSAGE, SUBJECT):
    server = SMTP
    message = MESSAGE
    subject = SUBJECT
    email= EMAIL
    pw = PW
    email_to = EMAIL_TO
    #now we connect to the smtp lib
    connection = smtplib.SMTP(server)
    connection.starttls()
    connection.login(user=email,password=pw)
    connection.sendmail(
        from_addr=email, 
        to_addrs=email_to, 
        msg=f"{subject}\n\n{message}")
    connection.close()

if current_time == target_time and current_price < target_price:
    send_email(SMTP, OUR_EMAIL, OUR_PW, EMAIL_TO, MESSAGE, SUBJECT)
else:
    print("Not on sale / not time")
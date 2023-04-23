#!usr/bin/env/python

### --- IMPORTS --- ###

#smptplub for sending emails
import smtplib
#pandas to read csv
import pandas
#random for random letter templates
import random
#os and load.env for env variables
import os
from dotenv import load_dotenv
#finally datetime for checking birthdays
import datetime as dt

### --- ENV VARS --- ### 

#first we load_dotenv
load_dotenv()

#next get our variables
GOOGLE_EMAIL= os.getenv("EMAIL")
GOOGLE_PW= os.getenv("PW")
#our email to send stuff to
SEND_EMAIL= os.getenv("SEND_EMAIL")

### --- SET TIME --- ###

#first we need the day, we get this by creating a now variable and tapping into that for the day
now = dt.datetime.now()
#we want to set a tuple up that looks at the month / day for cross checking our birthdays
today = (now.month, now.day)
print(today)


### --- READ BDAYS --- ###

#we get the csv
bday_path = "Day20-40/Day32-Automated_Birthday_Wisher/birthdays.csv"
#open it with pandas
birthdays = pandas.read_csv(bday_path)
#create a dict comprehension to get the month and day, {monthL day for (index, datarow) in birthdays, iterate over the rows}
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in birthdays.iterrows()}

print(birthdays_dict)

### --- SEND EMAIL --- ### 

if today in birthdays_dict:
    #if a match get the name of that person
    birthday_person = birthdays_dict[today]
    print(birthday_person["name"])

    ### --- GET AND MERGE LETTERS --- ###

    #choose a random letter
    letters_path = "Day20-40/Day32-Automated_Birthday_Wisher/letter_templates/"
    file_path = letters_path+f"letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        #merge the name with the birthday persons name
        contents = contents.replace("[NAME]", birthday_person["name"])

    ### --- EMAIL SETUP --- ###

    #now we connect to the smtp lib
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=GOOGLE_EMAIL,password=GOOGLE_PW)
    connection.sendmail(
        from_addr=GOOGLE_EMAIL, 
        to_addrs=birthday_person["email"], 
        msg=f"Subject:Happy Birthday :D!\n\n{contents}")
    connection.close()















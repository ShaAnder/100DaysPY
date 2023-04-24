### --- IMPORTS --- ###

#we want to import requests to request the api data from the iss 
import requests
#we want date time for pinging the location every 60 secs
from datetime import datetime
#import smtplib to send emails
import smtplib
#import os / dotenv here for importing env
import os
from dotenv import load_dotenv

### --- GET ENVS --- ###

load_dotenv()
#we want to get our long and latitudes to cross reference with the iss (longlat.net)
MY_LAT = os.getenv("LAT")
MY_LONG = os.getenv("LONG")

MY_EMAIL = os.getenv("EMAIL")
MY_PASS = os.getenv("PW")

RECIEVER_EMAIL = os.getenv("SEND_EMAIL")

### --- SETUP REQUEST / GET ISS DATA --- ###

#we want to contact the api for the iss position
response = requests.get(url="http://api.open-notify.org/iss-now.json")
#raise for status is error handling, so we can see if we get a bad HTTP code
response.raise_for_status()
#and now we have our data variable
data = response.json()

#we then get the iss lat and long with that data
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

### --- SUNRISE/SUNSET REQUEST --- ###

#we want to setup parameters for our latitude and longitude to feed into the next request
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    #we use format 0 so that it formats how we want
    "formatted": 0,
}

#we want to get the sunrise / sunset data for the current time and we feed our lat / long in as params
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
#raise for status
response.raise_for_status()
#get data and use it to get exact sunrise / sunset times
data = response.json()
#we want to split the string down to get the hour we need in 24 hours
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
#we also want the hour now to compare with sunrise/ sunset
time_now = datetime.now().hour

### --- MAIN --- ###

#Now we're going to use some if / else to weed down to what we want to do
# -We want the ISS above us at night, so i'm adding print statements for every eventuality

#if our lat / long + or - 5 is less than or equal to iss lat /long next step
if float(MY_LAT) - 5 <= iss_latitude <= float(MY_LAT) + 5 and float(MY_LONG) -5 <= iss_longitude <= float(MY_LONG) +5:
    print("The ISS is close")
    #we check the date time
    if time_now >= sunset or time_now <= sunrise:
        #this is our ideal statement so we will create the email here
        print("The iss is above and it's night time! Look up!")

        message = "HELLO! I am a bot! My job is to notify you when the ISS is overhead! It is by the way! LOOK UP!"

        #now we connect to the smtp lib
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL,password=MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL, 
            to_addrs=RECIEVER_EMAIL, 
            msg=f"Subject: Your ISS Notification!\n\n{message}")
        connection.close()

    else:
        print("The iss is above but you probably can't see it as it's daytime D:")
else:
    print("ISS is not here chief")

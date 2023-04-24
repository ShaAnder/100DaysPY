### --- PROJECT NAME / DESC --- ###

Ran Alert App - A small application utilizing sms apis and weather alert apis to send weather alert notifications to the user

### --- PARAMETERS --- ###

- Must be able to connect to and get api data relating to weather for 12 hours from the open weather appid
- Must be able to connect to and send sms information to a user via twilio

NOTE TO WORK REQUIRES AN ENV FILE WITH THE FOLLOWING FILLED IN:
 
LATITUDE="YOUR LAT"
LONGITUDE="YOUR LONG"
API_KEY="OPEN WEATHER KEY HERE"

TWILIO_ACCOUNT_SID="TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN="TWILIO AUTH TOKEN"

SENDING_NUMBER="NUMBER CREATED BY TWILIO"
RECEIVING_NUMBER="NUMBER MESSAGE IS SENT TO"

### --- HOW IT WORKS --- ###

- The program first uses the env data from .env file to get the users longitude / latitude to pinpoint exact location
    -> then sends that data in a request to the open weather api.
- Next the program will take the response and get the next 12 hour slice of data for comparison
    -> it will compare it against the status codes for rain and drizzle and return a bool
- If the bool is TRUE:
    -> Then enables the next step of the program, which will send a twilio message to the user telling them there could be rain and to bring an umbrella
- If it's false:
    -> Do nothing

### --- TO DO / FUTURE PLANS --- ### 

Much like the ISS overhead notifier this doesn't seem like an app by itself, if i were to use this I would include it as part of a larger personal assistant application, 
had the idea for a modular assistant app that acts as a calender, weather alerts ect.
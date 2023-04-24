### --- PROJECT NAME / DESC --- ###

ISS OVERHEAD NOTIFIER - a small program designed to email the user and tell them if the conditions are right that the iss is overhead and they should look up

### --- WHAT IT NEEDS TO DO --- ###

- Must be able to pull the api data from both the iss and sunrise / sunset
- take that data and cross reference it against set parameters of the user
- send an email when the conditions match

- NOTE: Requires an env file with these details filled in:
EMAIL="YOUR EMAIL"
PW="YOUR APP PW"
SEND_EMAIL="EMAIL SENDING TO"

LAT="YOUR LAT"
LONG="YOUR LONG"

### --- HOW IT WORKS --- ###

- first we feed in our lat and long from the env file as well as our other details for emailing
- the program will pull and format the ISS's current position, and format it for use later
- it will then take your lattitude and longitude and feed those into the sunrise-sunset api to get your times
    -> From here the program will cross reference your location with iss location to + or - 5 
    -> if it matches it will then check if it is sunrise or sunset
        -> if these conditions are met it will then open up the email module and send an email telling the user to look up.
        -> if any condion fails it will print a response in the console instead

### --- TO DO / FUTURE PLANS --- ### 

This is the kind of program that on it's own would not make a good app, it's a fun little idea to work on and maybe expand, where it could really shine is as part of a larger weather and science app 
aimed at fun little tools for people who are interested in that thing. 
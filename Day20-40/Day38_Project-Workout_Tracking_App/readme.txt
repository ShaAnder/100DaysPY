### --- PROJECT NAME / DESC --- ###

Workout tracker - This is a small project that utilizes a few apis to track and record data related to exercising onto a google sheet.

### --- PARAMETERS --- ###

- The program must be able to connect to  nutritionix api to send data needed
- It must then be abe to connect to a google sheet through sheety to paste the formatted data into the sheet

NOTE, for testing you need a .env file with the following parameters filled in.

USER="YOURUSERNAME"
TOKEN="YOURPW"

### --- HOW IT WORKS --- ###

-Firstly we get the user to enter the exercise done via the prompts, this is then stored as a string for later use
-We combine this query data with the other details the user has in the form of gender, weight, height and age and 
feed it to the exercise paramters
- Feeding those parameters into the nuritionix api, we are given back the exercise duration and calories
- These are then fed into a for loop along with date and time which is then posted to sheety which will write to the google sheet

### --- TO DO / FUTURE PLANS --- ### 

Much like some of the other projects done recently, this doesn't feel like it would be a good app on it's own, it would be more
benefiicial as part of a daily planner / personal assistant application
### --- PROJECT NAME / DESC --- ###

Automated_Birthday_Wisher, a simple piece of code designed to send a birthday greetings to a person when their birthday lines up with the date.

### --- PARAMETERS --- ###

- The program must be able to read the data from birthdays.csv
- Be able to create a letter from the templates shown
- Send an email to the recipient based on their email address in the birthdays.csv

- NOTE: Requires an env file with these details filled in:
EMAIL="YOUR EMAIL"
PW="YOUR APP PW"
SEND_EMAIL="EMAIL SENDING TO"

### --- HOW IT WORKS --- ###

- Firstly the program gets todays date and stores it as a tuple
- Next it will read the birthdays.csv file and format the data gotten into a dict with the birth month and day as a tuple
- In the next step the program will compare the tuples from datetime and the dict, and if it finds a match it will open one of the random letter templates
    -> from here it takes the matching peoples name, and adds them to the template, using mail merging, 
    -> it then opens smtplib connects to the dummy google account and sends the birthday email to the recipient

### --- TO DO / FUTURE PLANS --- ### 

This is just the barebones of this project, and with time could be adapted into a number of things, like a news letter, mailing list ect. There are integrated third party tools like this,
however having a completely inhouse free solution is always a good idea. My plan would be to build a mail templater to send various things across and allow it to work with various applications

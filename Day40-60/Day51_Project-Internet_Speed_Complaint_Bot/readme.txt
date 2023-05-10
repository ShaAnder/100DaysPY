### --- PROJECT NAME / DESC --- ###

A small bot / script that gets internet up and down speeds, compares them to the promised amount and then 
if the numbers do not match / are less than expected tweets it out. 

### --- PARAMETERS --- ###

Must be able to get internet speeds, either through speedtest.net scraping or speedtest-cli
must be able to login to your twitter account
must be able to tweet a message if statement is triggered


### --- HOW IT WORKS --- ###

we import everything into the main file and pass the driver into the CLASS_NAME
The bot once initialized will look for the internet speeds through speedtest() and return them
if they do not match the bot will log into your twitter accoun and post a twitter message stating as such


### --- REQUIREMENTS --- ###

Requires an env file with the following information:
LOGIN=""
PW=""
NAME=""

the chromedriver.exe (located in Dev_Tools)
and the packages from the requirements.txt folder

### --- TO DO / FUTURE PLANS --- ### 

As with the rest of these projects scraping is a gray area in the best of situations, aside from hobby projects or stuff for the course 
i won't be using scraping in anything. Considering as well now with twitters new management probably best not to mess with it :)
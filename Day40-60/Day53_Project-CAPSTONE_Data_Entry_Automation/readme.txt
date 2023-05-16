### --- PROJECT NAME / DESC --- ###

CAPSTONE PROJECT: DATA ENTRY JOB AUTOMATION, a project with the simple goal of scraping information from a renting site, and translating that data to a from
while it can be done in more efficient ways with the use of data frames pandas ect the objective was to do it with selenium

### --- PARAMETERS --- ###

The program must be able to take relevant information from the zillow website, format that information and put it onto a google sheet
with an address, a price and a link to the property. The person creating the code must use BS4, requests and selenium to achieve this


### --- HOW IT WORKS --- ###

Navigates to the zillow website (could have used any site but this was course recommended as it uses js)
scrapes the data and returns it to us for formatting
using list comprehension dives through the data to find the specific attributes for the address, price and links
then adds those to a list
finally navigates to the rent google form and using selenium finds and fills the fields
The rent form is tied to a google spreadsheet so it automatically gets filled

### --- REQUIREMENTS --- ###

Requires an env file with the following information:
ZILLOW = ""
RENT_FORM = ""

the zillow link for the houses
the rent form (google forms)

originally this project wanted us to actually go through google login, however with how it was google and selenium auto login do not get along
i came up with a workaround / idea to use a google form directly tied to the google sheet, it works without us having to login to google too.

1/ Create the google form with relevant fields, and get the link to view it
2/ in the settings tie that form to a google sheet
3/ point selenium to the form

no google login needed, it fills the form which passes the information over to the sheet in exactly the way the project expects.

### --- TO DO / FUTURE PLANS --- ### 

much like most of the scraping projects this is for learning purposes only, but automating data entry can be powerful and i aim to take a deeper dive on AUTOMATION
as i get more confident in the language
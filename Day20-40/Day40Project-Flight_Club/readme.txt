### --- PROJECT NAME / DESC --- ###

This Capstone Project - Flight Deal Finder / Flight Club, is designed around creating a small program that will constantly scan flight sites
for cheap prices, then email / sms the user when it finds a deal lower than the lowest number user sets.

### --- PARAMETERS --- ###

The program should be able to read a sheety endpoint and send the data back to the main application then search for relevant flight IATA codes, once it does this
it should be able to connect to the tequila api and find flights between now and 6 months. If it finds flights for cheaper than listed, it should then be able to send an sms
to the user in question with the flight, the price, the date and a booking link.

### --- HOW IT WORKS --- ###

PART 1. FLIGHT DEAL FINDER

1. Data_manager.py fetches the sheety information and feeds it to the main.py

2. From there the main.py feeds the information into the flight_search.py to the method "get_iata_code", this gets the various codes for the cities
and passes it back to main.py

3. This information is stored as a sheet_data variable and then used in the data_manager method update_iata_codes to update the flight codes on the sheet api
(kind of overly complex but this is a project about testing our knowledge with classes and apis)

4. from here the tequila api to gets flights from tomorrow (datetime +1) and 6 months from tomorrow, 
we feed in those args as well as an origin IATA (DUB, main.py) and our sheety IATA's

5. the program sends a request for any flights with those parameters and stores the relevant data in flight_data

6. Finally it runs an if statement, that if any of the flights we searched for in the next 6 months are cheaper than what is shown on the lowest price (in the sheet)
we send an sms alert / email with the date, the flight information and the price as well as a link to book the flight. 

PART 2. FLIGHT CLUB

The flight club replaces the twilio text alert instead with another sheet containing customer data that is then used to email the customers the flight deals. It will only send emails
if the flight is cheaper than what' scurrently listed mind you

### --- TO DO / FUTURE PLANS --- ### 
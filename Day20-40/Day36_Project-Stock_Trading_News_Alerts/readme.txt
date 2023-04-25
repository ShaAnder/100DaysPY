### --- PROJECT NAME / DESC --- ###

Stock trading news alert program. A program that will get stock closing prices and based on the % fluctuation, if high fluc, it will try to find relevant news articles that could be the reason behind
the fluctuation, then text the articles to the user.

### --- PARAMETERS --- ###

- Must be able to connect to and get api data relating to stock closing prices. You must use Time_Series_Daily_Adjusted for this as daily has been upgraded to premium only
- The program must be able to figure out the fluctuation % of the stock so that it can make a call on whether to find news articles
- Following getting the fluctuation the app must be able to connect to the news api and pull relevant articles to the company in question
- And finally must be able to connect to and send sms information to a user via twilio

NOTE, for testing you need a .env file with the following parameters filled in.

ALPHA_API_KEY="ALPHA ADVANTAGE KEY HERE"
NEWS_API_KEY="NEWS API KEY HERE"

TWILIO_ACCOUNT_SID="TWILIO SID"
TWILIO_AUTH_TOKEN="TWILIO AUTH TOKEN"

SENDING_NUMBER="TWILIO NUMBER SENDING"
RECEIVING_NUMBER="YOUR NUMBER RECEIVING"

### --- HOW IT WORKS --- ###

The program will first and foremost attempt to find the listed stocks closing prices, using the alpha advantage time series daily adjusted api, once it finds the relevant data it will
narrow down the data to the closing price. It will then try and find the closing price of the next day over. 
Instead of using specific days we use index 0 and 1 to find these. This allows us to cover times where the stocks are not being traded like weekends and holidays

After it finds the closing prices it will compare them and find the difference in both abs and %. 

After this it will compare the % difference to the set amount, i've changed the code a bit to allow the user to put in their own custom difference. If the difference is greater than the one 
specified, it will then try and find trending articles that may explain why there is a fluctuation.

Finally it will slice three articles and format them into messages to send to the user via twilios api.

### --- TO DO / FUTURE PLANS --- ### 

A news app based on stocks would be an invaluable tool to anyone looking to deal in stocks. personally while I like the idea of using twilio to send messages if i were to develop
this into a more app like program, id want it all in app, using a different menu or popup to actually allow users to stay in app. Also the ability to create an account and log into
the app and save your personal stock preferences.
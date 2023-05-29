### --- PROJECT NAME / DESC --- ###

A small Cafe website tracker than allows us to view cafes that have been 
indexed and rated based on their amenities

### --- PARAMETERS --- ###

Must be able to navigate between pages at the click of a button
must be styled fully in css
links must be clickable and lead to google maps locations
There's a hidden add menu must be accessible when entering /add on end of url
must be able to take information added in and add it to the csv
finally must have proper input validation

### --- HOW IT WORKS --- ###

on launch the server pulls the css file and styles the pages as required
we use a super inheritor to individually style elements as required without 
conflict. 

The program works by taking the data from the csv, formatting it into tables thanks
to flask wtf, and then posting them in a for loop to the cafes page. We use if / else 
statements to ensure that the links are displayed correctly and do not appear twice
then we have a secret add page to enable users to add their own cafe listings

### --- TO DO / FUTURE PLANS --- ### 

By itself not much is left to do with this, however with the upcoming modules on sql
and user authentication this could be fleshed out into a fully functioning website.
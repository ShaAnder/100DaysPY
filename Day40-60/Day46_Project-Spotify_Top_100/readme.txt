### --- PROJECT NAME / DESC --- ###

100 Movies To Watch List - A Small script that scrapes a website and pulls the 100 must watch movies as a dataform for manipulation, in this case we turn it into a helpful list which can be 
saved as a list for later use

### --- PARAMETERS --- ###

must be able to request movie data as a text form
must be able to scrape that data for relevant items
must be able to create a list of those items
and finally must be able to write that list to a text file


### --- HOW IT WORKS --- ###

The program will request the archived data and store them as a response, which we will then scrape using soup for all title class tags of H3 (our movie titles). This is then iterated
through to form a list of the movies which is reversed and finally added to a text file.

### --- TO DO / FUTURE PLANS --- ### 

On it's own this isn't really anything you can do much more with unless you say scrape a movie db and create a random movie suggestion program, even still scraping is ethically gray anything
best in a lot of cases so creating a commercial program that utilizes it is generally out of the question. This is purely for learning purposes
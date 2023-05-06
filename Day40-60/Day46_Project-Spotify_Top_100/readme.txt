### --- PROJECT NAME / DESC --- ###

Spotify Top 100 playlist maker

### --- PARAMETERS --- ###

must be able to request the music as a text form
must be able to scrape that data for relevant items
must be able to create a list of those items
and finally must be able to convert that list and send it as a reuqest to spotify to build a playlist


### --- HOW IT WORKS --- ###

The program will request the archived data and store them as a response, which we will then scrape using soup for all title class tags of H3 (our music titles). This is then iterated
through to form a list of the songs which is then sent through a request to spotify to create a playlist.

### --- TO DO / FUTURE PLANS --- ### 

This seems like an interesting prospect for beyong a project, the idea of being able to instantly create a playlist based on a genre or a year of popular music would be very useful to a lot of people.
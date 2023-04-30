### --- IMPORTS --- ###

import requests
from bs4 import BeautifulSoup

### --- URLS --- ###

#url to write to file
project_url = "Day40-60/Day45_Project-100_Movie_Project/"

#we use the web archive version to complete project to the standard listed
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

### --- SOUP --- ###

#we get our movie list as a response
response = requests.get(URL)
movies_page = response.text

#we then feed it into our bs4 for scraping
soup = BeautifulSoup(movies_page, "html.parser")

### --- CREATING OUR LIST --- ###

#movie list for appending
movies = []
#find all the movies in the soup
scraped_movie_titles = soup.find_all(name="h3", class_="title")
#setup a for loop to get the text and loop through it
for movie in scraped_movie_titles:
    movie_titles = movie.getText()
    movies.append(movie_titles)

#finally want to invert the list so that the #1 spot is first
movies.reverse()
print(movies)
### --- NOW WRITE TO OUR FILE --- ###

#now we want to do another for loop to write all the movies
with open(f"{project_url}movies.txt", "w", encoding="utf-8") as file:
    for movie in movies:
        file.write(f"{movie}\n")

print("Done writing the file!")
###---IMPORTS---###
 
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import spotipy as s

#we want to also get date time for error handling
from datetime import datetime

 
###--- ENV / VARS ---###

#want to load our env files
load_dotenv()
#now we want our spotify auth stuff
ID = os.getenv("SPOTIFY_ID")
SECRET = os.getenv("SPOTIFY_SECRET")
USERNAME = os.getenv("SPOTIFY_USER_NAME")
 
#next we set the scope and url redirect, scope is for the authentication, so the playlist is private
SCOPE = "playlist-modify-private"
#this is for the redirect (as an extra challenge step api wants you to give it the code for url it opens for you)
URL_REDIRECT = "https://example.com"

###---SETUP & DATE ERROR HANDLING---###

#we make up a quick function to start the code out, and go from there:
def get_date():
    """
    Gives the user a formatted date to feed into the rest of the code for later
    Added user feedback and extra steps to ensure correct formatting
    """
    #setup a loop
    give_date = True
    while give_date:
        #first ask the date:
        chosen_date = input("Choose the date you would like to go to! (YYYYMMDD format please):")
        #check if is integer
        if chosen_date.isnumeric() and len(chosen_date) == 8:
            print("Date format correct, we're now checking for a valid date!")
            #next we want to format the date to a correct date time
            formatted_date = datetime.strptime(chosen_date, '%Y%m%d').strftime("%Y-%m-%d")
            print("Formatted date, now checking to see if the date is real!")
            #we get today's date
            today = datetime.today().strftime('%Y-%m-%d')
            #check if they actually entered a date from between the launch of the billboard hot 100 or today (to stop people putting in the year 3000)
            if formatted_date < '1958-08-04' or formatted_date > today:
                print("Those Dates don't exist, please try again")
                continue
            else:
                give_date = False
                return formatted_date
        else:
            print("That's not a valid date, try again")
            continue

#finally we call get_date here at the start to load our date
CHOSEN_DATE = get_date()

#we also want to make a billboard 
BILLBOARD_TOP_100 = f"https://www.billboard.com/charts/hot-100/{CHOSEN_DATE}"

### --- AUTHENTICATE --- ###

def authenticate_user():
    return s.oauth2.SpotifyOAuth(
    client_id=ID,
    client_secret=SECRET,
    redirect_uri=URL_REDIRECT, 
    scope=SCOPE)

sp = authenticate_user()
 
###---SCRAPE BILLBOARD---###
soup = BeautifulSoup(requests.get(BILLBOARD_TOP_100).text, "html.parser")
top_100_songs = []
#now we make soup, tell it to go through this specific selector combination to find the text at the end
songs = soup.select(selector='li ul li h3')
for song in songs:
    #we append the songs to the list
    top_100_songs.append(song.get_text(strip=True))

###---REQUEST---###
 
# now we create our authentication manager, key with all our detals
spotify = s.Spotify(
    auth_manager=sp)
 
#get our cached token
access_token = sp.get_cached_token()
 
#if no cached token we get one
if access_token == None:
    access_token = sp.get_access_token()
else:
    print("We have a token!")
 
#set our current user
current_user = spotify.current_user() 
 
###---MAIN---###
 
#now the main loop, we make a list to hold the songs
top_100_uris = []
#loop through the song and find it in spotify
for song in top_100_songs:
    song_name = spotify.search(q=song, limit=1, type="track")
    #error handling to catch songs that don't work / can't be found
    try:
        song_uri = song_name["tracks"]["items"][0]["uri"]
        top_100_uris.append(song_uri)
    except IndexError:
        print(f"{song_name} could not be found. Skipped adding")
        continue

###---Create The Playlist---###

#set our playlist id / name
PLAYLIST_ID = None 
PLAYLIST_NAME = f"{CHOSEN_DATE} Billboard playlist"

#gets a list of playlists
playlists = spotify.current_user_playlists(limit = 50) 
 
#search for the playlist, if it finds one of same name, set the id for updating the playlist
#(this is in case the user creates multiple of the same it can then overwrite instead of making another)
for info in playlists['items']:
    if info['name'] == PLAYLIST_NAME:
        PLAYLIST_ID = info['id']
        break

#if it can't find the id, make a new playlist 
if not PLAYLIST_ID:
    print('Creating playlist: ', PLAYLIST_NAME)
    playlist = spotify.user_playlist_create(USERNAME, PLAYLIST_NAME, public=False, description="Auto generated billboard playlist")

    ###---Add To The Playlist---###

    ###THIS IS NOT PART OF THE PROJECT | ITS MY OWN ADDITION --- SEE README FOR INFO###
    spotify.playlist_add_items(
        playlist_id=playlist['id'], 
        items=top_100_uris, 
        position=None
        )
    ###THIS IS NOT PART OF THE PROJECT | ITS MY OWN ADDITION --- SEE README FOR INFO###

#finally we do setup / cleanup of confirmation, this will give a link to the user and also give basic feedback to them

    print(f'Playlist generated, Link: {playlist["external_urls"]["spotify"]}')
else: 
    print('Retrieving playlist: ', PLAYLIST_NAME)
    playlist = spotify.playlist(PLAYLIST_ID)
    print(f'Playlist already exists, Link: {playlist["external_urls"]["spotify"]}')
print(f'Playlist ID: {PLAYLIST_ID}. ID Check: ', playlist['id'] == PLAYLIST_ID) 
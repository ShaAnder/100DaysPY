### --- IMPORTS --- ### 

#we want tkinter to do our canvas
from tkinter import *
#pandas to read the csv
import pandas
#we want random to pull random cards
import random

### --- VARS/CONSTANTS --- ###

#next we want to create a variables for the path to the images
img_path ="Day20-40/Day31_Project-Flash_Card_App/course_project" 

card_back = ""
card_front = "/images/card_front.png"
right = "/images/right.png"
wrong = "/images/wrong.png"

#we want to get the location of the french words too, as well as create a var for where we want to save the words to learn file (for later learning)
french_words = "Day20-40/Day31_Project-Flash_Card_App/course_project/data/french_words.csv"
to_learn = "Day20-40/Day31_Project-Flash_Card_App/course_project/data/"

#we also will want some more here for the likes of BG colour, current word, ect

BG_COLOR = "#B1DDC6"
CURRENT_WORD = ""

### --- SCR SETUP --- ###

#setup our window
window = Tk()
window.title("Flash Card Study For Serious Gamers")
window.config(padx=50, pady=50, bg=BG_COLOR)

#setup canvas
canvas = Canvas(width=800, height=526)


#now we want our card_front image photoimage can't find full path so we store paths in 2 vars
front = PhotoImage(file=img_path+card_front)
card_background = canvas.create_image(400, 263, image=front)
#next we want two blank text pieces that will be filled later on witht hese fonts
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
#we want the background color to be filled 
canvas.config(bg=BG_COLOR, highlightthickness=0)
#finally we grid it
canvas.grid(row=0, column=0, columnspan=2)

### --- BUTTONS --- ###

#now we create our buttons for the check and cross 
cross_image = PhotoImage(file=img_path+wrong)
unknown_button = Button(image=cross_image, highlightthickness=0)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file=img_path+right)
known_button = Button(image=check_image, highlightthickness=0)
known_button.grid(row=1, column=1)

### --- RUN --- ###

window.mainloop()
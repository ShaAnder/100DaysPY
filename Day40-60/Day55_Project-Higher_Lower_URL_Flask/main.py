### --- IMPORTS --- ###

from flask import Flask
import random

### --- APP SETUP --- ###

app = Flask(__name__)

### --- SETUP OUR RANDOM NUMBERS --- ###

#we want to create a list of random numbers from 1 - 100 and i don't want to type it
guess_numbers = []
for i in range(1,101,1):
    guess_numbers.append(i)
print(guess_numbers)
#then pick a number to guess
number_to_guess = random.choice(guess_numbers)
print(number_to_guess)

### --- FUNCS --- ###

@app.route('/')
def welcome():
    return  '<h1>Welcome To The Higher Lower Game</h1>' \
            '<p>The Rules are simple type a number into the hotbar and see how right you are!</p>' \
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTUyNTlkYWUwZTU0YWNlMDIyYTlmN2U4OTFlZDE0OGRhNzA1MGZmZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/H1dxi6xdh4NGQCZSvz/giphy.gif" alt="cat-typing">'

@app.route('/<int:number>')
def guess(number):
    if number > number_to_guess:
        return  "<h1 style ='color: red;'>This ain't it chief try again! It's too high!</h1>" \
                '<img src="https://media.tenor.com/1CXKFszBrn4AAAAd/nya-suke-cat.gif" alt="cat-typing">'
    if number < number_to_guess:
        return  "<h1 style ='color: purple;'>This ain't it chief try again! It's too low</h1>" \
                '<img src="https://37.media.tumblr.com/6dc68e82ac10e8dd44235e14dd2ad567/tumblr_n7e3nfJmUX1qbxi45o1_500.gif" alt="cat-typing">'
    else:
        return  "<h1 style ='color: green;'>Ayy you got it!</h1>" \
                '<img src="https://media.tenor.com/Y8-MoUeKfd4AAAAC/cat-lick.gif" alt="cat-typing">'          

### --- MAIN --- ###

if __name__ == "__main__":
    app.run(debug=True)
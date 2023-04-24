### --- PROJECT NAME / DESC --- ###

OOP QUIZ USING TKINTER AND APIS - A precurser to an app that uses a ui and apis to create a quiz interface with modelled questions


### --- WHAT IT NEEDS TO DO --- ###

- The program needs to first be able to get the data in a formatted way from the apis
- Then take that data and display it for the user to be able to make a guess on
- Depending on the users guess it will then give feed back to the user on if it was correct or incorrect
- At the end will tally up the score and hand it back to the user 

### --- HOW IT WORKS --- ###

At it's base level there are 4 main functions going on in the app.
- Firstly the data file is querying a random quiz db from the api and getting back 10 questions to feed into the program
- The ui file is responsible for building the tkinter ui the user can interact with changing the questions and feedback
- the question model gets the questions and formats them for the ui
- finally the quizbrain is in charge of managing the quiz and keeping the quiz moving via question counting

The data file will be sent to main.py and fed into the question model then the result is fed into the quizbrain
The quizbrain sends all the data to the ui which then uses that data to progress the quiz
The user is then presented with a question and Y/N options, depending on what they answer they get feedback
The game goes for 10 questions at which point it will end the quiz and give the user a final score

### --- TO DO / FUTURE PLANS --- ### 

This is one I really want to make a working app out of using api knowledge ect. Firstly id want to design multiple state windows, a main menu a scoreboard
and menus to select difficulties / topics
As well as this having a random feature and a way to repeat the quiz would be great ideas. 
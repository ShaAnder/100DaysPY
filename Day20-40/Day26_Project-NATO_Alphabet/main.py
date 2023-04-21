#!usr/bin/env/python

### --- IMPORTS --- ###

import pandas

### --- USER INPUT --- ###

#we want the user to type a word or words, and they must be returned in upper case
user_word = input("Please type a word: ").upper()

### --- FILE LOC --- ###

#not cwd so creating var, this will enable easier changing / testing of the code
nato = "Day20-40/Day26_Project-NATO_Alphabet/nato_phonetic_alphabet.csv"

### --- MAIN --- ###

#first we read the csv
data = pandas.read_csv(nato)

#next we iterrows over the csv, to make our own nato alphabet dict structured like {"A":"Alpha", "B":"Bravo",} ect
nato_dict = {row.letter: row.code for (index, row) in data.iterrows()}

#now we check the letters of our word and pull back the values that the letter matches keys with 
# phonetics = [nato_dict[l] for l in user_word]
# print(phonetics)

#(this is project complete)

### --- EXTRA STEP --- ###

#As an added step, I wanted this to work even if numbers/spaces/symbols were included, to do this we add:
phonetics = [nato_dict[l] if l in nato_dict else l for l in list(user_word)]
#we tell it to check the dict for the letter, else put the letter in the list as seen in order of user_word
print(phonetics)


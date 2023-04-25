### --- IMPORTS --- ###

#import requests for our requests
import requests

#import os and dotenv for envvariables
import os
from dotenv import load_dotenv

#we need datetime for getting dates logged on the sheet
from datetime import *

### --- ENVS / VARS --- ###

#load our envs
load_dotenv()

#our google sheet here
GOOGLE_SHEET = os.getenv("G_SHEET")

#nutritionix api key and app ID
nutritionix_api_key = os.getenv("API_KEY")
nutritionix_app_id = os.getenv("APP_ID")

#variables for the exercise parameters
query = input("How much exercise did you do? Please answer in the form of (ex: I ran 2km and walked 3km): ")
gender = "male"
weight_kg = 80.01
height_cm = 181.12
age = 32

### --- ENDPOINT --- ###

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/6e075bd305c6812ca7005c8a4abfe0b9/workouts/workouts"

exercise_headers = {
"x-app-id": nutritionix_app_id,
"x-app-key": nutritionix_api_key,
}

exercise_parameters = {
    "query": query,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "age": age,
}

### --- REQUEST --- ###

#this is our nutritionix request, to tell it what we did exercise wise
response = requests.post(url=exercise_endpoint, json=exercise_parameters, headers=exercise_headers)
result = response.json()
print(result)

#we want to get datetime for now so we can add them to the sheet
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

#now we want to loop through the exercises in the result (in case multiple) and get the sheety inputs
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": f'{exercise["duration_min"]} min',
            "calories": exercise["nf_calories"]
        }
    }

    #finally we setup the sheet response
    sheet_response = requests.post(sheety_endpoint, json=sheet_inputs)
    print(sheet_response.text)
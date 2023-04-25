### --- IMPORTS --- ### 

#import os and load dotenv for env variables
import os
from dotenv import load_dotenv

#requests for our api calls
import requests

#import datetime for automating todays date
from datetime import date

### --- ENV VARS --- ###

#we load our env and then get our env vars
load_dotenv()

pixela_username = os.getenv("USER")
pixela_token = os.getenv("TOKEN")

### --- FUNCS --- ###

def get_date():
    """Gets todays date and formats it for the parameter
    """
    today = date.today()
    today_format = today.strftime("%Y%m%d")
    return today_format

### --- VARIABLES --- ###

#variables for creating the graph, we create these so as not to neeed to make changes to the params
graph_id = "graph1"
graph_name = "Walking Graph"
unit_of_measurement = "Km"
unit_type = "float"
graph_color = "ajisai"

#we want to get our date and the amount of work done for the day, we're going to automate the day using a function below

formatted_date = get_date()
quantity = input("How much work did you do / time spent [corresponds to the unit_of_measurement provided above]: ")

### --- PARAMETERS --- ###

#parameters needed to create a pixe.la user
pixela_params = {
    "token": pixela_token,
    "username": pixela_username, 
    "agreeTermsOfService": "yes", 
    "notMinor": "yes",
}

#header containing our pixela_token, for use when creating / editing a graph
graph_header = {
    "X-USER-TOKEN": pixela_token,
}

#parameters for creating a new graph
graph_params = {
    "id": graph_id,
    "name": graph_name,
    "unit": unit_of_measurement,
    "type": unit_type,
    "color": graph_color
}

add_to_graph_params = {
    "date": formatted_date,
    "quantity": quantity,
}

# ### --- ENDPOINTS --- ###

#endpoint for the website pixe.la
pixela_endpoint = "https://pixe.la/v1/users"

#endpoint to create the graph
graph_endpoint = f"{pixela_endpoint}/{pixela_username}/graphs"

#endpoint to add to the graph
add_to_graph_endpoint = f"{graph_endpoint}/{graph_id}"

### --- MAIN --- ###

#STEP1 - Creating a Pixe.la user

# using the pixe.la endpoint as well as our pixe.la params we send a request to create a user
# once made we can comment this out as it will no longer be used in the code

# response = requests.post(url=pixela_endpoint, json=pixela_params)
# print(response.text)

#STEP2 - Creating a graph

#we now create our graph with the graph endpoint, graph params and the graph header, once made this can be commented out

# response = requests.post(url=graph_endpoint, json=graph_params, headers=graph_header)
# print(response.text)

#to view the graph you need to go to the following link:
#f"https://www.pixe.la/v1/users/itsspookr/graphs/graph1.html"

#STEP3 - Adding to the graph

#to add to the graph we make another request, this one sending the information we want in the form of exercise done and the date
response = requests.post(url=add_to_graph_endpoint, json=add_to_graph_params, headers=graph_header)
print(response.text)

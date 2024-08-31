import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

# STEP 1:
APP_ID = "e01bf2f7"
API_KEY = "6793a5ae942ef0d748a97ec111236cd6"
# Sheety
SHEETY_USERNAME = "bhuvana"
SHEETY_PASSWORD = "sheetypassword"

#
google_sheet_api = "https://api.sheety.co/5f0c80811268371162049f2ec8037243/bhuvanaMyWorkouts/workouts"

# https://docs.google.com/spreadsheets/d/1LL1FfPbAzqWr0hS25EuFYdHEKXUJE7lBcKe7sQ9v1a0/edit#gid=0

# STEP2:
# Nutritionix
# Natural Language for Exercise

user_exercise = input("Tell me which exercise you did?: ")
nutritionix_endpoint = "https://trackapi.nutritionix.com"
nl_exercise_endpoint = "/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

nt_body = {
    "query": user_exercise
}

# getting data from Nutritionix API using POST method

response = requests.post(url=f"{nutritionix_endpoint}{nl_exercise_endpoint}", data=nt_body, headers=headers)
data = response.json()

# Format the date and time

whole_date = datetime.now()
current_date = whole_date.strftime("%d/%m/%y")
current_time = whole_date.strftime("%H:%M:%S")

# Format the data to upload in Google sheet

for i in range(0, len(data["exercises"])):
    exercise_data = data["exercises"][i]
    exercise = exercise_data["user_input"]
    duration = exercise_data["duration_min"]
    calories = exercise_data["nf_calories"]

    # Post the data to Google sheets :

    sheety_header = {
         "content-Type": "application/json",
         "Authorization": "Basic Ymh1dmFuYTpzaGVldHlwYXNzd29yZA=="
    }

    body = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    basic = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD)

    sheety_response = requests.post(url=google_sheet_api, json=body, headers=sheety_header, auth=basic)
    sheety_response.raise_for_status()
    print(sheety_response.text)

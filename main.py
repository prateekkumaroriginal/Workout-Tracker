import requests
import os
from datetime import datetime

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
SHEETY_AUTH_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")

nutritionix_endpoint = "https://trackapi.nutritionix.com"
sheety_endpoint = "https://api.sheety.co/"

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

params = {
    'query': input("What exercises did you do today?\n"),
    'gender': 'YOUR_GENDER',
    'weight_kg': 'YOUR_WEIGHT',
    'height_cm': 'YOUR_HEIGHT',
    'age': 'YOUR_AGE',
}

now = datetime.now()

response = requests.post(url=f"{nutritionix_endpoint}/v2/natural/exercise", json=params, headers=headers)
result = response.json()

exercises = result['exercises']

for exercise in exercises:
    sheet_inputs = {
        'workout': {
            'date': now.date().strftime("%d/%m/%Y"),
            'time': now.time().strftime("%H:%M:%S"),
            'exercise': exercise['user_input'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories'],
        }
    }

    auth_header = {
        'Authorization': SHEETY_AUTH_TOKEN
    }

    response = requests.post(
        url="https://api.sheety.co/2dc9cd05924e1a5bc77eb4f3a6902157/YOUR_SHEETY_PROJECT_NAME_IN_CAMEL_CASE/YOUR_SPREADSHEET_NAME_IN_CAMEL_CASE",
        json=sheet_inputs,
        headers=auth_header
    )

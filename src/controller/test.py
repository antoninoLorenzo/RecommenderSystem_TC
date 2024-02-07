import json
from http import HTTPStatus
import requests


# Define the URL of the running FastAPI server
url = "http://127.0.0.1:8000/engine/v1/offers"

# Define the payload for the POST request
payload = {
    "query": "python developer",

    "user": {
        "dev_id":  1,
        "f_name": "John",
        "l_name": "Doe",
        "mail": "john.doe@example.com",
        "psw": "password123",
        "location": {
            "loc_id":  1,
            "loc_name": "New York",
            "lat":  40.7128,
            "lon": -74.0060
        },
        "skills": ["Python", "Django"]
    }
}


# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == HTTPStatus.OK:
    print("Request was successful.")
    print("Response body:")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Request failed with status code {response.status_code}.")

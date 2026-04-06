import time
import random
import requests

URL = "http://localhost:8003/tracking/location"

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzhiYmFkZmItYTY2NS00MjYxLTk3OWQtZjA2Y2M0YWRjYjI0IiwiZXhwIjoxNzc1NDgwODc4fQ.qiELpR1GEpWd5MRmE9P_TpfiSU_Ty9ikGuxMOV2YbfQ",
    "Content-Type": "application/json"
}

def generate_coordinates():
    # Example: simulate movement near Bangalore
    latitude = round(random.uniform(12.90, 13.10), 6)
    longitude = round(random.uniform(77.50, 77.70), 6)
    return latitude, longitude


while True:
    lat, lon = generate_coordinates()

    payload = {
        "device_id": "GPS2",
        "latitude": lat,
        "longitude": lon
    }

    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        print(f"Sent: {payload} | Status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(7)
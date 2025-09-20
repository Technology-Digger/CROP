import requests

url = "http://127.0.0.1:8000/recommendation"

data = {
    "N": 0,
    "P": 0,
    "K": 0,
    "temperature": 0,
    "humidity": 0,
    "ph": 0,
    "rainfall": 0
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())

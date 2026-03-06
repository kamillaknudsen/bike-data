import requests
import json
from datetime import datetime
import os

# update

if not os.path.exists('data'):
    os.makedirs('data')

url = "https://api.datadeelmobiliteit.nl/vehicles"

try:
    response = requests.get(url)
    data = response.json()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data/bikes_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(data, f)

    print(f"Successfully saved data to {filename}")
except Exception as e:
    print(f"Error: {e}")
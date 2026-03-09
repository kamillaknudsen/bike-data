import requests
import csv
from datetime import datetime
import os

if not os.path.exists('data'):
    os.makedirs('data')

url = "https://mds.dashboarddeelmobiliteit.nl/stops"

try:
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()

    lat_min, lat_max = 51.837, 51.998
    lon_min, lon_max = 4.256, 4.712

    stops = json_data.get("data", {}).get("stops", [])
    timestamp = datetime.now().isoformat()

    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/hubs_{today_date}.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "fetch_timestamp", "stop_id", "name", "lat", "lon", 
                "bike_capacity", "bikes_available", "spaces_available"
            ])

        for stop in stops:
            lat = stop["location"]["geometry"]["coordinates"][1]
            lon = stop["location"]["geometry"]["coordinates"][0]

            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                capacity_data = stop.get("capacity", {})
                bike_cap = capacity_data.get("bicycle") or capacity_data.get("combined") or 0
                writer.writerow([
                    timestamp,
                    stop.get("stop_id"),
                    stop.get("name"),
                    lat,
                    lon,
                    bike_cap,
                    stop.get("num_vehicles_available", {}).get("bicycle", 0),
                    stop.get("num_places_available", {}).get("bicycle", 0)
                ])

    print(f"Successfully logged {len(stops)} hubs to {filename}")

except Exception as e:
    print(f"Error: {e}")
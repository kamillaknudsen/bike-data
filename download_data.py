import requests
import csv
from datetime import datetime
import os

if not os.path.exists('data'):
    os.makedirs('data')

url = "https://api.datadeelmobiliteit.nl/vehicles"

try:
    response = requests.get(url)
    response.raise_for_status()

    json_data = response.json()
    vehicles = json_data["data"]["vehicles"]

    lat_min, lat_max = 51.837, 51.998
    lon_min, lon_max = 4.256, 4.712

    timestamp_str = json_data["last_updated"]
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H:%M:%S")

    filename = f"data/bikes_{date_str}.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "system_id",
                "vehicle_id",
                "lat",
                "lon",
                "is_reserved",
                "is_disabled",
                "form_factor",
                "propulsion_type"
            ])

        for v in vehicles:
            lat = v.get("lat")
            lon = v.get("lon")

            if lat is not None and lon is not None:
                if lat_min <= v.get("lat") <= lat_max and lon_min <= v.get("lon") <= lon_max:
                    if v.get("form_factor") == "bicycle" and v.get('propulsion_type') != "electric_assist":

                        writer.writerow([
                            timestamp_str,
                            v.get("system_id"),
                            v.get("vehicle_id"),
                            v.get("lat"),
                            v.get("lon"),
                            v.get("is_reserved"),
                            v.get("is_disabled"),
                            v.get("form_factor"),
                            v.get("propulsion_type")
                        ])

    print(f"Saved bike snapshot at {time_str}")

except Exception as e:
    print(f"Error: {e}")

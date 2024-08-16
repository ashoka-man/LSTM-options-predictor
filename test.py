import csv
import requests
from datetime import datetime

# URLs and query parameters
theta_url = "http://127.0.0.1:25510/v2/bulk_hist/option/ohlc"
theta_querystring = {"exp": "20240809", "start_date": "20240805", "end_date": "20240809", "use_csv": "false",
                     "root": "SPY", "ivl": "60000"}
theta_headers = {"Accept": "application/json"}

polygon_url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-08-05/2024-08-09?adjusted=true&sort=asc&apiKey=ppCltLjDE20hppcB6gxF950W25rkL6_j"

# Fetch data from Polygon
polygon_response = requests.get(polygon_url)
polygon_data = polygon_response.json()

# Fetch data from Theta
theta_response = requests.get(theta_url, headers=theta_headers, params=theta_querystring)
theta_data = theta_response.json()

# Format the data
filtered_results = []

for polygon_entry in polygon_data['results']:
    polygon_price = polygon_entry['c']  # Close price from Polygon
    polygon_timestamp = polygon_entry['t']  # Timestamp from Polygon

    # Convert the Unix timestamp to YYYYMMDD format
    polygon_date = datetime.utcfromtimestamp(polygon_timestamp / 1000).strftime('%Y%m%d')

    for option_entry in theta_data['response']:
        for tick in option_entry['ticks']:
            option_close_price = tick[4] / 1000  # Adjust Theta close price to represent actual value
            option_date = str(tick[7])  # Date from Theta (already in YYYYMMDD format)

            # Check if the date matches
            if polygon_date == option_date:
                # Filter the options based on the price condition
                if abs(option_close_price - polygon_price) <= 5:
                    filtered_results.append({
                        "polygon_price": polygon_price,
                        "polygon_date": polygon_date,
                        "option_close_price": option_close_price,
                        "option_expiration": option_entry['contract']['expiration'],
                        "option_strike": option_entry['contract']['strike'] / 1000,  # Adjust strike price
                        "option_right": option_entry['contract']['right']
                    })

# Define CSV file name
csv_file_name = "test.csv"

# Define CSV columns
csv_columns = ["polygon_price", "polygon_date", "option_close_price", "option_expiration", "option_strike",
               "option_right"]

# Write data to CSV
with open(csv_file_name, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for data in filtered_results:
        writer.writerow(data)

print(f"Data has been written to {csv_file_name}")

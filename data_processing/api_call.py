import requests
from datetime import datetime
import pytz
import csv

# Define the API endpoint
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-08-14/2024-08-14?adjusted=true&sort=asc&apiKey=ppCltLjDE20hppcB6gxF950W25rkL6_j"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data)

    # Check if 'results' is in the response data
    if 'results' in data and data['results']:
        # Define the EST timezone
        est = pytz.timezone('US/Eastern')

        # Open a CSV file for writing
        with open('spy.csv', mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Volume', 'Close Price', 'Timestamp (EST)'])

            for result in data['results']:
                volume = result['v']
                close_price = result['c']
                timestamp = result['t']

                # Convert the Unix timestamp to a UTC datetime object
                utc_time = datetime.utcfromtimestamp(timestamp / 1000)

                # Convert the UTC datetime to EST
                est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(est)

                # Format the EST datetime object
                formatted_time = est_time.strftime('%Y-%m-%d %H:%M:%S')

                # Write the data points into the CSV file
                writer.writerow([volume, close_price, formatted_time])

        print("Data has been written to spy.csv")
    else:
        print("No results found in the API response.")
else:
    print(f"Failed to retrieve data: {response.status_code}")

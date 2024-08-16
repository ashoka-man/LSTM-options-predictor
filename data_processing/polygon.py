import requests
from datetime import datetime
import pytz
import csv

# Define the API endpoint
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-08-05/2024-08-09?adjusted=true&sort=asc&apiKey=ppCltLjDE20hppcB6gxF950W25rkL6_j"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Define the EST timezone
    est = pytz.timezone('US/Eastern')

    # Create a list to store the data
    data_list = []

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

        # Append the data point to the list
        data_list.append([volume, close_price, formatted_time])

    # Calculate the row numbers starting from 0 at the bottom (latest data)
    row_numbers = list(range(len(data_list)))

    # Reverse the row numbers to start from 0 at the bottom
    row_numbers.reverse()

    # Open a CSV file for writing
    with open('./stockprice.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Row Number', 'Volume', 'Close Price', 'Timestamp (EST)'])

        # Write the data points into the CSV file with reversed row numbers
        for i, row in zip(row_numbers, data_list):
            writer.writerow([i] + row)

    print("Data written to CSV file")

else:
    print(f"Failed to retrieve data: {response.status_code}")

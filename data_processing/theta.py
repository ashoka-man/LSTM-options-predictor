import requests
import csv
from datetime import datetime, timedelta

# Define the URL and query parameters
url = "http://127.0.0.1:25510/v2/hist/option/ohlc"
querystring = {
    "root": "SPY",
    "exp": "20240809",
    "strike": "522000",
    "right": "C",
    "start_date": "20240805",
    "end_date": "20240809",
    "use_csv": "false",
    "ivl": "60000"
}

# Set the headers
headers = {"Accept": "application/json"}

# Send the GET request
response = requests.get(url, headers=headers, params=querystring)

# Parse the JSON response
data = response.json()

# Extract indices based on the format
format_indices = {name: idx for idx, name in enumerate(data['header']['format'])}

# List to store extracted data
extracted_data = []

# Iterate over the response in reverse order to start with the earliest date
for i, record in enumerate(reversed(data['response']), start=1):
    ms_of_day = record[format_indices['ms_of_day']]
    close = record[format_indices['close']]
    volume = record[format_indices['volume']]
    date = record[format_indices['date']]

    # Convert ms_of_day to hours and minutes, then add to midnight (12:00 AM)
    timestamp = (datetime(1970, 1, 1) + timedelta(milliseconds=ms_of_day)).time()

    # Format the timestamp as HH:MM AM/PM
    formatted_time = timestamp.strftime("%I:%M %p")

    # Combine date and formatted time
    formatted_timestamp = f"{datetime.strptime(str(date), '%Y%m%d').strftime('%Y-%m-%d')} {formatted_time}"

    # Append data to the extracted_data list
    extracted_data.append([i, volume, close, formatted_timestamp])

# Reverse the list so the highest row number is at the top
extracted_data.reverse()

# Define the CSV file name
csv_file_name = "stockoption.csv"

# Write the extracted data to the CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Row Number", "Volume", "Close Price", "Timestamp (EST)"])
    # Write the data rows
    writer.writerows(extracted_data)

print(f"Data has been written to {csv_file_name}")

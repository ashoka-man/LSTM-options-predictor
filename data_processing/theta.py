import requests
import csv

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

# Iterate over the response and extract close, volume, and date
for i, record in enumerate(reversed(data['response']), start=1):
    close = record[format_indices['close']]
    volume = record[format_indices['volume']]
    date = record[format_indices['date']]
    extracted_data.append([i, volume, close, date])

# Define the CSV file name
csv_file_name = "extracted_data.csv"

# Write the extracted data to the CSV file
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Number", "Volume", "Close Price", "Timestamp"])
    # Write the data rows
    writer.writerows(extracted_data)

print(f"Data has been written to {csv_file_name}")

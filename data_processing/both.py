import requests
import csv
from datetime import datetime, timedelta
import pytz

# Define the URLs and query parameters
url_1 = "http://127.0.0.1:25510/v2/hist/option/quote"
querystring_1 = {
    "root": "SPY",
    "exp": "20240809",
    "strike": "522000",
    "right": "C",
    "start_date": "20240805",
    "end_date": "20240809",
    "ivl": "60000"
}
headers_1 = {"Accept": "application/json"}

url_2 = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-08-05/2024-08-09?adjusted=true&sort=asc&apiKey=ppCltLjDE20hppcB6gxF950W25rkL6_j"

# Send the GET requests
response_1 = requests.get(url_1, headers=headers_1, params=querystring_1)
response_2 = requests.get(url_2)

# Check if both requests were successful
if response_1.status_code == 200 and response_2.status_code == 200:
    data_1 = response_1.json()
    data_2 = response_2.json()

    # Extract indices based on the format from the first API
    format_indices = {name: idx for idx, name in enumerate(data_1['header']['format'])}

    # Define the EST timezone for the first and second API data
    est = pytz.timezone('US/Eastern')

    # Lists to store extracted data
    extracted_data_1 = []
    extracted_data_2 = []

    # Process data from the first API
    for i, record in enumerate(reversed(data_1['response']), start=1):
        ms_of_day = record[format_indices['ms_of_day']]
        ask_price = round(record[format_indices['ask']], 2)
        bid_price = round(record[format_indices['bid']], 2)
        ask_size = round(record[format_indices['ask_size']], 2)
        bid_size = round(record[format_indices['bid_size']], 2)
        date = record[format_indices['date']]

        # Calculate the average of ask and bid prices
        avg_price = round((ask_price + bid_price) / 2, 2)

        # Convert the date to a datetime object
        date_obj = datetime.strptime(str(date), '%Y%m%d')

        # Add milliseconds since midnight to the date (midnight ET)
        et_time = date_obj + timedelta(milliseconds=ms_of_day)

        # Convert to ET timezone
        et_time = est.localize(et_time)

        # Format the ET datetime object
        formatted_timestamp = et_time.strftime('%Y-%m-%d %I:%M %p')

        # Append the data to the extracted_data_1 list
        extracted_data_1.append([i, ask_size, ask_price, bid_size, bid_price, avg_price, formatted_timestamp])

    # Reverse the extracted_data_1 list so that the highest row number is at the top
    extracted_data_1.reverse()

    # Calculate deltas for the first API data
    delta_data_1 = []
    for j in range(len(extracted_data_1)):
        if j == 0:
            # No delta for the first entry, so use 0
            delta_data_1.append([0, 0, 0, 0, 0, 0, extracted_data_1[j][-1]])
        else:
            delta_data_1.append([
                extracted_data_1[j][0],
                round(extracted_data_1[j][1] - extracted_data_1[j-1][1], 2),  # Delta Ask Size
                round(extracted_data_1[j][2] - extracted_data_1[j-1][2], 2),  # Delta Ask Price
                round(extracted_data_1[j][3] - extracted_data_1[j-1][3], 2),  # Delta Bid Size
                round(extracted_data_1[j][4] - extracted_data_1[j-1][4], 2),  # Delta Bid Price
                round(extracted_data_1[j][5] - extracted_data_1[j-1][5], 2),  # Delta Average of Bid and Ask
                extracted_data_1[j][-1]  # Timestamp
            ])

    # Process data from the second API
    for result in data_2['results']:
        volume = round(result['v'], 2)
        close_price = round(result['c'], 2)
        timestamp = result['t']

        # Convert the Unix timestamp to a UTC datetime object
        utc_time = datetime.utcfromtimestamp(timestamp / 1000)

        # Convert the UTC datetime to EST
        est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(est)

        # Format the EST datetime object
        formatted_time = est_time.strftime('%Y-%m-%d %H:%M:%S')

        # Append the data point to the list
        extracted_data_2.append([volume, close_price, formatted_time])

    # Calculate deltas for the second API data
    delta_data_2 = []
    for k in range(len(extracted_data_2)):
        if k == 0:
            # No delta for the first entry, so use 0
            delta_data_2.append([0, 0, extracted_data_2[k][-1]])
        else:
            delta_data_2.append([
                round(extracted_data_2[k][0] - extracted_data_2[k-1][0], 2),  # Delta Volume
                round(extracted_data_2[k][1] - extracted_data_2[k-1][1], 2),  # Delta Close Price
                extracted_data_2[k][-1]  # Timestamp
            ])

    # Calculate the row numbers for the second API data starting from 0 at the bottom (latest data)
    row_numbers = list(range(len(delta_data_2)))
    row_numbers.reverse()

    # Define the CSV file names
    csv_file_name_1 = "stockoption_deltas.csv"
    csv_file_name_2 = "stockprice_deltas.csv"

    # Write the first delta data to the first CSV file
    with open(csv_file_name_1, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Row Number', 'Delta Ask Size', 'Delta Ask Price', 'Delta Bid Size', 'Delta Bid Price', 'Delta Average of Bid and Ask', 'Timestamp (EST)'])
        # Write the delta data rows
        writer.writerows(delta_data_1)

    print(f"Delta data has been written to {csv_file_name_1}")

    # Write the second delta data to the second CSV file
    with open(csv_file_name_2, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Row Number', 'Delta Volume', 'Delta Close Price', 'Timestamp (EST)'])
        # Write the delta data points into the CSV file with reversed row numbers
        for i, row in zip(row_numbers, delta_data_2):
            writer.writerow([i] + row)

    print(f"Delta data has been written to {csv_file_name_2}")

else:
    if response_1.status_code != 200:
        print(f"Failed to retrieve data from the first API: {response_1.status_code}")
    if response_2.status_code != 200:
        print(f"Failed to retrieve data from the second API: {response_2.status_code}")

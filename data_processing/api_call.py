import requests
from datetime import datetime
import pytz

# Define the API endpoint
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-08-14/2024-08-14?adjusted=true&sort=asc&apiKey=ppCltLjDE20hppcB6gxF950W25rkL6_j"

# Send a GET request to the API
response = requests.get(url)

# Parse the JSON data from the response
data = response.json()

# Define the EST timezone
est = pytz.timezone('US/Eastern')

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

    # Print the extracted values along with the converted timestamp in EST
    print(f"Volume: {volume}, Close Price: {close_price}, Timestamp (EST): {formatted_time}")

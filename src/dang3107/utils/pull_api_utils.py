import requests
import json
import os
import datetime




def add_timestamp_to_filename(original_filename):
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the timestamp
    timestamp = now.strftime('%Y-%m-%d-%H:%M')

    # Split the original filename into name and extension
    name, extension = os.path.splitext(original_filename)

    # Create a new filename with the timestamp appended before the file extension
    new_filename = f"{name}_{timestamp}{extension}"

    return new_filename


def fetch_ticketmaster_events(api_key, locale, startDateTime, size, countryCode, genreID, subGenreId, sort, endpoint):

    
    all_data = []
    # Loop through pages 0 to 4 to adhere to the 1000-item limit
    for page in range(5):
        # Define the parameters for the request
        params = {
            'apikey': api_key,
            'locale': locale,
            'startDateTime': startDateTime,
            'size': size,
            'countryCode': countryCode,
            'genreId': genreID,
            'subGenreId': subGenreId,
            'sort': sort,
            'page': page
        }

        # Send the GET request to the API
        response = requests.get(endpoint, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            events = data.get('_embedded', {}).get('events', [])
            if not events:
                print(f"No more events found. Stopping at page {page}.")
                break
            all_data.extend(events)
            return json.dumps(all_data, indent = 4)

        else:
            print(f'Error: {response.status_code}')
            print(response.text)
            break


if __name__ == "__main__":
    fetch_ticketmaster_events(        # Define your API key and endpoint
        os.environ['TICKETMASTER_API_KEY'],
        '*',
        '2024-12-01T01:57:00Z',
        200,
        'US',
        'KnvZfZ7vAv1',
        'KZazBEonSMnZfZ7vaa1',
        'date,asc',
        'https://app.ticketmaster.com/discovery/v2/events.json'
    )
   
#     # Save the data to a JSON file
#     with open('ticketmaster_data_2.json', 'w') as json_file:
#         json.dump(all_data, json_file, indent=4)
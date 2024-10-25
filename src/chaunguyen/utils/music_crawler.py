
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_url_for_date():
    today = datetime.today()
    target_date = today - timedelta(days=2)
    formatted_date = target_date.strftime('%Y%m%d')
    url = f"https://kworb.net/radio/archives/{formatted_date}.html"
    return url

def crawl_music_chart_to_df():
    url = get_url_for_date()
    # Get the HTML content of the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find column names from the table header
    table_header = soup.find('thead').find_all('th')
    column_names = [th.text.strip() for th in table_header]
    column_names[2] = 'Artist'  # Rename the 'Artist and Title' column to 'Artist'
    column_names[-2] = 'Apple Music'
    column_names.insert(3, 'Song Title')  # Insert a new 'Song Title' column

    music_data = []

    # Find the table body containing the song entries
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')  # Find all rows in the table body

    # Iterate over each row and extract the data
    for row in rows:
        cells = row.find_all('td')
        artist_song_div = cells[2].find('div')  # Extract artist and song title
        if artist_song_div is None:
            break  # Exit the function if rank not found        
        artist_song = artist_song_div.text.strip()
        artist, song_title = artist_song.split(' - ', 1)  # Split into artist and song title
        other_metrics = [cell.text.strip() for cell in cells[3:]]  # Extract other metrics

        # Combine data into a single row for CSV
        row_data = [cells[0].text.strip(), 
                    cells[1].text.strip(),
                    artist.strip(),  # Use the extracted artist
                    song_title.strip(),  # Use the extracted song title
                    *other_metrics
                ]
        
        music_data.append(row_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(music_data, columns=column_names)
    return df




import requests
from bs4 import BeautifulSoup
import base64
import datetime
import eyed3
import os


# Function to download image
def download_image(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)


for page in range(1, 11):
    # URL of the radio show webpage
    url = f'https://bff.fm/shows/warm-focus/page:{page}'

    # Get the HTML content of the webpage
    response = requests.get(url)

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')


    # Find all show elements
    show_elems = soup.find_all('li', class_='BroadcastRow')

    for i, show_elem in enumerate(show_elems):
        try:
            print(f'Processing show {i+1}/{len(show_elems)}')
            # Each title is inside the show element in an h3 element with class 'BroadcastRow-title'
            show_title = show_elem.find('h3', class_='BroadcastRow-title').text.strip()
            # Extract the show title by removing the 'Warm Focus: ' prefix
            show_title = show_title.replace('Warm Focus: ', '')

            # Each air date is inside the show element in a time element with class 'BroadcastRow-date'
            air_date = show_elem.find('time', class_='BroadcastRow-date')['datetime']
            # Split the datetime string to remove time and timezone
            air_date = air_date.split('T')[0]
            # Parse the date string to the required format
            air_date = datetime.datetime.strptime(air_date, '%Y-%m-%d').strftime('%Y-%m-%d')


            # Each album art URL is inside the show element in an img element with class 'BroadcastRow-image'
            album_art_url = show_elem.find('img', class_='BroadcastRow-image')['src']
            # Remove GET parameters
            album_art_url = album_art_url.split('?')[0]


            # Each MP3 URL is inside the show element in a button element with class 'PlaybackInvoker'.
            # The button element has an attribute called 'data-src'. This is a base64 encoded string of the URL for the MP3.
            mp3_url_base64 = show_elem.find('button', class_='PlaybackInvoker')['data-src']
            mp3_url = base64.b64decode(mp3_url_base64).decode()

            # Construct filename for the MP3 file
            mp3_filename = f'Warm Focus - {air_date} - {show_title}.mp3'

            # Download mp3 file'
            mp3_data = requests.get(mp3_url).content
            with open(f'mp3/{mp3_filename}', 'wb') as mp3_file:
                mp3_file.write(mp3_data)

            # Extract the extension of the album art image file (excluding parameters)
            base_url = album_art_url.split('?')[0]
            extension = base_url.split('.')[-1]

            # construct filename for album art
            art_filename_base = mp3_filename.split('.')[0]
            art_filename = f'{art_filename_base}.{extension}'

            # Download the album art image
            download_image(album_art_url, f'art/{art_filename}')

            # Load the mp3 file using eyed3
            mp3_file = eyed3.load(f'mp3/{mp3_filename}')

            # Initialize a new ID3 tag if none exists
            if mp3_file.tag is None:
                mp3_file.initTag()


            # Set the show title as the title of the mp3
            mp3_file.tag.title = show_title

            # Add album art to MP3
            with open(f'art/{art_filename}', 'rb') as img_file:
                mp3_file.tag.images.set(3, img_file.read(), 'image/jpeg')

            # Save the tag
            mp3_file.tag.save()

        except Exception as e:
            print(f'Error processing show {i+1}/{len(show_elems)}. MP3 file: mp3/{mp3_filename}')
            print(f'Detail: {e}')

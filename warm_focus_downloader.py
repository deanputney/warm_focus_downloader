
import requests
import json
import eyed3
import os

# Function to download image
def download_image(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Set working directory and MP3 filename
mp3_filename = '5310.mp3'
os.chdir('/Users/deanputney/projects/warm-focus')

# Load MP3 metadata
with open('metadata.json') as f:
  metadata = json.load(f)

# Get the show title
show_title = metadata['title']

# Get the album art URL
album_art_url = metadata['image']

# Download mp3 file
mp3_file_url = metadata['audio']
mp3_data = requests.get(mp3_file_url).content
with open(f'mp3/{mp3_filename}', 'wb') as mp3_file:
    mp3_file.write(mp3_data)

# Extract the extension of the album art image file (excluding parameters)
base_url = album_art_url.split('?')[0]
extension = base_url.split('.')[-1]
art_filename = f'{mp3_filename}.{extension}'

# Download the album art image
download_image(album_art_url, f'art/{art_filename}')

# Load the mp3 file using eyed3
mp3_file = eyed3.load(f'mp3/{mp3_filename}')

# Initialize a new ID3 tag if none exists
if mp3_file.tag is None:
    mp3_file.initTag()

# Extract the show title by removing the 'Warm Focus: ' prefix
show_title = show_title.replace('Warm Focus: ', '')

# Set the show title as the title of the mp3
mp3_file.tag.title = show_title

# Add album art to MP3
with open(f'art/{art_filename}', 'rb') as img_file:
    mp3_file.tag.images.set(3, img_file.read(), 'image/jpeg')

# Save the tag
mp3_file.tag.save()

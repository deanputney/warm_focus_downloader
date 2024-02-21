# Warm Focus radio show download script

This script collects and downloads the radio shows for the Warm Focus show.

AI Instructions:
1. Write and test code to complete the task described below.
2. When you have a working script, save it to the file "warm_focus_downloader.py"

Here is what the script should do:
1. Download MP3 files from the radio show web pages.
2. Save these MP3 files to a directory called "mp3".
3. Name the files in this format: "Warm Focus - {air_date} - {show_title}.mp3"
    Replace the data in brackets with the correct data found on the web.
4. Download the album art for each radio show.
5. Apply this album art to each MP3 in the correct metadata for the MP3.
6. Apply all other relevant metadata to the MP3.

Here is what we know so far about how to get this information:
1. The radio show webpage is: https://bff.fm/shows/warm-focus
2. All information is accessible via the HTML source.
3. Each show is in an li element with class "BroadcastRow"
    1. Each title is inside the show element in an h3 element with class "BroadcastRow-title"
    2. Each air date is inside the show element in a time element with class "BroadcastRow-date"
    2. Each album art URL is inside the show element in an img element with class "BroadcastRow-image"
        1. These URLs have GET parameters which define a cropped version of the file. Removing them should give you the full sized file.
    3. Each MP3 URL is inside the show element in a button element with class "PlaybackInvoker".
        1. The button element has an attribute called "data-src". This is a base64 encoded string of the URL for the MP3.

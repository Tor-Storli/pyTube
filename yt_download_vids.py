"""
This code will enable you to download individual videos 
or all the videos in playlist from YouTube.

Input: 
1) a comma seperated file with 1) link, and 2) Playlist (Y(es) or N(o))

i.e.
link, Playlist
https://www.youtube.com/watch?v=xOP_Mbd-nA0&list=PLJ03nQD7QmbvS0XX9NS3pzQi-ARbifsL9,Y
https://www.youtube.com/watch?v=n91fxMzkfFc&list=PLJ03nQD7Qmbu_f73DqayWfvsUCPwYTtSC,Y
https://www.youtube.com/watch?v=WH3is_Bm3GQ,N

Output:
1) downloaded videos from YouTube
2) A logfile with video download information

NOTE: the pytube library sometimes have issues downloading higher resoulution versions of a video. That is why
      I used a 720p resolution for the this demo code for my videos. 
      You need to experiment a little:: i.e. if you know that the videos are available in better quality, 
      i.e. 1080p or better try to set the filter(res="1080p") etc...

        youtube.streams.filter(res="1080p").first().download( ...etc)
"""

# Import Python Libraries
import logging
import os
import datetime
import csv
from pytube import YouTube, Playlist

# Get current directory
currentdir = os.getcwd()
print(currentdir)

# path to input csv file
ytfile = os.path.join(currentdir, "data", "ytfile.csv")

# Open youtube link/Playlist file
with open(ytfile, 'r', encoding="utf8") as f:
    # process each line into a tuple
    data = [tuple(line) for line in csv.reader(f,  delimiter=",")]

# Remove headers
data = data[1:]

# # Ininialize Python Logging
logging.basicConfig(level=logging.INFO,
                    filename="yt_download_log.txt", filemode="w")

# Set up youtube downloads video paths
filepath = './videos'

# Create divider strings
repdblStr = "=" * 125
repStr = "-" * 125

# Create two empty lists - one for single
# videos and one for playlist videos
videos = []
playlists = []

for line in data:
  # iterate in each tuple element and load the video url's into lists
    if line[1].strip() == 'N':
        videos.append(line[0])
    else:
        playlists.append(line[0])

# Download all individual videos
for vid in videos:
    youtube = YouTube(vid)
    print(youtube.title)

    youtube.streams.filter(res="720p").first().download(
        filepath, skip_existing=True)

    dtconverted = str(datetime.timedelta(seconds=youtube.length))

    # Log video attribute information
    logging.info("Title: {a}, Author: {b}, Length(HH.MI:SS): {c}".format(
        a=youtube.title, b=youtube.author,  c=dtconverted, d=youtube.publish_date))
    logging.info(repdblStr + "\n")


# Download all videos in a playlist based on one of the playlist video's url
for playlist in playlists:
    ytplaylist = Playlist(playlist)

    logging.info("Playlist Title: {a}".format(a=ytplaylist.title))
    logging.info(repdblStr + "\n\n")

    for video in ytplaylist.videos:
        print(video.title)
        # video.streams.get_highest_resolution()
        video.streams.filter(res="720p").first().download(
            filepath, skip_existing=True)

        # Convert video length (in seconds) into HH:MI:SS format
        dtconverted = str(datetime.timedelta(seconds=video.length))

        # Log video attribute information
        logging.info("Title: {a}, Author: {b}, Length(HH.MI:SS): {c}\n".format(
            a=video.title, b=video.author, c=dtconverted))

        logging.info("Description: {a}\n".format(a=video.description))

        logging.info(repStr + "\n")


print("Done! See log file for details here: " + currentdir)

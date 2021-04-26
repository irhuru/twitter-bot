# -*- coding: utf-8 -*-
"""
# Import libraries
"""

!pip install beautifulsoup4
!pip install tweepy
import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import tweepy
import time

"""
# Define main functions
"""

url = "https://spotifycharts.com/regional/global"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
webpage = requests.get(url, headers=headers)
soup = BeautifulSoup(webpage.text, "html.parser")
songs_list = soup.find("table", {"class":"chart-table"})

# Get song info

def get_song(songs_list):
  table_rows = songs_list.findChildren('tr')[1]
  track_data = table_rows.findChildren('td')[3]
  return track_data

# Get song title and artist

def song_info(track_data):
  title_data = track_data.findChildren('strong')[0]
  artist_data = track_data.findChildren('span')[0]
  return (title_data, artist_data)

# Clean HTML text

def clean_text(html_text):
  clean_re = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  clean_text = re.sub(clean_re, '', html_text)
  return clean_text

# Get date

def get_date():
  today = date.today()
  today = str(today)
  today_date = today[5:10]
  return today_date

# Write tweet

def write_tweet(song_info, today_date):
  title_data = song_info[0]
  artist_data = song_info[1]
  song_title = str(clean_text(title_data.text))
  song_artist = str(clean_text(artist_data.text))
  tweet = "#NowPlaying |" + today_date + "| " + song_title + " " + song_artist
  return tweet

tweet = write_tweet(song_info(get_song(songs_list)), get_date())

"""
# Link code to Twitter account and tweet
"""

CONSUMER_KEY = 'Your key goes here'
CONSUMER_SECRET = 'Your key goes here'
ACCESS_KEY = 'Your key goes here'
ACCESS_SECRET = 'Your key goes here'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

while True:
    this_tweet = tweet
    if len(this_tweet) <= 140:
        api.update_status(status=this_tweet)
        time.sleep(86400)

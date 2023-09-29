import os
import json
import pickle
import requests
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request
from youtube_test import *

yt, key = perform_authentication()
dict_of_youtubers_usernames = {'Hen Mazzig':'UCEkLqAhHhZI3NKmDAFbljpA', 'Rudy Rochman':'UCOcfVau723M1bHKJ0GdCbgQ', 'Noa Tishby':'UC1XUDNlTtcmpFgdF6hatRjQ', 'Hallel Silverman':'UCvIJvUax60-XsYy1_Spuikw', 'Ysabella Hazan':'UC-tIjpmGKnJXRJqaFYDvkjQ'}
queries = ['jew', 'jews', 'antisemitism', 'antizionism', 'zionazis', 'zionism', 'Israel']

def get_channel_details(channel_id):

    details_to_fetch = ['statistics', 'topicDetails', 'snippet', 'contentDetails', 'status', 'brandingSettings']

    for detail in details_to_fetch:
        request = yt.channels().list(part=detail, id=channel_id)
        response = request.execute()
        pretty_json = json.dumps(response['items'][0][detail], indent=4)
        print(pretty_json)

def search_by_keyword(key=key):
    video_ids = []
    for query in queries:
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part' : 'snippet',
            'q' : str(query),
            'key' : str(key)
        }
        response = requests.get(url, params=params)
        for video in json.loads(response.text)['items']:
            print("Video ID ", video['id']['videoId'], "\n", "Title", video['snippet']['title'], "\n", "Description", video['snippet']['description'], "\n\n")
            video_ids.append(str(video['id']['videoId']))
    return video_ids

def get_video_captions():
    videos = search_by_keyword()
    full_caption = ''
    print(videos)
    for id in videos:
        print("********************************************************************")
        print("\n\n\n\n")
        try:
            txt = YouTubeTranscriptApi.get_transcript(id)
            for line in txt:
                full_caption = full_caption + line['text'] + ' '
            print(full_caption)
            print("********************************************************************")
            print("\n\n\n\n")
        except:
            continue

def get_video_comments(key=key):
    videos = search_by_keyword()
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    for video_id in videos:
        params = {
            'key': str(key),
            'textFormat': 'plainText',
            'part' : 'snippet',
            'videoId' : str(video_id),
            'maxResults' : '20'
        }
        response = requests.get(url, params=params)
        for comment in json.loads(response.text)['items']:
            print(json.dumps(comment['snippet']['topLevelComment']['snippet']['authorDisplayName'], indent=4),
                json.dumps(comment['snippet']['topLevelComment']['snippet']['textDisplay'], indent=4))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n\n")

#for name, channel_id in dict_of_youtubers_usernames.items():
    #get_channel_details(channel_id)

    #print('\n')
    #print("********************************************************************")
    #print('\n')

search_by_keyword()
#get_video_captions()
#get_video_comments()
print("***")
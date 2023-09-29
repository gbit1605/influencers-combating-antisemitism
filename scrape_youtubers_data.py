import os
import json
import pickle
import requests
import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request
from youtube_test import *

yt, key = perform_authentication()
dict_of_youtubers_usernames = {'Hen Mazzig':'UCEkLqAhHhZI3NKmDAFbljpA', 'Rudy Rochman':'UCOcfVau723M1bHKJ0GdCbgQ', 'Noa Tishby':'UC1XUDNlTtcmpFgdF6hatRjQ', 'Hallel Silverman':'UCvIJvUax60-XsYy1_Spuikw', 'Ysabella Hazan':'UC-tIjpmGKnJXRJqaFYDvkjQ'}
queries = ['jew', 'jews', 'antisemitism', 'antizionism', 'zionazis', 'zionism', 'Israel']

def get_channel_details():

    details_to_fetch = ['statistics', 'topicDetails', 'snippet', 'contentDetails', 'status', 'brandingSettings']
    channel_details_data = {'Name':[], 'Description':[], 'Username':[], 'Channel setup date':[], 'View count':[], 'Video count':[], 'Subscriber count': [], 'Topic categories':[], 'Playlist details':[]}

    for name, channel_id in dict_of_youtubers_usernames.items():
        for detail in details_to_fetch:
            request = yt.channels().list(part=detail, id=channel_id)
            response = request.execute()
            if detail == 'statistics':
                channel_details_data['View count'].append(response['items'][0][detail]['viewCount'])
                channel_details_data['Subscriber count'].append(response['items'][0][detail]['subscriberCount'])
                channel_details_data['Video count'].append(response['items'][0][detail]['videoCount'])
            if detail == 'topicDetails':
                channel_details_data['Topic categories'].append(response['items'][0][detail]['topicCategories'])
            if detail == 'snippet':
                channel_details_data['Name'].append(response['items'][0][detail]['title'])
                channel_details_data['Description'].append(response['items'][0][detail]['description'])
                channel_details_data['Username'].append(response['items'][0][detail]['customUrl'])
                channel_details_data['Channel setup date'].append(response['items'][0][detail]['publishedAt'])  
            if detail == 'contentDetails':
                channel_details_data['Playlist details'].append(response['items'][0][detail]['relatedPlaylists'])
            #if detail == 'brandingSettings':
                #channel_details_data['Banner URL'].append(response['items'][0][detail]['image']['bannerExternalUrl'])
    
    df = pd.DataFrame(channel_details_data)
    excel_file = 'channel_details.xlsx'
    sheet_name = 'Sheet1'
    df.to_excel(excel_file, sheet_name=sheet_name, index=False)
    #print(channel_details_data)
    #for key, value in channel_details_data.items():
        #print(len(key), len(value), '\n')

        

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
#    get_channel_details(channel_id)

#    print('\n')
#    print("********************************************************************")
#    print('\n')

#search_by_keyword()
#get_video_captions()
#get_video_comments()
#print("***")

get_channel_details()
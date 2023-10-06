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
dict_of_youtubers_usernames = {'Hen Mazzig':'UCEkLqAhHhZI3NKmDAFbljpA', 
                               'Rudy Rochman':'UCOcfVau723M1bHKJ0GdCbgQ', 
                               'Noa Tishby':'UC1XUDNlTtcmpFgdF6hatRjQ', 
                               'Hallel Silverman':'UCvIJvUax60-XsYy1_Spuikw', 
                               'Ysabella Hazan':'UC-tIjpmGKnJXRJqaFYDvkjQ'}

manually_searched_youtube_antisemitism_combat_influencers = {
    'Tovia Singer': ['ToviaSinger1', 'UCaw8quRcRzjmw0BI1vn-dnA'],
    'SnappyDragon': ['SnappyDragon', 'UCTIcttrGKvoyZuPc8Xb_lbg'],
    'Yad Vashem': ['YadVashem', 'UCMIWdcUSEHSIGgTEgT5fU4g'],
    'Hananya Naftali': ['HananyaNaftali', 'UCIu679sa2q5Lw9CB95_-hdw'],
    'American Jewish Committee': ['AJCGlobal', 'UClLJWa0q-sSZQ_Jt9EEWWUg'],
    'AishJewish': ['Aishdotcom', 'UC8XGOrE1U_HYdYFonEuyCfw']
}
#queries = ['jew', 'jews', 'antisemitism', 'antizionism', 'zionazis', 'zionism', 'Israel']
queries  = ['Holocaust', 'white supremacy', 'jew', 'hatred', 'xenophobia', 'neo-nazi']
video_details = {'Video ID':[], 'Video Title':[], 'Video Description':[], 'Video caption':[], 'Video comments':[], 'Channel ID':[], 'Channel Title':[], 'Publish time':[]}

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

def search_by_keyword(key=key):
    video_ids, video_titles, video_description, channel_ids, channel_title, publish_time  = [], [], [], [], [], []
    for query in queries:
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part' : 'snippet',
            'q' : str(query),
            'key' : str(key), 
            'maxResults' : '50'
        }
        response = requests.get(url, params=params)
        print(response)
        try:
            for video in json.loads(response.text)['items']:
                #try:
                    #if str(video['id']['videoId']) not in video_details['Video ID']:
                video_ids.append(str(video['id']['videoId']))
                video_titles.append(str(video['snippet']['title']))
                video_description.append(str(video['snippet']['description']))
                channel_ids.append(str(video['snippet']['channelId']))
                channel_title.append(str(video['snippet']['channelTitle']))
                publish_time.append(str(video['snippet']['publishTime']))
                #except:
                    #continue
        except:
            continue
    return video_ids, video_titles, video_description, channel_ids, channel_title, publish_time

def get_video_captions(vid):
    full_caption = ''
    try:
        txt = YouTubeTranscriptApi.get_transcript(vid)
        for line in txt:
            full_caption = full_caption + line['text'] + ' '
        return full_caption         
    except:
        pass

def get_video_comments(k, vid):
    #videos = search_by_keyword()
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    #for video_id in videos:
    params = {
        'key': str(k),
        'textFormat': 'plainText',
        'part' : 'snippet',
        'videoId' : str(vid),
        'maxResults' : '20'
    }
    response = requests.get(url, params=params)
    vid_comment = {}
    for comment in json.loads(response.text)['items']:
        if str(comment['snippet']['topLevelComment']['snippet']['authorDisplayName']) not in vid_comment:
            vid_comment[str(comment['snippet']['topLevelComment']['snippet']['authorDisplayName'])] = comment['snippet']['topLevelComment']['snippet']['textDisplay']
    return vid_comment


returned_video_ids, returned_video_titles, returned_video_descriptions, returned_channel_ids, returned_channel_titles, returned_publish_times = search_by_keyword(key)
for v in range(len(returned_video_ids)):
    try:
        caption = get_video_captions(returned_video_ids[v])
        video_details['Video caption'].append(caption)
    except:
        video_details['Video caption'].append("No caption")
    try:
        comments = get_video_comments(key, returned_video_ids[v])
        video_details['Video comments'].append(comments)
    except:
        video_details['Video comments'].append("No comments")

video_details['Video ID'].extend(returned_video_ids)
video_details['Video Title'].extend(returned_video_titles)
video_details['Video Description'].extend(returned_video_descriptions)
video_details['Channel ID'].extend(returned_channel_ids)
video_details['Channel Title'].extend(returned_channel_titles)
video_details['Publish time'].extend(returned_publish_times)

print(video_details)


video_df = pd.DataFrame(video_details)
video_excel_file = 'video_details_4.xlsx'
sheet_name = 'Sheet1'
video_df.to_excel(video_excel_file, sheet_name=sheet_name, index=False)


def get_subscriber_list(key=key):
    url = 'https://youtube.googleapis.com/youtube/v3/subscriptions'

    for name, value in manually_searched_youtube_antisemitism_combat_influencers.items():
        params = {
            'part' : 'snippet',
            'channelId' : str(value[1]),
            'key' : str(key),
            'alt' : 'json'
        }
        response = requests.get(url, params=params)
        print(response.text)
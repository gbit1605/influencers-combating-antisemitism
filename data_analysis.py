import json
import requests
import pandas as pd
from youtube_test import *

yt, key = perform_authentication()
global_adjacency_list = {}

def get_subscriber_list(c_id, key=key):
    adjacent_list_for_one_video = []
    url = 'https://youtube.googleapis.com/youtube/v3/subscriptions'
    params = {
        'part' : 'snippet',
        'channelId' : str(c_id),
        'key' : str(key),
        'alt' : 'json',
        'maxResults' : 20
    }
    response = requests.get(url, params=params)
    result = json.loads(response.text)
    #print(result)
    if "error" not in result.keys():
        for i in result['items']:
            adjacent_list_for_one_video.append(i['snippet']['resourceId']['channelId'])
    return adjacent_list_for_one_video

df = pd.read_excel('video_details.xlsx')
print(df.head())
channel_ids = list(df['Channel ID'])

#comment_channel_ids = []



"""
video_comments = list(df['Video comments'])
new_video_comments = []
for i in range(len(video_comments)):
    if video_comments[i] == "No comments":
        continue
    v = eval(video_comments[i])
    new_video_comments.append(v)
#print(new_video_comments[0]) 
# 
#new_video_comments is a list od dictionaries where one dictinary is all of the comments for one video
"""

channel_ids = list(set(channel_ids))

#channel_ids_test = channel_ids[:5]

for i in channel_ids:
    returned_adjacent_list = get_subscriber_list(i)
    if len(returned_adjacent_list) > 0:
        global_adjacency_list[i] = returned_adjacent_list
print(global_adjacency_list)
print(len(global_adjacency_list))
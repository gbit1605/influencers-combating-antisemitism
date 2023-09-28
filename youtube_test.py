import os
import json
import pickle
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request


def perform_authentication():
    api_key = 'AIzaSyD4tYbAxtQXwc3TbcrZokbSU_M_NBlM_FI'
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube, api_key

"""
#Channel details
get_channel_details_request = youtube.channels().list(part='statistics')
                                                      #forUsername='', #id='')

#search by keywords
search_by_keyword_request = youtube.search().list(part='snippet', q='jews', maxResults=50)

#Get video captions
txt = YouTubeTranscriptApi.get_transcript('6foH3Zc82ZQ')
#for i in txt:
    #print(i)

video_id = '6foH3Zc82ZQ'
max_results = 50
comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults={max_results}'

#gives playlist upload id
playlist_upload_request = youtube.channels().list(part='contentDetails', id='UCCezIgC97PvUuR4_gbFUs5g')

playlist_info_request = youtube.playlistItems().list(part='status', playlistId='UUCezIgC97PvUuR4_gbFUs5g')

#Fetches comments
comment_threads_request = youtube.commentThreads().list(part='snippet', videoId='7INMI73qzjI', maxResults=100)

#Fetches list of channels that this person is subscribed to 
subscription_list_request = youtube.subscriptions().list(part='subscriberSnippet', channelId='UClKtjI8iP1Q9EvsiqNbgYoQ', maxResults=100)

response = subscription_list_request.execute()
pretty_json = json.dumps(response, indent=4)
#print(pretty_json)
"""
credentials = None

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)


# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'
            ]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

"""
This is for doing one time authentication
flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', scopes=['https://www.googleapis.com/auth/youtube.readonly'])

flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
credentials = flow.credentials
print(credentials.to_json())

"""

"""
{"token": "ya29.a0AfB_byD-FIZ7fojW75ekh0vv8LanEUFRbvUkoAZWFZMpRBUjqFL7Jt4XkkIO7uNm5Na0tWdybP3aiNmgLenuhY14ooiyN-poqx8UcCOmbkExWlmUSxJSwXo1_g2WzWqMJp6ffhALVAoDB994oUPDaaJZFnZ_ZQAz2otkaCgYKARESARESFQGOcNnCPBK39gz9e90YBeXuf8a5iQ0171", 
 "refresh_token": "1//01WHpBGjGqTL-CgYIARAAGAESNwF-L9IrGXqdjF7snPqtMdzPe3tqd0o2EXpzd4Dhb-enS4TnuQcuaf2QsY8AfKb1fNeVxoPKdus", 
 "token_uri": "https://oauth2.googleapis.com/token", 
 "client_id": "593919196288-umemlsfoij4a9tfenb7a6q96o8kbm2u2.apps.googleusercontent.com", 
 "client_secret": "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", 
 "scopes": ["https://www.googleapis.com/auth/youtube.readonly"], 
 "expiry": "2023-09-16T22:56:07.554547Z"}
"""



"""
youtube = build('youtube', 'v3', credentials=credentials)

#playlist_info_request_using_oauth = youtube.playlistItems().list(part='status', playlistId='UUCezIgC97PvUuR4_gbFUs5g', maxResults=50)

video_abuse_report_reason_request_using_oauth = youtube.videoAbuseReportReasons().list(part='snippet')

response = video_abuse_report_reason_request_using_oauth.execute()
pretty_json_oauth = json.dumps(response, indent=4)
print(pretty_json_oauth)
"""
import googleapiclient.discovery
import googleapiclient.errors
import youtube_video

YOUTUBE_API_SERVICE_NAME = u'youtube'
YOUTUBE_API_VERSION = u'v3'
SNIPPET = u'snippet'
ID = u'id'
TITLE = u'title'
ITEMS = u'items'
THUMBNAILS = u'thumbnails'
NEXT_PAGE_TOKEN = u'nextPageToken'
VIDEO_ID = u'videoId'
RESOURCE_ID = u'resourceId'
ITEM_COUNT = u'itemCount'
CONTENT_DETAILS = u'contentDetails'
PUBLISHED_AT = u'publishedAt'
CHANNEL_TITLE = u'channelTitle'
CHANNEL_ID = u'channelId'
PLAYLIST_ID = u'playlistId'


def get_all_playlist_ids_by_channel_id(channel_id, api_key):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    playlist_data = []
    next_page_token = None
    while True:
        playlist_results = youtube.playlists().list(part=SNIPPET,
                                                    channelId=channel_id,
                                                    maxResults=50,
                                                    pageToken=next_page_token
                                                    ).execute()
        playlist_data += playlist_results[ITEMS]
        next_page_token = playlist_results.get(NEXT_PAGE_TOKEN)
        if next_page_token is None:
            break

    playlist_ids = []
    for playlist_id in playlist_data:
        playlist_ids.append(playlist_id[ID])
    return playlist_ids


def get_all_video_ids_in_a_playlist(playlist_id, api_key):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = api_key)
    videos = []
    next_page_token = None
    while True:
        playlist_results = youtube.playlistItems().list(playlistId=playlist_id,
                                                        part=SNIPPET,
                                                        maxResults=50,
                                                        pageToken=next_page_token).execute()
        videos += playlist_results[ITEMS]
        next_page_token = playlist_results.get(NEXT_PAGE_TOKEN)
        if next_page_token is None:
            break
    video_ids = []
    for video in videos:
        video_ids.append(video[SNIPPET][RESOURCE_ID][VIDEO_ID])
    return video_ids


def get_playlist_info(playlist_id, api_key):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    playlist_info = youtube.playlists().list(part=SNIPPET+','+CONTENT_DETAILS,
                                             id=playlist_id).execute()
    playlist_data = populate_playlist_metadata(playlist_info, playlist_id)

    return playlist_data


def populate_playlist_metadata(playlist_info, playlist_id):
    data = {}

    data[PLAYLIST_ID] = playlist_id
    data[CHANNEL_TITLE] = playlist_info[ITEMS][0][SNIPPET][CHANNEL_TITLE]
    data[CHANNEL_ID] = playlist_info[ITEMS][0][SNIPPET][CHANNEL_ID]
    data[TITLE] = playlist_info[ITEMS][0][SNIPPET][TITLE]
    data[PUBLISHED_AT] = playlist_info[ITEMS][0][SNIPPET][PUBLISHED_AT]
    data[ITEM_COUNT] = int(playlist_info[ITEMS][0][CONTENT_DETAILS][ITEM_COUNT])
    data[THUMBNAILS] = playlist_info[ITEMS][0][SNIPPET][THUMBNAILS]

    return data

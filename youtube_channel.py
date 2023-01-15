import googleapiclient.discovery
import googleapiclient.errors

YOUTUBE_API_SERVICE_NAME = u'youtube'
YOUTUBE_API_VERSION = u'v3'
SNIPPET = u'snippet'
CONTENT_DETAILS = u'contentDetails'
STATISTICS = u'statistics'
STATUS = u'status'
ID = u'id'
TITLE = u'title'
ITEMS = u'items'
CUSTOM_URL = u'customUrl'
PUBLISHED_AT = u'publishedAt'
VIDEO_COUNT = u'videoCount'
SUBSCRIBER_COUNT = u'subscriberCount'
VIEW_COUNT = u'viewCount'
DESCRIPTION = u'description'
THUMBNAILS = u'thumbnails'
RELATED_PLAYLISTS = u'relatedPlaylists'
UPLOADS = u'uploads'
NEXT_PAGE_TOKEN = u'nextPageToken'
VIDEO_ID = u'videoId'
RESOURCE_ID = u'resourceId'


def get_channel_info(channel_id, api_key):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                                              YOUTUBE_API_VERSION,
                                              developerKey=api_key)

    request = youtube.channels().list(
        part=SNIPPET + ',' + CONTENT_DETAILS + ',' + STATISTICS
        + ',' + STATUS, id = channel_id
    )

    response = request.execute()

    channel_data = populate_channel_metadata(response)

    return channel_data


def populate_channel_metadata(response):

    data = {}

    data[TITLE] = response[ITEMS][0][SNIPPET][TITLE]
    data[ID] = response[ITEMS][0][ID]
    data[CUSTOM_URL] = response[ITEMS][0][SNIPPET][CUSTOM_URL]
    data[PUBLISHED_AT] = response[ITEMS][0][SNIPPET][PUBLISHED_AT]
    data[VIDEO_COUNT] = int(response[ITEMS][0][STATISTICS][VIDEO_COUNT])
    data[SUBSCRIBER_COUNT] = int(response[ITEMS][0][STATISTICS][SUBSCRIBER_COUNT])
    data[VIEW_COUNT] = int(response[ITEMS][0][STATISTICS][VIEW_COUNT])
    data[DESCRIPTION] = response[ITEMS][0][SNIPPET][DESCRIPTION]
    data[THUMBNAILS] = response[ITEMS][0][SNIPPET][THUMBNAILS]

    return data


def get_all_videos_ids_by_channel_id(channel_id, api_key):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                                              YOUTUBE_API_VERSION,
                                              developerKey=api_key)

    channel_results = youtube.channels().list(
        id=channel_id, part=CONTENT_DETAILS).execute()

    playlist_id = channel_results[ITEMS][0][CONTENT_DETAILS][RELATED_PLAYLISTS][UPLOADS]
    videos = []
    next_page_token = None
    while True:
        channel_results = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part=SNIPPET,
                                                       maxResults=50,
                                                       pageToken=next_page_token).execute()

        videos += channel_results[ITEMS]

        next_page_token = channel_results.get(NEXT_PAGE_TOKEN)

        if next_page_token is None:
            break

    video_ids = []
    for video in videos:
        video_ids.append(video[SNIPPET][RESOURCE_ID][VIDEO_ID])

    return video_ids









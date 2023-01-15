import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi

YOUTUBE_API_SERVICE_NAME = u'youtube'
YOUTUBE_API_VERSION = u'v3'
ISO_ENGLISH_CODE = u'en'
ITEMS = u'items'
SNIPPET = u'snippet'
CONTENT_DETAILS = u'contentDetails'
LICENSED_CONTENT = u'licensedContent'
STATISTICS = u'statistics'
STATUS = u'status'
CHANNEL_TITLE = u'channelTitle'
CHANNEL_ID = u'channelId'
TITLE = u'title'
ID = u'id'
VIDEO_URL = u'video_url'
PUBLISHED_AT = u'publishedAt'
DURATION = u'duration'
LICENSE = u'license'
VIEW_COUNT = u'viewCount'
LIKE_COUNT = u'likeCount'
CATEGORY_ID = u'categoryId'
DESCRIPTION = u'description'
THUMBNAILS = u'thumbnails'
TRANSCRIPTS = u'transcripts'
LOCALISED = u'localized'
DEFAULT_AUDIO_LANGUAGE = u'defaultAudioLanguage'


def get_transcripts(video_id):
    transcripts = []
    try:
        for transcript in YouTubeTranscriptApi.get_transcript(video_id,
                                                            languages=[ISO_ENGLISH_CODE]):
            transcripts.append(transcript)
    except Exception as e:
        transcripts.append("English Subtitles Unavailable")

    return transcripts


def check_license(video_metadata):
    if video_metadata is None:
        return False
    elif video_metadata[LICENSED_CONTENT] is False:
        return True
    elif video_metadata[LICENSE] == 'creativeCommons':
        return True
    elif "creative commons" in video_metadata[DESCRIPTION].lower():
        return True
    else:
        return False


def check_category(video_metadata):
    accepted_categories = [25, 26, 27, 28, 29, 35]

    if video_metadata is None:
        return False
    elif video_metadata[CATEGORY_ID] in accepted_categories:
        return True
    else:
        return False


def get_video_info(video_id, api_key):
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey = api_key
    )

    request = youtube.videos().list(part=SNIPPET + ',' + CONTENT_DETAILS +
                                    ',' + STATISTICS + ',' + STATUS, id=video_id)

    response = request.execute()

    try:
        video_data = populate_video_metadata(video_id, response)

    except Exception as e:
        print("ERROR: ", e)
        print("Suspected Private Video")
        video_data = None

    return video_data


def populate_video_metadata(video_id, response):

    data = {}

    data[CHANNEL_TITLE] = (response[ITEMS][0][SNIPPET][CHANNEL_TITLE])
    data[CHANNEL_ID] = (response[ITEMS][0][SNIPPET][CHANNEL_ID])
    data[TITLE] = (response[ITEMS][0][SNIPPET][TITLE])
    data[ID] = (response[ITEMS][0][ID])
    data[VIDEO_URL] = ("https://www.youtube.com/watch?v=" + video_id)
    data[PUBLISHED_AT] = (response[ITEMS][0][SNIPPET][PUBLISHED_AT])
    data[DURATION] = (response[ITEMS][0][CONTENT_DETAILS][DURATION])
    data[LICENSE] = (response[ITEMS][0][STATUS][LICENSE])
    data[VIEW_COUNT] = int(response[ITEMS][0][STATISTICS][VIEW_COUNT])
    data[LIKE_COUNT] = int(response[ITEMS][0][STATISTICS][LIKE_COUNT])
    data[CATEGORY_ID] = int(response[ITEMS][0][SNIPPET][CATEGORY_ID])
    data[DESCRIPTION] = (response[ITEMS][0][SNIPPET][DESCRIPTION])
    data[THUMBNAILS] = (response[ITEMS][0][SNIPPET][THUMBNAILS])
    data[TRANSCRIPTS] = get_transcripts(video_id)
    data[DEFAULT_AUDIO_LANGUAGE] = (response[ITEMS][0][SNIPPET][DEFAULT_AUDIO_LANGUAGE][:2])
    data[LICENSED_CONTENT] = (response[ITEMS][0][CONTENT_DETAILS][LICENSED_CONTENT])

    return data




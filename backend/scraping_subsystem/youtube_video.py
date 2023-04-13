
from scraping_subsystem.youtube_master import YoutubeMaster

import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeVideo(YoutubeMaster):
    def __init__(self):
        YoutubeMaster.__init__(self)

    def get_transcripts(self, video_id):
        transcripts = []
        try:
            for transcript in YouTubeTranscriptApi.get_transcript(video_id,
                                                                  languages=[self.iso_english_code]):
                transcripts.append(transcript)
        except Exception as e:
            transcripts.append("English Subtitles Unavailable")

        return transcripts

    def check_license(self, video_metadata):
        if video_metadata is None:
            return "No Video Metadata"
        elif video_metadata[self.licensed_content] is False:
            return "Possibly CC BY"
        elif video_metadata[self.license] == 'creativeCommons':
            return "CC BY"
        elif "creative commons" in video_metadata[self.description].lower():
            return "Possibly CC BY"
        else:
            return "Private Video"

    def check_category(self, video_metadata):
        accepted_categories = [25, 26, 27, 28, 29, 35]
        if video_metadata is None:
            return False
        elif video_metadata[self.category_id] in accepted_categories:
            return True
        else:
            return False

    def check_transcript(self, video_metadata):
        if video_metadata[self.transcripts]:
            return "Available"
        else:
            return "Not Available"

    def get_video_info(self, video_id, api_key):
        youtube = googleapiclient.discovery.build(
            self.youtube_api_service_name, self.youtube_api_version, developerKey=api_key
        )

        request = youtube.videos().list(part=self.snippet + ',' + self.content_details +
                                             ',' + self.statistics + ',' + self.status, id=video_id)

        response = request.execute()

        try:
            video_data = self.populate_video_metadata(video_id, response)
            if self.check_license(video_data) == "Private Video":
                video_data = None

        except Exception as e:
            print("ERROR: ", e)
            video_data = None

        return video_data

    def populate_video_metadata(self, video_id, response):
        data = {}

        data[self.channel_title] = (response[self.items][0][self.snippet][self.channel_title])
        data[self.channel_id] = (response[self.items][0][self.snippet][self.channel_id])
        data[self.title] = (response[self.items][0][self.snippet][self.title])
        data[self.id] = (response[self.items][0][self.id])
        data[self.video_url] = ("https://www.youtube.com/watch?v=" + video_id)
        data[self.published_at] = (response[self.items][0][self.snippet][self.published_at])
        data[self.duration] = (response[self.items][0][self.content_details][self.duration])
        data[self.license] = (response[self.items][0][self.status][self.license])
        data[self.view_count] = int(response[self.items][0][self.statistics][self.view_count])
        data[self.like_count] = int(response[self.items][0][self.statistics][self.like_count])
        data[self.category_id] = int(response[self.items][0][self.snippet][self.category_id])
        data[self.description] = (response[self.items][0][self.snippet][self.description])
        data[self.thumbnails] = (response[self.items][0][self.snippet][self.thumbnails])
        data[self.transcripts] = self.get_transcripts(video_id)
        data['deleted'] = False

        try:
            data[self.default_audio_language] = (response[self.items][0][self.snippet][self.default_audio_language][:2])
        except:
            data[self.default_audio_language] = 'not detected'
        data[self.licensed_content] = (response[self.items][0][self.content_details][self.licensed_content])

        return data


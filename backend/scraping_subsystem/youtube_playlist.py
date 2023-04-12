from scraping_subsystem.youtube_master import YoutubeMaster

import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubePlaylists(YoutubeMaster):
    def __init__(self):
        YoutubeMaster.__init__(self)

    def get_all_playlist_ids_by_channel_id(self, channel_id, api_key):
        youtube = googleapiclient.discovery.build(self.youtube_api_service_name, self.youtube_api_version, developerKey = self.api_key)
        playlist_data = []
        next_page_token = None
        while True:
            playlist_results = youtube.playlists().list(
                part=self.snippet,
                channelId=channel_id,
                pageToken=next_page_token
            ).execute()
            playlist_data += playlist_results[self.items]
            next_page_token = playlist_results.get(self.next_page_token)
            if next_page_token is None:
                break

        playlist_ids = []
        for playlist_id in playlist_data:
            playlist_ids.append(playlist_id[self.id])

        return playlist_ids

    def get_all_video_ids_in_a_playlist(self, playlist_id, api_key):
        youtube = googleapiclient.discovery.build(self.youtube_api_service_name, self.youtube_api_version, developerKey=self.api_key)
        videos = []
        next_page_token = None
        while True:
            playlist_results = youtube.playlistItems().list(
                playlistId=playlist_id,
                part=self.snippet,
                pageToken=next_page_token
            ).execute()
            videos += playlist_results[self.items]
            next_page_token = playlist_results.get(self.next_page_token)
            if next_page_token is None:
                break

        video_ids = []
        for video in videos:
            video_ids.append(video[self.snippet][self.resource_id][self.video_id])

        return video_ids

    def get_playlist_info(self, playlist_id, api_key):
        youtube = googleapiclient.discovery.build(self.youtube_api_service_name, self.youtube_api_version, developerKey=api_key)
        playlist_info = youtube.playlists().list(part=self.snippet+','+self.content_details,
                                                 id=playlist_id).execute()

        playlist_data = self.populate_playlist_metadata(playlist_info, playlist_id)

        return playlist_data

    def populate_playlist_metadata(self, playlist_info, playlist_id):
        data = {}

        data[self.playlist_id] = playlist_id
        data[self.channel_title] = playlist_info[self.items][0][self.snippet][self.channel_title]
        data[self.channel_id] = playlist_info[self.items][0][self.snippet][self.channel_id]
        data[self.title] = playlist_info[self.items][0][self.snippet][self.title]
        data[self.published_at] = playlist_info[self.items][0][self.snippet][self.published_at]
        data[self.item_count] = int(playlist_info[self.items][0][self.content_details][self.item_count])
        data[self.thumbnails] = playlist_info[self.items][0][self.snippet][self.thumbnails]
        data[self.description] = playlist_info[self.items][0][self.snippet][self.description]

        return data
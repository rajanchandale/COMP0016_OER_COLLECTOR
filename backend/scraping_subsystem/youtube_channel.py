from scraping_subsystem.youtube_master import YoutubeMaster

import googleapiclient.discovery
import googleapiclient.errors


class YoutubeChannel(YoutubeMaster):
    def __init__(self):
        YoutubeMaster.__init__(self)

    def get_channel_info(self, channel_id, api_key):
        youtube = googleapiclient.discovery.build(self.youtube_api_service_name,
                                                  self.youtube_api_version,
                                                  developerKey=api_key)
        request = youtube.channels().list(
            part=self.snippet + ',' + self.content_details + ',' + self.statistics
                 + ',' + self.status, id=channel_id
        )

        response = request.execute()

        channel_data = self.populate_channel_metadata(response)

        return channel_data

    def populate_channel_metadata(self, response):

        data = {}

        data[self.title] = response[self.items][0][self.snippet][self.title]
        data[self.id] = response[self.items][0][self.id]
        data[self.custom_url] = response[self.items][0][self.snippet][self.custom_url]
        data[self.published_at] = response[self.items][0][self.snippet][self.published_at]
        data[self.video_count] = int(response[self.items][0][self.statistics][self.video_count])
        data[self.subscriber_count] = int(response[self.items][0][self.statistics][self.subscriber_count])
        data[self.view_count] = int(response[self.items][0][self.statistics][self.view_count])
        data[self.description] = response[self.items][0][self.snippet][self.description]
        data[self.thumbnails] = response[self.items][0][self.snippet][self.thumbnails]

        return data

    def get_all_video_ids_by_channel_id(self, channel_id, api_key):
        youtube = googleapiclient.discovery.build(self.youtube_api_service_name,
                                                  self.youtube_api_version,
                                                  developerKey=api_key)

        channel_results = youtube.channels().list(
            id=channel_id, part=self.content_details).execute()

        playlist_id = channel_results[self.items][0][self.content_details][self.related_playlists][self.uploads]
        videos = []
        next_page_token = None
        while True:
            channel_results = youtube.playlistItems().list(playlistId=playlist_id,
                                                           part=self.snippet,
                                                           maxResults=50,
                                                           pageToken=next_page_token).execute()
            videos += channel_results[self.items]

            next_page_token = channel_results.get(self.next_page_token)

            if next_page_token is None:
                break

        video_ids = []

        for video in videos:
            video_ids.append(video[self.snippet][self.resource_id][self.video_id])

        return video_ids






from scraping_subsystem.youtube_master import YoutubeMaster

from scraping_subsystem.youtube_video import YouTubeVideo
from scraping_subsystem.youtube_channel import YoutubeChannel
from scraping_subsystem.youtube_playlist import YoutubePlaylists

from urllib.parse import urlparse, parse_qs
import psycopg2
import json


class Scraper(YoutubeMaster):
    def __init__(self):
        YoutubeMaster.__init__(self)
        self.youtube_video = YouTubeVideo()
        self.youtube_channel = YoutubeChannel()
        self.youtube_playlists = YoutubePlaylists()

    def get_video_id(self, url):
        if url.startswith(('youtu', 'www')):
            url = 'http://' + url
        query = urlparse(url)
        if 'youtube' in query.hostname:
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                return query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            return query.path[1:]
        else:
            raise ValueError

    def get_channel_id(self, url):
        video_id = self.get_video_id(url)
        video_details = self.youtube_video.get_video_info(video_id, self.api_key)

        return video_details[self.channel_id]

    def find_max(self, table, field, cursor):
        postgres_max_field_query = """SELECT MAX({}) FROM {}""".format(field, table)
        cursor.execute(postgres_max_field_query)
        max_result = cursor.fetchone()
        if max_result[0] is None:
            return 0
        else:
            return max_result[0]

    def find_title_match(self, cursor, table, title):
        postgres_select_query = """SELECT title FROM {} WHERE title = %s""".format(table)
        cursor.execute(postgres_select_query, (title,))
        title_match = cursor.fetchone()
        return title_match

    def get_oer_id(self, url):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()

            postgres_oer_id_query = f"""SELECT material_id FROM urls WHERE url = '{url}';"""

            cursor.execute(postgres_oer_id_query)

            return cursor.fetchone()[0]

        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")

    def get_url_by_oer_id(self, oer_id):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()

            postgres_url_query = f"""SELECT url from urls WHERE material_id = '{oer_id}';"""

            cursor.execute(postgres_url_query)

            return cursor.fetchone()[0]

        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")

    def get_all_existing_oer_urls(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()

            postgres_url_query = """SELECT url from urls WHERE provider_id = 73;"""
            cursor.execute(postgres_url_query)

            return cursor.fetchall()

        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")

    def ingest_material_video(self, video_metadata):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()

            title_match = self.find_title_match(cursor, 'oer_materials', video_metadata[self.title])

            max_oer_id = self.find_max('oer_materials', 'id', cursor)
            new_oer_id = int(max_oer_id) + 1

            postgres_provider_id_query = """SELECT id from providers WHERE name = 'YouTube' """
            cursor.execute(postgres_provider_id_query)
            provider_id = cursor.fetchone()[0]

            max_url_id = self.find_max('urls', 'id', cursor)
            new_url_id = int(max_url_id) + 1

            max_contents_id = self.find_max('material_contents', 'id', cursor)
            new_contents_id = int(max_contents_id) + 1

            transcript_dict = {'transcript': video_metadata[self.transcripts]}
            formatted_transcript = json.dumps(transcript_dict)

            if title_match is None and video_metadata['deleted'] is False:
                postgres_insert_query = """ INSERT INTO oer_materials (id, title, description, language, 
                creation_date, type, mimetype, license) 
                VALUES (%s ,%s , %s , %s , %s, %s, %s, %s)"""

                record_values = (str(new_oer_id), video_metadata[self.title], video_metadata[self.description],
                                 video_metadata[self.default_audio_language], video_metadata[self.published_at], 'mp4', 'video/mp4',
                                 'http://creativecommons.org/licenses/by-nc-nd/3.0/')

                cursor.execute(postgres_insert_query, record_values)

                postgres_urls_insert_query = """INSERT INTO urls (id, url, provider_id, material_id) 
                VALUES (%s, %s, %s, %s)"""

                record_values_urls = (str(new_url_id), str(video_metadata[self.video_url]), str(provider_id), str(new_oer_id))
                cursor.execute(postgres_urls_insert_query, record_values_urls)

                postgres_contents_insert_query = """INSERT INTO material_contents (language, type, extension, value, material_id, id)
                VALUES (%s, %s, %s, %s, %s, %s)"""

                record_values_contents = (video_metadata[self.default_audio_language], 'mp4', 'mp4', formatted_transcript,
                                          str(new_oer_id), str(new_contents_id))
                cursor.execute(postgres_contents_insert_query, record_values_contents)

                connection.commit()

            elif title_match is not None:
                print(title_match, " already exists")

        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")

    def ingest_material_playlist(self, video_metadata):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")

            cursor = connection.cursor()

            title_match = self.find_title_match(cursor, 'oer_materials', video_metadata[self.title])

            max_oer_id = self.find_max('oer_materials', 'id', cursor)
            new_oer_id = int(max_oer_id) + 1

            postgres_provider_id_query = """SELECT id from providers WHERE name = 'YouTube' """
            cursor.execute(postgres_provider_id_query)
            provider_id = cursor.fetchone()[0]

            max_url_id = self.find_max('urls', 'id', cursor)
            new_url_id = int(max_url_id) + 1

            if title_match is None:
                postgres_insert_query = """INSERT INTO oer_materials (id, title, description, language, 
                creation_date, type, mimetype, license) 
                VALUES (%s ,%s , %s , %s , %s, %s, %s, %s)"""

                record_values = (str(new_oer_id), video_metadata[self.title], video_metadata[self.description],
                                 video_metadata[self.default_audio_language], video_metadata[self.published_at], 'mp4', 'video/mp4',
                                 'http://creativecommons.org/licenses/by-nc-nd/3.0/')

                cursor.execute(postgres_insert_query, record_values)

                postgres_urls_insert_query = """INSERT INTO urls (id, url, provider_id, material_id) 
                            VALUES (%s, %s, %s, %s)"""

                record_values_urls = (str(new_url_id), str(video_metadata[self.video_url]), str(provider_id), str(new_oer_id))
                cursor.execute(postgres_urls_insert_query, record_values_urls)

                connection.commit()

            elif title_match is not None:
                print(title_match, "already exists")

        except (Exception, psycopg2.Error) as e:
            print("ERROR", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("connection closed")

    def ingest_series(self, playlist_metadata):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")

            cursor = connection.cursor()

            title_match = self.find_title_match(cursor, 'series', playlist_metadata[self.title])

            max_series_id = self.find_max('series', 'id', cursor)
            new_series_id = int(max_series_id) + 1

            if title_match is None:
                postgres_insert_query = """INSERT INTO series (id, title, description, type)
                VALUES (%s, %s, %s, %s)"""

                record_values = (str(new_series_id), playlist_metadata[self.title],
                                 playlist_metadata[self.description], 'mp4')
                cursor.execute(postgres_insert_query, record_values)

                connection.commit()

            else:
                print(title_match, " already exists")
        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("connection closed")

    def ingest_episode(self, video_metadata, episode_number):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="Incorrect-10",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()

            title_match = self.find_title_match(cursor, 'oer_materials', video_metadata[self.title])

            max_oer_id = self.find_max('oer_materials', 'id', cursor)
            new_oer_id = int(max_oer_id) + 1

            postgres_provider_id_query = """SELECT id from providers WHERE name = 'YouTube' """
            cursor.execute(postgres_provider_id_query)
            provider_id = cursor.fetchone()[0]

            max_url_id = self.find_max('urls', 'id', cursor)
            new_url_id = int(max_url_id) + 1

            max_series_id = self.find_max('series', 'id', cursor)

            max_contents_id = self.find_max('material_contents', 'id', cursor)
            new_contents_id = int(max_contents_id) + 1

            transcript_dict = {'transcript': video_metadata[self.transcripts]}
            formatted_transcript = json.dumps(transcript_dict)

            print("DELETED: ", video_metadata['deleted'])

            if title_match is None and video_metadata['deleted'] is False:
                postgres_insert_query = """ INSERT INTO oer_materials (id, title, description, language, 
                creation_date, type, mimetype, license) 
                VALUES (%s ,%s , %s , %s , %s, %s, %s, %s)"""

                record_values = (str(new_oer_id), video_metadata[self.title], video_metadata[self.description],
                                 video_metadata[self.default_audio_language], video_metadata[self.published_at], 'mp4',
                                 'video/mp4', 'http://creativecommons.org/licenses/by-nc-nd/3.0/')

                cursor.execute(postgres_insert_query, record_values)

                postgres_urls_insert_query = """INSERT INTO urls (id, url, provider_id, material_id) 
                VALUES (%s, %s, %s, %s)"""
                record_values_urls = (str(new_url_id), str(video_metadata[self.video_url]), str(provider_id),
                                      str(new_oer_id))
                cursor.execute(postgres_urls_insert_query, record_values_urls)

                postgres_episodes_insert_query = """INSERT INTO episodes (episode_number, material_id, series_id) 
                VALUES (%s, %s, %s)"""
                record_values_episodes = (str(episode_number), new_oer_id, max_series_id)
                cursor.execute(postgres_episodes_insert_query, record_values_episodes)

                postgres_contents_insert_query = """INSERT INTO material_contents (language, type, extension, value, material_id, id)
                VALUES (%s, %s, %s, %s, %s, %s)"""

                record_values_contents = (video_metadata[self.default_audio_language], 'mp4', 'mp4', formatted_transcript,
                                          str(new_oer_id), str(new_contents_id))
                cursor.execute(postgres_contents_insert_query, record_values_contents)

                connection.commit()

            else:
                print(title_match, " already exists")

        except (Exception, psycopg2.Error) as e:
            print("ERROR: ", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")

    def scrape_playlists(self, channel_id, visited_videos):
        playlist_ids = self.youtube_playlists.get_all_playlist_ids_by_channel_id(channel_id, self.api_key)
        materials = []
        playlist_count = 0
        for playlist_id in playlist_ids:
            video_ids = self.youtube_playlists.get_all_video_ids_in_a_playlist(playlist_id)
            if video_ids is not None:
                playlist_info = self.youtube_playlists.get_playlist_info(playlist_id, self.api_key)
                episode_number = 1
                for video_id in video_ids:
                    visited_videos.append(video_id)
                    video_details = self.youtube_video.get_video_info(video_id, self.api_key)

                    if self.youtube_video.check_license(video_details) and self.youtube_video.check_category(video_details) \
                            and video_details is not None:

                        episode_number += 1
                        final_video_details = {
                            "id": video_id,
                            "playlist_id": playlist_info[self.playlist_id],
                            "playlist_title": playlist_info[self.title],
                            "title": video_details[self.title],
                            "channel": video_details[self.channel_title],
                            "description": video_details[self.description],
                            "thumbnail": video_details[self.thumbnails][self.default][self.url],
                            "defaultAudioLanguage": video_details[self.default_audio_language],
                            "publishedAt": video_details[self.published_at],
                            "video_url": video_details[self.video_url],
                            "transcript_available": self.youtube_video.check_transcript(video_details),
                            "licence_available": self.youtube_video.check_license(video_details),
                            "transcripts": video_details[self.transcripts]
                        }

                        materials.append(final_video_details)
                        break
                break
            playlist_count += 1

        return materials

    def scrape_videos(self, channel_id, visited_videos):
        video_ids = self.youtube_channel.get_all_video_ids_by_channel_id(channel_id, self.api_key)
        video_titles = []
        materials = []
        video_count = 0
        for video_id in video_ids:
            video_details = self.youtube_video.get_video_info(video_id, self.api_key)
            if self.youtube_video.check_license(video_details) and self.youtube_video.check_category(video_details):
                if video_id not in visited_videos and video_id is not None:
                    video_titles.append([video_details[self.title], video_details[self.category_id],
                                         video_details[self.published_at]])

                    materials.append({
                        "id": video_id,
                        "title": video_details[self.title],
                        "description": video_details[self.description],
                        "channel": video_details[self.channel_title],
                        "thumbnail": video_details[self.thumbnails][self.default][self.url],
                        "defaultAudioLanguage": video_details[self.default_audio_language],
                        "publishedAt": video_details[self.published_at],
                        "video_url": video_details[self.video_url],
                        "transcript_availability": self.youtube_video.check_transcript(video_details),
                        "licence_available": self.youtube_video.check_license(video_details),
                        "transcripts": video_details[self.transcripts]
                    })

                    video_count += 1
                    break
            break
        return materials


def main(yt_url):
    scraper = Scraper()
    yt_url_info = scraper.youtube_video.get_video_info(scraper.get_video_id(yt_url), scraper.api_key)
    channel_id = scraper.get_channel_id(yt_url)
    channel_data = scraper.youtube_channel.get_channel_info(channel_id, scraper.api_key)
    visited_videos = []
    scraped_playlist_data = scraper.scrape_playlists(channel_id, visited_videos)
    #scraped_video_data = scraper.scrape_videos(channel_id, visited_videos)
    return scraped_playlist_data


if __name__ == "__main__":
    yt_url = input("Enter URL:\n")
    main(yt_url)






import json
import os

import youtube_playlists
import youtube_video
import youtube_channel
from urllib.parse import urlparse, parse_qs
import psycopg2

MAX_VIDEOS_PER_FILE = 50
API_KEY = "AIzaSyAjbf9cg4eT384Gv21LpsM87qIIgj3wpK8"
CHANNEL_ID = u'channelId'
TITLE = u'title'
DESCRIPTION = u'description'
PUBLISHED_AT = u'publishedAt'
PLAYLIST_ID = u'playlistId'
DEFAULT_AUDIO_LANGUAGE = u'defaultAudioLanguage'


def get_video_id(url):
    if url.startswith(('youtu','www')):
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


def get_channel_id(url):
    video_id = get_video_id(url)
    video_details = youtube_video.get_video_info(video_id, API_KEY)

    return video_details[CHANNEL_ID]


def ingest_material(video_metadata):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="Incorrect-10",
                                      host="localhost",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()

        postgres_select_query = """SELECT title FROM oer_materials WHERE title = %s"""
        cursor.execute(postgres_select_query, (video_metadata[TITLE], ))
        title_match = cursor.fetchone()

        if title_match is None:

            postgres_insert_query = """ INSERT INTO oer_materials (id, title, description, language, 
            creation_date, type, mimetype, license) 
            VALUES (%s, %s ,%s , %s , %s , %s, %s, %s)"""
            record_values = (9999995, video_metadata[TITLE], video_metadata[DESCRIPTION],
                             video_metadata[DEFAULT_AUDIO_LANGUAGE], video_metadata[PUBLISHED_AT], 'mp4', 'video/mp4',
                             'http://creativecommons.org/licenses/by-nc-nd/3.0/')
            cursor.execute(postgres_insert_query, record_values)

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


def main2(channel_id, output_dir):
    channel_info = youtube_channel.get_channel_info(channel_id,API_KEY)
    video_ids = youtube_channel.get_all_videos_ids_by_channel_id(channel_id, API_KEY)
    output_dir = os.path.join(output_dir, '')
    total_videos = len(video_ids)
    print(total_videos)
    count = 1
    video_count = 1
    video_titles = []
    while video_count <= 200:
        filepath = output_dir + channel_info[TITLE] + "_" + str(count) + '.jsonl'
        with open(filepath, 'w') as f:
            for id in range((count-1)*50, min(total_videos, 50*count)):
                video_details = youtube_video.get_video_info(video_ids[id], API_KEY)
                if youtube_video.check_license(video_details) and youtube_video.check_category(video_details):
                    f.write(json.dumps(video_details, ensure_ascii=True))
                    f.write('\n')
                    CATEGORY_ID = u'categoryId'
                    PUBLISHED_AT = u'publishedAt'
                    video_titles.append([video_details[TITLE], video_details[CATEGORY_ID], video_details[PUBLISHED_AT]])
                print(video_count)
                video_count += 1
            count += 1

    print("Found ", len(video_titles), " Matching Videos")
    for title in video_titles:
        print(title)


def main(channel_id, output_dir):
    print("scraping videos ...")
    visited_videos = []
    scrape_playlists(channel_id, visited_videos)
    scrape_videos(channel_id, visited_videos)


def scrape_playlists(channel_id, visited_videos):
    channel_info = youtube_channel.get_channel_info(channel_id, API_KEY)
    playlist_ids = youtube_playlists.get_all_playlist_ids_by_channel_id(channel_id, API_KEY)
    print("playlist_ids: ", playlist_ids)
    for playlist_id in playlist_ids:
        video_ids = youtube_playlists.get_all_video_ids_in_a_playlist(playlist_id, API_KEY)
        print("video_ids: ", video_ids)
        if video_ids is not None:
            total_videos = len(video_ids)
            playlist_info = youtube_playlists.get_playlist_info(playlist_id, API_KEY)

            for video_id in video_ids:
                visited_videos.append(video_id)
                video_details = youtube_video.get_video_info(video_id, API_KEY)
                final_video_details = {
                    "playlist_id": playlist_info[PLAYLIST_ID],
                    "playlist_title": playlist_info[TITLE],
                    "video_title": video_details[TITLE]
                }
                print(final_video_details)


def scrape_videos(channel_id, visited_videos):
    channel_info = youtube_channel.get_channel_info(channel_id,API_KEY)
    video_ids = youtube_channel.get_all_videos_ids_by_channel_id(channel_id, API_KEY)
    total_videos = len(video_ids)
    video_count = 1
    video_titles = []
    CATEGORY_ID = u'categoryId'
    PUBLISHED_AT = u'publishedAt'
    for video_id in video_ids:
        video_details = youtube_video.get_video_info(video_id, API_KEY)
        #if youtube_video.check_license(video_details) and youtube_video.check_category(video_details):
        if video_id not in visited_videos and video_id is not None:
            video_titles.append([video_details[TITLE], video_details[CATEGORY_ID], video_details[PUBLISHED_AT]])
            print(video_count)
            video_count += 1

    print("Found: ", len(video_titles), " Matching Videos")
    for title in video_titles:
        print(title)

    """
    Sub-category of creative commons licence
    Playlists
    Correct ingestion of material 
    Sort into playlists 
    Fix licensing issues
    Qs: playlists, id, ttp_id, authors, providers, language/language_detected
    """


if __name__ == '__main__':
    yt_url = input("Enter URL:\n")
    yt_url_info = youtube_video.get_video_info(get_video_id(yt_url), API_KEY)
    print("Provided Video: ", yt_url_info[TITLE])
    channel_id = get_channel_id(yt_url)
    channel_data = youtube_channel.get_channel_info(channel_id, API_KEY)
    print("Provided Channel: ", channel_data[TITLE])
    output_dir = os.getcwd()
    print("Fetching Videos ...")
    main(channel_id, output_dir)
    ingest_material(yt_url_info)



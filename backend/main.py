from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from scraping_subsystem.youtube_scraper import Scraper
from scraping_subsystem.youtube_video import YouTubeVideo
from scraping_subsystem.youtube_playlist import YoutubePlaylists

from analytics import timedata, browserdata, cookiedata, language, links, typedata

from licence import LicenceTool

app = FastAPI()

scraper = Scraper()
youtube_video = YouTubeVideo()
youtube_playlists = YoutubePlaylists()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/general_statistics/')
def general_statistics() -> dict:
    print("ANALYSING")

    user_browser_data = browserdata.browser_name_data()

    print("USER_BROWSER_DATA: ", user_browser_data)

    material_language_data = language.material_language_data()

    print("MATERIAL_LANGUAGE_DATA: ", material_language_data)

    user_language_data = language.user_language_data()

    print("USER_LANGUAGE_DATA: ", user_language_data)

    material_type_data = typedata.material_type_data()

    print("MATERIAL_TYPE_DATA: ", material_type_data)

    device_name_data = browserdata.device_name_data()

    print("DEVICE NAME DATA: ", device_name_data)

    video_type_data = typedata.vid_type_data()

    print("VIDEO TYPE DATA: ", video_type_data)

    language_comparison_data = language.compare_language_data()

    print("LANGUAGE COMPARISON DATA: ", language_comparison_data)

    general_data = {
        "user_browser": user_browser_data,
        "material_language_data": material_language_data,
        "user_language_data": user_language_data,
        "material_type_data": material_type_data,
        "device_name_data": device_name_data,
        "video_type_data": video_type_data,
        "language_comparison_data": language_comparison_data
    }

    print("DONE ANALYSING")

    return {"data": general_data}


@app.get('/activity_statistics/')
def activity_statistics() -> dict:

    print("ANALYSING ACTIVITY STATISTICS")

    users_week_data = timedata.users_week_data()

    print("USERS WEEK DATA DONE")

    users_month_data = timedata.users_month_data()

    print("USERS MONTH DATA DONE")

    cookie_events_data = cookiedata.eventcount()

    print("COOKIE EVENTS DATA DONE")

    month_comparison_data = timedata.compare_months_data()

    print("MONTH COMPARISON DATA DONE")

    links_between_materials = links.process()

    print("LINKS BETWEEN MATERIALS DONE")

    activity_data = {
        "cookie_events_data": cookie_events_data,
        "users_week_data": users_week_data,
        "users_month_data": users_month_data,
        "links_between_materials": links_between_materials,
        "month_comparison_data": month_comparison_data
    }

    print("ANALYSIS COMPLETE")

    return {"data": activity_data}


@app.post('/add_materials/')
async def add_materials(request: Request) -> dict:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        return "No Content-Type Provided"

    elif content_type == "application/json":
        try:
            json = await request.json()
            video_metadata = youtube_video.get_video_info(scraper.get_video_id(json['url']), scraper.api_key)
            scraper.ingest_material_video(video_metadata)

            return {"data": scraper.get_oer_id(json['url'])}

        except Exception as e:
            return {"data": "Invalid JSON data"}


@app.get("/add_materials/playlists/{oer_id}/")
async def view_playlist_materials(oer_id: str) -> dict:
    url = scraper.get_url_by_oer_id(oer_id)
    playlist_data = scraper.scrape_playlists(scraper.get_channel_id(url), [])
    return {"data": playlist_data}


@app.post('/ingest_playlists/{oer_id}/')
async def ingest_playlists(request: Request, oer_id: str ) -> dict:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        return "No Content-Type Provided"

    elif content_type == "application/json":
        try:
            json = await request.json()

            playlist_data = json['playlistData']

            channel_id = scraper.get_channel_id(scraper.get_url_by_oer_id(oer_id))

            playlist_ids = youtube_playlists.get_all_playlist_ids_by_channel_id(channel_id, scraper.api_key)

            print("PLAYLIST IDs: ", playlist_ids)

            print("LENGTH = ")

            for playlist_id in playlist_ids:
                print("INGESTING A PLAYLIST")
                playlist_info = youtube_playlists.get_playlist_info(playlist_id, scraper.api_key)
                scraper.ingest_series(playlist_info)

                episode_number = 1

                for video in playlist_data:
                    if video['playlist_id'] == playlist_id:
                        scraper.ingest_episode(video, episode_number)
                        episode_number += 1

            return {"status": "received"}

        except Exception as e:
            print(e)
            return {"status": "Invalid JSON Data"}


@app.post("/ingest_videos")
async def ingest_videos(request: Request) -> dict:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        return "No Content-Type Provided"

    elif content_type == "application/json":
        try:
            json = await request.json()

            video_data = json['videoData']

            for video in video_data:
                if video['deleted'] is False:
                    scraper.ingest_material_video(video)

            return {"status": "received"}

        except Exception as e:
            return {"status": "Invalid JSON Data"}


@app.get("/add_materials/videos/{oer_id}/")
async def view_video_materials(oer_id: str) -> dict:
    url = scraper.get_url_by_oer_id(oer_id)

    all_urls = [existing_url[0] for existing_url in scraper.get_all_existing_oer_urls()]

    indexed_videos = [scraper.get_video_id(indexed_url) for indexed_url in all_urls]

    video_data = scraper.scrape_videos(scraper.get_channel_id(url), indexed_videos)
    return {"data": video_data}


@app.post("/licensing_tool/")
async def licensing_tool(request: Request) -> dict:
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        return "No Content-Type Provided"

    elif content_type == "application/json":
        try:
            json = await request.json()
            print("JSON: ", json)
            licence_tool = LicenceTool()
            acceptable_licences = licence_tool.licences(json)
            return {"data": acceptable_licences}

        except Exception as e:
            print(e)
            return {"data": "Invalid JSON data"}


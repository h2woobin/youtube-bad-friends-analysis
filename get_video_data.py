import requests
import pandas as pd

API_KEY = "AIzaSyA7h2QD0OiVj3sdQwCtPUwqxhu00H2BW0M" #나의 API
CHANNEL_ID = "UCmuRHGhh-g0f9f5JiuW6dMw" #Bad friends의 API

def get_upload_playlist_id(api_key, channel_id):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": api_key
    }
    res = requests.get(url, params=params)
    items = res.json().get("items", [])
    if not items:
        print("❌ Can't find channel detail.")
        return None
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids_from_playlist(api_key, playlist_id, max_results=30):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "maxResults": max_results,
        "key": api_key
    }
    res = requests.get(url, params=params)
    items = res.json().get("items", [])
    return [item["contentDetails"]["videoId"] for item in items]

def get_video_details(api_key, video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": api_key
    }
    res = requests.get(url, params=params)
    items = res.json().get("items", [])
    data = []
    for item in items:
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        content = item["contentDetails"]
        data.append({
            "video_id": item["id"],
            "title": snippet["title"],
            "publishedAt": snippet["publishedAt"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "duration": content["duration"],
            "viewCount": stats.get("viewCount", 0),
            "likeCount": stats.get("likeCount", 0),
            "commentCount": stats.get("commentCount", 0)
        })
    return pd.DataFrame(data)

# ▶ 실행 순서
playlist_id = get_upload_playlist_id(API_KEY, CHANNEL_ID)
if playlist_id:
    video_ids = get_video_ids_from_playlist(API_KEY, playlist_id, max_results=30)
    print("📺 가져온 영상 ID:", video_ids)

    if video_ids:
        df = get_video_details(API_KEY, video_ids)
        df.to_csv("video_metadata.csv", index=False)
        print("✅ 영상 메타데이터 저장 완료! → 'video_metadata.csv'")
    else:
        print("❌ 영상 ID를 가져오지 못했습니다.")
else:
    print("❌ 재생목록 ID를 가져오지 못했습니다.")
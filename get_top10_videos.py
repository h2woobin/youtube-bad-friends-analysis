import requests
import pandas as pd
from tqdm import tqdm
import time

API_KEY = "AIzaSyA7h2QD0OiVj3sdQwCtPUwqxhu00H2BW0M" 

# 채널 ID 목록 (이름: 채널ID)
channels = {
    "techjoyce": "UCR4ZpFWX29p4YCajQA5fcfQ",
    "hanjustin": "UCA-LbP7nxuapv7vIBuiJUsw",
    "urmomashley": "UC1zACndCursf-RTGr9YvQmQ",
    "hjevelyn": "UCSGoIq_tVESqNYF1Re-zn1Q"
}

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
        return None
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_all_video_ids_from_playlist(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_ids = []
    next_page_token = None

    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": api_key
        }
        res = requests.get(url, params=params)
        data = res.json()
        items = data.get("items", [])
        video_ids += [item["contentDetails"]["videoId"] for item in items]
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def get_video_details(api_key, video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    all_data = []

    for i in tqdm(range(0, len(video_ids), 50)):
        batch_ids = video_ids[i:i+50]
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(batch_ids),
            "key": api_key
        }
        res = requests.get(url, params=params)
        items = res.json().get("items", [])
        for item in items:
            stats = item.get("statistics", {})
            snippet = item["snippet"]
            content = item["contentDetails"]
            all_data.append({
                "videoId": item["id"],
                "title": snippet["title"],
                "publishedAt": snippet["publishedAt"],
                "duration": content["duration"],
                "viewCount": int(stats.get("viewCount", 0)),
                "likeCount": int(stats.get("likeCount", 0)),
                "commentCount": int(stats.get("commentCount", 0)),
                "thumbnail": snippet["thumbnails"]["high"]["url"]
            })
        time.sleep(1)
    return pd.DataFrame(all_data)

# 전체 채널 순회
for name, channel_id in channels.items():
    print(f"\n🔍 Processing channel: {name}")
    playlist_id = get_upload_playlist_id(API_KEY, channel_id)
    if playlist_id:
        video_ids = get_all_video_ids_from_playlist(API_KEY, playlist_id)
        print(f"📺 Found {len(video_ids)} videos for {name}")
        if video_ids:
            df = get_video_details(API_KEY, video_ids)
            df_top10 = df.sort_values(by="viewCount", ascending=False).head(10)
            df_top10.to_csv(f"{name}_top10.csv", index=False)
            print(f"✅ Saved {name}_top10.csv")
        else:
            print(f"❌ No video IDs found for {name}")
    else:
        print(f"❌ Could not retrieve playlist ID for {name}")
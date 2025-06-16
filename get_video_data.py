import requests
import pandas as pd
from tqdm import tqdm

API_KEY = "AIzaSyA7h2QD0OiVj3sdQwCtPUwqxhu00H2BW0M" #나의 API
CHANNEL_ID = "UCRBpynZV0b7ww2XMCfC17qg" #Bad friends의 API

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

def get_video_details_batched(api_key, video_ids, batch_size=50):
    all_data = []
    for i in tqdm(range(0, len(video_ids), batch_size)):
        batch = video_ids[i:i+batch_size]
        df = get_video_details(api_key, batch)
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)


# ▶ 실행 순서
playlist_id = get_upload_playlist_id(API_KEY, CHANNEL_ID)
if playlist_id:
    video_ids = get_all_video_ids_from_playlist(API_KEY, playlist_id)
    print(f"📺 전체 영상 수: {len(video_ids)}")

    if video_ids:
        df_all = get_video_details_batched(API_KEY, video_ids)
        df_all["viewCount"] = pd.to_numeric(df_all["viewCount"], errors="coerce")

        # 조회수 상위 30개만 선택
        df_top30 = df_all.sort_values(by="viewCount", ascending=False).head(30)
        df_top30.to_csv("top_30_by_views.csv", index=False)
        print("✅ 조회수 상위 30개 영상 저장 완료! → 'top_30_by_views.csv'")
    else:
        print("❌ 영상 ID를 가져오지 못했습니다.")
else:
    print("❌ 재생목록 ID를 가져오지 못했습니다.")
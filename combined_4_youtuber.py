import pandas as pd

files = {
    "techjoyce_top10.csv": "TechJoyce",
    "hanjustin_top10.csv": "Han Justin",
    "urmomashley_top10.csv": "ur mom ashley",
    "hjevelyn_top10.csv": "HJ Evelyn"
}
# 원본 csv에 존재하는 이름을 내가 원하는 이름으로 바꾸기 위한 딕셔너리
required_columns = {
    "title": "video_title",
    "publishedAt": "published_date",
    "duration": "duration",
    "viewCount": "views",
    "likeCount": "likes",
    "commentCount": "comments"
}

# 빈 데이터프레임 생성
combined_df = pd.DataFrame()

for file, channel in files.items():
    df = pd.read_csv(file)

    #실제로 파일에 존재하는 열만 선택
    existing_cols = [col for col in required_columns if col in df.columns]
    # 필요한 열만 추출해서 데이터 프레임으로 다시 구성함
    df = df[existing_cols]
    # 열 이름을 내가 정한 이름으로 바꿔줌 
    df = df.rename(columns={col: required_columns[col] for col in existing_cols})

    for col in required_columns.values():
        if col not in df.columns:
            df[col] = pd.NA

    df["channel_name"] = channel

    ordered_cols = ["channel_name"] + list(required_columns.values())
    df = df[ordered_cols]

    combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_df.to_csv("combined_top10_videos.csv", index=False)
print("합치기 완료! 'combined_top10_videos.csv' 파일로 저장됐습니다.")

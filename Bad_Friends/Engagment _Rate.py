import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

df = pd.read_csv("top_30_by_views.csv")

df["viewCount"] = pd.to_numeric(df["viewCount"], errors="coerce")
df["likeCount"] = pd.to_numeric(df["likeCount"], errors="coerce")

def parse_duration(duration_str):
    pattern = re.compile(r'PT((?P<h>\d+)H)?((?P<m>\d+)M)?((?P<s>\d+)S)?')
    match = pattern.match(duration_str)
    if not match:
        return 0
    parts = match.groupdict()
    h = int(parts['h']) if parts['h'] else 0
    m = int(parts['m']) if parts['m'] else 0
    s = int(parts['s']) if parts['s'] else 0
    return h * 60 + m + s / 60

df["duration_minutes"] = df["duration"].apply(parse_duration)

df["publishedAt"] = pd.to_datetime(df["publishedAt"])
df["weekday"] = df["publishedAt"].dt.day_name()

df["like_rate"] = df["likeCount"] / df["viewCount"]

top_like_videos = df.sort_values(by="like_rate", ascending=False).head(5)

print("👍 Top Videos by likeCounts:")
print(top_like_videos[["title", "viewCount", "likeCount", "like_rate", "duration_minutes", "weekday"]])

text = " ".join(top_like_videos["title"])
wc = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title("Top Like Rate Video Keywords")
plt.show()
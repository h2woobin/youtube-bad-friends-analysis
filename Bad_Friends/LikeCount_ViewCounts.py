import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv("top_30_by_views.csv")

df["viewCount"] = pd.to_numeric(df["viewCount"], errors = "coerce")
df["likeCount"] = pd.to_numeric(df["likeCount"], errors = "coerce")

plt.figure(figsize=(10,6))
plt.scatter(df["viewCount"],df["likeCount"], alpha=0.7,color="green")

plt.xlabel("View Counts")
plt.ylabel("Like Counts")
plt.title("View Count vs Like Count")
plt.grid(True)
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x/1_000_000)}M'))
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y/1_000)}K'))

plt.tight_layout()
plt.show()

df["like_rate"] = df["likeCount"] / df["viewCount"]

top_like_rate = df.sort_values(by="like_rate", ascending=False)[["title", "viewCount", "likeCount", "like_rate"]]
print(top_like_rate.head(5))
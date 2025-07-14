import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("combined_top10_videos.csv")

df["views"] = df["views"].str.replace(",","").astype(int)
df["likes"] = df["likes"].str.replace(",","").astype(int)

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="views",y="likes", hue="channel_name",s=80,alpha=0.7)
plt.title("View Counts vs Like Counts")
plt.xlabel("Views",fontsize=12)
plt.ylabel("Likes",fontsize=12)

import matplotlib.ticker as ticker

def human_format(num, pos):
    if num >= 1_000_000:
        return f'{int(num/1_000_000)}M'
    elif num >= 1_000:
        return f'{int(num/1_000)}K'
    else:
        return str(int(num))

plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(human_format))
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(human_format))

plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(title="Channel Name")
plt.tight_layout()
plt.show()

corr = df["views"].corr(df["likes"])
print(f"조회수와 좋아요 수의 상관계수: {corr:.4f}")

##회귀선 그릴지 결정
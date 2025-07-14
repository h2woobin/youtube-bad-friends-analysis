import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

df = pd.read_csv("combined_top10_videos.csv")

df["views"] = df["views"].str.replace(",","").astype(int)

def duration_to_seconds(duration_str):
    if pd.isna(duration_str):
        return 0

    minutes = seconds = 0
    min_match = re.search(r'(\d+)\s*min', duration_str)
    sec_match = re.search(r'(\d+)\s*sec', duration_str)

    if min_match:
        minutes = int(min_match.group(1))
    if sec_match:
        seconds = int(sec_match.group(1))

    return minutes * 60 + seconds

df["duration_seconds"] = df["duration"].apply(duration_to_seconds)

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="duration_seconds", y="views", hue="channel_name", s=80, alpha=0.7)
plt.title("Duration (sec) vs View Counts",fontsize=14)
plt.xlabel("Duration (sec)",fontsize=12)
plt.ylabel("View Counts",fontsize=12)

def human_format(num, pos):
    if num >= 1_000_000:
        return f'{int(num/1_000_000)}M'
    elif num >= 1_000:
        return f'{int(num/1_000)}K'
    else:
        return str(int(num))

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(human_format))
plt.legend(title="Channel Name")
plt.grid(True,linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
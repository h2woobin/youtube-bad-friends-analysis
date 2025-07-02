import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv("top_30_by_views.csv")

def parse_duration(duration_str):
    pattern = re.compile(r'PT((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?')
    match = pattern.match(duration_str)
    if not match:
        return 0
    time_data = match.groupdict()
    hours = int(time_data['hours']) if time_data['hours'] else 0
    minutes = int(time_data['minutes']) if time_data['minutes'] else 0
    seconds = int(time_data['seconds']) if time_data['seconds'] else 0

    total_minutes = hours * 60 + minutes + seconds / 60
    return total_minutes

# duration 컬럼 변환
df["duration_minutes"] = df["duration"].apply(parse_duration)
# 조회수 숫자형 변환
df["viewCount"] = pd.to_numeric(df["viewCount"], errors="coerce")

df["is_short"] = df["duration_minutes"] < 10 

plt.figure(figsize=(10,6))

plt.scatter(
    df[df["is_short"]]["duration_minutes"],
    df[df["is_short"]]["viewCount"],
    color = "red", label = "Short Videos (<10 min)", alpha=0.7
)

plt.scatter(
    df[~df["is_short"]]["duration_minutes"],
    df[~df["is_short"]]["viewCount"],
    color="blue", label="Long Videos (≥10 min)", alpha=0.7
)

plt.xlabel("Video Duration (minutes)")
plt.ylabel("View Count")
plt.title("Video Duration vs View Count")
plt.legend()

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x/1_000_000)}M'))

plt.grid(True)
plt.tight_layout()
plt.show()


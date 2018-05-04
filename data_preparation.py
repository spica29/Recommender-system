import json
import pandas as pd
import collections
from pprint import pprint

with open('E:\D\FRI\Recommendation System\data\mpd.slice.0-999.json') as f:
    data = json.load(f)

data1 = pd.DataFrame.from_dict(data["playlists"])
data1.to_csv("file.csv", columns=["name", "tracks"])

dict = collections.defaultdict(list)
for playlist in data["playlists"]:
    for song in playlist["tracks"]:
        song_name = song["track_name"] + ", " + song["artist_name"] + ", " + song["album_name"]
        dict[playlist["name"]].append(song_name)

data2 = pd.DataFrame.from_dict(dict, orient='index')
data2 = data2.to_csv("file2.csv")



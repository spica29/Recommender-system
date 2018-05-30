import json

with open('D:\D\FRI\Recommendation System\data\mpd.slice.0-999.json') as f:
    given_playlist = json.load(f)

a = 0
size_list = []
for playlist in given_playlist["playlists"]:
    for track in playlist["tracks"]:
        print track

    #take size
        size_list.append(len(playlist["tracks"]))

    a = a + 1
    if a >= 2:
        break

print(size_list[0])
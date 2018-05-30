import math
from elasticsearch import Elasticsearch
es = Elasticsearch()

res = es.search(index="playlists", body={"query": {"match_all": {}}})

counter = 0
tracksA_size = 0
tracksB_size = 0
dict_songs = dict()
for hit in res['hits']['hits']:
    #cosine similarity - scalar product (intersection) / size(tracks A) * size( tracks B)

    name = hit['_source'].get('name')
    print "Playlist name: " + name

    tracks = hit['_source'].get('tracks')
    if counter == 0:
        tracksA_size = hit['_source'].get('num_tracks')
    else:
        tracksB_size = hit['_source'].get('num_tracks')
    print "Artists:"
    for track in tracks:
        track_uri = str(track["track_uri"])
        dict_songs.setdefault(track_uri, []).append(1)

    counter = counter + 1
    if counter >= 2:
        break

#find intersection
same_songs = filter(lambda x: len(x) > 1, dict_songs.values())
num_of_same_songs = sum(same_songs)
cos = (num_of_same_songs / math.sqrt(int(tracksA_size)) * math.sqrt(int(tracksB_size)))

print cos
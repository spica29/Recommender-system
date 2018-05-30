import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

with open('D:\D\FRI\Recommendation System\data\mpd.slice.1000-1999.json') as f:
    data = json.load(f)
es.indices.delete(index='playlists')
mapping = "{ 'properties': { 'tracks.track_uri': { 'type': 'text','fielddata': true }}}"
es.indices.create(index='playlists', ignore=400)

for playlist in data["playlists"]:
    # index name is playlists
    #es.update(index='playlists', doc_type='playlist')
    es.index(index='playlists', doc_type="playlist", body=playlist)


    #for song in playlist["tracks"]:
        #song_name = song["track_name"] + ", " + song["artist_name"] + ", " + song["album_name"]
        #dict[playlist["name"]].append(song_name)

es.indices.put_mapping(index='playlists', mapping=mapping)




import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

#given list of songs from new playlist try to find playlists with biggest number of same songs
#make body request
es.indices.create(index='challenge', ignore=400)

with open('C:\Users\Amela\Downloads\challenge_set.json') as f:
    given_playlist = json.load(f)
for playlist in given_playlist["playlists"]:
    es.index(index='challenge', doc_type="playlist", body=playlist)


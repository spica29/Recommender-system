from elasticsearch import Elasticsearch
es = Elasticsearch()

#given list of songs from new playlist try to find playlists with biggest number of same songs

res = es.search(index="playlists", body={"query": {"match_all": {}}})

for playlist in given_playlist["playlists"]:
    es.index(index='challenge', doc_type="playlist", body=playlist)


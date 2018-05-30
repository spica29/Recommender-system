import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

with open('challenge.pt1.json') as f:
    challenge = json.load(f)
es.indices.delete(index='challenge')
es.indices.create(index='challenge', ignore=400)

more_like_string = ""

for track in challenge["tracks"]:
    # index name is playlists
    #es.index(index='playlists', doc_type="playlist", body=playlist)

    more_like_string += track["artist_name"] + " " + track["track_name"] + " "

print "More like " + more_like_string
query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"tracks.artist_name\", \"tracks.track_name\"], \"like\":\"" + more_like_string + "\",\"min_term_freq\" : 1,\"max_query_terms\" : 100}}}"
print "query: " + query
res = es.search(index="playlists", body=query)
print "Result: "
for hit in res['hits']['hits']:
    playlist_name = hit['_source'].get('name')
    playlist_score = hit['_score']
    print "playlist name: " + str(playlist_name) + ", playlist score " + str(playlist_score)

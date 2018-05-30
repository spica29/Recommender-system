import json
from elasticsearch import Elasticsearch
es = Elasticsearch()

with open('challenge.pt6.json') as f:
    challenge = json.load(f)
#es.indices.delete(index='challenge')
#es.indices.create(index='challenge', ignore=400)

more_like_string = ""

for track in challenge["tracks"]:
    more_like_string += track["artist_name"] + " " + track["track_name"] + " "

print "More like " + more_like_string
query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"tracks.artist_name\", \"tracks.track_name\"], \"like\":\"" + more_like_string + "\",\"min_term_freq\" : 1,\"max_query_terms\" : 100}}}"
print "query: " + query
res = es.search(index="playlists", body=query, size=100)
print "Result: "
score_results = ""
for hit in res['hits']['hits']:
    playlist_name = hit['_source'].get('name')
    playlist_score = hit['_score']
    #print playlist_name
    #print str(playlist_score)
    score_results += "playlist name: " + playlist_name.encode('utf-8').strip() + ", playlist score " + str(round(playlist_score, 5)) + "\n"

with open("results.txt", "w") as text_file:
    text_file.write(score_results )
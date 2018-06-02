import json
import re
import songs_popularity
import synonyms
import es_functions
from elasticsearch import Elasticsearch
es = Elasticsearch()

#with open('challenge/challenge.pt4.notracks.json') as f:
with open('challenge/challenge.pt1.json') as f:
    challenge = json.load(f)
#es.indices.delete(index='challenge')
#es.indices.create(index='challenge', ignore=400)

more_like_string = ""
query = ""
#if there are no tracks in playlist
#print "len " + len(challenge["tracks"])
print len(challenge["tracks"])
if len(challenge["tracks"]) == 0:
    #first try to figure out if it is some singer or album

    #second find synonyms of the word, give bigger score to the one similar to real name of playlist, less score to synonyms
    playlist_name = challenge["name"]
    more_like_string = str(playlist_name)
    synonyms_string = synonyms.find_synonyms(playlist_name)
    if len(more_like_string) > 0:
        query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"name\"], \"like\":[\"" + re.sub('\W', ' ', more_like_string) + "\", \"" + synonyms_string + "\"],\"min_term_freq\" : 1}}}"
    #else:
        #synonym not found, suggest most famous songs
else:
    print "search similar songs"
    #if there are tracks in playlist
    for track in challenge["tracks"]:
        more_like_string += track["artist_name"] + " " + track["track_name"] + " "
    query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"tracks.artist_name\", \"tracks.track_name\"], \"like\":\"" + re.sub('\W', ' ', more_like_string) + "\",\"min_term_freq\" : 1}}}"
#print "More like " + more_like_string

#print "query: " + query

print query
res = es.search(index="playlists", body=query, size=100)

score_results = ""
playlists = ""
songs = ""
#query_aggs = "{\"aggs\": {\"top-songs\": {\"terms\": { \"field\" : \"tracks.track_uri\"}}}}

#put each list of tracks to index songs
es.indices.delete(index='tracks')
mapping = "{\"properties\": {\"track_uri\": {\"type\": \"text\",\"fielddata\": true}}}"
es.indices.create(index='tracks', ignore=400, body=mapping)
es_functions.put_mapping("tracks", "track", mapping)
for hit in res['hits']['hits']:
    playlist_name = hit['_source'].get('name')
    playlist_score = hit['_score']
    playlists += str(hit['_source'].get('pid'))
    #print playlist_name
    #print str(playlist_score)
    score_results += "playlist name: " + playlist_name.encode('utf-8').strip() + ", playlist score " + str(round(playlist_score, 5)) + "\n"
    tracks = hit['_source'].get('tracks')

    #find popularity of songs in list and rank them
    for track in tracks:
        es.index(index='tracks', doc_type="track", body=track)
        track_uri = re.sub('spotify:track:', '', str(track["track_uri"]))
        #print track_uri
        popularity = songs_popularity.popularity(track_uri)
        #print "popularity " + str(popularity)
        songs += track_uri

top_songs = songs_popularity.sort_famous_songs()

score_results += "\n songs: \n" + top_songs
#with open("results/results4.notracks.txt", "w") as text_file:
with open("results/results1.analyzed.txt", "w") as text_file:
    text_file.write(score_results)
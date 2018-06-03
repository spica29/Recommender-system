import json
import re
import songs_popularity
import synonyms
import es_functions
from elasticsearch import Elasticsearch
es = Elasticsearch()

def index_songs_from_similar_playlist(challenge_file, results_file):
    with open(challenge_file) as f:
        challenge = json.load(f)

    if es.indices.exists(index="challenge"):
        es.indices.delete(index='challenge')
    es.indices.create(index='challenge', ignore=400)

    more_like_string = ""
    query = ""
    #if there are no tracks in playlist
    if len(challenge["tracks"]) == 0:
        #first try to figure out if it is some singer or album

        #second find synonyms of the word, give bigger score to the one similar to real name of playlist, less score to synonyms
        playlist_name = challenge["name"]
        more_like_string = str(playlist_name)
        synonyms_string = synonyms.find_synonyms(playlist_name)
        if len(more_like_string) > 0:
            query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"name\"], \"like\":[\"" + re.sub('\W', ' ', more_like_string) + "\", \"" + synonyms_string + "\"],\"min_term_freq\" : 1, \"max_query_terms\": 500}}}"
        #else:
            #synonym not found, suggest most famous songs
    else:
        #print "size " + str(len(challenge["tracks"]))
        #print "search similar songs"
        #if there are tracks in playlist
        for track in challenge["tracks"]:
            more_like_string += track["artist_name"] + " " + track["track_name"] + " "
            # index challenge songs
            es.index(index='challenge', doc_type="challenge", body=track)
        query = "{ \"query\" :{\"more_like_this\" : {\"fields\" : [\"tracks.artist_name\", \"tracks.track_name\"], \"like\":\"" + re.sub('\W', ' ', more_like_string) + "\",\"min_term_freq\" : 1}}}"

    print query
    res = es.search(index="playlists", body=query, size=100)

    score_results = ""
    playlists = ""
    songs = ""
    #query_aggs = "{\"aggs\": {\"top-songs\": {\"terms\": { \"field\" : \"tracks.track_uri\"}}}}

    #put each list of tracks to index songs
    if es.indices.exists(index="tracks"):
        es.indices.delete(index='tracks')

    es.indices.create(index='tracks', ignore=400)
    #mapping = "{\"properties\": {\"track_uri\": {\"type\": \"text\",\"fielddata\": true}}}"
    #es_functions.put_mapping("tracks", "track", mapping)
    es_functions.mapping_fielddata("tracks", "track", "track_uri")
    for hit in res['hits']['hits']:
        playlist_name = hit['_source'].get('name')
        playlist_score = hit['_score']
        playlists += str(hit['_source'].get('pid'))
        #print playlist_name
        #print str(playlist_score)
        score_results += "playlist name: " + playlist_name.encode('utf-8').strip() + ", playlist score " + str(round(playlist_score, 5)) + "\n"
        tracks = hit['_source'].get('tracks')

        #make new index of songs
        for track in tracks:
            es.index(index='tracks', doc_type="track", body=track)
            track_uri = re.sub('spotify:track:', '', str(track["track_uri"]))
            popularity = songs_popularity.popularity(track_uri)
            songs += track_uri
    #find popularity of songs in list and rank them
    with open(results_file, "w") as text_file:
        text_file.write(score_results)

def songs_popularity_file(results_file):
    #aggs
    score_results = ""
    top_songs = songs_popularity.sort_famous_songs()

    score_results += "\n songs: \n" + top_songs
    with open(results_file, "a") as text_file:
        text_file.write(score_results)

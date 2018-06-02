from elasticsearch import Elasticsearch
es = Elasticsearch()

def popularity(track_uri):
    query = "{ \"query\" : {\"bool\" : {\"must\" : [{ \"match\" : {\"tracks.track_uri\" : \"" + track_uri + "\"} }]}}}"

    res = es.search(index="playlists", body=query, size=100)
    num = res["hits"]["total"]

    return num

def sort_famous_songs():
    # find most famous songs
    query = "{\"aggs\": {\"top-terms-aggregation\": {\"terms\": { \"field\" : \"track_uri\"}}}}"

    res = es.search(index="tracks", body=query, size=100)
    track_uri_dict = {}
    top_songs = ""
    # suggest most famous ones from playlist
    for agg in res['aggregations']["top-terms-aggregation"]["buckets"]:
        if "spotify" in agg["key"]:
            continue
        track_uri = agg["key"]
        top_songs += track_uri + " "
        track_uri_dict[track_uri] = 1

    top_songs = ""
    for track_uri in track_uri_dict:
        # get song name and artist
        #print track_uri
        query_find_info = "{ \"query\" : {\"bool\" : {\"must\" : [{ \"match\" : {\"track_uri\" : \"" + track_uri + "\"}}]}}}\""
        track_info = es.search(index="tracks", body=query_find_info, size=1)

        for hit in track_info["hits"]["hits"]:
            top_songs += str(hit["_source"].get("artist_name")) + " " + str(hit["_source"].get("track_name")) + "\n"

    return top_songs

#print sort_famous_songs()

from elasticsearch import Elasticsearch
es = Elasticsearch()

def popularity(track_uri):
    query = "{ \"query\" : {\"bool\" : {\"must\" : [{ \"match\" : {\"tracks.track_uri\" : \"" + track_uri + "\"} }]}}}"

    res = es.search(index="playlists", body=query, size=100)
    num = res["hits"]["total"]

    return num

def sort_famous_songs():
    #idea for improvement: rank songs by popularity (similarity) of playlist

    # find most famous songs
    query = "{\"aggs\" : {\"top-terms-aggregation\" : {\"terms\" : {\"field\" : \"track_uri\",\"size\" : 100}}}}"

    res = es.search(index="tracks", body=query, size=100)
    track_uri_dict = {}
    top_songs = ""
    print res['aggregations']["top-terms-aggregation"]["buckets"]
    # suggest most famous ones from playlist
    counter = 0
    for agg in res['aggregations']["top-terms-aggregation"]["buckets"]:
        if "spotify" in agg["key"]:
            continue
        track_uri = agg["key"]
        #if songs exist in challenge index don't put it in the dict
        query_find_info = "{ \"query\" : {\"bool\" : {\"must\" : [{ \"match\" : {\"track_uri\" : \"" + track_uri + "\"}}]}}, \"size\": 100}\""
        track_exists = es.search(index="challenge", body=query_find_info, size=1)
        if track_exists["hits"]["total"] > 0:
            continue

        top_songs += track_uri + " "
        track_uri_dict[counter] = track_uri
        counter += 1
    counter = 0
    top_songs = ""
    print track_uri_dict
    for num in track_uri_dict.items():
        # get song name and artist
        #print track_uri
        query_find_info = "{ \"query\" : {\"bool\" : {\"must\" : [{ \"match\" : {\"track_uri\" : \"" + str(num) + "\"}}]}}, \"size\": 100}\""
        track_info = es.search(index="tracks", body=query_find_info, size=1)

        for hit in track_info["hits"]["hits"]:
            song = str(counter) + " " + str(hit["_source"].get("artist_name").encode('utf-8').strip()) + " " + str(
                hit["_source"].get("track_name").encode('utf-8').strip()) + "\n"
            top_songs += song
        counter += 1

    return top_songs

#score_results_songs = sort_famous_songs()
#with open("results/results1.justsongs2.txt", "w") as text_file:
    #text_file.write(score_results_songs)
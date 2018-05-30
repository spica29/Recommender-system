import os, json
import pandas as pd
from elasticsearch import Elasticsearch
es = Elasticsearch()

json_files = [pos_json for pos_json in os.listdir("./") if pos_json.startswith('mpd.slice')]
#with open('.\mpd.slice.0-999.json') as f:
    #data = json.load(f)
#es.indices.delete(index='playlists')
#mapping = "{ 'properties': { 'tracks.track_uri': { 'type': 'text','fielddata': true }}}"
#es.indices.create(index='playlists', ignore=400)
#print json_files
es.indices.delete(index='playlists')
mapping = "{ 'properties': { 'tracks.track_uri': { 'type': 'text','fielddata': true }}}"
es.indices.create(index='playlists', ignore=400)
for file in json_files:
    with open(file) as file:
        data = json.load(file)

    for playlist in data["playlists"]:
        # index name is playlists
        es.index(index='playlists', doc_type="playlist", body=playlist)

es.indices.put_mapping(index='playlists', mapping=mapping)




from elasticsearch import Elasticsearch
es = Elasticsearch()
import json
import requests

def mapping_fielddata(index, type, field):
    mapping = "{\"properties\": {\"" + field + "\": {\"type\": \"text\",\"fielddata\": true}}}"
    url = "http://localhost:9200/" + index + "/_mapping/" + type
    print "url" + str(url)
    print " mapping " + str(mapping)
    r = requests.post(url, json=json.loads(mapping))
    print r.content

def put_mapping(index, type, mapping):
    es.indices.put_mapping(index=index, doc_type=type, body=mapping)
    print "mapping done"
#mapping = "{\"properties\": {\"bla\": {\"type\": \"keyword\"}}}"
#mapping = "{\"properties\": {\"bla\": {\"type\": \"text\",\"fielddata\": true}}}"

#if es.indices.exists(index="trial"):
#    es.indices.delete(index="trial")
#es.indices.create(index='trial', ignore=400)
#mapping_fun("trial", "trial", mapping)
#es.index(index='trial', doc_type="trial", body="{\"bla\":\"bla\"}")
#print "DONE"
from elasticsearch import Elasticsearch
es = Elasticsearch()
import json

def put_mapping(index, type, mapping):
    es.indices.put_mapping(index=index, doc_type=type, body=mapping)
    print "mapping done"
#mapping = "{\"properties\": {\"bla\": {\"type\": \"keyword\"}}}"
#mapping = {
 #   "properties": {
  #      "bla": {
    #        "type": "text",
   #         "fielddata": True
     #   }
   # }
#}
#put_mapping("tracks", "track", mapping)
#es.indices.delete(index="trial")
#es.indices.create(index='trial', ignore=400, body=mapping)
#put_mapping("trial", "trial", mapping)
#es.index(index='trial', doc_type="trial", body="{\"bla\":\"bla\"}")
#print "DONE"
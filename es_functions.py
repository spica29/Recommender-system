from elasticsearch import Elasticsearch
es = Elasticsearch()

def put_mapping(index, type, mapping):
    es.indices.put_mapping(index=index, doc_type=type, body=mapping)


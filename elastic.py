from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

def es_index(data):
    return es.index(index="tweet",body=data)

def bulk_json_data(json_list, _index):
    for doc in json_list:
    # use a `yield` generator so that the data
    # isn't loaded into memory
        # if '{"index"' not in doc:
        yield {
            "_index": _index,
            "_type": "document",
            "_source": doc
        }

def es_bulk_index(data):
    try:
        # make the bulk call, and get a response
        response = helpers.bulk(es, bulk_json_data(data, "tweet"))
        print("Response -", response)
        # print ("\nbulk_json_data() RESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)

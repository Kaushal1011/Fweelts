from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()


def es_index(data):
    return es.index(index="tweet", body=data)


def bulk_json_data(json_list, _index):
    for doc in json_list:
        # use a `yield` generator so that the data
        # isn't loaded into memory
        # if '{"index"' not in doc:
        yield {
            "_index": _index,
            "_type": "_doc",
            "_source": doc
        }


def es_add(data):
    print(len(data["data"]))
    for i in data["data"]:
        es.index(index="tweet_v2",
                 body={"tweet": i})


def es_bulk_index(data):
    try:
        # make the bulk call, and get a response
        response = helpers.bulk(es, bulk_json_data(data, "tweet"))
        # print("Response -", response)
        # print ("\nbulk_json_data() RESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)


def es_delete():
    es.indices.delete(index='tweet_v2', ignore=[400, 404])
    es.delete_by_query(index="tweet", body={
                       "query": {"match_all": {}}}, ignore=[400, 404])

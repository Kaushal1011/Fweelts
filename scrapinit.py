
import requests
import os
import json
from elasticsearch import Elasticsearch
from pprint import pprint


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def create_url_location(query, nooftweets):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    #     tweet_fields = "tweet.fields=author_id"
    # max_results=100
    url = 'https://api.twitter.com/2/tweets/search/recent?query="point_radius:[{} {} {}mi]"&max_results={}'.format(
        query[0], query[1], query[2], nooftweets
    )
    return url


def create_url(query, nooftweets):
    url = 'https://api.twitter.com/2/tweets/search/recent?query={}&tweet.fields=created_at,geo,lang&place.fields=geo,country&max_results={}'.format(
        query, nooftweets
    )
    return url


def auth():
    return "AAAAAAAAAAAAAAAAAAAAAC6vMwEAAAAA5uumFGxBM1e4Kfyfr8E5TJseEZw%3DHV6mjkDp1QrpVm1bpi2yZrvAEkpqhxCK91fGkjl5gevPwtLScM"


if __name__ == "__main__":
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    bearer_token = auth()
    url = create_url("DOGE", 10)
    headers = create_headers(bearer_token)
    print(url)
    json_response = connect_to_endpoint(url, headers)
    print(type(json_response))
    # es.indices.delete(index='idx_twp', ignore=[400, 404])
    # Puts data in elastic
    for i in json_response["data"]:
        es.index(index="idx_twp",
                 body={"tweet": i})
    res = es.search(index="idx_twp", body={
        "query": {
            "match": {
                "tweet.text": {
                    "query": "doge"
                }
            }
        }
    })
    pprint(res)

import tweepy
from config import *
import requests
import os
import json

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def create_url(query):
    url = 'https://api.twitter.com/2/tweets/search/recent?query={}&max_results=100&tweet.fields=created_at,geo,id,lang,public_metrics,source,text&expansions=attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'.format(
        query
    )
    return url


def auth():
    return "AAAAAAAAAAAAAAAAAAAAAC6vMwEAAAAA5uumFGxBM1e4Kfyfr8E5TJseEZw%3DHV6mjkDp1QrpVm1bpi2yZrvAEkpqhxCK91fGkjl5gevPwtLScM"


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def search_tweets_v2(query):
    bearer_token = auth()
    url = create_url(query)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response


def search_tweets(query, count=400):
    tweets = tweepy.Cursor(api.search, query, count=count,
                           tweet_mode="extended").items(count)
    return [tweet._json for tweet in tweets]
    # return api.search(q=query, count=100, tweet_mode="extended")


# if __name__ == '__main__':
    # tweets = search_tweets('covid')
    # print(type(tweets))
    # for tweet in tweets:
    #     print(tweet.text)

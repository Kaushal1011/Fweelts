# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from elastic import *
from twitter import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from state import sentiment_count, emotion_count
# from sentiment import sentiment_classifier

# Emotion Detection

API_URL = "https://api-inference.huggingface.co/models/nateraw/bert-base-uncased-emotion"

headers = {"Authorization": "Bearer api_DZJYiVotgUyAUOyftasDrSxnKjxodgPABr"}


def query(payload):
    data = json.dumps(payload)
    response = requests.request(
        "POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='COVID-19'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Button(id='analyse-submit',  n_clicks=0, children='Analyse'),
    html.Button(id='delete-submit',  n_clicks=0, children='Delete'),
    dcc.Input(id='input-2-state', type='text',
              placeholder="Word Relation Analyser"),
    html.Button(id='wr-submit',  n_clicks=0, children='Analyse Word Relation'),
    html.Div(id='output-state'),
    html.Div(id='output-state2')
])


@app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_output(n_clicks, input1):
    es_delete()
    tweets = search_tweets_v2(input1)
    # output = 'NEW TWEET'.join(tweet['full_text'] for tweet in tweets)
    # print(es_index(tweets[0]))
    # es_bulk_index(tweets)
    es_add(tweets)
    return("Added Tweets to Elastic {}".format(n_clicks))


@app.callback(Output('output-state2', 'children'),
              Input('analyse-submit', 'n_clicks'),
              State('input-1-state', 'value'))
def update_output(n_clicks, input1):

    res = es.search(index="tweet_v2", body={
        "size": 100,
        "query": {
            "match": {
                "tweet.text": {
                    "query": input1,
                    "analyzer": "stop"
                }
            }
        },
        "_source": "tweet.text",
        "aggs": {
            "keywords": {
                "significant_text": {
                    "field": "tweet.text", "size": 25
                }},
            "keywords2": {
                "significant_text": {
                    "field": "tweet.text.keyword", "size": 25
                }
            }
        }}, ignore=[400, 404])
    # print(res)
    tweettext = [text["_source"]["tweet"]["text"]
                 for text in res["hits"]["hits"]]

    # call sentiment api
    keywords = [word["key"]
                for word in res["aggregations"]["keywords"]["buckets"]]
    score = [int(10000*word["score"])
             for word in res["aggregations"]["keywords"]["buckets"]]

    # Word Cloud Processing

    wc_dict = {}
    for i in range(len(keywords)):
        wc_dict[keywords[i]] = score[i]

    wordcloud = WordCloud(
        width=500, height=500).generate_from_frequencies(wc_dict)
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.show()
    plt.savefig('yourfile.png', bbox_inches='tight')
    plt.close()

    # sentiment processing

    url = "http://localhost:8000/sentiment"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # proces sentiment values here
    sentiment_count = {
        "POSITIVE": 0,
        "NEGATIVE": 0
    }
    for i in response.json()["data"][0]:
        sentiment_count[i["label"]] += 1

    print(sentiment_count)

    # Emotion Process

    url = "http://localhost:8000/emotion"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Process emotion data here
    emotion_count = {
        "sadness": 0,
        "joy": 0,
        "love": 0,
        "anger": 0,
        "fear": 0,
        "surprise": 0
    }

    for i in response.json()["data"][0]:
        emotion_count[i["label"]] += 1

    print(emotion_count)


if __name__ == '__main__':
    app.run_server(debug=True)

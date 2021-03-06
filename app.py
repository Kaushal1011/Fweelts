# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from elastic import *
from twitter import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import dash_d3cloud
from collections import Counter
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


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Input(id='input-1-state',
                          type='text', value='COVID-19'), width=3),
        dbc.Col(html.Button(id='submit-button-state',
                            n_clicks=0, children='Submit'), width=3),
        dbc.Col(html.Button(id='analyse-submit',
                            n_clicks=0, children='Analyse'), width=3),
        dbc.Col(html.Button(id='delete-submit',
                            n_clicks=0, children='Delete'), width=3),
    ], align="center"),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Input(id='input-2-state', type='text',
                          placeholder="Word Relation Analyser"), width=3),
        dbc.Col(html.Button(id='wr-submit',  n_clicks=0,
                            children='Analyse Word Relation'), width=3),
    ], align="center"),
    dbc.Row([
        dbc.Col(html.Div(id='output-state')),
    ]),
    # html.Div(id='output-state2'),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="positive-negative-pie"), width=6),
            dbc.Col(dcc.Graph(id="emotion-pie"), width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="twsent-pie"), width=6),
            dbc.Col(dcc.Graph(id="finsent-pie"), width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dash_d3cloud.WordCloud(
                id='wordcloud',
                words=[{"text": 'wordcloud', "value": 20}, {"text": 'will', "value": 15}, {
                    "text": 'appear', "value": 15}, {"text": 'here', "value": 15}],
                options={"scale": "log"}
            ), width=12),
        ], align="baseline"
    ),
    dbc.Row(
        [dbc.Col(dcc.Graph(id="source-bar"), width=12), ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="positive-negative-pie-wa"), width=6),
            dbc.Col(dcc.Graph(id="emotion-pie-wa"), width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="twsent-pie-wa"), width=6),
            dbc.Col(dcc.Graph(id="finsent-pie-wa"), width=6),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dash_d3cloud.WordCloud(
                id='wordcloud-wa',
                words=[{"text": 'wordcloud', "value": 20}, {"text": 'will', "value": 15}, {
                    "text": 'appear', "value": 15}, {"text": 'here', "value": 15}],
                options={"scale": "log"}
            ), width=12),
        ], align="baseline"
    ),
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

# Output('output-state2', 'children'),


@app.callback(Output('positive-negative-pie', 'figure'),
              Output('emotion-pie', 'figure'),
              Output('twsent-pie', 'figure'),
              Output('finsent-pie', 'figure'),
              Output('wordcloud', 'words'),
              Output('source-bar', 'figure'),
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
        "aggs": {
            "keywords": {
                "significant_text": {
                    "field": "tweet.text", "size": 50
                }},
            "keywords2": {
                "significant_text": {
                    "field": "tweet.text.keyword", "size": 30
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
    keywords_wordcloud = []
    for k, s in zip(keywords, score):
        if k != input1:
            keywords_wordcloud.append({"text": k, "value": int(s**0.25)+1})

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
    count = 0
    for i in response.json()["data"][0]:
        sentiment_count[i["label"]] += 1
        es_update(res["hits"]["hits"][count]["_id"], res["hits"]
                  ["hits"][count]["_source"], i)
        count += 1

    df = pd.DataFrame(np.array([['POSITIVE', sentiment_count['POSITIVE']], [
                      'NEGATIVE', sentiment_count['NEGATIVE']]]), columns=['sentiment', 'count'])
    print(df)
    pos_neg_pie = px.pie(df, values='count', names='sentiment')

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

    emotion_arr = []
    for k, v in emotion_count.items():
        emotion_arr.append([k, v])
    df = pd.DataFrame(np.array(emotion_arr), columns=['emotion', 'count'])
    emotion_pie = px.pie(df, values='count', names='emotion')
    print(emotion_count)

    # Twitter sentiment pie

    url = "http://localhost:8000/twsent"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Process emotion data here
    twsent_count = {
        "LABEL_0": 0,
        "LABEL_1": 0,
        "LABEL_2": 0,
    }

    for i in response.json()["data"][0]:
        twsent_count[i["label"]] += 1

    twsent_count["Positive"] = twsent_count.pop("LABEL_2")
    twsent_count["Neutral"] = twsent_count.pop("LABEL_1")
    twsent_count["Negative"] = twsent_count.pop("LABEL_0")

    print(twsent_count)

    tw_arr = []
    for k, v in twsent_count.items():
        tw_arr.append([k, v])
    df = pd.DataFrame(np.array(tw_arr), columns=['sentiment', 'count'])
    tw_pie = px.pie(df, values='count', names='sentiment')

    # Financial Sentiment
    url = "http://localhost:8000/finsent"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Process emotion data here
    finsent_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }

    for i in response.json()["data"][0]:
        finsent_count[i["label"]] += 1

    fin_arr = []
    print(finsent_count)
    for k, v in finsent_count.items():
        fin_arr.append([k, v])
    df = pd.DataFrame(np.array(fin_arr), columns=['fin sentiment', 'count'])
    fin_pie = px.pie(df, values='count', names='fin sentiment')
    # Tweet Source Analysis
    # res = es.search(index="tweet_v2", body={
    #     "query": {
    #         "match_all": {}
    #     },
    #     "_source" : {
    #         "includes" : [
    #         "tweet.source"
    #         ]
    #     },
    #     "size" : 100
    # }, ignore=[400, 404])
    # source_count = Counter(res["_source"]["tweet"]["source"])
    # print(source_count)

    res = es.search(index="tweet_v2", body={
        "query": {
            "match_all": {}
        },
        "aggs": {
            "keywords": {
                "terms": {
                    "field": "tweet.source.keyword",
                    "size": 50
                }
            }
        },
        "_source": False
    }, ignore=[400, 404])
    # print(res["aggregations"]["keywords"]["buckets"])
    df = pd.DataFrame.from_dict(res["aggregations"]["keywords"]["buckets"])
    # print("hi")
    # print(res["aggregations"]["buckets"])
    # print(df)
    source_bar = px.bar(df, x='key', y='doc_count')
    return pos_neg_pie, emotion_pie, tw_pie, fin_pie, keywords_wordcloud, source_bar

# Word relation analyse


@app.callback(Output('positive-negative-pie-wa', 'figure'),
              Output('emotion-pie-wa', 'figure'),
              Output('twsent-pie-wa', 'figure'),
              Output('finsent-pie-wa', 'figure'),
              Output('wordcloud-wa', 'words'),
              Input('wr-submit', 'n_clicks'),
              State('input-2-state', 'value'))
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
        "aggs": {
            "keywords": {
                "significant_text": {
                    "field": "tweet.text", "size": 50
                }},
            "keywords2": {
                "significant_text": {
                    "field": "tweet.text.keyword", "size": 30
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
    keywords_wordcloud = []
    for k, s in zip(keywords, score):
        if k != input1:
            keywords_wordcloud.append({"text": k, "value": int(s**0.25)+1})

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
    count = 0
    for i in response.json()["data"][0]:
        sentiment_count[i["label"]] += 1
        es_update(res["hits"]["hits"][count]["_id"], res["hits"]
                  ["hits"][count]["_source"], i)
        count += 1

    df = pd.DataFrame(np.array([['POSITIVE', sentiment_count['POSITIVE']], [
                      'NEGATIVE', sentiment_count['NEGATIVE']]]), columns=['sentiment', 'count'])
    print(df)
    pos_neg_pie_wa = px.pie(df, values='count', names='sentiment')

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

    emotion_arr = []
    for k, v in emotion_count.items():
        emotion_arr.append([k, v])
    df = pd.DataFrame(np.array(emotion_arr), columns=['emotion', 'count'])
    emotion_pie_wa = px.pie(df, values='count', names='emotion')
    print(emotion_count)

    # Twitter sentiment pie

    url = "http://localhost:8000/twsent"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Process emotion data here
    twsent_count = {
        "LABEL_0": 0,
        "LABEL_1": 0,
        "LABEL_2": 0,
    }

    for i in response.json()["data"][0]:
        twsent_count[i["label"]] += 1

    twsent_count["Positive"] = twsent_count.pop("LABEL_2")
    twsent_count["Neutral"] = twsent_count.pop("LABEL_1")
    twsent_count["Negative"] = twsent_count.pop("LABEL_0")
    print(twsent_count)
    tw_arr = []
    for k, v in twsent_count.items():
        tw_arr.append([k, v])
    df = pd.DataFrame(np.array(tw_arr), columns=['sentiment', 'count'])
    tw_pie = px.pie(df, values='count', names='sentiment')

    # Financial Sentiment
    url = "http://localhost:8000/finsent"

    payload = json.dumps({
        "textlist": tweettext
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=Cu0qDKmbrZNCk1yDORM52IrPx9ylB8fmdiKrFrrqXTf0qt67BgL67h71q0aqR2zM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Process emotion data here
    finsent_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }

    for i in response.json()["data"][0]:
        finsent_count[i["label"]] += 1

    fin_arr = []
    for k, v in finsent_count.items():
        fin_arr.append([k, v])
    df = pd.DataFrame(np.array(fin_arr), columns=['fin sentiment', 'count'])
    fin_pie = px.pie(df, values='count', names='fin sentiment')

    return pos_neg_pie_wa, emotion_pie_wa, tw_pie, fin_pie, keywords_wordcloud


if __name__ == '__main__':
    app.run_server(debug=True)

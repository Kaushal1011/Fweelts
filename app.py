# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from elastic import *
from twitter import *
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
        }

    })
    print(res)

    # data = query({"inputs": "I like you. I love you"})

    # print(data)
    # for tweet in tweets:
    #     print(tweet.text)
    return("Added Tweets to Elastic")
    # return u'''
    # {}
    # '''.format(input1)


if __name__ == '__main__':
    app.run_server(debug=True)

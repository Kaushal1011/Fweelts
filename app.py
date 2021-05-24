# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from twitter import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='COVID-19'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'))
def update_output(n_clicks, input1):
    tweets = search_tweets(input1)
    output = 'NEW TWEET'.join(tweet.full_text for tweet in tweets)
    # for tweet in tweets:
    #     print(tweet.text)
    return(output)
    # return u'''    
    # {}
    # '''.format(input1)


if __name__ == '__main__':
    app.run_server(debug=True)

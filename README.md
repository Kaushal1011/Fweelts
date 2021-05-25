# fweelts

## Demo video
See it in action on [YouTube](https://youtu.be/eIp2K6CeRc0)

## Inspiration
Twitter 🐦 API is a powerful resource of information 💾. We thought that Elastic search can definitely do cool stuff with this type of data. 🤓 We mixed in some of our data science knowledge and decided to create a web app that fetches sentiment and emotion-related data of tweets.

## What it does
fweelts takes a keyword from the user, fetches relevant tweets using the Twitter Search API and stores them in Elastic search. Thereafter, appropriate queries are made to elastic which are sent to pre-trained machine learning models to perform sentiment and emotional analysis. 🔎🔎

### Features
- Show the number of tweets with a particular sentiment value as well as from the English language.
- Show the number of tweets with a particular emotion value.
- Show the different sources of tweets and the distribution of tweets in the data.
- Wordcloud indicating the most common words inside tweets.

All the above features can be performed separately for tweets containing a particular keyword.

## How we built it
- We decided what stack we want to use and quickly set things up. ⛏️
- We wrote functions for Twitter API (using Tweepy) as well as Elasticsearch (using its Python API)
- We set up Dash and placed function call at relevant places.
- We spun off a FastAPI server 🏢 and configured it to execute pre-trained models from HuggingFace. 
- We set up Dash to make calls to the server and subsequently write the data back to Elastic search.
- We wrote Elastic search queries for different tasks such as aggregation and filter.
- We created various visualisations to show the results back to the user. 

## Challenges we ran into
- We had to figure out how to integrate Dash to allow using Twitter API and Elastic search.
- For machine learning models, we couldn't work with Dash alone so we quickly had to spin up a FastAPI server.
- We had to understand how to use Elasticsearch's Python wrapper. Documentation wasn't extensive here.
- We wanted to do more with aggregations and therefore had to spend a lot of time reading documentation and exploring things like an aggregation pipeline.
- Our PCs fried up with elastic, kibana, dash and FastAPI server hogged up with models running all at once. Working was painfully slow.

## Accomplishments that we're proud of
- We quickly learned so much and assembled everything in a time crunch.
- We knew nothing about elastic before, except for the fact that it's a mere buzzword. Now we're comfortable using it in any future project or work.
- We combined several technologies and got them to work together.

## What we learned
- What elastic is, its use cases, setting it up and navigating its documentation.
- How to use Dash to plot visualizations.
- How to use pre-trained models from HuggingFace and integrating them to our service.

## What's next for fweelts - Feel the tweets
- There's a lot of scope to increase the amount of visualisation that can be done. More data can be fetched from a twitter API and an enhanced schema can be created.
- Some optimization to improve the working time.
- Deploying fweelts on the web for everyone to use.

## Setup and usage
- Run Elastic locally
- Install requirements
- Run FastAPI
```bash
python3 sentimentserver/main.py
```
- Run Dash
```bash
python3 app.py
```
- Go to `localhost:8050`

Models courtesy - [Hugging Face](https://huggingface.co/)



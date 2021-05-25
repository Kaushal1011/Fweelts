from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from sentiment import emotion_classifier, sentiment_classifier,  finsent_classifier, twsent_classifier
from model import Prediction, ResponseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/emotion", response_description="Predict Emotion")
async def emotionclassifier(data: Prediction = Body(...)):
    data = jsonable_encoder(data)
    print(data["textlist"])
    return ResponseModel(emotion_classifier(data["textlist"]), "Emotion Values")


@app.post("/sentiment", response_description="Predict Sentiment")
async def sentimentclassifier(data: Prediction = Body(...)):
    data = jsonable_encoder(data)
    print(data["textlist"])
    return ResponseModel(sentiment_classifier(data["textlist"]), "Sentiment Values")


@app.post("/twsent", response_description="Predict contra")
async def twsentclassifier(data: Prediction = Body(...)):
    data = jsonable_encoder(data)
    print(data["textlist"])
    return ResponseModel(twsent_classifier(data["textlist"]), "tw sent Values")


@app.post("/finsent", response_description="Predict finsent")
async def finsentclassifier(data: Prediction = Body(...)):
    data = jsonable_encoder(data)
    print(data["textlist"])
    return ResponseModel(finsent_classifier(data["textlist"]), "Fin Sentiment Values")

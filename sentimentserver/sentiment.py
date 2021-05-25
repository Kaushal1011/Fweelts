from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Emotion model

tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")

model = AutoModelForSequenceClassification.from_pretrained(
    "nateraw/bert-base-uncased-emotion")

emotion_classifier = pipeline(
    'text-classification', model=model, tokenizer=tokenizer)

# sentiment model

tokenizer_sent = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english")

model_sent = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english")

sentiment_classifier = pipeline(
    'text-classification', model=model_sent, tokenizer=tokenizer_sent)

# Twitter sentiment

tokenizer_twsent = AutoTokenizer.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment")

model_twsent = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment")

twsent_classifier = pipeline(
    'text-classification', model=model_twsent, tokenizer=tokenizer_twsent)
# financial sentiment

tokenizer_fin = AutoTokenizer.from_pretrained("ProsusAI/finbert")

model_fin = AutoModelForSequenceClassification.from_pretrained(
    "ProsusAI/finbert")

finsent_classifier = pipeline(
    'text-classification', model=model_fin, tokenizer=tokenizer_fin)

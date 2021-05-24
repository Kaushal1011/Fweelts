from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")

model = AutoModelForSequenceClassification.from_pretrained(
    "nateraw/bert-base-uncased-emotion")

emotion_classifier = pipeline(
    'text-classification', model=model, tokenizer=tokenizer)
sentiment_classifier = pipeline('sentiment-analysis')

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion")

model = AutoModelForSequenceClassification.from_pretrained(
    "nateraw/bert-base-uncased-emotion")

classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
print(classifier('We are very happy to show you the 🤗 Transformers library.'))
print(pipeline('sentiment-analysis')(["I Like You", "I hate you"]))

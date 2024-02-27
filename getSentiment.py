import torch
from transformers import pipeline

def getSentiment(comment):
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    res = classifier(comment)

    result = res[0]['label']

    acc = res[0]['score']
    acc = float(acc)

    if acc >= .9:
        print(comment)
        print(result)
        return result
    else:
        return "Neutral"
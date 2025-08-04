from transformers import XLMRobertaTokenizer, AutoModelForSequenceClassification
from langdetect import detect
import torch
import numpy as np
import emoji

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

labels = ['Negative', 'Neutral', 'Positive']

# Language map for display
LANGUAGE_MAP = {
    "en": "English 🇬🇧",
    "hi": "Hindi 🇮🇳",
    "bn": "Bengali 🇧🇩",
    "ta": "Tamil 🇮🇳",
    "te": "Telugu 🇮🇳",
    "es": "Spanish 🇪🇸",
    "fr": "French 🇫🇷",
    "zh": "Chinese 🇨🇳",
    "ar": "Arabic 🇸🇦",
    "de": "German 🇩🇪",
    "ko": "Korean Kr" ,
    "it": "Italian",
    "ja": "Japanese"
}

def preprocess(text):
    text = emoji.demojize(text)
    return text.replace('\n', ' ').strip()

def analyze_sentiment(text):
    language_code = detect(text)
    language = LANGUAGE_MAP.get(language_code, language_code)

    text = preprocess(text)
    encoded = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        output = model(**encoded)

    scores = output.logits[0].numpy()
    probs = np.exp(scores) / np.sum(np.exp(scores))

    top = np.argmax(probs)
    return {
        "label": labels[top].upper(),
        "score": round(float(probs[top]) * 100, 2),
        "all_scores": {labels[i]: round(float(probs[i]) * 100, 2) for i in range(3)},
        "language": language
    }




"""
from transformers import XLMRobertaTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import emoji

# Use XLM-Roberta slow tokenizer
MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

labels = ['Negative', 'Neutral', 'Positive']

def preprocess(text):
    text = emoji.demojize(text)
    text = text.replace('\n', ' ').strip()
    return text

def analyze_sentiment(text):
    text = preprocess(text)
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        output = model(**inputs)

    scores = output.logits[0].numpy()
    probs = np.exp(scores) / np.sum(np.exp(scores))

    top = np.argmax(probs)
    return {
        "label": labels[top].upper(),
        "score": round(float(probs[top]) * 100, 2),
        "all_scores": {labels[i]: round(float(probs[i]) * 100, 2) for i in range(3)}
    }

"""
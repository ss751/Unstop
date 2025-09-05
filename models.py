# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    scores = outputs.logits.softmax(dim=-1).detach().numpy()[0]
    rating = (scores * range(1, 6)).sum()  # Weighted average for star rating
    sentiment = "positive" if rating >= 3 else "negative"
    return {"rating": rating, "sentiment": sentiment}

def cal_urgency(subject, body):
    urgency_weights = {
    "instantly": 0,
    "immediate": 1,
    "critical": 2,
    "essential": 4,
    "urgent": 2,
    }   
    sub_urg = 6
    for i in urgency_weights:
        if i in subject.lower():
            sub_urg = min(sub_urg, urgency_weights[i])

    body_sent = analyze_sentiment(body)
    urgency = sub_urg + body_sent['rating']
    return urgency


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: list[str]


positive_words = {
    "love", "loved", "like", "liked", "great", "good", "excellent",
    "amazing", "awesome", "wonderful", "fantastic", "happy", "joy",
    "joyful", "best", "perfect", "nice", "enjoy", "enjoyed",
    "beautiful", "brilliant", "success", "successful", "win", "won",
    "helpful", "excited", "thank", "thanks", "thankful", "pleased"
}

negative_words = {
    "hate", "hated", "dislike", "disliked", "bad", "terrible",
    "awful", "horrible", "worst", "sad", "angry", "anger", "poor",
    "failed", "failure", "fail", "problem", "problems", "wrong",
    "broken", "disappointed", "disappointing", "annoying", "annoyed",
    "pain", "painful", "unhappy", "difficult", "disaster", "boring"
}


def classify_sentiment(sentence: str) -> str:
    words = (
        sentence.lower()
        .replace("!", " ")
        .replace("?", " ")
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )

    positive_score = sum(word in positive_words for word in words)
    negative_score = sum(word in negative_words for word in words)

    text = sentence.lower()

    if "not good" in text or "not great" in text or "not happy" in text:
        negative_score += 1

    if "not bad" in text or "not terrible" in text or "not horrible" in text:
        positive_score += 1

    if positive_score > negative_score:
        return "happy"
    elif negative_score > positive_score:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
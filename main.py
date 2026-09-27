from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

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
    "love", "loved", "loving",
    "like", "liked", "likes", "liking",
    "great", "good", "better", "best",
    "excellent", "amazing", "awesome", "wonderful",
    "fantastic", "fabulous", "brilliant", "perfect",
    "happy", "happier", "happiness",
    "joy", "joyful", "excited", "exciting",
    "pleased", "pleasant", "satisfied",
    "enjoy", "enjoyed", "enjoying",
    "beautiful", "helpful", "useful",
    "success", "successful", "win", "won", "winning",
    "celebrate", "celebration",
    "thank", "thanks", "thankful", "grateful",
    "impressed", "impressive",
    "recommend", "recommended",
    "fun", "funny", "delightful",
    "positive", "wonderful", "nice",
    "easy", "easier", "smooth",
    "thrilled", "glad", "hopeful",
    "calm", "peaceful", "comfortable",
    "loveable", "lovely"
}

negative_words = {
    "hate", "hated", "hating",
    "dislike", "disliked", "disliking",
    "bad", "worse", "worst",
    "terrible", "awful", "horrible",
    "sad", "sadder", "sadness",
    "angry", "anger", "mad",
    "poor", "failed", "failure", "fail",
    "problem", "problems", "wrong",
    "broken", "disappointed", "disappointing",
    "annoying", "annoyed", "annoyance",
    "pain", "painful",
    "unhappy", "unpleasant",
    "difficult", "hard",
    "disaster", "boring", "bored",
    "frustrated", "frustrating", "frustration",
    "upset", "worried", "worry",
    "fear", "afraid", "scared",
    "horrible", "disgusting", "disgusted",
    "useless", "waste", "wasted",
    "complaint", "complain",
    "regret", "regretful",
    "negative", "dislike",
    "broken", "crash", "crashed",
    "late", "delay", "delayed"
}


positive_phrases = {
    "very good",
    "really good",
    "very happy",
    "really happy",
    "very pleased",
    "really pleased",
    "highly recommend",
    "love this",
    "love it",
    "works great",
    "works perfectly",
    "great job",
    "well done",
    "so good",
    "so happy",
    "feels great",
    "feel great",
    "made my day"
}

negative_phrases = {
    "very bad",
    "really bad",
    "very sad",
    "really sad",
    "very disappointed",
    "really disappointed",
    "very unhappy",
    "really unhappy",
    "hate this",
    "hate it",
    "not good",
    "not great",
    "not happy",
    "not satisfied",
    "does not work",
    "doesn't work",
    "did not work",
    "didn't work",
    "worst ever",
    "terrible experience",
    "horrible experience",
    "waste of money",
    "fed up",
    "let down",
    "feel terrible",
    "feels terrible"
}


def classify_sentiment(sentence: str) -> str:
    text = sentence.lower().strip()
    words = re.findall(r"[a-z']+", text)

    positive_score = 0
    negative_score = 0

    # Phrase scoring
    for phrase in positive_phrases:
        if phrase in text:
            positive_score += 2

    for phrase in negative_phrases:
        if phrase in text:
            negative_score += 2

    # Individual word scoring
    for word in words:
        if word in positive_words:
            positive_score += 1

        if word in negative_words:
            negative_score += 1

    # Handle negation of positive/negative words.
    negations = {"not", "no", "never", "n't"}

    for i, word in enumerate(words):
        if word in positive_words:
            previous = words[max(0, i - 3):i]
            if any(n in previous for n in negations):
                positive_score -= 2
                negative_score += 2

        if word in negative_words:
            previous = words[max(0, i - 3):i]
            if any(n in previous for n in negations):
                negative_score -= 2
                positive_score += 2

    if positive_score > negative_score:
        return "happy"

    if negative_score > positive_score:
        return "sad"

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

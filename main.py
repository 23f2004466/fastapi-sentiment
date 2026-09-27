from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: list[str]


@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        scores = analyzer.polarity_scores(sentence)
        compound = scores["compound"]

        if compound >= 0.05:
            label = "happy"
        elif compound <= -0.05:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}

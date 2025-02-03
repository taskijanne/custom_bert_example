# main.py
import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load environment variables from .env file
load_dotenv()

# API key from environment
API_KEY = os.getenv("APIKEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  

translate_prompt = "Translate the following text to Finnish:"
analyze_prompt = """Analyze the sentiment of the following text. Always return EITHER 'positive' OR 'negative'  
                    AND a real number between 0 and 1 Of HOW CONFIDENT YOU ARE with your response (0 = not condident at all, 1 = very condident). 
                    If you are able to analyze the text, return the sentiment and the confidence separated with blank space, DO NOT use commas or other separators than blank space.
                    If you are unable to analyze, just return value -1 WITH NO explanation. 
                    Here is a text to analyze:"""

# FastAPI app initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = AutoTokenizer.from_pretrained("jannetas/distilbert-imdb")
model = AutoModelForSequenceClassification.from_pretrained("jannetas/distilbert-imdb")

class Model(Enum):
    CUSTOM = "custom"
    LLAMA = "llama"

class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

# Pydantic model for input data
class TranslationRequest(BaseModel):
    text: str


class AnalyzeRequest(BaseModel):
    text: str
    model: Model

class AnalyzeResponse():
    def __init__(self, sentiment: Sentiment, score: float):
        self.sentiment = sentiment
        self.confidence = score


def analyze_with_custom_model(text: str) -> AnalyzeResponse:
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).tolist()[0]
    print(f"Probs: {probs}")
    sentiment = Sentiment.POSITIVE if probs[1] > probs[0] else Sentiment.NEGATIVE
    confidence = round(max(probs),2)
    return AnalyzeResponse(sentiment, confidence)

def make_groq_request(text: str, prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
    }
    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    return response

# Function to call the Groq API for translation
def translate_text(text: str) -> str:

    response = make_groq_request(text, translate_prompt)
    
    if response.status_code == 200:
        return response.json().get("choices")[0].get("message").get("content")
    else:
        raise HTTPException(status_code=response.status_code, detail="Translation failed")
    
# Function to call the Groq API for sentiment analysis
def analyze_text(text: str, model: Model) -> AnalyzeResponse:

    if model == Model.CUSTOM:
        try:   
            result = analyze_with_custom_model(text)
            return result
        except:
            raise HTTPException(status_code=500, detail="Something went wrong with custom model")
    else:
        response = make_groq_request(text, analyze_prompt)

        if response.status_code == 200:
            result = response.json().get("choices")[0].get("message").get("content")
            if result == "-1":
                return AnalyzeResponse(None, -1)
            try:    
                print(result)
                result = result.split(" ")
                sentiment = Sentiment(result[0])
                score = float(result[1])
                return AnalyzeResponse(sentiment, score)
            except:
                raise HTTPException(status_code=500, detail="Error parsing sentiment analysis result")
        else:
            raise HTTPException(status_code=response.status_code, detail="Translation failed")

# FastAPI endpoint for translation
@app.post("/translate/")
async def translate(request: TranslationRequest):
    translated_text = translate_text(request.text)
    return {"original_text": request.text, "translated_text": translated_text}

@app.post("/analyze/")
async def analyze(request: AnalyzeRequest):
    result = analyze_text(request.text, request.model)
    return {"text": request.text, "sentiment": result.sentiment, "confidence": result.confidence}

# To run the FastAPI server with: uvicorn main:app --reload
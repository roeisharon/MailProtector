from fastapi import FastAPI
from models.request_models import EmailRequest
from scoring.scoring_engine import analyze_email

app = FastAPI()

# Endpoint to analyze incoming email
@app.post("/analyze")
async def analyze(email: EmailRequest):
    result = analyze_email(email)
    return result
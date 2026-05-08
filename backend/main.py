from fastapi import FastAPI
from utils.logger import logger
from models.request_models import EmailRequest
from scoring.scoring_engine import analyze_email

app = FastAPI()

# Endpoint to analyze incoming email
@app.post("/analyze")
async def analyze(email: EmailRequest):
    try:
        result = analyze_email(email)
        return result
    
    except Exception as e:
        logger.exception(f"Error occurred while analyzing email: {e}")
        # Return a structured error response
        return {
            "score": 0,
            "verdict": "Error",
            "reasons": [f"An error occurred during analysis: {str(e)}"],
            "llm_summary": "An error occurred while generating the summary."
        }

# Health check endpoint    
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "service": "MailProtector API",
        "status": "running"
    }
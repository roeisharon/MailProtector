from pydantic import BaseModel

# Response model for email analysis results
class AnalysisResult(BaseModel):
    score: int
    verdict: str
    reasons: list[str]
    llm_summary: str
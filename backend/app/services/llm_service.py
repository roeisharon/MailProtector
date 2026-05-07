import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_summary(body: str, findings: list[str], score: int, verdict: str) -> str:
    prompt = f"""
    You are an email security assistant.
    Analyze the following email content and provide a concise, user-friendly explanation and
    summary of its content, highlighting any potential security concerns.

    Detection results:
    - Risk Score: {score}/100
    - Verdict: {verdict}

    Detected Findings:
    {chr(10).join(f"- {finding}" for finding in findings) if findings else "- No suspicious findings detected"}

    Guidelines:
    - Align your explanation with the detected findings.
    - Do not exaggerate or overstate certainty.
    - If no major suspicious indicators were detected, clearly communicate that the email appears routine or low-risk.
    - Mention suspicious indicators only if they were actually detected.
    - Keep the response concise and non-technical.
    - Avoid fear-inducing language.

    Limit the response to 3-5 concise sentences.
    Do not definitively classify the email as malicious.
    Focus only on characteristics supported by the detected findings and email content.
    The summary should help users quickly understand the potential risks associated with the email.
    Email Content:
    {body}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            #timeout=10
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM error: {e}")
        return ("AI-generated explanation is currently unavailable. "
                "The verdict and findings are still based on the deterministic security analyzers.")
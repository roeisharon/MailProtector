# Gmail Add-on — Malicious Email Scorer

## Project Vision

This project is an explainable email security assistant built as a Gmail Add-on.

The system analyzes opened emails and produces:

- A maliciousness score
- A clear verdict
- Explainable findings
- AI-assisted semantic explanations
- Security recommendations

The project is intentionally designed as a realistic MVP that prioritizes:

- Explainability
- Security awareness
- Product thinking
- Clean architecture
- Reliable deployment
- Engineering judgment

Rather than attempting to build a full enterprise-grade phishing detection platform, the focus is on building a strong, realistic, explainable security assistant within a constrained timeline.

---

# Core Product Philosophy

The system intentionally combines:

- Deterministic heuristic-based security analysis
- Real email authentication signals
- AI-assisted semantic reasoning

The LLM is intentionally NOT the primary decision-maker.

Instead:

## Deterministic systems decide:

- Risk score
- Final verdict
- Security findings

## The LLM assists with:

- Semantic understanding
- Human-readable explanations
- Suspicious language interpretation
- User-facing summaries

This design improves:

- Explainability
- Reliability
- Predictability
- Trustworthiness

---

# Final System Architecture

```text
Gmail Add-on (Apps Script)
        |
        | HTTPS
        v
FastAPI Backend
        |
        +--> Header Analyzer
        |      ├ SPF
        |      ├ DKIM
        |      └ DMARC
        |
        +--> URL Analyzer
        |      ├ Suspicious domains
        |      ├ URL heuristics
        |      └ Google Safe Browsing
        |
        +--> Language Analyzer
        |      ├ Urgency
        |      ├ Threat language
        |      └ LLM explanation
        |
        +--> Attachment Analyzer
        |
        +--> Scoring Engine
```

---

# User Experience

Example output shown to the user:

```text
Risk Score: 82/100
Verdict: Likely Phishing

Reasons:
⚠ SPF validation failed
⚠ Suspicious shortened URL
⚠ Urgent language detected
⚠ Dangerous attachment type

LLM Summary:
"This email pressures the recipient into immediate action
while using suspicious sender verification patterns."
```

---

# Technology Stack

## Frontend / Add-on

- Google Apps Script
- Gmail Add-on APIs
- CardService UI

## Backend

- Python
- FastAPI
- Pydantic
- Requests
- OpenAI SDK

## External Services

- Google Safe Browsing API
- OpenAI API

## Deployment

- Render (recommended for MVP)

---

# Repository Structure

```text
malicious-email-scorer/
│
├── backend/
│
├── addon/
│
├── docs/
│
├── examples/
│
└── README.md
```

---

# Backend Structure

```text
backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── analyzers/
│   │   ├── header_analyzer.py
│   │   ├── url_analyzer.py
│   │   ├── language_analyzer.py
│   │   └── attachment_analyzer.py
│   │
│   ├── services/
│   │   ├── safe_browsing_service.py
│   │   └── llm_service.py
│   │
│   ├── scoring/
│   │   └── scoring_engine.py
│   │
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   └── utils/
│       ├── regex_utils.py
│       └── sanitization.py
│
├── requirements.txt
├── .env
└── .gitignore
```

---

# Add-on Structure

```text
addon/
│
├── Code.gs
├── UI.gs
└── appsscript.json
```

---

# What Each File Does

## Backend

| File | Responsibility |
|---|---|
| main.py | FastAPI entrypoint |
| header_analyzer.py | SPF/DKIM/DMARC analysis |
| url_analyzer.py | URL extraction and URL heuristics |
| language_analyzer.py | urgency/threat language detection |
| attachment_analyzer.py | dangerous attachment metadata analysis |
| llm_service.py | semantic phishing explanation generation |
| scoring_engine.py | final risk scoring logic |
| request_models.py | request schemas |
| response_models.py | response schemas |
| sanitization.py | input cleaning and sanitization |

## Add-on

| File | Responsibility |
|---|---|
| Code.gs | receives email and calls backend |
| UI.gs | builds Gmail Add-on UI cards |
| appsscript.json | permissions and Gmail scopes |

---

# Security Learning Section

Before implementation, it is important to understand core email security concepts.

---

# SPF

## What It Solves

SPF helps prevent sender spoofing.

It allows domain owners to define:

```text
Which mail servers are allowed to send emails for this domain.
```

## Learn About

- DNS
- TXT records
- Spoofing
- Mail servers

## Recommended Reading

Search:

```text
Cloudflare SPF explained
```

---

# DKIM

## What It Solves

DKIM cryptographically signs emails to ensure:

- The email was not modified
- The sender is authentic

## Learn About

- Public/private keys
- Digital signatures
- Email tampering

## Recommended Reading

Search:

```text
Cloudflare DKIM explained
```

---

# DMARC

## What It Solves

DMARC defines policies for handling failed SPF/DKIM checks.

## Learn About

- Email trust
- Policy enforcement
- Email authentication

## Recommended Reading

Search:

```text
Cloudflare DMARC explained
```

---

# Phishing Techniques

## Learn About

- Typo squatting
- Display-name spoofing
- Urgency manipulation
- Fake login pages
- Shortened URLs
- Punycode attacks

## Recommended Reading

Search:

```text
Google phishing protection guide
```

---

# 4-Day Development Plan

---

# Day 1 — Infrastructure & Pipeline

## Goal

By the end of Day 1:

- Gmail Add-on appears inside Gmail
- Backend runs locally
- Add-on successfully sends email data to backend
- Backend responds successfully

---

## Step 1 — Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## requirements.txt

```txt
fastapi
uvicorn
python-dotenv
requests
pydantic
openai
tldextract
```

---

## main.py

### Responsibility

- Receive email data
- Trigger analyzers
- Return final analysis

### Skeleton

```python
from fastapi import FastAPI
from models.request_models import EmailRequest
from scoring.scoring_engine import analyze_email

app = FastAPI()

@app.post("/analyze")
async def analyze(email: EmailRequest):
    result = analyze_email(email)
    return result
```

---

## request_models.py

```python
from pydantic import BaseModel

class EmailRequest(BaseModel):
    subject: str
    sender: str
    body: str
    headers: str
    attachments: list[str] = []
```

---

## response_models.py

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    score: int
    verdict: str
    reasons: list[str]
    llm_summary: str
```

---

# Step 2 — Gmail Add-on Setup

## Learn First

Search:

```text
Google Apps Script Gmail Add-on tutorial
```

---

## Code.gs

### Responsibility

- Access currently opened email
- Extract data
- Send backend request

### Skeleton

```javascript
function getContextualAddOn(e) {
  const accessToken = e.gmail.accessToken;
  GmailApp.setCurrentMessageAccessToken(accessToken);

  const message = GmailApp.getMessageById(e.gmail.messageId);

  const payload = {
    subject: message.getSubject(),
    sender: message.getFrom(),
    body: message.getPlainBody(),
    headers: message.getRawContent()
  };

  const response = UrlFetchApp.fetch(
    "YOUR_BACKEND_URL/analyze",
    {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload)
    }
  );

  const result = JSON.parse(response.getContentText());

  return buildResultCard(result);
}
```

---

## UI.gs

### Responsibility

- Build Gmail card UI
- Display score/verdict/findings

### Skeleton

```javascript
function buildResultCard(result) {

  const section =
    CardService.newCardSection()
      .addWidget(
        CardService.newTextParagraph()
          .setText(
            `<b>Risk Score:</b> ${result.score}/100`
          )
      );

  const card =
    CardService.newCardBuilder()
      .addSection(section)
      .build();

  return card;
}
```

---

## appsscript.json

```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

---

# Checkpoint — End of Day 1

You should now have:

- Real Gmail integration
- Working backend communication
- Distributed architecture
- Deployable MVP foundation

---

# Day 2 — Intelligence Layer

## Goal

By the end of Day 2:

- URLs are analyzed
- SPF/DKIM are analyzed
- Suspicious language is detected
- LLM explanations work
- Risk score is generated

---

# URL Analyzer

## Responsibility

- Extract URLs
- Analyze suspicious domains
- Use Google Safe Browsing

## Learn First

Search:

```text
Google Safe Browsing API tutorial
```

---

## url_analyzer.py

```python
import re

def analyze_urls(body: str):

    findings = []

    urls = re.findall(r'https?://\S+', body)

    for url in urls:

        if "bit.ly" in url:
            findings.append(
                "Shortened URL detected"
            )

    return findings
```

---

# Header Analyzer

## Responsibility

Analyze:

- SPF
- DKIM
- DMARC
- Sender mismatches

## Learn First

Open Gmail:

```text
Show Original
```

Study real headers.

---

## header_analyzer.py

```python
def analyze_headers(headers: str):

    findings = []

    lower_headers = headers.lower()

    if "spf=fail" in lower_headers:
        findings.append(
            "SPF validation failed"
        )

    if "dkim=fail" in lower_headers:
        findings.append(
            "DKIM validation failed"
        )

    return findings
```

---

# Language Analyzer

## Responsibility

Detect:

- Urgency
- Threat language
- Manipulation patterns

Also:

- Trigger LLM explanation layer

---

## language_analyzer.py

```python
SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify immediately",
    "account suspended",
    "click below"
]

def analyze_language(body: str):

    findings = []

    lower_body = body.lower()

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in lower_body:
            findings.append(
                f"Suspicious phrase detected: {keyword}"
            )

    return findings
```

---

# LLM Service

## Responsibility

Generate:

- Human-readable phishing explanation
- Semantic reasoning
- Suspicious intent summary

NOT:

- Final score
- Final verdict

---

## Important Design Decision

The LLM augments the deterministic engine.

It does not replace it.

---

## llm_service.py

```python
from openai import OpenAI

client = OpenAI()

def generate_summary(body: str):

    prompt = f"""
    Analyze this email for phishing indicators.
    Focus on urgency, manipulation,
    suspicious requests, and tone.

    Email:
    {body}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
```

---

# Attachment Analyzer

## Responsibility

Analyze attachment metadata ONLY.

Never execute files.

---

## attachment_analyzer.py

```python
DANGEROUS_EXTENSIONS = [
    ".exe",
    ".scr",
    ".bat",
    ".zip"
]

def analyze_attachments(attachments):

    findings = []

    for file in attachments:

        for ext in DANGEROUS_EXTENSIONS:

            if file.endswith(ext):

                findings.append(
                    f"Dangerous attachment type: {ext}"
                )

    return findings
```

---

# Scoring Engine

## Responsibility

Combine:

- Findings
- Heuristics
- LLM explanation

Into:

- Score
- Verdict
- Recommendations

---

## scoring_engine.py

```python
from analyzers.url_analyzer import analyze_urls
from analyzers.header_analyzer import analyze_headers
from analyzers.language_analyzer import analyze_language
from analyzers.attachment_analyzer import analyze_attachments

from services.llm_service import generate_summary

def analyze_email(email):

    findings = []

    findings += analyze_urls(email.body)
    findings += analyze_headers(email.headers)
    findings += analyze_language(email.body)
    findings += analyze_attachments(email.attachments)

    score = 0

    for finding in findings:

        if "failed" in finding.lower():
            score += 30

        elif "dangerous" in finding.lower():
            score += 40

        else:
            score += 10

    score = min(score, 100)

    verdict = "Safe"

    if score > 60:
        verdict = "Likely Phishing"

    elif score > 25:
        verdict = "Suspicious"

    llm_summary = generate_summary(email.body)

    return {
        "score": score,
        "verdict": verdict,
        "reasons": findings,
        "llm_summary": llm_summary
    }
```

---

# Checkpoint — End of Day 2

You should now have:

- Multi-signal phishing analysis
- Deterministic scoring
- LLM semantic reasoning
- Explainable findings
- Working maliciousness engine

---

# Day 3 — UI, Security & Deployment

## Goal

By the end of Day 3:

- UI is polished
- Backend is deployed
- Security improvements are added
- Demo is stable

---

# UI Improvements

Add:

- Color coding
- Verdict section
- Findings list
- Recommendations
- LLM summary section

---

# Security Hardening

## Learn First

Search:

```text
OWASP input validation
```

---

## Add

### Sanitization

Create:

```text
utils/sanitization.py
```

Responsibilities:

- Clean HTML
- Remove suspicious scripts
- Normalize untrusted input

---

## Environment Variables

Use:

```text
.env
```

Example:

```text
OPENAI_API_KEY=...
SAFE_BROWSING_API_KEY=...
```

Never hardcode secrets.

---

## Logging

Add structured logs for:

- Requests
- Findings
- Errors
- API failures

---

## Gmail Scopes

Use minimum required scopes only.

---

# Deployment

## Recommended Platform

Render

## Learn First

Search:

```text
Deploy FastAPI on Render
```

---

# Checkpoint — End of Day 3

You should now have:

- Real deployable product
- Security-aware implementation
- Stable Gmail Add-on
- LLM-assisted phishing explanations
- Demo-ready system

---

# Day 4 — README, Presentation & Interview

---

# README Sections

## 1. Problem Statement

## 2. Product Vision

## 3. Architecture

## 4. Detection Signals

## 5. LLM Layer

## 6. Security Decisions

## 7. Trade-offs

## 8. Future Work

## 9. Setup Instructions

---

# Presentation Structure

| Slide | Topic |
|---|---|
| 1 | Problem |
| 2 | Product Overview |
| 3 | Architecture |
| 4 | Detection Signals |
| 5 | LLM Layer |
| 6 | Demo |
| 7 | Security Decisions |
| 8 | Trade-offs |
| 9 | Future Work |

---

# Demo Plan

Prepare:

## 1. Safe Email

## 2. Obvious Phishing Email

## 3. Suspicious Gray-Area Email

This demonstrates:

- False positives awareness
- Security maturity
- Product thinking

---

# Trade-offs To Explain In Interview

## Why FastAPI?

Rapid development, strong typing, clean APIs.

---

## Why deterministic scoring?

Explainability and predictability.

---

## Why not fully trust the LLM?

LLMs may hallucinate or behave inconsistently.

---

## Why backend instead of Apps Script only?

Scalability, flexibility, security separation.

---

## Privacy Considerations

- Avoid sending unnecessary PII
- Sanitize inputs
- Do not store emails persistently

---

# Future Work

---

# 1. Attachment Sandboxing

Run suspicious attachments in isolated environments for dynamic malware analysis.

---

# 2. Organization-wide Intelligence

If one user flags a sender as malicious, increase sender risk reputation across the organization.

---

# 3. Graph Analysis

Analyze communication relationships:

- Is this a known sender?
- Is this communication pattern unusual?
- Is the sender interacting with the organization for the first time?

---

# 4. Performance Optimization

Add caching layers for:

- URL scans
- Domain reputation
- Sender analysis

Possible technologies:

- Redis
- In-memory cache
- TTL-based caching

---

# 5. ML-Augmented Detection

Future versions could combine:

- Heuristics
- Behavioral analysis
- Supervised ML models

Potential directions:

- XGBoost
- Transformer classifiers
- Threat intelligence feeds
- Communication anomaly detection

---

# Final Interview Narrative

```text
I designed an explainable phishing analysis assistant
that combines deterministic security heuristics
with AI-assisted semantic reasoning.

The system prioritizes transparency,
security awareness, and realistic deployment constraints.
```

---

# Final Priority Order

## 1. Demo reliability

MOST IMPORTANT.

---

## 2. Clean architecture

---

## 3. Explainability

---

## 4. Security awareness

---

## 5. Fancy features

LAST.

---

# Final Goal

At the end of the project, you should be able to:

- Demonstrate a real Gmail Add-on
- Explain the architecture confidently
- Discuss security trade-offs
- Explain deterministic scoring decisions
- Explain the role of the LLM layer
- Discuss future scalability directions
- Present the system as a realistic MVP security product


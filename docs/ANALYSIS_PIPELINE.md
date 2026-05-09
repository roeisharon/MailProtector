# Analysis Pipeline

[← Back to Main README](../README.md)

---

# Overview

This document describes the runtime lifecycle of an email analysis request inside MailProtector.

The pipeline processes an opened Gmail email through multiple preprocessing, analysis, scoring, and explanation stages before returning a final verdict to the Gmail Add-on.

---

# High-Level Runtime Flow

```text
User Opens Gmail Email
            ↓
Gmail Add-on Extracts Email Data
            ↓
HTTPS Request Sent to Backend
            ↓
Input Sanitization
            ↓
Language Normalization
            ↓
Security Analyzer Pipeline
            ↓
Scoring Engine
            ↓
LLM Explanation Generation
            ↓
Structured JSON Response
            ↓
Verdict Rendered Inside Gmail
```

---

# Step 1 — Email Extraction

The analysis lifecycle begins when the user opens an email inside Gmail.

The Gmail Add-on extracts:

* Subject
* Sender
* Email body
* Email headers
* Attachment names

The extracted data is prepared for backend analysis.

---

# Step 2 — Backend Request

The Add-on sends the extracted email data to the FastAPI backend using an HTTPS POST request.

Example request structure:

```json
{
  "subject": "Immediate Account Verification Required",
  "sender": "security-alerts@gmail.com",
  "body": "Your account access will be suspended...",
  "headers": "spf=fail dkim=fail dmarc=fail",
  "attachments": [
    "secure_verification_form.zip",
    "account_update.docm"
  ]
}
```

The backend validates the request structure using Pydantic models before processing begins.

---

# Step 3 — Input Sanitization

Before analysis begins, the backend sanitizes the email body.

The sanitization stage removes:

* Null bytes
* HTML tags
* Excessive noise
* Oversized content

The body is also truncated to a controlled maximum length.

This preprocessing stage improves analyzer consistency and reduces parsing noise.

---

# Step 4 — Language Normalization

After sanitization, the backend normalizes the email body.

Normalization includes:

* Lowercasing text
* Character substitutions
* Removing special characters
* Whitespace normalization

Example substitutions:

```text
0 → o
1 → i
3 → e
@ → a
```

This improves resilience against simple phishing obfuscation techniques such as:

```text
v3rify y0ur acc0unt
```

---

# Step 5 — Analyzer Execution

Once preprocessing completes, the analyzer pipeline begins.

```text
Sanitized Email
       ↓
Header Analyzer
       ↓
URL Analyzer
       ↓
Attachment Analyzer
       ↓
Language Analyzer
```

Each analyzer contributes findings independently into a shared findings collection.

---

# Step 6 — Findings Aggregation

After analyzer execution completes:

* Findings are aggregated
* Duplicate findings are removed
* Findings are prepared for scoring

This prevents repeated signals from artificially inflating the final score.

---

# Step 7 — Scoring

The scoring engine evaluates the aggregated findings using predefined weighted rules.

Example scoring categories:

```text
SPF failure → High weight
Suspicious TLD → Medium weight
Urgency wording → Lower weight
```

The final score is mapped into verdict levels:

* Safe
* Low Risk
* Suspicious
* High Risk
* Likely Phishing

---

# Step 8 — LLM Explanation Generation

After scoring completes, the backend generates a concise AI-assisted explanation.

The LLM receives:

* Deterministic findings
* Final score
* Verdict
* Email metadata
* Sanitized email body

The LLM generates:

* User-friendly explanations
* Lightweight semantic context
* Concise verdict summaries

Prompt injection protections are enforced throughout this stage.

---

# Step 9 — Response Construction

The backend constructs a structured JSON response.

Example response:

```json
{
  "score": 85,
  "verdict": "Likely Phishing",
  "reasons": [
    "SPF validation failed",
    "Shortened URL detected",
    "Suspicious attachment filename detected"
  ],
  "llm_summary": "The email contains several suspicious indicators..."
}
```

---

# Step 10 — Gmail Rendering

The Gmail Add-on receives the backend response and renders the results directly inside Gmail.

Displayed information includes:

* Risk score
* Verdict
* Findings list
* AI-generated explanation

The UI intentionally prioritizes readability and quick interpretation.

---

# Error Handling

The backend includes defensive error handling across the pipeline.

Examples include:

* External API timeout handling
* Safe Browsing lookup failures
* LLM generation failures
* Malformed request handling

Whenever possible, the system fails safely while still returning partial analysis results.

For example:

* If Safe Browsing fails, heuristic URL analysis still continues
* If the LLM fails, deterministic findings and verdicts are still returned

---

# Runtime Design Decisions

## Deterministic Analysis Before LLM

Deterministic analyzers execute before the LLM layer to preserve explainability and predictable scoring behavior.

---

## Lightweight Preprocessing

Sanitization and normalization improve signal quality while keeping processing efficient.

---

## Explainable Results

The pipeline intentionally exposes findings and reasoning instead of relying on opaque classifications.

---

## Defensive Processing

All email content is treated as untrusted input throughout the analysis lifecycle.

# MailProtector

AI-assisted Gmail Add-on for explainable phishing and malicious email detection.

MailProtector is a Gmail Add-on that analyzes opened emails and provides a clear maliciousness assessment directly inside Gmail.
The system combines deterministic security analyzers with lightweight LLM-assisted semantic analysis to generate transparent, explainable verdicts for potentially suspicious emails.

---

# Problem & Motivation

Email phishing and social engineering attacks often rely on a combination of weak signals rather than a single obvious indicator.
Suspicious links, spoofed sender identities, manipulative language, malicious attachments, and deceptive formatting may each appear harmless individually, but become risky when combined together.

MailProtector was designed to provide:

* Lightweight email security analysis directly inside Gmail
* Explainable verdicts
* Fast and modular analysis architecture
* Human-readable reasoning for detected risks
* A security-oriented backend that treats all email content as untrusted input

Instead of automatically blocking emails or making irreversible decisions, the system focuses on helping users understand why an email may be suspicious.

---

# Solution Overview

The system consists of two main components:

1. A Gmail Add-on built using Google Apps Script and Gmail Workspace APIs
2. A FastAPI backend responsible for email analysis, scoring, and explanation generation

The Gmail Add-on extracts the currently opened email, sends it to the backend for analysis, and displays the final risk score, verdict, findings, and AI-generated explanation directly inside Gmail.

```text
Gmail Add-on
       ↓
FastAPI Backend
       ↓
Security Analyzers
       ↓
Scoring Engine
       ↓
LLM-Assisted Explanation
       ↓
Verdict Displayed Inside Gmail
```

---

# Key Features

* Gmail contextual Add-on integrated directly into Gmail
* Real-time maliciousness scoring
* SPF / DKIM / DMARC validation analysis
* Suspicious URL and domain heuristics
* Google Safe Browsing integration
* Attachment risk analysis
* LLM-assisted semantic phishing analysis
* Explainable verdict generation
* Modular analyzer-based backend architecture
* Security-oriented handling of untrusted input

---

# Screenshots

## Safe Email Analysis

![Safe Email Analysis](screenshots/safe-example.png)

---

## Suspicious Email Analysis

![Suspicious Email Analysis](screenshots/sus-example.png)

---

## Likely Phishing Analysis

![Phishing Email Analysis](screenshots/phishing-example.png)

---

# System Architecture

The backend is structured as a modular analysis pipeline where each analyzer is responsible for a dedicated security domain.

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
        |      ├ Urgency detection
        |      ├ Credential theft patterns
        |      └ Financial pressure indicators
        |
        +--> Attachment Analyzer
        |
        +--> Scoring Engine
        |
        +--> LLM Explanation Layer
```

Additional architecture details:

[Architecture Documentation](docs/ARCHITECTURE.md)

---

# Email Analysis Lifecycle

High-level analysis flow:

1. The user opens an email inside Gmail
2. The Add-on extracts email metadata and content
3. The backend sanitizes and validates the request
4. Multiple analyzers inspect headers, URLs, language patterns, and attachments
5. The scoring engine calculates a final risk score
6. An LLM generates a concise explanation layer
7. The final verdict is displayed inside Gmail

Detailed technical walkthrough:

[Analysis Pipeline](docs/ANALYSIS_PIPELINE.md)

---

# Quick Start

## Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

## Gmail Add-on

The Gmail Add-on requires manual setup inside Google Apps Script.

Full setup instructions:

[Local Setup Guide](docs/LOCAL_SETUP.md)

---

# Repository Documentation

| Document                                           | Description                                       |
| -------------------------------------------------- | ------------------------------------------------- |
| [Local Setup](docs/LOCAL_SETUP.md)                 | Full Gmail Add-on and backend setup               |
| [Architecture](docs/ARCHITECTURE.md)               | System design, analyzers, and backend structure   |
| [Analysis Pipeline](docs/ANALYSIS_PIPELINE.md)     | End-to-end email analysis lifecycle               |
| [Security Decisions](docs/SECURITY_DECISIONS.md)   | Security considerations and engineering tradeoffs |
| [Future Improvements](docs/FUTURE_IMPROVEMENTS.md) | Scalability ideas and future extensions           |

---

# Security & Engineering Decisions

The project intentionally prioritizes explainability and modular analysis over opaque black-box classification approaches.

Several engineering tradeoffs were made during development, including:

* Combining deterministic analyzers with lightweight LLM-assisted reasoning
* Favoring transparent rule-based scoring over autonomous classification
* Treating all email content as untrusted input
* Applying prompt injection-aware constraints to the LLM explanation layer 
* Isolating analyzers into independent modules
* Failing safely when external security APIs are unavailable

Additional security considerations and architectural tradeoffs:

[Security Decisions](docs/SECURITY_DECISIONS.md)

---

# Future Improvements

Potential future improvements include:

* Historical sender and domain reputation tracking
* Attachment sandboxing and recursive archive scanning
* Organization-wide threat intelligence and shared signals
* ML-assisted detection models
* Production optimization and scalability
* Expanded user interface and experience

Additional scalability and product-extension ideas:

[Future Improvements](docs/FUTURE_IMPROVEMENTS.md)

---

# Closing Notes

This project was designed as a lightweight, explainable email security assistant focused on balancing usability, security awareness, and transparent reasoning.

The implementation intentionally prioritizes modularity, clarity, and security-oriented engineering decisions over feature completeness or fully autonomous threat classification.

The solution is deployable to a real Gmail account and was designed to support live demonstration scenarios.

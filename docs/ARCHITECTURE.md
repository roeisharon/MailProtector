# Architecture

[← Back to Main README](../README.md)

---

# High-Level System Overview

MailProtector is designed as a lightweight modular email analysis platform composed of two primary layers:

1. A Gmail Add-on integrated directly into Gmail using Google Apps Script
2. A FastAPI backend responsible for analysis, scoring, and explanation generation

The system combines deterministic security analyzers with lightweight LLM-assisted semantic reasoning to produce explainable maliciousness verdicts directly inside Gmail.

```text
Gmail Add-on
       ↓
FastAPI Backend
       ↓
Security Analyzers
       ↓
Scoring Engine
       ↓
LLM Explanation Layer
       ↓
Verdict Returned to Gmail
```

The architecture intentionally prioritizes modularity, explainability, and clear separation of responsibilities.

---

# System Components

## Gmail Add-on Layer

The Gmail Add-on acts as the user-facing interface of the system.

Responsibilities include:

* Detecting the currently opened Gmail message
* Extracting email metadata and content
* Sending analysis requests to the backend
* Rendering verdicts and findings inside Gmail

The Add-on is intentionally lightweight and delegates all security analysis logic to the backend service.

Technologies used:

* Google Apps Script
* Gmail Workspace Add-on APIs
* CardService UI components

---

## FastAPI Backend

The backend is responsible for orchestrating the complete analysis process.

Responsibilities include:

* Receiving analysis requests
* Running analyzers
* Aggregating findings
* Calculating risk scores
* Generating AI-assisted explanations
* Returning structured responses

The backend exposes a minimal REST API:

```text
POST /analyze
GET /health
```

---

# Backend Structure

The backend is organized into isolated modules with clearly separated responsibilities.

```text
backend/
├── analyzers/
├── models/
├── scoring/
├── services/
├── utils/
└── main.py
```

This structure improves:

* Maintainability
* Extensibility
* Debugging
* Testing
* Signal isolation

---

# Analyzer Architecture

The analyzer layer is intentionally modular.

Each analyzer focuses on a dedicated security domain and contributes findings independently.

Current analyzers include:

* Header Analyzer
* URL Analyzer
* Attachment Analyzer
* Language Analyzer

This architecture allows new analyzers and heuristics to be added without redesigning the overall system.

---

# Header Analyzer

The header analyzer evaluates email authentication and sender-related indicators.

Current checks include:

* **SPF validation** — Verifies that the sending server is authorized to send emails for the sender’s domain.

* **DKIM validation** — Verifies that the email was cryptographically signed by the sender’s domain and was not modified in transit.

* **DMARC validation** — Checks whether the email aligns with the domain’s SPF and DKIM policies to help detect spoofing attempts.

* Reply-To mismatch detection

* Suspicious sender naming patterns

* Free email provider detection

The goal is to identify spoofing attempts and suspicious sender identities.

---

# URL Analyzer

The URL analyzer evaluates links appearing inside the email body.

Checks include:

* URL shorteners
* Suspicious top-level domains
* IP-based URLs
* Suspicious domain keywords
* Excessive subdomain depth
* Google Safe Browsing lookups

The analyzer combines heuristic analysis with external reputation validation.

---

# Attachment Analyzer

The attachment analyzer evaluates attachment names and extensions for potentially risky patterns.

Checks include:

* Executable files
* Script files
* Archive files
* Macro-enabled Office documents
* Double-extension patterns
* Suspicious attachment naming

The implementation intentionally focuses on lightweight static heuristics rather than full sandbox execution.

---

# Language Analyzer

The language analyzer evaluates manipulative or socially engineered wording.

Checks include:

* Urgency indicators
* Credential theft wording
* Financial pressure language

The analyzer intentionally focuses on behavioral indicators rather than definitive malicious classification.

---

# Scoring Engine

The scoring engine aggregates findings from all analyzers into a unified maliciousness score.

The scoring model is intentionally rule-based and transparent.

Reasons for this design include:

* Explainability
* Predictable behavior
* Easier tuning
* Simpler debugging
* Easier demonstration and reasoning

The final score is mapped into verdict levels such as:

* Safe
* Low Risk
* Suspicious
* High Risk
* Likely Phishing

The scoring layer intentionally prioritizes transparency over opaque machine-learning classification.

---

# LLM Integration

The system uses an LLM as an explanation and semantic reasoning layer rather than as the primary detection engine.

Responsibilities include:

* Explaining deterministic findings in user-friendly language
* Providing lightweight semantic context
* Generating concise summaries

The implementation intentionally constrains the LLM:

* Deterministic analyzers remain the primary source of truth
* The LLM does not autonomously classify emails
* Prompt injection protections are enforced
* Email content is treated as untrusted input

This hybrid design balances explainability with semantic flexibility.

---

# Gmail Add-on Design

The Gmail Add-on intentionally contains minimal business logic.

Responsibilities are limited to:

* Email extraction
* Backend communication
* UI rendering

This separation keeps the security logic centralized inside the backend and simplifies future backend evolution.

---

# Design Principles

Several architectural principles guided the implementation.

## Explainability First

The system prioritizes transparent findings and understandable verdicts over opaque classifications.

---

## Modular Analyzer Design

Each analyzer operates independently and focuses on a dedicated security domain.

---

## Lightweight Frontend

The Add-on remains lightweight while delegating security analysis to the backend.

---

## Security-Oriented Input Handling

All email content is treated as untrusted input throughout the system.

---

## Incremental Extensibility

New analyzers and scoring rules can be added without redesigning the overall architecture.

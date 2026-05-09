# Security Decisions

[← Back to Main README](../README.md)

---

# Security Philosophy

MailProtector was designed with a security-oriented mindset that treats all incoming email content as potentially untrusted.

The implementation prioritizes:

* Defensive input handling
* Safe preprocessing
* Controlled LLM behavior
* Resilient external integrations
* Clear and predictable security analysis

The goal is to reduce unsafe assumptions while maintaining lightweight and explainable analysis behavior, and help users understand why an email may be suspicious instead of relying on full black-box classification.

---

# Treating Email Content as Untrusted Input

All incoming email content is treated as untrusted input throughout the analysis pipeline.

This includes:

* Email bodies
* Headers
* URLs
* Attachment names
* LLM-facing content

The system assumes that malicious actors may intentionally attempt to manipulate analyzers or AI-generated explanations.

As a result, multiple defensive preprocessing stages are applied before analysis begins.

---

# Prompt Injection Awareness

The implementation explicitly accounts for prompt injection attempts against the LLM explanation layer.

Email content is never treated as trusted instructions.

The LLM system prompt explicitly instructs the model to:

* Ignore instructions appearing inside the email body
* Avoid following attacker-controlled commands
* Focus only on security analysis
* Generate concise explanations only

The LLM is intentionally constrained to an explanation role rather than acting as an autonomous decision engine.

---

# Input Sanitization

Before analysis begins, the backend sanitizes incoming email content.

Sanitization includes:

* HTML tag removal
* Null byte removal
* Excessive content truncation
* Noise reduction

This improves:

* Parsing reliability
* Analyzer consistency
* Input stability
* Defensive processing safety

Sanitization occurs before all downstream analysis stages.

---

# Defensive External API Usage

Some security signals rely on external services such as Google Safe Browsing.

External integrations are treated as potentially unreliable and are isolated from the core analysis pipeline.

The system intentionally fails safely:

* If Safe Browsing fails, heuristic URL analysis still continues
* If external requests timeout, the pipeline still returns results
* External API failures do not abort the full analysis flow

This improves resilience and avoids unnecessary full-request failures.

---

# Secrets and Sensitive Data

Sensitive credentials such as API keys are intentionally stored outside the source code using environment variables.

The implementation avoids hardcoding external API credentials directly inside the repository.

The Gmail Add-on communicates only with the backend service and does not expose security-related secrets to the client layer.

---

# Minimal Data Exposure

The Gmail Add-on extracts only the information required for analysis and delegates all security processing to the backend service.

This reduces unnecessary exposure of backend logic and centralizes security-sensitive operations inside the server environment.

---

# Graceful Degradation

The pipeline is designed to continue operating even when some subsystems fail.

Examples include:

* Safe Browsing API failures
* LLM generation failures
* Partial analyzer failures
* Malformed external responses

Whenever possible, the system still returns:

* Deterministic findings
* Partial analysis results
* A usable verdict

This improves reliability and avoids complete request failures.

---

# Rate Limiting Considerations

The current implementation assumes a trusted demonstration environment and therefore does not yet enforce strict request-level rate limiting.

In a production deployment, rate limiting would be important to reduce:

* Abuse attempts
* API exhaustion
* Excessive LLM usage
* Denial-of-service scenarios

This was intentionally left outside the current project scope in favor of focusing on the core analysis pipeline.

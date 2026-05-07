from analyzers.language_analyzer import analyze_language
from analyzers.url_analyzer import analyze_urls
from analyzers.header_analyzer import analyze_headers
from analyzers.attachment_analyzer import analyze_attachments
from services.llm_service import generate_summary
from utils.sanitizer import sanitize_email_body
from utils.logger import logger
from utils.normalizer import normalize_for_detection

def analyze_email(email):
    logger.info(f"Starting analysis for email from: {email.sender}")

    findings = []

    sanitized_body = sanitize_email_body(email.body)
    logger.info(f"Sanitized body length: {len(sanitized_body)}")

    normalized_body = normalize_for_detection(sanitized_body)
    logger.info(f"Normalized body length: {len(normalized_body)}")

    language_findings = analyze_language(normalized_body)
    logger.info(f"Language findings: {language_findings}")
    findings += language_findings

    url_findings = analyze_urls(sanitized_body)
    logger.info(f"URL findings: {url_findings}")
    findings += url_findings

    attachment_findings = analyze_attachments(email.attachments)
    logger.info(f"Attachment findings: {attachment_findings}")
    findings += attachment_findings

    header_findings = analyze_headers(email.headers)
    logger.info(f"Header findings: {header_findings}")
    findings += header_findings

    score = 0

    for finding in findings:

        lower_finding = finding.lower()

        if "spf" in lower_finding:
            score += 40
        elif "dkim" in lower_finding:
            score += 40
        elif "dmarc" in lower_finding:
            score += 35
        elif "shortened" in lower_finding:
            score += 25
        elif "suspicious tld" in lower_finding:
            score += 30
        elif "ip-based url" in lower_finding:
            score += 35
        elif "suspicious url keyword" in lower_finding:
            score += 20
        elif "subdomain depth" in lower_finding:
            score += 20
        elif "executables attachment" in lower_finding:
            score += 45
        elif "scripts attachment" in lower_finding:
            score += 35
        elif "archives attachment" in lower_finding:
            score += 15
        elif "macro documents attachment" in lower_finding:
            score += 35
        elif "source code attachment" in lower_finding:
            score += 10
        elif "binary artifacts attachment" in lower_finding:
            score += 20
        elif "suspicious attachment filename" in lower_finding:
            score += 20
        elif "double-extension" in lower_finding:
            score += 45
        elif "urgency" in lower_finding:
            score += 15
        elif "credential_theft" in lower_finding:
            score += 25
        elif "financial_pressure" in lower_finding:
            score += 20
        elif "safe browsing" in lower_finding:
            score += 50
        else:
            score += 10

    if score >= 60:
        verdict = "Likely phishing"
    elif score >= 25:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    logger.info(f"Final score: {score} | Verdict: {verdict}")

    llm_summary = generate_summary(
        body = sanitized_body,
        findings = findings,
        score = min(score, 100),
        verdict = verdict
    )
    logger.info("LLM summary generated successfully")

    return {
        "score": min(score, 100),
        "verdict": verdict,
        "reasons": findings,
        "llm_summary": llm_summary
    }
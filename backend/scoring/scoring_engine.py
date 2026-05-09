from analyzers.language_analyzer import analyze_language
from analyzers.url_analyzer import analyze_urls
from analyzers.header_analyzer import analyze_headers
from analyzers.attachment_analyzer import analyze_attachments
from services.llm_service import generate_summary
from utils.sanitizer import sanitize_email_body
from utils.logger import logger
from utils.normalizer import normalize_for_detection

SCORING_RULES = {
    # Email authentication
    "spf": 40,
    "dkim": 40,
    "dmarc": 35,

    # Sender identity
    "suspicious sender identity": 20,
    "free email provider": 5,
    "reply-to mismatch": 30,

    # URL analysis
    "shortened": 20,
    "suspicious tld": 30,
    "ip-based url": 35,
    "suspicious url keyword": 15,
    "subdomain depth": 15,
    "safe browsing": 50,

    # Attachments
    "executables attachment": 45,
    "scripts attachment": 30,
    "archives attachment": 10,
    "macro documents attachment": 35,
    "source code attachment": 5,
    "binary artifacts attachment": 10,
    "suspicious attachment filename": 20,
    "double-extension": 45,

    # Language analysis
    "urgency": 10,
    "credential_theft": 25,
    "financial_pressure": 20
}

def analyze_email(email):
    """
    Analyze an email and return a risk score, verdict, and reasons.
    """
    
    logger.info(f"Starting analysis for email from: {email.sender}")

    findings = []

    sanitized_body = sanitize_email_body(email.body) # sanitize body to remove noise and irrelevant content
    logger.info(f"Sanitized body length: {len(sanitized_body)}")

    normalized_body = normalize_for_detection(sanitized_body) # normalize body to improve detection of phishing indicators
    logger.info(f"Normalized body length: {len(normalized_body)}")

    language_findings = analyze_language(normalized_body) # language analysis findings
    logger.info(f"Language findings: {language_findings}")
    findings += language_findings

    url_findings = analyze_urls(sanitized_body) # URL analysis findings
    logger.info(f"URL findings: {url_findings}")
    findings += url_findings

    attachment_findings = analyze_attachments(email.attachments) # attachment analysis findings
    logger.info(f"Attachment findings: {attachment_findings}")
    findings += attachment_findings

    header_findings = analyze_headers(email.headers) # header analysis findings
    logger.info(f"Header findings: {header_findings}")
    findings += header_findings

    score = 0

    for finding in findings:

        lower_finding = finding.lower()
        matched = False

        for rule, points in SCORING_RULES.items(): # check if any of the scoring rules match the finding
            if rule in lower_finding:
                score += points
                matched = True
                break
        
        if not matched:
            logger.warning(f"No scoring rule matched finding: {finding}")
        

    # gradings
    if score >= 75:
        verdict = "Likely phishing"
    elif score >= 50:
        verdict = "High Risk"
    elif score >= 25:
        verdict = "Suspicious"
    elif score >= 10:
        verdict = "Low Risk"
    else:
        verdict = "Safe"

    logger.info(f"Final score: {score} | Verdict: {verdict}")

    # Generate LLM summary of the analysis baesed on the findings, score and extra semantic analysis
    llm_summary = generate_summary(
        body = sanitized_body,
        findings = findings,
        score = min(score, 100),
        verdict = verdict,
        sender = email.sender,
        subject = email.subject,
        attachments = email.attachments
    )
    
    logger.info("LLM summary generated successfully")

    return {
        "score": min(score, 100),
        "verdict": verdict,
        "reasons": findings,
        "llm_summary": llm_summary
    }
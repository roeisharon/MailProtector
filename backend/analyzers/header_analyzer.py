import re

SUSPICIOUS_SENDER_KEYWORDS = [
    "security", "support", "admin", "noreply", "no-reply", "donotreply", "do-not-reply",
    "billing", "verification", "account", "accounts", "it-helpdesk", "helpdesk", "service"]

FREE_EMAIL_PROVIDERS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

# Find sender's address using regex
def extract_email_sender(headers: str):
    match = re.search(
        r'From:.*?<([^>]+)>',
        headers,
        re.IGNORECASE
    )

    if match:
        return match.group(1).lower()

    return None

# Find reply-to address using regex
def extract_reply_to(headers: str):
    match = re.search(
        r'Reply-To:\s*(.+)',
        headers,
        re.IGNORECASE
    )

    if match:
        return match.group(1).lower()

    return None

def analyze_headers(headers: str):
    """
    Analyze the email headers for suspicious patterns.
    """
    findings = []

    lower_headers = headers.lower()

    # SPF / DKIM / DMARC
    if "spf=fail" in lower_headers:
        findings.append("SPF validation failed")
    if "dkim=fail" in lower_headers:
        findings.append("DKIM validation failed")
    if "dmarc=fail" in lower_headers:
        findings.append("DMARC validation failed")  

    sender_email = extract_email_sender(headers)
    if sender_email:
        # Check for suspicious sender keywords
        for keyword in SUSPICIOUS_SENDER_KEYWORDS:
            if keyword in sender_email:
                findings.append(f"Suspicious sender identity detected")
                break

        # Check for free email providers
        for provider in FREE_EMAIL_PROVIDERS:
            if sender_email.endswith(provider):
                findings.append(f"Free email provider detected")
                break
        
        # Check for mismatched Reply-To
        reply_to = extract_reply_to(headers)
        if sender_email and reply_to and sender_email != reply_to:
            findings.append("Reply-To mismatch detected")
        
    return findings
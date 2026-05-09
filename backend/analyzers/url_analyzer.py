import re
import ipaddress
import tldextract
from services.safe_browsing_service import check_url_safety


SHORTENERS = ["bit.ly", "tinyurl.com", "t.co"]
SUSPICIOUS_TLDS = ["xyz", "top", "click", "ru"]
SUSPICIOUS_DOMAIN_KEYWORDS = ["login", "secure", "verify", "update", "verify", "auth", "account"]
MAX_SUBDOMAIN_DEPTH = 3

def is_ip_address(domain: str):
    """
    Check if the given domain is an IP address."""
    try:
        ipaddress.ip_address(domain)
        return True
    except ValueError:
        return False

def analyze_urls(body: str):
    """
    Analyze the email body for suspicious URLs.
    """
    
    findings = []

    urls = re.findall(
        r'(https?://[^\s]+|www\.[^\s]+)',
        body)

    for url in urls:
        lower_url = url.lower()
        extracted = tldextract.extract(lower_url)

        domain = extracted.domain
        suffix = extracted.suffix
        subdomain = extracted.subdomain
        full_domain = f"{domain}.{suffix}"

        if full_domain in SHORTENERS: # Check for URL shorteners
            findings.append(f"Shortened URL detected: {full_domain}")
        
        if suffix in SUSPICIOUS_TLDS: # Check for suspicious TLDs
            findings.append(f"Suspicious TLD detected: {suffix}")
        
        hostname_match = re.search(r'://([^/:]+)', lower_url)
        if hostname_match:
            hostname = hostname_match.group(1)

            if is_ip_address(hostname): # Check for IP address in URL
                findings.append(f"IP-based URL detected")
            
        # Check for suspicious keywords in domain
        sus_keywords_found = False
        for keyword in SUSPICIOUS_DOMAIN_KEYWORDS:
            if keyword in lower_url:
                sus_keywords_found = True
                break
        
        if sus_keywords_found:
            findings.append(f"Suspicious URL keyword detected")
        
        # Check for excessive subdomain depth
        if subdomain:
            subdomain_depth = len(subdomain.split('.'))
            if subdomain_depth > MAX_SUBDOMAIN_DEPTH:
                findings.append(f"Excessive subdomain depth detected")

        # Check against Google Safe Browsing API
        safe_browsing_match = check_url_safety(url)
        if safe_browsing_match:
            findings.append(f"Google Safe Browsing flagged URL as malicious")

    return findings
def analyze_headers(headers: str):
    findings = []

    lower_headers = headers.lower()

    if "spf=fail" in lower_headers:
        findings.append("SPF validation failed")
    
    if "dkim=fail" in lower_headers:
        findings.append("DKIM validation failed")
    
    if "dmarc=fail" in lower_headers:
        findings.append("DMARC validation failed")

    return findings
import re

SUSPICIOUS_PATTERNS = {

    "urgency": [
        r"\burgent\b",
        r"\bimmediate action\b",
        r"\bimmediately\b",
        r"\bact now\b",
        r"\bwithin \d+ hours\b",
        r"\bfinal warning\b",
        r"\baccount suspended\b"
    ],

    "credential_theft": [
        r"\bverify (your )?email\b",
        r"\bverify (your )?account\b",
        r"\bconfirm (your )?identity\b",
        r"\breset (your )?password\b",
        r"\blogin required\b",
        r"\bsecurity verification\b",
    ],

    "financial_pressure": [
        r"\bpayment failed\b",
        r"\bunpaid invoice\b",
        r"\brefund available\b",
        r"\bclaim your refund\b"
    ]
}

def analyze_language(body: str):

    findings = []

    normalized_body = body.lower()

    normalized_body = re.sub(
        r'\s+',
        ' ',
        normalized_body
    )

    for category, patterns in SUSPICIOUS_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, normalized_body):

                findings.append(
                    f"Suspicious {category.replace('_', ' ').title()} language detected"
                )

    return findings
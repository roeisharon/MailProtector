import re

ATTACHMENT_CATEGORIES = {
    "executables": [
        ".exe",
        ".dll",
        ".app",
        ".dmg",
        ".pkg"
    ],

    "scripts": [
        ".bat",
        ".cmd",
        ".js",
        ".vbs",
        ".ps1",
        ".sh",
        ".run"
    ],

    "archives": [
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".tgz"
    ],

    "macro_documents": [
        ".docm",
        ".xlsm",
        ".pptm"
    ],

    "source_code": [
        ".py",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".cs",
        ".java",
        ".asm",
        ".s",
        ".go",
        ".rs",
        ".js"
    ],

    "binary_artifacts": [
        ".o",
        ".so",
        ".out"
    ]
}

SUSPICIOUS_FILENAME_KEYWORDS = [
    "invoice",
    "payment",
    "secure",
    "password",
    "reset",
    "account",
    "urgent",
    "verification",
    "auth"
]

DOUBLE_EXTENSION_PATTERN = (
    r'\.[a-zA-Z0-9]{2,4}\.(exe|scr|bat|cmd|js)$'
)


def analyze_attachments(attachments):
    """
    Analyze the email attachments for suspicious patterns.
    """

    findings = []

    for attachment in attachments:
        lower_attachment = attachment.lower()

        # Category-based detection
        for category, extensions in ATTACHMENT_CATEGORIES.items():
            matched = False
            for ext in extensions:
                if lower_attachment.endswith(ext):
                    findings.append(
                        f"{category.replace('_', ' ').title()} attachment detected: {ext}"
                    )
                    matched = True
                    break

            if matched:
                continue

        # Suspicious filename keywords
        suspicious_keyword_found = False

        for keyword in SUSPICIOUS_FILENAME_KEYWORDS:
            if keyword in lower_attachment:
                suspicious_keyword_found = True
                break

        if suspicious_keyword_found:
            findings.append(
                "Suspicious attachment filename detected"
            )

        # Double extension detection
        if re.search(DOUBLE_EXTENSION_PATTERN, lower_attachment):
            findings.append(
                f"Double-extension attachment detected: {lower_attachment}"
            )

    return findings
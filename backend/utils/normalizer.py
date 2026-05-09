import re

CHAR_SUBSTITUTIONS = {
    "0": "o",
    "1": "i",
    "3": "e",
    "@": "a",
    "$": "s"
}

def normalize_for_detection(text: str):
    """
    Normalizes the input text for detection
    """

    normalized = text.lower()

    for original, replacement in CHAR_SUBSTITUTIONS.items():
        normalized = normalized.replace(
            original,
            replacement
        )

    normalized = re.sub(
        r'[^a-zA-Z\s]',
        '',
        normalized
    )

    normalized = re.sub(
        r'\s+',
        ' ',
        normalized
    )

    collapsed = []

    words = normalized.split()

    for word in words:
        if len(word) <= 1:
            continue

        collapsed.append(word)

    normalized = " ".join(collapsed)

    return normalized.strip()
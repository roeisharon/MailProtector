import re

MAX_LENGTH = 12000

# helper function to sanitize email body, removing null bytes, HTML tags, and truncating to a reasonable length
def sanitize_email_body(body: str):
    if not body:
        return ""
    
    sanitized = body
    sanitized = sanitized.replace("\x00", "")  # Remove null bytes
    sanitized = re.sub(r'<[^>]+>', '', sanitized)  # Remove HTML tags
    sanitized = sanitized.strip()  # Remove leading/trailing whitespace
    sanitized = sanitized[:MAX_LENGTH]  # Truncate to max length

    return sanitized

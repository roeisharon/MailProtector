import requests
import os
from dotenv import load_dotenv

load_dotenv()

SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

def check_url_safety(url):
    body = {
        "client": {
            "clientId": "malicious-email-scorer",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    response = requests.post(
        f"{SAFE_BROWSING_URL}?key={API_KEY}",
        json=body,
        timeout=5
    )

    if response.status_code != 200:
        return False
    
    data = response.json()

    return "matches" in data
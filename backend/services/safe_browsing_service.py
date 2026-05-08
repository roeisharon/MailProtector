import requests
import os
from dotenv import load_dotenv
from utils.logger import logger

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

    try:
        response = requests.post(
            f"{SAFE_BROWSING_URL}?key={API_KEY}",
            json=body,
            timeout=5
        )

        if response.status_code != 200:
            return False
        
        data = response.json()
    
    except requests.RequestException:
        logger.warning(f"Safe Browsing lookup failed for URL: {url}")
        return False

    return "matches" in data